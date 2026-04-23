from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

# 建立名為 tasks 的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@tasks_bp.route('/tasks')
def index():
    """任務列表頁面"""
    status_filter = request.args.get('status')
    
    # 從資料庫取得統計資料與任務列表
    stats = Task.get_stats()
    tasks = Task.get_all(status_filter)
    
    return render_template('tasks/index.html', tasks=tasks, stats=stats, current_status=status_filter)

@tasks_bp.route('/tasks/new')
def new():
    """新增任務頁面"""
    return render_template('tasks/new.html')

@tasks_bp.route('/tasks', methods=['POST'])
def create():
    """建立任務"""
    # 取得表單資料
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip()
    priority = request.form.get('priority', 'medium')
    
    # 驗證必填欄位
    if not title:
        flash('任務標題為必填欄位！', 'danger')
        return render_template('tasks/new.html', 
                               description=description, 
                               due_date=due_date, 
                               priority=priority)
    
    # 準備寫入資料
    data = {
        'title': title,
        'description': description,
        'due_date': due_date if due_date else None,
        'priority': priority
    }
    
    # 寫入資料庫
    Task.create(data)
    flash('任務已成功新增！', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>')
def detail(id):
    """任務詳情"""
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
        
    return render_template('tasks/detail.html', task=task)

@tasks_bp.route('/tasks/<int:id>/edit')
def edit(id):
    """編輯任務頁面"""
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
        
    return render_template('tasks/edit.html', task=task)

@tasks_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update(id):
    """更新任務"""
    # 先確認任務是否存在
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
        
    # 取得表單資料
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip()
    priority = request.form.get('priority', 'medium')
    
    # 驗證必填欄位
    if not title:
        flash('任務標題為必填欄位！', 'danger')
        # 建立一個臨時字典模擬 task 物件傳回給模板，以免使用者輸入消失
        temp_task = {
            'id': id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority
        }
        return render_template('tasks/edit.html', task=temp_task)
        
    # 準備更新資料
    data = {
        'title': title,
        'description': description,
        'due_date': due_date if due_date else None,
        'priority': priority
    }
    
    # 更新資料庫
    Task.update(id, data)
    flash('任務已成功更新！', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除任務"""
    if Task.delete(id):
        flash('任務已刪除！', 'success')
    else:
        flash('刪除失敗！', 'danger')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle(id):
    """切換完成狀態"""
    if Task.toggle_status(id):
        flash('任務狀態已更新！', 'success')
    else:
        flash('狀態更新失敗！', 'danger')
        
    # 回到原來篩選的頁面
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)
    return redirect(url_for('tasks.index'))
