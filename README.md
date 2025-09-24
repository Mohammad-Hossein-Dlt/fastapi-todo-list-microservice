[How dose it work?](#how-dose-it-work)

[How dose it deploy?](#how-dose-it-deploy)

ENV File Parameters

Put it next to the app

```
EXTERNAL_FASTAPI_PORT = 80
INTERNAL_FASTAPI_PORT = 8000

AUTH_BASE_URL = http://nginx/auth/api/v1

DB_STACK = mongo_db # postgresql, mongo_db

MONGO_HOST = mongo-db
MONGO_PORT = 27017
MONGO_INITDB_ROOT_USERNAME = root
MONGO_INITDB_ROOT_PASSWORD = rootpassword
MONGO_INITDB_DATABASE = db

POSTGRES_HOST = postgres-db
POSTGRES_PORT = 5432
POSTGRES_USER = admin
POSTGRES_PASSWORD = adminpassword
POSTGRES_DB = db

PGADMIN_DEFAULT_EMAIL = admin@example.com
PGADMIN_DEFAULT_PASSWORD = secret

JWT_SECRET = 5fd4a7c9-7b61-49bf-8aea-ae8c53727290
JWT_ALGORITHM = HS256
JWT_EXPIRATION_MINUTES = 2
JWT_REFRESH_EXPIRATION_MINUTES = 4
```

To Run

```
fastapi dev app/src/main.py
```

## App architecture description

### Infra Layer

In this layer, the application infrastructure is defined, such as:

- Authentication utilities such as token creation, management, and validation

- Database client and its models (tables)

- Errors related to this layer and other layers

  - include status code and message

- Services for interacting with external APIs

  - include interfaces and their implementation

- Fastapi config such as

  - middleware
  - tasks that should be run on startup or shutdown, such as create and close database client
  - implement some states based on settings loaded from .env in main app, to have access them throughout the entire project

- Mixin classes

- Application settings load from the `.env` file
  - load with pydantic_settings

```
infra/
│
├── auth/
│   └── <files or directories...>
│
├── db/
│   ├── redis/
│   │   └── <files or directories...>
│   │
│   ├── mongodb/
│   │   └── <files or directories...>
│   │
│   └── sqlite/
│       └── <files or directories...>
│
├── exceptions/
│   └── <files...>
│
├── external_api/
│   ├── interface/
│   │   └── <files...>
│   │
│   └── service/
│       └── <files...>
│
├── fastapi_config/
│   └── <files...>
│
├── mixins/
│   └── <files...>
│
└── settings/
    └── <files...>
```

### Domain Layer

In this layer, data models are defined that are only used inside the application, meaning between layers, for transferring data.

```
domain/
├── mock_data/
│   └── <files...>
│
└── schemas/
    └── <schema_group_name>/
       └── <files...>
```

### Models Layer

In this layer, data models are defined that are only used for receiving or sending data to the client.

```
models/
├── filter/
│   └── <files...>
│
└── schemas/
    └── <schema_group_name>/
        └── <files...>

```

### Repo Layer

In this layer, communication with the database is handled.
Repository classes are defined here, whose methods provide interaction with the database.
Each repository class inherits from an interface defined in this layer.
Interfaces define the structure of database communication, so we can have multiple repository classes based on a single interface and use them for dependency injection.

```
repo/
├── interface/
│   └── <files...>
│
└── <implementation_name>/
    └── <files...>
```

Naming implementations can be based on:

- **Storage type** — for example: `sql`, `nosql`

```
repo/
├── interface/
│   └── <files...>
│
├── sql/
│   └── <files...>
│
└── nosql/
    └── <files...>
```

- **Storage name** — for example: `postgresql`, or `mongodb`.

```
repo/
├── interface/
│   └── <files...>
│
├── postgresql/
│   └── <files...>
│
└── mongodb/
    └── <files...>
```

### Routes Layer

In this layer, endpoints are defined along with their dependencies, response statuses, and other endpoint-related configurations.

```
routes/
├── api_endpoints/
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   └── main_router.py
│
├── depends/
│   └── <files...>
│
└── http_response/
    └── <files...>
```

### Usecase Layer

In this layer, the application’s business logic is defined.
This layer acts as an important bridge between endpoints in the Routes layer, the database in the Repo layer, and external APIs in the Infra layer.

```
usecase/
├── <usecase_group_name>/
│   └── <files...>
│
└── <usecase_group_name>/
    └── <files...>
```

#### Note

The layers are not limited to the mentioned items and can also include other related configurations.

## How dose it work?

I used both PostgreSQL and MongoDB in this mini project.

The databases each have two tables or collections for users and tasks, with tasks connected to users via the `user_id` field.

In PostgreSQL, this relationship is implemented as a foreign key with `ON DELETE CASCADE`. This means that when a user is deleted, their tasks are automatically deleted as well.

For MongoDB, the deletion of tasks when a user is deleted is handled manually.

Each user must register and log in to the app to create and store tasks. This process, along with authentication and token management, has been implemented in the app.

To switch the type of database, you only need to change the `DB_STACK` value in the `.env` file.

The app is also dockerized: both databases and the FastAPI application are configured in Docker Compose.

For direct and easy access to the PostgreSQL database, pgAdmin is used, which is also configured in the Docker Compose file.

To access the contents of the `.env` file, you can refer to the beginning of this document.

## How dose it deploy?

**Configuring Docker Compose**

**Services:**

- **FastAPI app:** This is our to-do list application.
- **MongoDB service:** Our NoSQL database, running on internal and external port `27017:27017`.
- **PostgreSQL service:** Our SQL database, running on internal port `5432`.
- **pgAdmin service:** Added for easier access to the PostgreSQL database. It runs on `8080:80`, meaning we connect externally through port `8080` to the internal port `80`.

**Volumes:**
Both databases have their own storage volumes defined: `pgdata` and `mongo_data`.

**Environment variables:**
All environment variables for the services are read from the `.env` file.

**Restart policy:**
All services are set with `restart: always`. This ensures that whenever a container stops, it will automatically restart.

**Service dependencies:**

- The database services don’t depend on any other services.
- The FastAPI app depends on both database services. This means the databases must be fully created and running before the FastAPI app is built and started.
- The pgAdmin service also depends on the PostgreSQL service.

**FastAPI service details:**

- The build process for the FastAPI service starts with the `Dockerfile` located in the root directory of the app. This file copies the app’s files and directories into the container’s work directory (`/app`) and installs the required packages from `requirements.txt`.
- The container ports for this service are defined in the `.env` file, and the `ports` section of the Docker Compose file references these environment variables.
- Since we can change the default port of the FastAPI app via the `.env` file, the command to run the app is placed at the end of the service definition in the Docker Compose file. This way, the application always uses the internal port defined in `.env`.
