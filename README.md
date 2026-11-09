# FastAPI DevOps Practice Project

This project is a FastAPI task management API with authentication and task CRUD endpoints.

## Local development

```bash
cd /Users/Dev/Desktop/ASYNC
. .venv/bin/activate
uvicorn mian:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

Build the image:

```bash
docker build -t async-fastapi:latest .
```

Run the container:

```bash
docker run -d -p 8000:8000 --env-file .env --name async-fastapi async-fastapi:latest
```

Or use Docker Compose:

```bash
docker compose up --build
```

## Day 1 learning goals

- Understand difference between virtual machines and containers
- Learn Docker architecture
- Practice Dockerfile instructions
- Build multi-stage images later
- Understand port exposure and runtime configuration

## API health check

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"message": "Welcome to the Task Management API"}
```
