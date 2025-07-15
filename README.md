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

There are two steps to follow:

1. configuration
2. run the *demo-services* application
3. run the *api* application

### Configuration

This system leverages GitHub for authentication; thus you need to create a GitHub Oauth App from [your account's settings](https://github.com/settings/developers). 

During the process, you will be assigned a *client ID* and a *secret key*; this data needs to be stored in a file called `.env`, placed in the project directory.

Assuming you have just cloned the repository, you have to manually create this file; use `.env.sample` for reference. 

Start by filling in `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` accordingly.

The other commented lines may be useful later, but they can be ignored for now, since the system will use defaults.

### Demo-services

The demo-services application serves two models (iris and digits) to simulate a real process available through the Web.

To run this application:

1. Open a terminal
2. Navigate to the project directory
3. enter the venv
4. run the following command

```python
python run_demo_services.py
```

> To stop the process, use `CTRL+C`, any key combination specific to your OS.

### Api application

This application is the core component of experimental-api.

To run it:

1. Open a terminal
2. Navigate to the project directory
3. enter the venv
4. run the following command

```python
python run_api.py
```

> To stop the process, use `CTRL+C`, any key combination specific to your OS.

Now you have two options:

- (a) use the API through the built-in tool (Swagger)
- (b) use the API through the front-end

Read the sections below for details.

#### 1. Use the API through Swagger

1. go to [localhost:8000/docs](http://localhost:8000/docs)
2. authenticate with GitHub by going to [localhost:8000/login/github](http://localhost:8000/login/github) and following the instructions
3. choose any operation and follow the instructions to test it
4. have fun!

To logout, go to [localhost:8000/logout](http://localhost:8000/logout);

#### 2. Use the API through the frontend

First, you need to setup the frontend application;

To do so, follow the instructions in the [frontend repo](https://github.com/anto31ad/experimental-api-fe);

At that point:

1. re-read the instructions in this document to make sure everything is setup correctly.
2. To log in, tap to the login button in the `/login` page
3. Have fun with the web app!


## Licence

This project is currently licenced under the [MIT Licence](./LICENCE.txt).
