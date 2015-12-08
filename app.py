from flask import Flask, request

from utils.gsheets import gsheet
import utils.db as db
import utils.project_constants as constants

app = Flask(__name__)

ATTENDANCE_SHEET = None

def load_attendance_sheet():
    """
    Loads in the ATTENDANCE_SHEET global variable via utils.gsheets

    Params:
        None

    Returns:
        True if successful or if already loaded, False otherwise
    """
    global ATTENDANCE_SHEET
    if ATTENDANCE_SHEET is not None:
        return True
    status = True
    # gs denotes Google Sheet
    gs = gsheet()
    status = gs.load_credentials()
    if not status:
        return False
    # ss denotes Spread Sheet
    ss = gs.get_sheet_from_name(constants.STUYCS_DOJO_ATTENDANCE_SHEET_NAME)
    if ss is None:
        return False
    worksheets = gs.get_list_of_sheets(ss)
    if len(worksheets) == 0:
        return False
    ATTENDANCE_SHEET = worksheets[0]
    return True

def get_available_column():
    """
    Gets the index (starting with coordinate 1)  of the next available column

    Params:
        None

    Returns:
        None
    """
    load_attendance_sheet() # Load the attendance sheet it is not yet loaded
    global ATTENDANCE_SHEET
    HEADING = ATTENDANCE_SHEET.row_values(1)
    return len(ATTENDANCE_SHEET) + 1

@app.route("/", methods=["GET"])
def add_id():
    """
    Adds a single ID into the google spreadsheet, given data in the GET
    parameters

    Params:
        None

    Returns:
        None
    """
    u_name = request.args.get('username')
    p_word = request.args.get('pword')
    if u_name is None or p_word is None:
        return "Failed"

