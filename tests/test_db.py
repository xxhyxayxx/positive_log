import unittest
import sqlite3
import os

import db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_temp.db"
        db.DATABASE = self.test_db
        db.init_db()
        
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

    def test_insert_and_get_log(self):
        db.init_db()
        test_context = "I felt happy because I imagined a beautifuly scene in Scotland."
        
        from db import save_log, get_all_logs
        save_log(test_context)
        
        logs = get_all_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['context'], test_context)
        

if __name__ ==  '__main__':
    unittest.main()