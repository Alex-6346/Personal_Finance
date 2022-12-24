from splitwise import Splitwise


def create_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Users("
                   "id integer PRIMARY KEY,"
                   "full_name text,"
                   "email text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Groups_users("
                   "id integer PRIMARY KEY,"
                   "group_name text,"
                   "group_type text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Categories("
                   "id integer PRIMARY KEY,"
                   "category_name text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Subcategories("
                   "id integer PRIMARY KEY,"
                   "subcategory_name text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Transactions("
                   "id integer PRIMARY KEY,"
                   "expense_date datetime,"
                   "group_id integer,"
                   "subcategory_id integer,"
                   "description text,"
                   "currency_code text,"
                   "repeat_interval text,"
                   "updated_date datetime,"
                   "FOREIGN KEY (group_id) REFERENCES Groups_users(id),"
                   "FOREIGN KEY (subcategory_id) REFERENCES Subcategories(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS TransactionItems ("
                   "id integer PRIMARY KEY,"
                   "transaction_id integer,"
                   "user_id integer,"
                   "amount float,"
                   "base_amount float,"
                   "FOREIGN KEY (transaction_id) REFERENCES Transactions(id),"
                   "FOREIGN KEY (user_id) REFERENCES Users(id)"
                   "UNIQUE(transaction_id,user_id))")


def fill_tables(s_obj: Splitwise, cursor):
    user = s_obj.getCurrentUser()
    # Insert information about current user in Users table
    cursor.execute("INSERT OR IGNORE INTO Users (id,full_name,email) VALUES (?,?,?)",
                   [user.getId(), user.getFirstName() + " " + user.getLastName(), user.getEmail()])

    # Get list of friends of a current user, insert information about them in Users table
    other_users = s_obj.getFriends()
    for u in other_users:
        cursor.execute("INSERT OR IGNORE INTO Users (id,full_name,email) VALUES (?,?,?)",
                       [u.getId(), u.getFirstName() + " " + u.getLastName(), u.getEmail()])

    # Insert information about groups in Groups_users table
    groups = s_obj.getGroups()
    for g in groups:
        cursor.execute("INSERT OR IGNORE INTO Groups_users (id,group_name,group_type) VALUES (?,?,?)",
                       [g.getId(), g.getName(), g.getType()])

    # Insert information about categories and subcategories in  Categories and Subcategories tables
    categories = s_obj.getCategories()
    subcategories = []
    for c in categories:
        subcategories.extend(c.getSubcategories())
        cursor.execute("INSERT OR IGNORE INTO Categories (id,category_name) VALUES (?,?)",
                       [c.getId(), c.getName()])
    for s in set(subcategories):
        cursor.execute("INSERT OR IGNORE INTO Subcategories (id,subcategory_name) VALUES (?,?)",
                       [s.getId(), s.getName()])

    # Insert information about expenses and how much every user in it paid in Transactions and TransactionItems tables
    transactions = s_obj.getExpenses()
    for t in transactions:
        cursor.execute("INSERT OR IGNORE INTO Transactions (id,expense_date,group_id,"
                       "subcategory_id,description,currency_code,"
                       "repeat_interval,updated_date) VALUES (?,?,?,?,?,?,?,?)",
                       [t.getId(), t.getDate(), t.getGroupId(), t.getCategory().getId(), t.getDescription(),
                        t.getCurrencyCode(), t.getRepeatInterval(), t.getUpdatedAt()])
        t_users = t.getUsers()
        for t_user in t_users:
            cursor.execute("INSERT OR IGNORE INTO TransactionItems (transaction_id,user_id,amount) VALUES (?,?,?)",
                           [t.getId(), t_user.getId(), t_user.getPaidShare()])

    # Delete expenses for which deleted_date field is not empty from Transactions and TransactionItems tables
    for t in transactions:
        if t.getDeletedAt() is not None:
            cursor.execute('DELETE FROM Transactions WHERE id=(?)', [t.getId()])
            cursor.execute('DELETE FROM TransactionItems WHERE transaction_id=(?)', [t.getId()])

    # Update expenses for which updated_date field is not empty for Transactions and TransactionItems tables
    for t in transactions:
        if t.getUpdatedAt() is not None:
            cursor.execute('UPDATE Transactions SET  expense_date = ? ,group_id = ?,'
                           'subcategory_id = ? ,description = ? ,currency_code = ?,'
                           'repeat_interval = ?, updated_date = ? WHERE id = ?',
                           [t.getDate(), t.getGroupId(), t.getCategory().getId(), t.getDescription(),
                            t.getCurrencyCode(), t.getRepeatInterval(), t.getUpdatedAt(), t.getId()])
            t_users = t.getUsers()
            for t_user in t_users:
                cursor.execute('UPDATE TransactionItems SET  amount = ?  WHERE transaction_id = ? AND user_id = ?',
                               [t_user.getPaidShare(), t.getId(), t_user.getId()])
