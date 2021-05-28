FROM python:3.9.5-buster
WORKDIR /src
COPY requirements.txt requirements.txt
ENV TEST_VAR="change this"
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
