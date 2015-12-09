import os, json, gspread
import project_constants
from oauth2client.client import SignedJwtAssertionCredentials

class gsheet:
    KEY = None
    SCOPE = None
    CREDENTIALS = None
    g_auth = None

    def __init__(self):
        """
        Required __init__ method (constructor) for all Python classes
        Ensures that the credential variables are 'None'

        Params:
            None

        Returns:
            None
        """
        self.KEY = None
        self.SCOPE = None
        self.CREDENTIALS = None
        self.g_auth = None

    def load_credentials(self):
        """
        Loads the credentials provided by a JSON file containing a Google OAuth
        Service Account credentials

        Params:
            None

        Returns:
            True if successful, False otherwise
        """
        # Load the json file
        print("Loading JSON File...")
        if not os.path.exists(project_constants.GOOGLE_CRED_JSON_FILE):
            print("JSON file not found. Exitting.")
            return False
        self.KEY = json.load(open(project_constants.GOOGLE_CRED_JSON_FILE))
        print("JSON file loaded")
        # Define the scope for the Google Sheets feed
        self.SCOPE = [project_constants.GOOGLE_SHEETS_FEED]
        # Generate an assertion credential from the JSON and the scope
        self.CREDENTIALS = SignedJwtAssertionCredentials(
            self.KEY['client_email'],
            self.KEY['private_key'],
            self.SCOPE)
        # Check for authorization
        print("Authorizing...")
        try:
            self.g_auth = gspread.authorize(self.CREDENTIALS)
            print("Authorized!")
            return True
        except Exception as e:
            print("Authorization Failed.")
            # print("ERROR ({0}): {1}".format(e.errno, e.strerror))
            return False

    def logout_credentials(self):
        """
        Resets the credential variables to None

        Params:
            None

        Returns:
            None
        """
        # Reset all the values to None
        self.KEY = None
        self.SCOPE = None
        self.CREDENTIALS = None
        self.g_auth = None

    def get_sheet_from_name(self, name):
        """
        Gets a sheet, if authorized, by name.

        Params:
            name - A string containing the name of the spreadsheet

        Returns:
            The sheet if successful, None otherwise
        """
        try:
            sheet = self.g_auth.open(name)
            return sheet
        except:
            return None

    def get_sheet_from_key(self, key):
        """
        Gets a sheet, if authorized, by the key.

        Params:
            key - A string containing the key of the spreadsheet

        Returns:
            The sheet if successful, None otherwise
        """
        try:
            sheet = self.g_auth.open_by_key(key)
            return sheet
        except:
            return None

    def get_list_of_sheets(self, spreadsheet):
        """
        Returns a list of all the worksheets, given a spreadsheet

        Params:
            spreadsheet - A spreadsheet object obtained from
                          'get_sheet_from_name' or 'get_sheet_from_key'

        Returns:
            A list of all the worksheets contained inside the spreadsheet, None
            otherwise.
        """
        try:
            wsheets = spreadsheet.worksheets()
            return wsheets
        except:
            return None

    def insert_value_into_cell(self, worksheet, cell, value):
        """
        Inserts a value into a cell of the worksheet

        Params:
            worksheet - A worksheet object to insert into
            cell - The cell location (i.e. 'A1', 'H9', 'Z54') to insert at
            value - A string to put into the cell

        Returns:
            None
        """
        worksheet.update_acell(cell, value)
