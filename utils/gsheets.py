import os, json, gspread
import project_constants
from oauth2client.client import SignedJwtAssertionCredentials

KEY = None
SCOPE = None
CREDENTIALS = None
g_auth = None

def load_credentials():
    """
    Loads the credentials provided by a JSON file containing a Google OAuth
    Service Account credentials

    Params:
        None

    Returns:
        True if successful, False otherwise
    """
    # Tell Python we want to modify the global variables
    global KEY
    global SCOPE
    global CREDENTIALS
    global g_auth
    # Load the json file
    print("Loading JSON File...")
    if not os.path.exists(project_constants.GOOGLE_CRED_JSON_FILE):
        print("JSON file not found. Exitting.")
        return False
    KEY = json.load(open(project_constants.GOOGLE_CRED_JSON_FILE))
    print("JSON file loaded")
    # Define the scope for the Google Sheets feed
    SCOPE = [project_constants.GOOGLE_SHEETS_FEED]
    # Generate an assertion credential from the JSON and the scope
    CREDENTIALS = SignedJwtAssertionCredentials(
                    KEY['client_email'],
                    KEY['private_key'],
                    SCOPE)
    # Check for authorization
    print("Authorizing...")
    try:
        g_auth = gspread.authorize(CREDENTIALS)
        print("Authorized!")
        return True
    except Exception as e:
        print("Authorization Failed.")
        print("ERROR ({0}): {1}".format(e.errno, e.strerror))
        return False

def logout_credentials():
    """
    Resets the credential variables to None

    Params:
        None

    Returns:
        None
    """
    # Tell Python we want to modify the global variables
    global KEY
    global SCOPE
    global CREDENTIALS
    global g_auth
    # Reset all the values to None
    KEY = None
    SCOPE = None
    CREDENTIALS = None
    g_auth = None

def get_sheet_from_name(name):
    """
    Gets a sheet, if authorized, by name.

    Params:
        name - A string containing the name of the spreadsheet

    Returns:
        The sheet if successful, None otherwise
    """
    try:
        sheet = g_auth.open(name).sheet1
        return sheet
    except:
        return None

def get_sheet_from_key(key):
    """
    Gets a sheet, if authorized, by the key.

    Params:
        key - A string containing the key of the spreadsheet

    Returns:
        The sheet if successful, None otherwise
    """
    try:
        sheet = g_auth.open_by_key(key).sheet1
        return sheet
    except:
        return None

