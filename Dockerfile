FROM python:latest
COPY . /python
WORKDIR /python
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install flask-mysql
EXPOSE 8000
CMD ["python", "phonebook-app.py", "-d"]
