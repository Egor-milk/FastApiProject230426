FROM python:3.14.4

RUN echo ls
WORKDIR /app
RUN echo ls

COPY . .

RUN pip install -r requirements-win.txt


CMD ["python", "src/main.py"] 