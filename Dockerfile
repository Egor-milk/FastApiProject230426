FROM python:3.14.4

RUN echo ls
WORKDIR /app
RUN echo ls


COPY requirements-win.txt requirements-win.txt
RUN pip install -r requirements-win.txt

COPY . .

#CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py