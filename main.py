from flask import Flask
import os
import sqlite3

def create_app():
    # 建立 Flask 應用實體，明確指定 template 和 static 的路徑
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 設定 SECRET_KEY (用於 flash messages 等)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-for-local-testing')
    
    # 註冊 Blueprint
    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    return app

def init_db():
    """初始化資料庫"""
    # 確保 instance 資料夾存在
    os.makedirs('instance', exist_ok=True)
    
    # 讀取 schema.sql 並執行
    conn = sqlite3.connect('instance/database.db')
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

# 供 flask run 執行的實體
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
