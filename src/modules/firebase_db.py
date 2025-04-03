from .db import sqlite, firebase
import logging
import os

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "firebase_migration.log")

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler(log_file)
console_handler = logging.StreamHandler()

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def migrate_firebase_db():
    """
    Migrate data from SQLite to Firebase
    """
    logger.info("Starting migration from SQLite to Firebase")
    try:
        criteria = ""
        issue_list = sqlite.getListIssue(criteria)
        logger.info(f"Found {len(issue_list)} issues in SQLite")
        
        save_item = []
        for issue_item in issue_list:
            try:
                criteria = ['issue_url', issue_item.issue_url]
                data = firebase.getListIssue(criteria)
                
                if not data:
                    logger.info(f"New issue found: {issue_item.issue_url}")
                    save_item.append(issue_item)
                else:
                    logger.info(f"Existing issue found: {issue_item.issue_url}")
                    item_to_update = None
                    for item in data:
                        if item.issue_test_url == issue_item.issue_test_url:
                            item_to_update = item
                            break
                            
                    if item_to_update is None:
                        logger.info(f"New test URL found: {issue_item.issue_test_url}")
                        save_item.append(issue_item)
                    else:
                        logger.info(f"Updating issue: {issue_item.issue_url}")
                        firebase.update(item_to_update.id, issue_item)
                        
            except Exception as e:
                logger.error(f"Error processing issue {issue_item.issue_url}: {str(e)}")
                continue

        if save_item:
            logger.info(f"Saving {len(save_item)} new issues")
            firebase.save(save_item)
            
        logger.info("Migration completed successfully")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise 