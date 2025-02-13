[![python](https://img.shields.io/badge/Python-gray?logo=Python)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
## Car Data Sample Normalization to 2NF

This Python script automates the process of setting up a MySQL database, loading car data from a CSV file, and normalizing the data to the Second Normal Form (2NF).

### Functionality

1. **Database Setup:**
   - Creates a MySQL database named `car_data` if it doesn't exist (using `sqlalchemy-utils`).
   - Creates a database user named `test_user` with a password stored in the `DATABASE_USER_PASSWORD` variable.
   - Grants the `test_user` all privileges on the `car_data` database.

2. **Data Loading:**
   - Reads car data from a CSV file named `car_data.csv` using pandas.
   - Creates a table named `car_list` in the `car_data` database to store the data.
   - Replaces any existing data in the `car_list` table with the new data from the CSV file.
   - Prints a sample of the loaded data using `df.head()`.

3. **Data Normalization**

   - Connects to the database as the newly created user `test_user`.
   - Executes a series of functions defined in the `Python_Data_to_2NF_SQL_Commands.py` file to normalize the car data to the Second Normal Form (2NF). These functions likely perform actions such as:
      - Adding new columns to the `car_list` table.
      - Modifying existing columns.
      - Creating additional tables to store related data (e.g., make/model information, transmission types, engine specifications).
      - Establishing foreign key relationships between tables.
      - Dropping redundant columns.
      - Reordering columns for better readability.
      - Creating a view for easier data access.

### Instructions

1. If you want, you  can update the following variables in the script:
   - `DATABASE`: Set the name of the database.
   - `DATABASE_TABLE`: Set the name of the database table.
   - `HOSTNAME`: Set the name of your database host.
   - `USER`: Set the name of your admin user.
   - `PASSWORD`: Set the password of your admin user.
   - `DATABASE_USER`: Set the name of the database user that you want to create.
   - `DATABASE_USER_PASSWORD`: Set the password for the newly created database user.
   - `CSV_PATH`: Ensure the path to your `car_data.csv` file is correct.
2. Make sure you have the required libraries installed (check requirements section).
3. Run the script: `Data_to_MySQL.py`

**Alternatively:**
You can use the provided `Car_data_dump.sql` file to create the database schema in your MySQL instance. This file contains all the necessary SQL statements to set up the database tables and relationships as defined in `Python_Data_to_2NF_SQL_Commands.py` script.
Import the `Car_data_dump.sql` file using a tool like mysql command-line client or a graphical MySQL administration tool (e.g., phpMyAdmin, MySQL Workbench).

### Suggestions for future improvements

- **Code organization:** This script could benefit from creating a class that encapsulates the database interaction logic.
- **Error Handling:** The script currently doesn't handle potential errors explicitly. Consider implementing try-except blocks or custom error classes to handle issues like database connection failures, invalid CSV data format, or unexpected SQL exceptions.
- **Information about changes made to the database schema:** The script could benefit from added functionality about what has been done to the database after using specific function.

### Requirements

- Python 3
- pandas library (`pip install pandas`)
- sqlalchemy library (`pip install sqlalchemy`)
- sqlalchemy-utils library (`pip install sqlalchemy-utils`)
- PyMySQL library (`pip install PyMySQL`) (for connecting to MySQL)
- The `Python_Data_to_2NF_SQL_Commands.py` file containing the data normalization functions
- Whole list of modules listed in `requirements.txt`

**Feel free to fork this repository and make your own modifications!**