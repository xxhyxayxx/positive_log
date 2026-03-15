import unittest
import sqlite3
import os
from db import get_db, DATABASE

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_temp.db"
        import db
        db.DATABASE = self.test_db
        
    def tearDown(self):
        if os.path.exists("test_temp.db"):
            os.remove("test_temp.db")
    
    def test_get_db_returns_connection(self):
        conn = get_db()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_get_db_uses_row_factory(self):
        conn = get_db()
        self.assertEqual(conn.row_factory, sqlite3.Row)
        conn.close()

if __name__ ==  '__main__':
    unittest.main()