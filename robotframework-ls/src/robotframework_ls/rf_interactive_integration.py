from concurrent import futures
from functools import partial
import itertools
from typing import Dict, Union

from robocorp_ls_core.protocols import (
    IConfig,
    ActionResultDict,
    ActionResult,
    Sentinel,
    IEndPoint,
    IFuture,
)
from robocorp_ls_core.robotframework_log import get_logger
from robotframework_ls.commands import ROBOT_INTERNAL_RFINTERACTIVE_COMPLETIONS

log = get_logger(__name__)


class _RfInfo:
    def __init__(
        self,
        rf_interpreter_server_manager,
        commands_thread_pool: futures.ThreadPoolExecutor,
        ls_thread_pool: futures.ThreadPoolExecutor,
    ):
        from robotframework_interactive.server.rf_interpreter_server_manager import (
            RfInterpreterServerManager,
        )

        self.interpreter: RfInterpreterServerManager = rf_interpreter_server_manager
        self.commands_thread_pool = commands_thread_pool
        self.ls_thread_pool = ls_thread_pool


class _RfInterpretersManager:
    def __init__(self, endpoint: IEndPoint):
        self._interpreter_id_to_rf_info: Dict[int, _RfInfo] = {}
        self._next_interpreter_id = partial(next, itertools.count(0))
        self._endpoint = endpoint

    def interpreter_start(
        self, arguments, config: IConfig
    ) -> IFuture[ActionResultDict]:

        # Thread pool with 1 worker (so, we're mostly sequentializing the
        # work to be done to another thread).
        commands_thread_pool = futures.ThreadPoolExecutor(max_workers=1)

        def run():
            from robotframework_ls import import_rf_interactive

            import_rf_interactive()

            from robocorp_ls_core.options import Setup

            try:
                from robotframework_interactive.server.rf_interpreter_server_manager import (
                    RfInterpreterServerManager,
                )

                interpreter_id = self._next_interpreter_id()

                def on_interpreter_message(interpreter_message: dict):
                    """
                    :param interpreter_message:
                    Something as:
                    {
                        "jsonrpc": "2.0",
                        "method": "interpreter/output",
                        "params": {
                            "output": "Some output\n",
                            "category": "stdout",
                        },
                    }
                    """

                    params = interpreter_message["params"]
                    params["interpreter_id"] = interpreter_id
                    self._endpoint.notify(interpreter_message["method"], params)

                rf_interpreter_server_manager = RfInterpreterServerManager(
                    verbose=Setup.options.verbose,
                    base_log_file=Setup.options.log_file,
                    on_interpreter_message=on_interpreter_message,
                )
                rf_interpreter_server_manager.config = config
                rf_interpreter_server_manager.interpreter_start()
                ls_thread_pool = futures.ThreadPoolExecutor(max_workers=2)
                self._interpreter_id_to_rf_info[interpreter_id] = _RfInfo(
                    rf_interpreter_server_manager, commands_thread_pool, ls_thread_pool
                )

            except Exception as e:
                log.exception("Error starting interpreter.")
                return ActionResult(False, message=str(e)).as_dict()
            else:
                return ActionResult(
                    True, result={"interpreter_id": interpreter_id}
                ).as_dict()

        return commands_thread_pool.submit(run)

    def get_interpreter_from_arguments(
        self, arguments
    ) -> Union[_RfInfo, ActionResultDict]:
        from robotframework_ls import import_rf_interactive

        import_rf_interactive()

        if not arguments:
            return ActionResult(
                False, message="Expected arguments ([{'interpreter_id': <id>}])"
            ).as_dict()
        if not isinstance(arguments, (list, dict)):
            return ActionResult(
                False, message=f"Arguments should be a Tuple[Dict]. Found: {arguments}"
            ).as_dict()

        args: dict = arguments[0]
        interpreter_id = args.get("interpreter_id", Sentinel.SENTINEL)
        if interpreter_id is Sentinel.SENTINEL:
            return ActionResult(
                False, message=f"Did not find 'interpreter_id' in {args}"
            ).as_dict()

        rf_info = self._interpreter_id_to_rf_info.get(interpreter_id)
        if rf_info is None:
            return ActionResult(
                False, message=f"Did not find interpreter with id: {interpreter_id}"
            ).as_dict()
        return rf_info

    def interpreter_evaluate(
        self, arguments
    ) -> Union[IFuture[ActionResultDict], ActionResultDict]:
        from robotframework_ls import import_rf_interactive

        import_rf_interactive()

        from robotframework_interactive.server.rf_interpreter_server_manager import (
            RfInterpreterServerManager,
        )

        rf_info_or_dict_error: Union[
            _RfInfo, ActionResultDict
        ] = self.get_interpreter_from_arguments(arguments)
        if isinstance(rf_info_or_dict_error, dict):
            return rf_info_or_dict_error

        def run():
            interpreter: RfInterpreterServerManager = rf_info_or_dict_error.interpreter

            args: dict = arguments[0]
            code = args.get("code", Sentinel.SENTINEL)
            if code is Sentinel.SENTINEL:
                return ActionResult(
                    False, message=f"Did not find 'code' in {args}"
                ).as_dict()

            return interpreter.interpreter_evaluate(code)

        return rf_info_or_dict_error.commands_thread_pool.submit(run)

    def interpreter_stop(
        self, arguments
    ) -> Union[IFuture[ActionResultDict], ActionResultDict]:
        from robotframework_ls import import_rf_interactive

        import_rf_interactive()

        rf_info_or_dict_error: Union[
            _RfInfo, ActionResultDict
        ] = self.get_interpreter_from_arguments(arguments)
        if isinstance(rf_info_or_dict_error, dict):
            return rf_info_or_dict_error

        rf_info: _RfInfo = rf_info_or_dict_error

        def run():
            try:
                return rf_info.interpreter.interpreter_stop()
            finally:
                try:
                    rf_info.commands_thread_pool.shutdown(wait=False)
                except:
                    log.exception("Error shutting down commands thread pool.")
                try:
                    rf_info.ls_thread_pool.shutdown(wait=False)
                except:
                    log.exception("Error shutting down ls thread pool.")

        return rf_info_or_dict_error.commands_thread_pool.submit(run)


def _handle_semantic_tokens(
    language_server_impl, rf_interpreters_manager: _RfInterpretersManager, arguments
):
    # When the user is entering text in the interpreter, the text
    # may not be the full text or it may be based on the text previously
    # entered, so, we need to ask the interpreter to compute the full
    # text so that we can get the semantic tokens based on the full
    # text that'll actually be evaluated.

    rf_info_or_dict_error: Union[
        _RfInfo, ActionResultDict
    ] = rf_interpreters_manager.get_interpreter_from_arguments(arguments)
    if isinstance(rf_info_or_dict_error, dict):
        msg = rf_info_or_dict_error.get("message")
        if msg:
            log.info(msg)
        return {"resultId": None, "data": []}

    api = language_server_impl._server_manager.get_others_api_client("")
    if api is None:
        log.info(
            "Unable to get api client when computing semantic tokens (for interactive usage)."
        )
        return {"resultId": None, "data": []}

    if not arguments or not isinstance(arguments, (list, tuple)) or len(arguments) != 1:
        log.info(f"Expected arguments to be a list of size 1. Found: {arguments}")
        return {"resultId": None, "data": []}

    def run():
        try:
            args: dict = arguments[0]
            code = args.get("code", Sentinel.SENTINEL)
            if code is Sentinel.SENTINEL:
                log.info(f"Did not find 'code' in {args}")
                return {"resultId": None, "data": []}

            evaluate_text_result = rf_info_or_dict_error.interpreter.interpreter_compute_evaluate_text(
                code
            )
            if not evaluate_text_result["success"]:
                log.info(
                    "Unable to get code to evaluate semantic tokens (for interactive usage)."
                )
                return {"resultId": None, "data": []}
            else:
                code = evaluate_text_result["result"]

                return language_server_impl._async_api_request_no_doc(
                    api,
                    "request_semantic_tokens_from_code_full",
                    prefix=code["prefix"],
                    full_code=code["full_code"],
                    monitor=None,
                )
        except:
            log.exception(f"Error computing semantic tokens for arguments: {arguments}")
            return {"resultId": None, "data": []}

    return rf_info_or_dict_error.ls_thread_pool.submit(run)


def _handle_completions(language_server_impl, rf_interpreters_manager, arguments):
    rf_info_or_dict_error: Union[
        _RfInfo, ActionResultDict
    ] = rf_interpreters_manager.get_interpreter_from_arguments(arguments)
    if isinstance(rf_info_or_dict_error, dict):
        msg = rf_info_or_dict_error.get("message")
        if msg:
            log.info(msg)
        return {"suggestions": []}

    api = language_server_impl._server_manager.get_others_api_client("")
    if api is None:
        log.info(
            "Unable to get api client when computing completions (for interactive usage)."
        )
        return {"suggestions": []}

    if not arguments or not isinstance(arguments, (list, tuple)) or len(arguments) != 1:
        log.info(f"Expected arguments to be a list of size 1. Found: {arguments}")
        return {"suggestions": []}

    def run():
        try:
            args: dict = arguments[0]
            code = args.get("code", Sentinel.SENTINEL)
            if code is Sentinel.SENTINEL:
                log.info(f"Did not find 'code' in {args}")
                return {"suggestions": []}

            position = args.get("position", Sentinel.SENTINEL)
            if position is Sentinel.SENTINEL:
                log.info(f"Did not find 'position' in {args}")
                return {"suggestions": []}

            context = args.get("context", Sentinel.SENTINEL)
            if context is Sentinel.SENTINEL:
                log.info(f"Did not find 'context' in {args}")
                return {"suggestions": []}

            evaluate_text_result = rf_info_or_dict_error.interpreter.interpreter_compute_evaluate_text(
                code
            )
            if not evaluate_text_result["success"]:
                log.info(
                    "Unable to get code to evaluate completions (for interactive usage)."
                )
                return {"suggestions": []}
            else:
                code = evaluate_text_result["result"]

                return language_server_impl._async_api_request_no_doc(
                    api,
                    "request_completions_from_code",
                    prefix=code["prefix"],
                    full_code=code["full_code"],
                    monitor=None,
                )
        except:
            log.exception(f"Error computing semantic tokens for arguments: {arguments}")
            return {"suggestions": []}

    return rf_info_or_dict_error.ls_thread_pool.submit(run)


def execute_command(
    command,
    language_server_impl,
    rf_interpreters_manager: _RfInterpretersManager,
    arguments,
):
    from robotframework_ls.commands import (
        ROBOT_INTERNAL_RFINTERACTIVE_START,
        ROBOT_INTERNAL_RFINTERACTIVE_EVALUATE,
        ROBOT_INTERNAL_RFINTERACTIVE_STOP,
        ROBOT_INTERNAL_RFINTERACTIVE_SEMANTIC_TOKENS,
    )

    if command == ROBOT_INTERNAL_RFINTERACTIVE_START:
        return rf_interpreters_manager.interpreter_start(
            arguments, language_server_impl.config
        )

    elif command == ROBOT_INTERNAL_RFINTERACTIVE_EVALUATE:
        return rf_interpreters_manager.interpreter_evaluate(arguments)

    elif command == ROBOT_INTERNAL_RFINTERACTIVE_STOP:
        return rf_interpreters_manager.interpreter_stop(arguments)

    elif command == ROBOT_INTERNAL_RFINTERACTIVE_SEMANTIC_TOKENS:
        return _handle_semantic_tokens(
            language_server_impl, rf_interpreters_manager, arguments
        )

    elif command == ROBOT_INTERNAL_RFINTERACTIVE_COMPLETIONS:
        return _handle_completions(
            language_server_impl, rf_interpreters_manager, arguments
        )