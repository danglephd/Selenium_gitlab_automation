from .db import sqlite, firebase_db

def migrate_firebase_db():
    print('>>>migrate_firebase_db')
    criteria = ""
    issue_list = sqlite.getListIssue(criteria)
    print('>>>len', len(issue_list))
    save_item = []
    for issue_item in issue_list:
        criteria = ['issue_url', issue_item.issue_url]
        data = firebase_db.getListIssue(criteria)
        if len(data) <= 0:
            save_item.append(issue_item)
        else:
            print('>>>Exist item, ', len(data))
            item_to_update = None
            for item in data:
                if item.issue_test_url == issue_item.issue_test_url:
                    item_to_update = item
                    break
                if item_to_update is None:
                    save_item.append(issue_item)
                else:
                    firebase_db.update(item_to_update.id, issue_item)

    if len(save_item) > 0:
        print('>>>Save len: ',  len(save_item) )
        firebase_db.save(save_item) 
