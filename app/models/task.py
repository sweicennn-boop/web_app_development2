import sqlite3
import os

def get_db_connection():
    """取得資料庫連線，並設定 row_factory 以便透過欄位名稱存取資料"""
    # 確保 instance 資料夾存在
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    @staticmethod
    def get_all(status_filter=None):
        """取得所有任務，可選傳入 status_filter ('completed' 或 'pending') 進行篩選"""
        conn = get_db_connection()
        try:
            if status_filter == 'completed':
                tasks = conn.execute('SELECT * FROM tasks WHERE is_completed = 1 ORDER BY created_at DESC').fetchall()
            elif status_filter == 'pending':
                tasks = conn.execute('SELECT * FROM tasks WHERE is_completed = 0 ORDER BY created_at DESC').fetchall()
            else:
                tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
            return tasks
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id):
        """根據 ID 取得單筆任務"""
        conn = get_db_connection()
        try:
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            return task
        finally:
            conn.close()

    @staticmethod
    def create(data):
        """新增一筆任務
        data 應包含: title, description, due_date, priority
        """
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)',
                (data.get('title'), data.get('description'), data.get('due_date'), data.get('priority', 'medium'))
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def update(task_id, data):
        """更新現有任務"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ? WHERE id = ?',
                (data.get('title'), data.get('description'), data.get('due_date'), data.get('priority'), task_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete(task_id):
        """刪除任務"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def toggle_status(task_id):
        """切換任務完成狀態"""
        conn = get_db_connection()
        try:
            task = conn.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
            if task:
                new_status = 0 if task['is_completed'] == 1 else 1
                conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
                conn.commit()
                return True
            return False
        finally:
            conn.close()

    @staticmethod
    def get_stats():
        """取得任務統計資訊"""
        conn = get_db_connection()
        try:
            total = conn.execute('SELECT COUNT(*) as count FROM tasks').fetchone()['count']
            completed = conn.execute('SELECT COUNT(*) as count FROM tasks WHERE is_completed = 1').fetchone()['count']
            
            completion_rate = 0
            if total > 0:
                completion_rate = round((completed / total) * 100)
                
            return {
                'total': total,
                'completed': completed,
                'pending': total - completed,
                'completion_rate': completion_rate
            }
        finally:
            conn.close()
