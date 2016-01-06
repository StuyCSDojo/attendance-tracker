import utils.db as db
import getpass

def commander(query):
    """
    Command parser for the admin console

    Params:
        query - A string containing the command or query from the console

    Returns:
        True if successful execution, False otherwise
    """
    args = query.strip().split(" ")
    if len(args) == 0:
        return True
    # >> list
    # Lists out the admins inside the database
    if args[0] == "list":
        for admin in db.list_admin():
            print admin
        return True
    # >> add username password
    # Adds a new user with credentials username:password
    if args[0] == "add" and len(args) == 3:
        db.add_admin(args[1], args[2])
        return True
    # >> remove username
    # Exits immediately if 'username' doesn't exist. Otherwise, it will prompt
    # for the password of 'username', and if validated, will delete the user.
    if args[0] == "remove" and len(args) == 2:
        if not db.username_exists(args[1]):
            return False
        pword = str(getpass.getpass("Password: "))
        if db.admin_exists(args[1], pword):
            db.remove_admin(args[1], pword)
            return True
        else:
            return False
    # >> exit
    # Exits the console
    if args[0].upper() == "EXIT":
        exit(0)
    return False

while True:
    q = str(raw_input(">> "))
    if not commander(q):
        print("FAILED")

