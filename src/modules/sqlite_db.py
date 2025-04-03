from .db import sqlite, firebase
import logging
from typing import List
import re
import os

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "sqlite_migration.log")

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

def _escape_sql_value(value: str) -> str:
    """
    Escape special characters in SQL values to prevent SQL injection
    """
    if value is None:
        return "NULL"
    # Replace single quotes with two single quotes
    return str(value).replace("'", "''")

def _validate_issue(issue) -> bool:
    """
    Validate issue data before processing
    """
    required_fields = ['project', 'path', 'test_state', 'issue_test_url', 
                      'issue_test_number', 'issue_number', 'issue_url']
    
    # Check required fields
    if not all(hasattr(issue, field) for field in required_fields):
        return False
        
    # Validate URL format
    url_pattern = re.compile(r'https?://\S+')
    if not url_pattern.match(issue.issue_url) or not url_pattern.match(issue.issue_test_url):
        return False
        
    # Validate test state
    valid_states = ['Created', 'Done', 'Finish', 'Old']
    if issue.test_state not in valid_states:
        return False
        
    return True

def _process_batch(batch: List):
    """
    Process a batch of issues with improved error handling and performance
    """
    logger.info(f"Processing batch of {len(batch)} issues")
    try:
        # Get all issue URLs in the batch
        issue_urls = [issue.issue_url for issue in batch]
        
        # Build WHERE clause for the query with escaped values
        escaped_urls = [_escape_sql_value(url) for url in issue_urls]
        where_clause = "WHERE issue_url IN ('" + "','".join(escaped_urls) + "')"
        
        # Get existing issues
        existing_issues = sqlite.getListIssue(where_clause)
        existing_map = {(issue.issue_url, issue.issue_test_url): issue 
                       for issue in existing_issues}
        logger.info(f"Found {len(existing_issues)} existing issues")
        
        # Prepare lists for bulk operations
        new_issues = []
        updates = []
        
        # Categorize issues
        for fb_issue in batch:
            try:
                # Validate issue data
                if not _validate_issue(fb_issue):
                    continue
                    
                key = (fb_issue.issue_url, fb_issue.issue_test_url)
                if key in existing_map:
                    existing = existing_map[key]
                    is_finished = fb_issue.test_state in ['Done', 'Finish', 'Old']
                    if is_finished or existing.test_state == 'Created':
                        updates.append((fb_issue.test_state, existing.id))
                else:
                    new_issues.append(fb_issue)
            except Exception as e:
                logger.error(f"Error processing issue {fb_issue.issue_url}: {str(e)}")
                continue
        
        logger.info(f"Found {len(new_issues)} new issues and {len(updates)} updates")
        
        # Process new issues and updates
        if new_issues:
            _bulk_insert(new_issues)
        if updates:
            _bulk_update(updates)
                
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        raise

def _bulk_insert(issues: List):
    """
    Bulk insert new issues with input validation and value escaping
    """
    if not issues:
        return
        
    try:
        # Prepare values for bulk insert
        for issue in issues:
            # Validate issue data
            if not _validate_issue(issue):
                continue
                
            # Escape all values
            query = f"""
                INSERT INTO ISSUE (project, path, test_state, issue_test_url, 
                                 issue_test_number, issue_number, issue_url, duedate)
                VALUES ('{_escape_sql_value(issue.project)}', 
                       '{_escape_sql_value(issue.path)}', 
                       '{_escape_sql_value(issue.test_state)}', 
                       '{_escape_sql_value(issue.issue_test_url)}', 
                       '{_escape_sql_value(issue.issue_test_number)}',
                       '{_escape_sql_value(issue.issue_number)}', 
                       '{_escape_sql_value(issue.issue_url)}', 
                       '{_escape_sql_value(issue.duedate)}')
            """
            sqlite.executeQuery(query)
            
        logger.info(f"Successfully inserted {len(issues)} new issues")
            
    except Exception as e:
        logger.error(f"Error in bulk insert: {str(e)}")
        raise

def _bulk_update(updates: List):
    """
    Bulk update existing issues with input validation and value escaping
    """
    if not updates:
        return
        
    try:
        # Execute bulk update
        for test_state, issue_id in updates:
            # Validate test state
            if test_state not in ['Done', 'Finish', 'Old', 'Created']:
                continue
                
            query = f"""
                UPDATE ISSUE
                SET test_state = '{_escape_sql_value(test_state)}'
                WHERE id = {issue_id}
            """
            sqlite.executeQuery(query)
            
        logger.info(f"Successfully updated {len(updates)} issues")
            
    except Exception as e:
        logger.error(f"Error in bulk update: {str(e)}")
        raise

def migrate_SQLiteDb():
    """
    Migrate data from Firebase to SQLite with improved performance and error handling
    """
    logger.info("Starting migration from Firebase to SQLite")
    try:
        # Get all issues from Firebase
        fb_issue_list = firebase.getAllIssue()
        logger.info(f"Found {len(fb_issue_list)} issues in Firebase")

        # Process in batches for better performance
        batch_size = 1000
        total_batches = (len(fb_issue_list) + batch_size - 1) // batch_size
        logger.info(f"Processing {total_batches} batches")
        
        for i in range(0, len(fb_issue_list), batch_size):
            batch = fb_issue_list[i:i + batch_size]
            try:
                logger.info(f"Processing batch {i//batch_size + 1}/{total_batches}")
                _process_batch(batch)
                logger.info(f"Completed batch {i//batch_size + 1}/{total_batches}")
            except Exception as e:
                logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                # Continue with next batch even if current batch fails
                continue
            
        logger.info("Migration completed successfully")
            
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise 
