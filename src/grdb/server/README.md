# grdb/server Documentation for Developers

The Flask app that servers GR-RESQ web APIs.

## Deployment

#### Dependencies

* ```docker```

* ```docker-compose```

This app is a containerized app managed by docker and docker-compose.

Look for ```docker-compose.yaml``` and ```Dockerfile``` in ```src``` folder.

However, depending on the use case, feel free to deploy the app without docker.

Before deployment, make sure that the Flask environment settings to production.

To deploy the app, make sure you have pasted ```.env```file as ```src/grdb/server/.env```.

Next, ```cd``` into ```src``` and run ```docker-compose up --build``` in terminal.

## Steps to debug locally

Step 1-3 is optional when Conda environment is used.

1. Create a python virtual environment. Run ```python3 -m venv venv```
2. Activate the virtual environment. Run ```source venv/bin/activate```
3. Download dependency libraries Run ```pip3 install -r src/requirements.txt```
4. Paste the ```.env``` file as ```src/grdb/server/.env```
5. Run ```src/app.py```
   - ```host=127.0.0.1``` to run in local machine, ```host=0.0.0.0``` for docker container 
   - default port is `5000` 
    
## File Structure

```src/grdb/database``` stores Model files for SQLAlchemy.

```src/grdb/server``` stores the Flask app.

```src/grdb/server/app``` is the [Flask application factory](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/)

## API

Overall introduction to API endpoints. Refer to the code base for details.

---

```/experiments/init```

[GET] Fetch data required for initializing the GR-RESQ tool.

---

```/experiments/submit```

[POST] Post a new experiment data to the server.

---

```/experiments/<experiment id>```

[GET] Fetch detailed information about a particular experiment.

---

```/experiments/filter```

[POST] Fetch experiment ids that are associated with the filteres included in the post body.

---

```/auth/signup```

[POST] Create a new user in the database.

---

```/auth/signin```

[POST] Token validation upon signing in with token OR email and password matching upon signing in with email & password.

---

```/auth/countries```

[GET] Fetch all countries (used for sign up).

---

```/auth/institutions/<country>```

[GET] Fetch institutions by country (used for sign up).
