# Experimental API 

## Goal

The goal of the project is to create an API framework with the following features:

- ease in plugging ML systems
- ability to serve ML systems over the web
- secure communication between the system and the user 
- anomaly detection in API traffic
- ability to monitor status of the service


## How to install (debian-based distros)

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

```
(venv) user@computer:~/path/to/project-dir$
```

3. At this point it is time to install the dependencies!

## How to install dependencies

Assuming you are positioned inside a virtual enviroment, container or any other preferred environment:

1. open the terminal and change current directory to the root folder of the project
2. run the following command:

```bash
pip install -r requirements.txt
```

## Licence

This project is currently licenced under the [MIT Licence](./LICENCE.txt).

This choice is temporary: it may change or be confirmed at some point;
The *when* and the *if* depends on whether the project gets serious.

Anyhow, all commits before the final decision will obviously stay under the MIT Licence.
