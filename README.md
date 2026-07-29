# Task API

A small REST API for managing a list of tasks, built with **FastAPI** and backed by
**PostgreSQL**. The whole stack — API plus database — runs from a single command with
Docker Compose. No local Python install and no manual database setup are required.

The app is organised in layers:

- [models/task.py](models/task.py) — the `Task` SQLModel (also the request/response schema)
- [repositories/task_repository.py](repositories/task_repository.py) — all database access
- [services/task_services.py](services/task_services.py) — business logic (filtering, stats)
- [routes/task_routes.py](routes/task_routes.py) — HTTP endpoints
- [database.py](database.py) — engine, table creation, and seed data
- [main.py](main.py) — app wiring and lifespan startup
- [docker-compose.yaml](docker-compose.yaml) — the `api` and `db` services

## Run it

```bash
docker compose up
```

That's the whole thing. It builds the API image, starts PostgreSQL, creates the `tasks`
table, and seeds three example tasks on first boot.

The API is then at **http://localhost:3000**, with interactive docs at
[/docs](http://localhost:3000/docs) (Swagger UI) and [/redoc](http://localhost:3000/redoc).

To stop it:

```bash
docker compose down
```

Task data lives in a named Docker volume (`taskdata`), so it survives `docker compose down`
and is still there on the next `up`. To wipe the database and start fresh, use
`docker compose down -v`.

## Configuration

Copy the example env file before your first run:

```bash
cp .env.example .env
```

| Variable       | Used by                        | Example                                            |
| -------------- | ------------------------------ | -------------------------------------------------- |
| `DATABASE_URL` | [database.py](database.py), via `load_dotenv()` | `postgresql://postgres:dev@localhost:5432/tasks` |

See [.env.example](.env.example) for the value to copy. `.env` is git-ignored and is
never committed — only `.env.example` is.

This variable matters when you run the app **directly on your machine**. Under Docker
Compose the `api` service receives its own `DATABASE_URL` from
[docker-compose.yaml](docker-compose.yaml), pointing at host `db` (the compose service
name) rather than `localhost`.

## Endpoints

Base URL: `http://localhost:3000`

| Method | Path          | Success         | Description                            |
| ------ | ------------- | --------------- | -------------------------------------- |
| GET    | `/`           | 200             | API name, version, and endpoint list   |
| GET    | `/health`     | 200             | Liveness check — `{"status": "ok"}`    |
| GET    | `/tasks`      | 200             | All tasks, optionally filtered         |
| GET    | `/tasks/{id}` | 200 / 404       | One task by id                         |
| POST   | `/tasks`      | 201 / 400       | Create a task from `{"title"}`         |
| PUT    | `/tasks/{id}` | 200 / 400 / 404 | Replace a task's title and done flag   |
| DELETE | `/tasks/{id}` | 204 / 404       | Remove a task                          |
| GET    | `/stats`      | 200             | Counts — `{"total", "done", "open"}`   |

A task is `{"id": int, "title": str, "done": bool}`. `id` is assigned by the database.
`POST /tasks` takes a `title` and always creates the task as not done; use `PUT` to
change the `done` flag. Errors come back as `{"error": "..."}`.

### Filtering `/tasks`

| Param    | Type   | Effect                                            |
| -------- | ------ | ------------------------------------------------- |
| `done`   | bool   | Only tasks whose `done` matches                   |
| `search` | string | Only tasks whose title contains it, ignoring case |

Both combine — `done` is applied first, then `search` narrows further. A non-boolean
`done` (e.g. `?done=yes please`) is a 422.

## Example request

The seeded data, straight after `docker compose up`:

```console
$ curl -i http://localhost:3000/tasks
HTTP/1.1 200 OK
date: Tue, 29 Jul 2026 14:22:07 GMT
server: uvicorn
content-length: 143
content-type: application/json

[{"id":1,"title":"Task 1","done":false},{"id":2,"title":"Task 2","done":true},{"id":3,"title":"Task 3","done":false}]
```

Creating one:

```console
$ curl -i -X POST http://localhost:3000/tasks \
    -H "Content-Type: application/json" \
    -d '{"title":"Write README"}'
HTTP/1.1 201 Created
server: uvicorn
content-type: application/json

{"id":4,"title":"Write README","done":false}
```

And a miss:

```console
$ curl -i http://localhost:3000/tasks/99
HTTP/1.1 404 Not Found
server: uvicorn
content-type: application/json

{"error":"Task 99 not found"}
```

## The data in PostgreSQL

Opening a `psql` shell against the running database:

```bash
docker compose exec db psql -U postgres -d tasks
```

```console
tasks=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | tasks | table | postgres
(1 row)

tasks=# SELECT * FROM tasks;
 id | title  | done
----+--------+------
  1 | Task 1 | f
  2 | Task 2 | t
  3 | Task 3 | f
(3 rows)
```

![Tasks table in the database](image-1.png)

## Swagger docs

![Swagger docs](image.png)
