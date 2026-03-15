import unittest
from app import app
from db import init_db, save_log, DATABASE
import os

class TestApp(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_app_temp.db"
        import db
        db.DATABASE = self.test_db
        with db.get_db() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) 
            ''')
        
        self.app = app.test_client()
        self.app.testing = True
        
    def tearDown(self):
        if os.path.exists("test_app_temp.db"):
            os.remove("test_app_temp.db")
            
    def test_index_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_index_display_logs(self):
        test_context = "Test context"
        save_log(test_context)
        
        response = self.app.get('/')
        
        self.assertIn(test_context, response.data.decode('utf-8'))
    
    def test_add_log(self):
        test_context = "New Positive Thought"
        response = self.app.post('/add', data={"context": test_context}, follow_redirects=True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_context, response.data.decode('utf-8'))
        
        from db import get_all_logs
        logs = get_all_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['context'], test_context)
    
    def test_delete_log(self):
        test_context = "Delete context"
        save_log(test_context)
        
        from db import get_all_logs
        logs = get_all_logs()
        log_id = logs[0]['id']
        
        response = self.app.post(f'/delete/{log_id}', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_context, response.data.decode('utf-8'))
        remaining_logs = get_all_logs()
        self.assertEqual(len(remaining_logs), 0)
            

