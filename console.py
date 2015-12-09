import utils.db as db

def commander(query):
    """
    Command parser for the admin console

    Params:
        query - A string containing the command or query from the console

    Returns:
        True if successful execution, False otherwise
    """
    args = query.split(" ")
    if len(args) == 0:
        return True
    if args[0] == "list":
        print db.list_admin
        return True
    if args[0] == "add":
        if len(args) != 3:
            return False
        db.add_admin(args[1], args[2])
        return True
    return False

while True:
    q = str(raw_input(">> "))
    if not commander(q):
        print("FAILED")

