# Experimental API 

This is the graduation project for my Bachelor degree.

The goal of the project is to create a system that makes it easy to manage and test multiple AI models served through the Internet.

---

## Usage

1. make a copy `.env.sample` and rename it to just `.env`
2. setup github Oauth App and store the keys in the `.env` (see below)
3. run the docker compose command (see below)

### Github Oauth App

This system leverages GitHub for authentication; thus you need to create a GitHub Oauth App from [your account's settings](https://github.com/settings/developers). 

During the process, you will be assigned a *client ID* and a *secret key*; this data needs to be stored in a file called `.env`, placed in the project directory.

Assuming you have just cloned the repository, you have to manually create this file; use `.env.sample` for reference. 

Start by filling in `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` accordingly.

The other commented lines may be useful later, but they can be ignored for now, since the system will use defaults.

### Install with docker compose

In the root directory, run

```sh
docker compose up
```

### Clean up

To clean up run (in the root directory):

```
docker compose down
```

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

At that point:

1. re-read the instructions in this document to make sure everything is setup correctly.
2. To log in, tap to the login button in the `/login` page
3. Have fun with the web app!



## Licence

This project is currently licenced under the [MIT Licence](./LICENCE.txt).
