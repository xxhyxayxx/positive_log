import unittest
import sqlite3
import os

import db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_temp.db"
        db.DATABASE = self.test_db
        
    def tearDown(self):
        if os.path.exists("test_temp.db"):
            os.remove("test_temp.db")
    
    def test_get_db_returns_connection(self):
        conn = db.get_db()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_get_db_uses_row_factory(self):
        conn = db.get_db()
        self.assertEqual(conn.row_factory, sqlite3.Row)
        conn.close()
    
    def test_init_db_creates_table(self):
        db.init_db()
        conn = db.get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        table_exists = cursor.fetchone()
        
        self.assertIsNotNone(table_exists, 'logsテーブルが作成されていません')
        conn.close()

        

if __name__ ==  '__main__':
    unittest.main()