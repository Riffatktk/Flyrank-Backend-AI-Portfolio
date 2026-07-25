# BE-06: Your First Background Job

## 📌 Assignment Overview
This project demonstrates how to process background tasks using **FastAPI**, **Celery**, and **Redis**. Instead of handling long-running tasks during the request-response cycle, the API creates a background job that is processed asynchronously by a Celery worker.

## 🎯 Objectives
- Build a FastAPI application with background job support.
- Use Redis as the message broker.
- Process jobs asynchronously using Celery.
- Check job status through API endpoints.

## 🛠️ Technologies Used
- Python
- FastAPI
- Celery
- Redis
- Docker & Docker Compose
- Uvicorn

## 📂 Project Structure
```
BE-06/
├── app/
├── celery_app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── screenshots/
```

## ▶️ How to Run
```bash
docker compose up --build
```

Then open:
- **API:** http://localhost:8001
- **Swagger Docs:** http://localhost:8001/docs

## 📡 API Endpoints

### Create Background Job
```
POST /jobs
```

### Check Job Status
```
GET /jobs/{job_id}
```

## 📸 Screenshots
| # | Screenshot | Description |
|---|------------|--------------|
| 1 | `01_Terminal_Containers_Running.png` | Docker containers running successfully |
| 2 | `02_API_Home_Page_Port_8001.png` | API home page on port 8001 |
| 3 | `03_Swagger_API_Documentation.png` | Swagger API documentation |
| 4 | `04_Create_Background_Job_POST.png` | Creating a background job (POST request) |
| 5 | `05_Job_Status_Success_GET.png` | Successful job status check (GET request) |

## ✅ Learning Outcomes
- Understood asynchronous background processing.
- Learned how Celery works with Redis.
- Built and tested background job APIs using FastAPI.
- Containerized the application with Docker.

---
Status:
Completed
---
Author: **Riffat**
BS Computer Science Student
*Part of the FlyRank.ai AI Fluency Internship — Backend Engineering Track*
