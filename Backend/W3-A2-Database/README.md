# W3-A2 — Task API with SQLite Database

A CRUD Task Management API built with **FastAPI**, **SQLModel**, and **SQLite** for FlyRank Internship Backend Track.

This project upgrades the previous in-memory Task API by connecting CRUD operations with a persistent SQLite database.

---

## 🚀 Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

---

## 📁 Project Structure

```
W3-A2-Database/
│
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── tasks.db
```

> Note: `tasks.db` is ignored from GitHub because it is a local database file.

---

# ⚙️ Setup & Run

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Server

```bash
uvicorn main:app --reload --port 8001
```

## Swagger Documentation

Open:

```
http://127.0.0.1:8001/docs
```

---

# ✨ Features

The API supports complete CRUD operations:

- Create tasks
- Read all tasks
- Read single task
- Update tasks
- Delete tasks
- Task statistics

---

# 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a single task |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Get task statistics |

---

# 📸 API Testing Screenshots

## GET All Tasks

Endpoint:

```
GET /tasks
```

Screenshot:

![GET Tasks](screenshots/01-get-tasks.png)


---

## Create Task

Endpoint:

```
POST /tasks
```

Screenshot:

![Create Task](screenshots/02-create-task.png)


---

## Update Task

Endpoint:

```
PUT /tasks/{id}
```

Screenshot:

![Update Task](screenshots/03-update-task.png)


---

## Get Single Task

Endpoint:

```
GET /tasks/{id}
```

Screenshot:

![Get Single Task](screenshots/04-get-single-task.png)


---

## Delete Task

Endpoint:

```
DELETE /tasks/{id}
```

Screenshot:

![Delete Task](screenshots/05-delete-task.png)


---

## Task Statistics

Endpoint:

```
GET /stats
```

Screenshot:

![Task Stats](screenshots/06-stats.png)

---

# 🗄️ Database

This project uses **SQLite with SQLModel ORM**.

Database model:

```
Task
│
├── id
├── title
└── done
```

The database tables are automatically created when the application starts.

---

# 🧪 Testing Summary

All required endpoints were tested successfully:

✅ GET `/tasks`  
✅ POST `/tasks`  
✅ GET `/tasks/{id}`  
✅ PUT `/tasks/{id}`  
✅ DELETE `/tasks/{id}`  
✅ GET `/stats`

---

# 👩‍💻 Author

**Riffat **

FlyRank Internship Cohort July 2026. 

