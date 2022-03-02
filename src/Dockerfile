FROM python:3.9-alpine
WORKDIR /flaskapp
ADD . /flaskapp
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:5000", "grdb.server.app:create_app()"]