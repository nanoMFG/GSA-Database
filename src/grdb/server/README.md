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
