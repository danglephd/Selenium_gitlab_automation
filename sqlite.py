import sqlite3

def createTable():
    conn = sqlite3.connect('gitlab_issue.db')
    c = conn.cursor()
    print("Opened database successfully")	
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ISSUE' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0] == 1: 
        print('Table exists.')
    else:
        print("Create table ISSUE")
        conn.execute('''CREATE TABLE ISSUE
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                project        TEXT    NOT NULL, 
                path        TEXT    NOT NULL, 
                test_state        TEXT    NOT NULL, 
                issue_test_url        TEXT    NOT NULL, 
                issue_test_number        TEXT    NOT NULL, 
                issue_number        TEXT    NOT NULL, 
                issue_url        TEXT    NOT NULL
                );''')

        print("Table created successfully")

        conn.close()

def save(gitLab_issue_obj):
    conn = sqlite3.connect('gitlab_issue.db')
    # print("Opened database successfully")

    for item in gitLab_issue_obj:
        # print(">>item", item.project, item.path, item.test_state, item.issue_test_url, item.issue_test_number, item.issue_number, item.issue_url)
        conn.execute("""INSERT INTO ISSUE (project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url) 
                     VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                     .format(item.project, item.path, item.test_state, item.issue_test_url, item.issue_test_number, item.issue_number, item.issue_url))

    conn.commit()
    # print("Records insert successfully")

    conn.close()
    
def initTable(lst_issue):
    createTable()
    conn = sqlite3.connect('gitlab_issue.db')
    print("Opened database successfully")

    print("Truncate table ISSUE")
    conn.execute("DELETE FROM ISSUE")
    conn.commit()
    
    for item in lst_issue:
        print(">>item", item.project, item.path, item.test_state, item.issue_test_url, item.issue_test_number, item.issue_number, item.issue_url)
        conn.execute("""INSERT INTO ISSUE (project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url) 
                     VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                     .format(item.project, item.path, item.test_state, item.issue_test_url, item.issue_test_number, item.issue_number, item.issue_url))

    conn.commit()
    print("Records created successfully")

    conn.close()
    
def executeQuery(query):
    try:
        conn = sqlite3.connect('gitlab_issue.db')
        # print("Opened database successfully")
        # print(">>>sql_query: " + query)
        
        # for query in query_lst:
        conn.execute(query)
        conn.commit()
        
        # print("Operation done successfully")
        conn.close()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    
def getListIssue(criteria):
    try:
        conn = sqlite3.connect('gitlab_issue.db')
        # print("Opened database successfully")
        sql_query = """SELECT id, project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url 
                              from ISSUE """ + criteria
        # print(">>>sql_query: " + sql_query)
        cursor = conn.execute(sql_query)
        data = []
        for row in cursor:
            print("project = ", row[1])
            print("path = ", row[2])
            print("state = ", row[3])
            print("test_url = ", row[4])
            print("test_no = ", row[5])
            print("issue_no = ", row[6])
            print("issue_url = ", row[7], "\n")
            data.append(GitLab_Issue_Obj(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        # print("Operation done successfully")
        conn.close()
        return data
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        
class GitLab_Issue_Obj:
    def __init__(self, id, project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url):
        self.id = id
        self.issue_number = issue_number
        self.issue_url = issue_url
        self.issue_test_number = issue_test_number
        self.issue_test_url = issue_test_url
        self.project = project
        self.test_state = test_state

        self.path = path