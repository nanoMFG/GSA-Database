FROM python:3.9-alpine
WORKDIR /flaskapp
ADD . /flaskapp
RUN pip install -r requirements.txt
CMD ["python", "app.py"]