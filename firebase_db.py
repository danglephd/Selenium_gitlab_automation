import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import sqlite
from sqlite import GitLab_Issue_Obj

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./Firebase/projp21-17b04-firebase-adminsdk-kgxr3-5292b73c39.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projp21-17b04-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def create_db():
    print('>>>create_db')
    lst_gitLab_issue_obj = sqlite.getListIssue("")
    ref = db.reference('issues')
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
            'issue_number': gitLab_issue_obj.issue_number
        })


def save(gitLab_issue_obj):
    print('>>>save')
    ref = db.reference('issues')
    
    for item in gitLab_issue_obj:
        ref.push({
            'project': item.project,
            'path': item.path,
            'test_state': item.test_state,
            'issue_test_url': item.issue_test_url,
            'issue_test_number': item.issue_test_number,
            'issue_url': item.issue_url,
            'issue_number': item.issue_number
        })

def executeQuery():
    print('>>>executeQuery')

def update_testcase_status(issue_url):
    print('>>>update_testcase_status')
    try:
        ref = db.reference('issues')
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
        ref = db.reference('issues')
        data = []
        snapshot = ref.order_by_child(criteria[0]).equal_to(criteria[1]).get()
        
        for key, val in snapshot.items():
            print('{0} => {1}'.format(key, val))
            data.append(GitLab_Issue_Obj(
                id=0, project=val['project'], path=val['path'], test_state=val['test_state'], 
                issue_test_url=val['issue_test_url'], issue_test_number=val['issue_test_number'], issue_number=val['issue_number'], issue_url=val['issue_url']))
        return data
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

def getAllIssue():
    print('>>>getAllIssue')
    try:
        ref = db.reference('issues')
        data = []
        snapshot = ref.get()
        
        for key, val in snapshot.items():
            # print('{0} => {1}'.format(key, val))
            data.append(GitLab_Issue_Obj(
                id=0, project=val['project'], path=val['path'], test_state=val['test_state'], 
                issue_test_url=val['issue_test_url'], issue_test_number=val['issue_test_number'], issue_number=val['issue_number'], issue_url=val['issue_url']))
        return data
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    