# Experimental API 

## Purpose and goals

This is the graduation project for my Bachelor degree.

The long term goal of the project is to create an API framework with the following features:

- ease in plugging ML systems
- ability to serve ML systems over the web
- secure communication between the system and the user 
- anomaly detection in API traffic
- ability to monitor status of the service

---

## Installation

### a) setup virtual environment

Open a terminal and change the current directory to the root directory of the project.

1. Create virtual environment with:

```bash
python -m venv .venv
```

This creates a python virtual environment in the form of a directory called `.venv`.

2. Enter `.venv` with

```bash
source .venv/bin/activate
```

You should see something like

```bash
(.venv) user@computer:~/path/to/project-dir$
```

3. Now it's time to install the dependencies!

### b) install project dependencies

Assuming you have activated the virtual environment already:

1. open the terminal and change current directory to the root folder of the project
2. run the following command:

```bash
pip install -r requirements.txt
```

## Usage

Assuming you activated the virtual environment, to run the API service, execute

```python
fastapi dev src/main.py
```

Where `dev` tells fastapi to run the script `main.py` in dev mode.

Now:

1. go to [localhost:8000/docs](http://localhost:8000/docs)
2. authenticate using `admin` as username and `secret` as password (not necessary, if you want to see what happens in step 3 when you're not authenticated)
3. choose any operation and follow the instructions to test it
4. have fun!

---

## Licence

This project is currently licenced under the [MIT Licence](./LICENCE.txt).

This choice is temporary: it may change or be confirmed at some point;
The *when* and the *if* depends on whether the project gets serious.

Anyhow, all commits before the final decision will obviously stay under the MIT Licence.
