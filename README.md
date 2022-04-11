## Development Environment

- Ubuntu 16.04 LTS
- Python 3.6.9

## Build Theia Codebase Development Environment

#### Create Virtual Environment

By conda

```
> conda create -n <venv name> python=3.6 pip
> conda activate <venv name>
```

By virtualenv

```
> virtualenv <venv name>
> source <venv name>/bin/activate
```

#### Download Theia Codebase

```
> git clone http://192.168.50.2:4000/vizuro/product/theia/theia_codebase.git
> cd theia_codebase
```

#### Install Python Packages

```
> pip install --upgrade pip
> pip install -r requirements.txt
```

#### Run Services (NGINX, POSTGRESQL, REDIS, RABBITMQ, etc) in Background

```
> pip install docker-compose
> docker volume create pgdata
> docker-compose -f docker-compose-db.yml up -d
```

#### Initialize / Upgrade Database

```
> cd src
> python manager.py db upgrade
```

#### Run Theia

There are four applications need to start up

- Flask Application

```
> python manager.py server run master
```

- Celery Worker for System Tasks

```
> python manager.py server run worker
```

- Celery Worker for Theia's Jobs

```
python manager.py server run worker -c <config_filename>
```

- Celery Scheduler (beat)

```
python manager.py server run scheduler
```

## How to Run Theia in Docker Container

#### Build Theia as a Docker Image

```
> cd theia_codebase
> docker build -t theia/v2:2.0 .
```

#### Run Theia Master

```
> docker-compose -f docker-compose-master.yml up -d
```

#### Run Theia Worker

Setup config file for worker

```
> vim ./configs/<worker_config>.py
```

Config worker to run with above config file
```
> vim docker-compose-worker.yml

Add or modify the following line under `volumes` tag
    - ./configs/<worker_config>.py:/home/theia/custom_config.py:z
```

Run worker

```
> docker-compose -f docker-compose-worker.yml up -d
```
