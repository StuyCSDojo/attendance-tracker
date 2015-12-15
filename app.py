from flask import Flask, request

import datetime
from datetime import datetime
import time, os

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

def get_columns(try_again=True):
    """
    Gets the row 1 elements of all used columns

    Params:
        None

    Returns:
        A list of strings if successful, None otherwise
    """
    load_attendance_sheet() # Load the attendance sheet it is not yet loaded
    global ATTENDANCE_SHEET
    try:
        column_headers = ATTENDANCE_SHEET.row_values(1)
        return column_headers
    except Exception as e:
        # print("ERROR ({0}): {1}".format(e.errno, e.strerror))
        if try_again:
            ATTENDANCE_SHEET = None
            load_attendance_sheet()
            return get_columns(try_again=False)
        else:
            return None

def get_known_osis():
    """
    Gets a list of known osis numbers. We know that the first column is a list
    of all the osis numbers, where the 0th index of the list is "OSIS"

    Params:
        None

    Returns:
        A list of strings if successful, None otherwise
    """
    load_attendance_sheet() # Load the attendance sheet it is not yet loaded
    global ATTENDANCE_SHEET
    try:
        osis_numbers = ATTENDANCE_SHEET.col_values(1)
        return osis_numbers
    except Exception as e:
        print("ERROR ({0}): {1}".format(e.errno, e.strerror))
        return None

@app.route("/")
def add_id():
    """
    Adds a single ID into the google spreadsheet, given data in the GET
    parameters

    Params:
        None

    Returns:
        None
    """
    # Grab the parameters and exit if not provided or incorrect
    u_name = request.args.get('username')
    p_word = request.args.get('pword')
    if u_name is None or p_word is None:
        return "no_creds"
    if not db.admin_exists(u_name, p_word):
        return "bad_login"
    date = request.args.get('date')
    if date is None:
        date = str(datetime.now())[0:10].replace("-", "_")
        print("No given date. Generating from system time: " + str(date))
    osis = request.args.get('osis')
    if osis is None:
        return "no_osis"
    # Denote ATTENDANCE_SHEET as the global variable, not instance variable
    global ATTENDANCE_SHEET
    # Calculate the column for the specific day
    cols = get_columns()
    col_num = 0
    while col_num < len(cols):
        if cols[col_num] == date:
            break
        col_num += 1
    col_num += 1 # The spreadsheet is 1 indexed, not 0 indexed
    # Get the row number (row for the osis)
    osis_nums = get_known_osis()
    # Resize the table!
    ATTENDANCE_SHEET.resize(len(osis_nums) + 1, len(cols) + 1)
    # Update the date for that column:
    ATTENDANCE_SHEET.update_cell(1, col_num, date)
    # Keep in mind that osis_nums should be sorted
    row_num = 1
    while row_num < len(osis_nums):
        # If the osis matches, stop iterating
        if osis_nums[row_num] == osis:
            break
        # Convert the values into integers
        # If the osis is between the values, insert a row
        intval = -1
        intosis = -1
        try:
            intval = int(osis_nums[row_num])
            intosis = int(osis)
        except:
            row_num += 1
            continue
        if int(osis_nums[row_num]) > int(osis):
            print("Unrecognized OSIS. Adding to sheet")
            ATTENDANCE_SHEET.insert_row(["" for i in cols], row_num + 1)
            break
        # Increase the counter
        row_num += 1
    # When we are done iterating to get the osis, mark as present
    ATTENDANCE_SHEET.update_cell(row_num + 1, 1, str(osis))
    ATTENDANCE_SHEET.update_cell(row_num + 1, col_num, 'X')
    return "OK"

if __name__ == "__main__":
    app.debug = True
    # app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.run("0.0.0.0", 11235)

