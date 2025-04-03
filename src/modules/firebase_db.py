from .db import sqlite, firebase
import logging
import os
import time
from datetime import datetime

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

def _retry_operation(operation, max_retries=3, delay=1):
    """Retry an operation with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Retry {attempt + 1}/{max_retries} after error: {str(e)}")
            time.sleep(delay * (2 ** attempt))

def migrate_firebase_db():
    """
    Migrate data from SQLite to Firebase
    """
    start_time = time.time()
    logger.info("Starting migration from SQLite to Firebase")
    try:
        criteria = ""
        issue_list = sqlite.getListIssue(criteria)
        logger.info(f"Found {len(issue_list)} issues in SQLite")
        
        # Process in batches
        batch_size = 100  # Process 100 issues at a time
        total_batches = (len(issue_list) + batch_size - 1) // batch_size
        
        for i in range(0, len(issue_list), batch_size):
            batch_start_time = time.time()
            batch_issues = issue_list[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{total_batches}")
            
            try:
                save_item = []
                update_items = []
                
                for issue_item in batch_issues:
                    try:
                        criteria = ['issue_url', issue_item.issue_url]
                        data = _retry_operation(
                            lambda: firebase.getListIssue(criteria)
                        )
                        
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
                                logger.info(f"Adding issue to update list: {issue_item.issue_url}")
                                update_items.append((item_to_update.id, issue_item))
                                
                    except Exception as e:
                        logger.error(f"Error processing issue {issue_item.issue_url}: {str(e)}")
                        continue

                # Save new issues
                if save_item:
                    logger.info(f"Saving {len(save_item)} new issues")
                    _retry_operation(lambda: firebase.save(save_item))
                    
                # Update existing issues
                if update_items:
                    logger.info(f"Updating {len(update_items)} existing issues")
                    for issue_id, issue_data in update_items:
                        try:
                            _retry_operation(lambda: firebase.update(issue_id, issue_data))
                        except Exception as e:
                            logger.error(f"Error updating issue {issue_id}: {str(e)}")
                            continue
                            
            except Exception as e:
                logger.error(f"Error processing batch: {str(e)}")
                continue
                
            batch_time = time.time() - batch_start_time
            logger.info(f"Batch {i//batch_size + 1}/{total_batches} completed in {batch_time:.2f} seconds")
                
        total_time = time.time() - start_time
        logger.info(f"Migration completed successfully in {total_time:.2f} seconds")
        
    except Exception as e:
        total_time = time.time() - start_time
        logger.error(f"Migration failed after {total_time:.2f} seconds: {str(e)}")
        raise 