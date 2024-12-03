# SoftwareArchitectureMessageBrokers

This project is for comparing RabbitMQ message broker and basic pipes-and-filters pattern.

## Agenda

* [Demo](#demo)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Contacts](#contacts)

## Demo

## Features

- User facing REST API service: receives POST request from the users consisting of message text and user alias.
- Filter service: filters messages for a stop-words: bird-watching, ailurophobia, mango.
- SCREAMING service: converts messages to upper case.
- Publish service: sends emails.

## Prerequisites

- Python 3.10+
- Docker/docker compose

## Installation

1. Clone the repository:

```shell
git@github.com:mihdenis85/SoftwareArchitectureMessageBrokers.git
```

2. Create .env file for event-driven system (check .env.sample).

3. Create .env file for pipes-and-filter system (check .env.sample inside pipes-and-filters folder).

## Usage

1. Run docker compose for event-driven system (with rabbitmq):

```shell
docker compose up --build
```

Now you can access the API using localhost:8001.

2. Run docker compose for pipes-and-filters system (without rabbitmq).

```shell
cd pipes_and_filters
docker compose up --build
```

Now you can access the API using localhost:8002.

3. If you want to run load_testing, then run this for event-driven system:

```shell
locust -f .\load_test\locustfile.py --host=http://localhost:8001
```

4. And this for pipes-and-filters system:

```shell
locust -f .\load_test\locustfile.py --host=http://localhost:8002
```

Then you should go to the specified address and start load testing.

## Contacts

- Denis Mikhailov - d.mikhailov@innopolis.university
- Anton Chulakov - a.chulakov@innopolis.university
- Adel Shagaliev - a.shagaliev@innopolis.iniversity
- Ilya Zubkov - i.zubkov@innopolis.university
