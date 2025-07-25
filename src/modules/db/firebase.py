import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# import sqlite module
from . import sqlite
from .sqlite import GitLab_Issue_Obj

# Constants
ISSUES_COLLECTION = 'issues'

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./Firebase/projp21-17b04-firebase-adminsdk-kgxr3-5292b73c39.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projp21-17b04-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def create_db():
    print('>>>create_db')
    lst_gitLab_issue_obj = sqlite.getListIssue("")
    ref = db.reference(ISSUES_COLLECTION)
    # ref.set({
    #     'issues': 
    #         {
    #             'issue1': {
    #                 'project': 'test',
    #                 'path': 'url://xx',
    #                 'test_state': 'Created',
    #                 'issue_test_url': 'url://xx',
    #                 'issue_test_number': 11,
    #                 'issue_url': 'url://xx',
    #                 'duedate': 'duedate',
    #                 'issue_number': 11
    #             }
    #         }
    #     })
    for gitLab_issue_obj in lst_gitLab_issue_obj:
        ref.push({
            'project': gitLab_issue_obj.project,
            'path': gitLab_issue_obj.path,
            'test_state': gitLab_issue_obj.test_state,
            'issue_test_url': gitLab_issue_obj.issue_test_url,
            'issue_test_number': gitLab_issue_obj.issue_test_number,
            'issue_url': gitLab_issue_obj.issue_url,
            'duedate': gitLab_issue_obj.duedate,
            'issue_number': gitLab_issue_obj.issue_number
        })

def save(gitLab_issue_obj):
    print('>>>save')
    ref = db.reference(ISSUES_COLLECTION)
    
    for item in gitLab_issue_obj:
        ref.push({
            'project': item.project,
            'path': item.path,
            'test_state': item.test_state,
            'issue_test_url': item.issue_test_url,
            'issue_test_number': item.issue_test_number,
            'issue_url': item.issue_url,
            'duedate': item.duedate,
            'issue_number': item.issue_number
        })

def update(id, gitLab_issue_obj):
    print('>>>update ', id, gitLab_issue_obj.duedate)
    ref = db.reference(ISSUES_COLLECTION)
    box_ref = ref.child(id)
    box_ref.update({
        'test_state': gitLab_issue_obj.test_state,
        'duedate': gitLab_issue_obj.duedate,
    })

def update_issue_test_state(id, test_state):
    print('>>>update_status ', id, test_state)
    ref = db.reference(ISSUES_COLLECTION)
    box_ref = ref.child(id)
    box_ref.update({
        'test_state': test_state
    })

def update_testcase_status(issue_url):
    print('>>>update_testcase_status')
    try:
        ref = db.reference(ISSUES_COLLECTION)
        snapshot = ref.order_by_child("issue_url").equal_to(issue_url).limit_to_first(2).get()
        for key, val in snapshot.items():
            print(f"issue_key {key=}")
            box_ref = ref.child(key)
            box_ref.update({
                'test_state': 'Done'
            })
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

def getListIssue(criteria):
    print('>>>getListIssue', criteria)
    try:
        ref = db.reference(ISSUES_COLLECTION)
        data = []
        snapshot = ref.order_by_child(criteria[0]).equal_to(criteria[1]).get()
        
        for key, val in snapshot.items():
            print('{0} => {1}'.format(key, val))
            duedate = " "

            try:
                duedate = val['duedate']
            except Exception as err:
                print(f"Duedate is not exist")
                duedate = " "

            data.append(GitLab_Issue_Obj(
                id=key, 
                project=val['project'], 
                path=val['path'], 
                test_state=val['test_state'], 
                issue_test_url=val['issue_test_url'], 
                issue_test_number=val['issue_test_number'], 
                issue_number=val['issue_number'], 
                issue_url=val['issue_url'],
                duedate=duedate
                ))
        return data
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

def getListIssue2(criteria):
    """
    Get list of issues with multiple values
    criteria format: [field, operator, value_list]
    Example: ['issue_url', 'IN', ['url1', 'url2', 'url3']]
    """
    print('>>>getListIssue2', criteria)
    try:
        if len(criteria) != 3:
            raise ValueError("Invalid criteria format. Expected: [field, operator, value_list]")
            
        field, operator, value_list = criteria
        if not isinstance(value_list, list):
            raise ValueError("value_list must be a list")
            
        ref = db.reference(ISSUES_COLLECTION)
        data = []
        
        # Get all issues first
        snapshot = ref.get()
        if not snapshot:
            return data
            
        # Process all issues in memory
        for key, val in snapshot.items():
            try:
                # Check if the field exists and matches any value in the list
                if field in val and val[field] in value_list:
                    duedate = val.get('duedate', " ")
                    
                    data.append(GitLab_Issue_Obj(
                        id=key, 
                        project=val['project'], 
                        path=val['path'], 
                        test_state=val['test_state'], 
                        issue_test_url=val['issue_test_url'], 
                        issue_test_number=val['issue_test_number'], 
                        issue_number=val['issue_number'], 
                        issue_url=val['issue_url'],
                        duedate=duedate
                    ))
            except Exception as e:
                print(f"Error processing issue {key}: {str(e)}")
                continue
                
        return data
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return []

def getAllIssue():
    print('>>>getAllIssue')
    ref = db.reference(ISSUES_COLLECTION)
    data = []
    snapshot = ref.get()
    
    for key, val in snapshot.items():
        # print('{0} => {1}'.format(key, val))
        duedate = " "

        try:
            duedate = val['duedate']
        except Exception as err:
            print(f"Duedate is not exist")
            duedate = " "
        data.append(GitLab_Issue_Obj(
            id=0, project=val['project'], path=val['path'], test_state=val['test_state'], 
            issue_test_url=val['issue_test_url'], issue_test_number=val['issue_test_number'], 
            issue_number=val['issue_number'], issue_url=val['issue_url'], duedate=duedate))
    return data
    