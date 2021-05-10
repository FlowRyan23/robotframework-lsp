// Warning: Don't edit file (autogenerated from python -m dev codegen).

export const ROBOCORP_GET_LANGUAGE_SERVER_PYTHON = "robocorp.getLanguageServerPython";  // Get a python executable suitable to start the language server
export const ROBOCORP_GET_LANGUAGE_SERVER_PYTHON_INFO = "robocorp.getLanguageServerPythonInfo";  // Get info suitable to start the language server {pythonExe, environ}
export const ROBOCORP_GET_PLUGINS_DIR = "robocorp.getPluginsDir";  // Get the directory for plugins
export const ROBOCORP_CREATE_ROBOT = "robocorp.createRobot";  // Create Robot
export const ROBOCORP_LIST_ROBOT_TEMPLATES_INTERNAL = "robocorp.listRobotTemplates.internal";  // Provides a list with the available robot templates
export const ROBOCORP_CREATE_ROBOT_INTERNAL = "robocorp.createRobot.internal";  // Actually calls rcc to create the robot
export const ROBOCORP_UPLOAD_ROBOT_TO_CLOUD = "robocorp.uploadRobotToCloud";  // Upload Robot to the Robocorp Cloud
export const ROBOCORP_LOCAL_LIST_ROBOTS_INTERNAL = "robocorp.localListRobots.internal";  // Lists the activities currently available in the workspace
export const ROBOCORP_IS_LOGIN_NEEDED_INTERNAL = "robocorp.isLoginNeeded.internal";  // Checks if the user is already linked to an account
export const ROBOCORP_GET_LINKED_ACCOUNT_INFO_INTERNAL = "robocorp.getLinkedAccountInfo.internal";  // Provides information related to the current linked account
export const ROBOCORP_CLOUD_LOGIN = "robocorp.cloudLogin";  // Link to Robocorp Cloud
export const ROBOCORP_CLOUD_LOGIN_INTERNAL = "robocorp.cloudLogin.internal";  // Link to Robocorp Cloud (receives credentials)
export const ROBOCORP_CLOUD_LIST_WORKSPACES_INTERNAL = "robocorp.cloudListWorkspaces.internal";  // Lists the workspaces available for the user (in the Robocorp Cloud)
export const ROBOCORP_UPLOAD_TO_NEW_ROBOT_INTERNAL = "robocorp.uploadToNewRobot.internal";  // Uploads a Robot as a new Robot in the Robocorp Cloud
export const ROBOCORP_UPLOAD_TO_EXISTING_ROBOT_INTERNAL = "robocorp.uploadToExistingRobot.internal";  // Uploads a Robot as an existing Robot in the Robocorp Cloud
export const ROBOCORP_RUN_IN_RCC_INTERNAL = "robocorp.runInRcc.internal";  // Runs a custom command in RCC
export const ROBOCORP_RUN_ROBOT_RCC = "robocorp.runRobotRcc";  // Run Robot
export const ROBOCORP_DEBUG_ROBOT_RCC = "robocorp.debugRobotRcc";  // Debug Robot
export const ROBOCORP_ROBOTS_VIEW_TASK_RUN = "robocorp.robotsViewTaskRun";  // Launch selected Task in Robots view
export const ROBOCORP_ROBOTS_VIEW_TASK_DEBUG = "robocorp.robotsViewTaskDebug";  // Debug selected Task in Robots view
export const ROBOCORP_SAVE_IN_DISK_LRU = "robocorp.saveInDiskLRU";  // Saves some data in an LRU in the disk
export const ROBOCORP_LOAD_FROM_DISK_LRU = "robocorp.loadFromDiskLRU";  // Loads some LRU data from the disk
export const ROBOCORP_COMPUTE_ROBOT_LAUNCH_FROM_ROBOCORP_CODE_LAUNCH = "robocorp.computeRobotLaunchFromRobocorpCodeLaunch";  // Computes a robot launch debug configuration based on the robocorp code launch debug configuration
export const ROBOCORP_SET_PYTHON_INTERPRETER = "robocorp.setPythonInterpreter";  // Set pythonPath based on robot.yaml
export const ROBOCORP_RESOLVE_INTERPRETER = "robocorp.resolveInterpreter";  // Resolves the interpreter to be used given a path
export const ROBOCORP_CLOUD_LOGOUT = "robocorp.cloudLogout";  // Unlink and remove credentials from Robocorp Cloud
export const ROBOCORP_CLOUD_LOGOUT_INTERNAL = "robocorp.cloudLogout.internal";  // Unlink and remove credentials from Robocorp Cloud internal
export const ROBOCORP_REFRESH_ROBOTS_VIEW = "robocorp.refreshRobotsView";  // Refresh Robots view
export const ROBOCORP_REFRESH_CLOUD_VIEW = "robocorp.refreshCloudView";  // Refresh Cloud view
export const ROBOCORP_START_BROWSER_LOCATOR = "robocorp.startBrowserLocator";  // Start browser to create Locators
export const ROBOCORP_START_BROWSER_LOCATOR_INTERNAL = "robocorp.startBrowserLocator.internal";  // Start browser to create Locators. Requires the robot where the locators should be saved
export const ROBOCORP_CREATE_LOCATOR_FROM_BROWSER_PICK = "robocorp.createLocatorFromBrowserPick";  // Create Locator from browser pick
export const ROBOCORP_CREATE_LOCATOR_FROM_SCREEN_REGION = "robocorp.createLocatorFromScreenRegion";  // Create Image Locator from screen region
export const ROBOCORP_CREATE_LOCATOR_FROM_SCREEN_REGION_INTERNAL = "robocorp.createLocatorFromScreenRegion.internal";  // Create Image Locator from screen region (internal)
export const ROBOCORP_CREATE_LOCATOR_FROM_BROWSER_PICK_INTERNAL = "robocorp.createLocatorFromBrowserPick.internal";  // Create Locator from browser pick (internal: provides no UI in case of errors)
export const ROBOCORP_STOP_BROWSER_LOCATOR = "robocorp.stopBrowserLocator";  // Stop browser used to create Locators
export const ROBOCORP_GET_LOCATORS_JSON_INFO = "robocorp.getLocatorsJsonInfo";  // Obtain information from the locators.json given a robot.yaml
export const ROBOCORP_NEW_LOCATOR_UI = "robocorp.newLocatorUI";  // Create locator
export const ROBOCORP_NEW_LOCATOR_UI_TREE_INTERNAL = "robocorp.newLocatorUI.tree.internal";  // New locator
export const ROBOCORP_COPY_LOCATOR_TO_CLIPBOARD_INTERNAL = "robocorp.copyLocatorToClipboard.internal";  // Copy locator name to clipboard
export const ROBOCORP_OPEN_ROBOT_TREE_SELECTION = "robocorp.openRobotTreeSelection";  // Open robot.yaml
export const ROBOCORP_CLOUD_UPLOAD_ROBOT_TREE_SELECTION = "robocorp.cloudUploadRobotTreeSelection";  // Upload Robot to Robocorp Cloud
export const ROBOCORP_OPEN_LOCATOR_TREE_SELECTION = "robocorp.openLocatorTreeSelection";  // Open locators.json
export const ROBOCORP_CREATE_RCC_TERMINAL_TREE_SELECTION = "robocorp.rccTerminalCreateRobotTreeSelection";  // Open terminal with Robot environment
export const ROBOCORP_SEND_METRIC = "robocorp.sendMetric";  // Send metric
export const ROBOCORP_SUBMIT_ISSUE_INTERNAL = "robocorp.submitIssue.internal";  // Submit issue (internal)
export const ROBOCORP_SUBMIT_ISSUE = "robocorp.submitIssue";  // Submit issue
export const ROBOCORP_CONFIGURATION_DIAGNOSTICS_INTERNAL = "robocorp.configuration.diagnostics.internal";  // Robot Configuration Diagnostics (internal)
export const ROBOCORP_CONFIGURATION_DIAGNOSTICS = "robocorp.configuration.diagnostics";  // Robot Configuration Diagnostics
export const ROBOCORP_RCC_TERMINAL_NEW = "robocorp.rccTerminalNew";  // Terminal with Robot environment