import pytest
from src.modules import sqlite_db, firebase_db

class TestRPA_Generate_DB():
  
  def test_migrate_SQLiteDb(self):
    sqlite_db.migrate_SQLiteDb()

  def test_migrate_firebase_db(self):
    firebase_db.migrate_firebase_db()