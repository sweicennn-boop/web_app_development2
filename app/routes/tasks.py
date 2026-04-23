from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

# 建立名為 tasks 的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@tasks_bp.route('/tasks')
def index():
    """
    任務列表頁面 (GET / 或 GET /tasks)
    - 接收可選的 ?status= 參數 (completed 或 pending)
    - 取得任務統計資料
    - 取得任務列表
    - 渲染 tasks/index.html
    """
    pass

@tasks_bp.route('/tasks/new')
def new():
    """
    新增任務頁面 (GET /tasks/new)
    - 渲染 tasks/new.html 顯示空白表單
    """
    pass

@tasks_bp.route('/tasks', methods=['POST'])
def create():
    """
    建立任務 (POST /tasks)
    - 接收表單提交的資料 (title, description, due_date, priority)
    - 驗證 title 必填
    - 呼叫 Task.create()
    - 成功後重導向至首頁
    """
    pass

@tasks_bp.route('/tasks/<int:id>')
def detail(id):
    """
    任務詳情 (GET /tasks/<id>)
    - 呼叫 Task.get_by_id(id)
    - 找不到則 404
    - 渲染 tasks/detail.html
    """
    pass

@tasks_bp.route('/tasks/<int:id>/edit')
def edit(id):
    """
    編輯任務頁面 (GET /tasks/<id>/edit)
    - 呼叫 Task.get_by_id(id) 取得原始資料
    - 找不到則 404
    - 渲染 tasks/edit.html 並帶入原始資料
    """
    pass

@tasks_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新任務 (POST /tasks/<id>/update)
    - 接收表單提交的資料
    - 驗證 title 必填
    - 呼叫 Task.update(id, data)
    - 成功後重導向至首頁
    """
    pass

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除任務 (POST /tasks/<id>/delete)
    - 呼叫 Task.delete(id)
    - 成功後發送 flash 訊息並重導向至首頁
    """
    pass

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle(id):
    """
    切換完成狀態 (POST /tasks/<id>/toggle)
    - 呼叫 Task.toggle_status(id)
    - 重導向回首頁 (或根據 referer 回前一頁)
    """
    pass
