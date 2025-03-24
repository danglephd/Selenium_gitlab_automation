from .db import sqlite, firebase_db

def migrate_SQLiteDb():
    print('>>>migrate_SQLiteDb')
    fb_issue_list = firebase_db.getAllIssue()
    print('>>>len', len(fb_issue_list))

    for fb_issue_item in fb_issue_list:
        criteria = "WHERE issue_url = '{0}' and issue_test_url = '{1}'"
        sqlite_issue_lst = sqlite.getListIssue(str.format(criteria, fb_issue_item.issue_url, fb_issue_item.issue_test_url))
        isFinishIssue = "and test_state = 'Created'"

        if fb_issue_item.test_state == 'Done' or  fb_issue_item.test_state == 'Finish' or fb_issue_item.test_state == 'Old':
            isFinishIssue = ""
        else:
            isFinishIssue = "and test_state = 'Created'"

        if len(sqlite_issue_lst) <= 0:
            sqlite.save([fb_issue_item]) 
        else:
            print('>>>Exist item, ', len(sqlite_issue_lst))
        for sqlite_item in sqlite_issue_lst:
            query = """UPDATE ISSUE
    SET test_state = '{1}'
    WHERE id = {0} {2};
    """.format(sqlite_item.id, fb_issue_item.test_state, isFinishIssue)
            sqlite.executeQuery(query) 
