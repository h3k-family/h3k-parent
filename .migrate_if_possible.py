import os

# 1. Get the values, irregardless of whether they exist
db_user = os.environ.get("DB_USER")
db_name = os.environ.get("DB_NAME")
db_pass = os.environ.get("DB_PASS")
db_port = os.environ.get("DB_PORT")
db_host = os.environ.get("DB_HOST")

# 2. If they don't exists, dump default data.
# The dockerfile will dump this too, hence the choice
db_user = db_user if db_user is not None else "db_user"
db_name = db_name if db_user is not None else "db_name"
db_pass = db_pass if db_pass is not None else "db_pass"
db_port = db_port if db_port is not None else "db_port"
db_host = db_host if db_host is not None else "db_host"


# 3. If has default data, don't attempt to migrate
if (db_user != "db_user"
        and db_name != "db_name"
        and db_pass != "db_pass"
        and db_port != "db_port"
        and db_host != "db_host"):
    env_contents = """DB_USER={}
DB_PASS={}
DB_PORT={}
DB_NAME={}
DB_HOST="{}"
    """
    env_contents = env_contents.format(
        db_user, db_pass, db_port, db_name, db_host)

    with open('.env', 'w') as f:
        f.write(env_contents)

    os.system("alembic upgrade head")
else:
    print("Environment variables not set. Won't do anything.")
