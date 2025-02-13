import pandas as pd
from sqlalchemy import create_engine, text, exc
from sqlalchemy_utils import database_exists, create_database
import Python_Data_to_2NF_SQL_Commands as sc
import config as cfg

DATABASE = "car_data_0708"
DATABASE_TABLE = "car_list"
HOSTNAME = cfg.HOSTNAME
USER = cfg.USER
PASSWORD = cfg.PASSWORD
CONNECTION_STRING = f"mysql+pymysql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}"
CSV_PATH = "car_data.csv"
DATABASE_USER = "test_user"
DATABASE_USER_PASSWORD = "your_password"

engine = create_engine(CONNECTION_STRING)

# Create database if it doesn't exist //pip install sqlalchemy-utils python3 // -m pip install PyMySQL // pip install cryptography
if not database_exists(engine.url):
    create_database(engine.url)
print("Database exists: ", database_exists(engine.url))

# Create database user
try:
    with engine.connect() as conn:
        sql1 = text(
            f"CREATE USER '{DATABASE_USER}'@'{HOSTNAME}' IDENTIFIED BY '{DATABASE_USER_PASSWORD}';"
        )
        conn.execute(sql1)
        print("User created successfully!")
except exc.SQLAlchemyError as err:
    print(f"Connection error: {err}")

# Add user privileges
try:
    with engine.connect() as conn:
        sql2 = text(f"GRANT ALL ON `{DATABASE}`.* TO '{DATABASE_USER}'@'{HOSTNAME}';")
        conn.execute(sql2)
        print(sql2)
        print("Permissions granted successfully!")
except exc.SQLAlchemyError as err:
    print(f"Connection error: {err}")

# Create table and read data from csv
df = pd.read_csv(CSV_PATH)
engine = create_engine(CONNECTION_STRING)
df.to_sql(DATABASE_TABLE, engine, if_exists="replace")
# Print a part of the table as an example
print(df.head())

# Connect to the engine as a new created user
NEW_CONNECTION_STRING = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_USER_PASSWORD}@{HOSTNAME}/{DATABASE}"
)
new_engine = create_engine(NEW_CONNECTION_STRING)
# Apply functions for data normalization
try:
    with new_engine.connect() as conn:
        sc.add_car_id_column(conn, DATABASE, DATABASE_TABLE)
        sc.modify_car_id_column(conn, DATABASE, DATABASE_TABLE)
        sc.update_price_and_mileage_run_columns(conn, DATABASE, DATABASE_TABLE)
        sc.create_make_model_info_table(conn, DATABASE)
        sc.insert_into_make_model_info(conn, DATABASE, DATABASE_TABLE)
        sc.create_make_transmission_table(conn, DATABASE)
        sc.insert_into_transmission_info(conn, DATABASE, DATABASE_TABLE)
        sc.create_engines_info_table(conn, DATABASE)
        sc.insert_into_engine_info(conn, DATABASE, DATABASE_TABLE)
        sc.add_engine_id_key(conn, DATABASE, DATABASE_TABLE)
        sc.update_car_list_with_engine_id(conn, DATABASE, DATABASE_TABLE)
        sc.add_make_model_id_key(conn, DATABASE, DATABASE_TABLE)
        sc.update_car_list_with_make_model_id(conn, DATABASE, DATABASE_TABLE)
        sc.add_transmission_id_key(conn, DATABASE, DATABASE_TABLE)
        sc.update_car_list_with_transmission_id(conn, DATABASE, DATABASE_TABLE)
        sc.drop_columns(conn, DATABASE, DATABASE_TABLE)
        sc.change_columns_position(conn, DATABASE, DATABASE_TABLE)
        sc.create_view(conn, DATABASE_TABLE)
        print("All data iserted and normalized to 2NF!")
except exc.SQLAlchemyError as err:
    print(f"Connection error: {err}")
