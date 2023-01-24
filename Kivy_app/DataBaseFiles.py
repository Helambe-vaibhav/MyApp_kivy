# Helambe Vaibhav
# version 1.0
import sqlite3
import datetime


# creating a class for the for accessing  and manipulating the data in the database for the tasks
class TasksData():
    def __init__(self):
        self.conn = sqlite3.connect("Tasks.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Tasks(id INTEGER PRIMARY KEY, Task TEXT,CompletionDate DATE, TaskCategory TEXT, Status BOOLEAN, ExtraDays INTEGER)''')

    #   create view for all Tasks that are not completed
    def current_Tasks(self):
        self.c.execute("SELECT * FROM Tasks WHERE Status = 0 ORDER BY CompletionDate ASC")
        rows = self.c.fetchall()
        return rows
    #  create view for all Task that are completed
    def completed_Task(self):
        self.c.execute("SELECT * FROM Tasks WHERE Status = 1 ORDER BY CompletionDate DESC ")
        rows = self.c.fetchall()
        return rows
    # insert data into the table by calling the insert method
    def add_new_Task(self, Task, completionDate, TaskCategory, status, extraDays):
        # auto increment id
        self.c.execute("INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?, ?)", (Task, completionDate, TaskCategory, status, extraDays))
        self.conn.commit()

    # get all the categories
    def TaskCategory(self):
        self.c.execute("SELECT DISTINCT TaskCategory FROM Tasks")
        rows = self.c.fetchall()
        return rows

    # get task by id
    def get_Task(self, id):
        self.c.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
        rows = self.c.fetchone()
        return rows

    # update data in the table by calling the update method for status
    def updateTaskStatus(self, id, status):
        # get completion date
        self.c.execute("SELECT CompletionDate FROM Tasks WHERE id = ?", (id,))
        completionDate = self.c.fetchone()
        # get current date
        currentDate = datetime.datetime.now()
        # get difference between current date and completion date
        difference = currentDate - datetime.datetime.strptime(completionDate[0], '%Y-%m-%d')
        difference = difference.days
        # update status and extra days
        self.c.execute("UPDATE Tasks SET Status = ?, ExtraDays = ? WHERE id = ?", (status, difference, id))
        self.conn.commit()

    # destroy the object
    def __del__(self):
        self.conn.close()

"""====================================================================================================="""

# creating a class for the for accessing  and manipulating the data in the database for the account 
class AccountData():
    def __init__(self):
        self.conn = sqlite3.connect("Account_Data.db")
        self.c = self.conn.cursor()
        # crete coulumn for total balance 
        self.c.execute('''CREATE TABLE IF NOT EXISTS Account_Data(id INTEGER PRIMARY KEY,Type BOOLEAN, Description TEXT, Amount INTEGER, Record_time DATETIME)''') 

    # add new record
    def add_new_record(self, Type, Description, Amount):
        # type 1 for expense and 0 for income
        if Type:
            Amount = -Amount
        self.c.execute("INSERT INTO Account_Data VALUES (NULL, ?, ?, ?, ?)", (Type, Description, Amount, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
 
    # delete record
    def delete_record(self, id):
        self.c.execute("DELETE FROM Account_Data WHERE id = ?", (id,))
        self.conn.commit()


    # get record by id
    def get_record(self, id):
        self.c.execute("SELECT * FROM Account_Data WHERE id = ?", (id,))
        rows = self.c.fetchone()
        return rows

    # get all records
    def get_all_records(self):
        self.c.execute("SELECT Description, Amount, Record_time FROM Account_Data WHERE Record_time >= date('now', '-30 days') ORDER BY Record_time DESC")
        rows = self.c.fetchall()
        return rows

    # get total balance
    def get_total_Balance(self):
        self.c.execute("SELECT SUM(Amount) FROM Account_Data")
        rows = self.c.fetchone()
        print(rows)
        return rows[0]

    # destroy the object
    def __del__(self):
        self.conn.close()

"====================================================================================================="


# creating a class for the for accessing  and manipulating the data in the database for the skills
class SkillsData():
    def __init__(self):
        self.conn = sqlite3.connect("Skills.db")
        self.c = self.conn.cursor()

    # get all major categorys of skills  
    def get_all_categorys(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = self.c.fetchall()
        all_tables = []
        for row in rows:
            all_tables.append(row[0])
        return all_tables   
        
        
    # create new category of skills
    def add_category(self, category):
        self.c.execute("CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY, Skill TEXT, SkillLevel INTEGER, SkillDescription TEXT,learned TEXT,to_lean TEXT,last_accessed DATETIME)".format(category))
        self.conn.commit()
        print("table created")

    # add skills to the category
    def add_skills(self, category, skill, skillLevel, skillDescription,learned,to_lean):
        self.c.execute("INSERT INTO {} VALUES (NULL, ?, ?, ?, ?, ?, ?)".format(category), (skill, skillLevel, skillDescription,learned,to_lean, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    # get all skills in the category
    def get_all_skills(self, category):
        self.c.execute("SELECT id,skill FROM {}".format(category))
        rows = self.c.fetchall()
        return rows

    # get skill by id
    def get_skill(self, category, id):
        self.c.execute("SELECT * FROM {} WHERE id = ?".format(category), (id,))
        rows = self.c.fetchone()
        return rows

    # update skill by id
    def update_skill(self, category, id, skill, skillLevel, skillDescription,learned,to_lean):
        self.c.execute("UPDATE {} SET skill = ?, skillLevel = ?, skillDescription = ?, learned = ?, to_lean = ?, last_accessed = ? WHERE id = ?".format(category), (skill, skillLevel, skillDescription,learned,to_lean, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))
        self.conn.commit()

    # delete skill
    def delete_skill(self, category, id):
        self.c.execute("DELETE FROM {} WHERE id = ?".format(category), (id,))
        self.conn.commit()

    # delete category
    def delete_category(self, category):
        self.c.execute("DROP TABLE {}".format(category))
        self.conn.commit()
    
    # destroy the object
    def __del__(self):
        self.conn.close()
