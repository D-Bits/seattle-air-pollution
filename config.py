from sqlalchemy import create_engine
from os import getenv


# Get SQL Alchemy connection string from
# an environment variable
db_conn = getenv("DB_CONN")

# Create engiens for the database
db_engine = create_engine(db_conn)

