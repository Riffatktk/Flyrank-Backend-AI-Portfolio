# BE-06 – Your First Background Job

## Assignment Overview

This assignment was completed as part of the **Backend Engineering** specialization during the **FlyRank AI Internship (July 2026 Cohort)**.

The goal of this project was to move time-consuming operations outside the main request cycle by using background jobs. Instead of waiting for a long-running AI request to finish, the application immediately accepts the request and processes it asynchronously.

---

## Objectives

- Implement asynchronous background task processing.
- Use Celery for task execution.
- Configure Redis as the message broker.
- Build an API to submit background jobs.
- Track the progress and result of submitted jobs.

---

## Technologies Used

- Python
- FastAPI
- Celery
- Redis
- Docker
- Docker Compose
- Git & GitHub

---

## Project Structure

This assignment includes:

- `main.py`
- `celery_app.py`
- `tasks.py`
- `alerts.py`
- `docker-compose.yml`
- `requirements.txt`
- `README.md`

---

## How to Run

Start the project using Docker Compose:

```bash
docker compose up --build
```

The project requires a `.env` file containing the necessary environment variables.

Example:

```text
GROQ_API_KEY=your_api_key
REDIS_URL=redis://redis:6379/0
```

---

## Testing

Submit a background job:

```bash
curl -X POST http://localhost:8000/jobs
```

Check job status:

```bash
curl http://localhost:8000/jobs/{job_id}
```

---

## Expected Outcome

The application should:

- Accept requests immediately.
- Process AI tasks in the background.
- Allow users to check job status.
- Handle retries for temporary failures.
- Log permanent failures for monitoring.

---

## Screenshots

Screenshots demonstrating the application, worker execution, Redis connection, and successful job processing will be added after completing the assignment.

---

## Learning Outcomes

Through this assignment, I learned how to:

- Build asynchronous backend workflows.
- Process long-running tasks using Celery.
- Configure Redis as a message broker.
- Design APIs for background processing.
- Improve application responsiveness by separating request handling from task execution.

---

## Status

🚧 In Progress

---

## Author

**Riffat **

BS Computer Science Student


FlyRank AI Internship – July 2026 Cohort
