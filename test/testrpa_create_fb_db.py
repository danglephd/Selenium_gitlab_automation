import pytest
from src.modules import firebase_db

class TestRPA_Create_DB():
  
  def test_create_firebase_db(self):
    firebase_db.create_firebase_db()
