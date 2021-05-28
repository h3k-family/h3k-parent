FROM python:3.9.5-buster
WORKDIR /src
COPY requirements.txt requirements.txt
ENV DB_USER="db_user"
ENV DB_PASS="db_pass"
ENV DB_PORT="db_port"
ENV DB_NAME="db_name"
ENV DB_HOST="db_host"
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
RUN ["python", ".migrate_if_possible.py"]
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
