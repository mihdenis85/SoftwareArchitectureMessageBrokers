# SoftwareArchitectureMessageBrokers
This project is for comparing RabbitMQ message broker and basic pipes-and-filters pattern.

## Agenda

## Demo

## Features

- User facing REST API service: receives POST request from the users consisting of message text and user alias.
- Filter service: filters messages for a stop-words: bird-watching, ailurophobia, mango.
- SCREAMING service: converts messages to upper case.
- Publish service: sends emails.

## Prerequisites

- Python 3.10+
- Docker/docker compose
- 