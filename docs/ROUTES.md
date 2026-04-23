# 路由與頁面設計 — 任務管理系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 任務列表 | GET | `/` 或 `/tasks` | `templates/tasks/index.html` | 首頁，顯示所有任務（支援狀態篩選） |
| 新增任務頁面 | GET | `/tasks/new` | `templates/tasks/new.html` | 顯示新增任務的表單 |
| 建立任務 | POST | `/tasks` | — | 接收新增表單資料，存入 DB，成功後重導向至列表頁 |
| 任務詳情 | GET | `/tasks/<int:id>` | `templates/tasks/detail.html` | 顯示單筆任務的完整資訊 |
| 編輯任務頁面 | GET | `/tasks/<int:id>/edit` | `templates/tasks/edit.html` | 顯示編輯任務的表單（帶有原始資料） |
| 更新任務 | POST | `/tasks/<int:id>/update` | — | 接收編輯表單資料，更新 DB，成功後重導向至列表頁 |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除單筆任務，成功後重導向至列表頁 |
| 切換完成狀態 | POST | `/tasks/<int:id>/toggle` | — | 一鍵切換任務完成/未完成狀態，成功後重導向至列表頁 |

---

## 2. 每個路由的詳細說明

### `GET /` 或 `GET /tasks` (任務列表)
- **輸入**: URL 查詢參數 `?status=` (可選，`completed` 或 `pending`)
- **處理邏輯**: 呼叫 `Task.get_stats()` 取得統計資料，呼叫 `Task.get_all(status)` 取得任務清單。
- **輸出**: 渲染 `tasks/index.html`，傳入 `tasks` 與 `stats` 變數。

### `GET /tasks/new` (新增任務頁面)
- **輸入**: 無
- **處理邏輯**: 僅負責顯示表單。
- **輸出**: 渲染 `tasks/new.html`。

### `POST /tasks` (建立任務)
- **輸入**: 表單資料 (`title`, `description`, `due_date`, `priority`)
- **處理邏輯**: 驗證 `title` 是否為空。若為空，發送 flash 錯誤訊息並重新渲染 `new.html`；若成功，呼叫 `Task.create(data)`。
- **輸出**: 成功則重導向 (redirect) 至 `/`，失敗則重新渲染表單。

### `GET /tasks/<int:id>` (任務詳情)
- **輸入**: URL 中的任務 `id`
- **處理邏輯**: 呼叫 `Task.get_by_id(id)`，若找不到則回傳 404。
- **輸出**: 渲染 `tasks/detail.html`，傳入 `task` 變數。

### `GET /tasks/<int:id>/edit` (編輯任務頁面)
- **輸入**: URL 中的任務 `id`
- **處理邏輯**: 呼叫 `Task.get_by_id(id)` 取得原始資料以預填表單，若找不到則回傳 404。
- **輸出**: 渲染 `tasks/edit.html`，傳入 `task` 變數。

### `POST /tasks/<int:id>/update` (更新任務)
- **輸入**: URL 中的任務 `id`，以及表單資料 (`title`, `description`, `due_date`, `priority`)
- **處理邏輯**: 驗證 `title` 是否為空。若為空，發送 flash 錯誤訊息；若成功，呼叫 `Task.update(id, data)`。
- **輸出**: 重導向至 `/`。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**: URL 中的任務 `id`
- **處理邏輯**: 呼叫 `Task.delete(id)`。
- **輸出**: 成功後重導向至 `/`，並發送 flash 成功訊息。

### `POST /tasks/<int:id>/toggle` (切換完成狀態)
- **輸入**: URL 中的任務 `id`
- **處理邏輯**: 呼叫 `Task.toggle_status(id)`。
- **輸出**: 成功後重導向至 `/`（或原來的頁面）。

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄下：

| 模板檔案 | 繼承自 | 說明 |
|----------|--------|------|
| `base.html` | (無) | 基礎模板，包含共用的 `<head>` (Bootstrap CDN)、導覽列與 flash 訊息區塊 |
| `tasks/index.html` | `base.html` | 任務列表與統計面板 |
| `tasks/new.html` | `base.html` | 新增任務的表單頁面 |
| `tasks/detail.html`| `base.html` | 任務詳細內容展示 |
| `tasks/edit.html` | `base.html` | 編輯任務的表單頁面 |

---

*文件版本：v1.0*  
*建立日期：2026-04-23*  
*最後更新：2026-04-23*
