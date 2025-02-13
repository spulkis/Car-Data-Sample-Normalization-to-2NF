from sqlalchemy import text

def add_car_id_column(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    DROP COLUMN `index`,
    ADD Car_ID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ADD CONSTRAINT PK_Car PRIMARY KEY (Car_ID);
    """)
    conn.execute(sql)
    conn.commit()

def modify_car_id_column(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    MODIFY COLUMN Car_ID SMALLINT FIRST;
    """)
    conn.execute(sql)
    conn.commit()

def update_price_and_mileage_run_columns(conn,db,db_table):
    sql = text(f"""
    UPDATE {db}.{db_table}
    SET Price = ROUND(CAST(REPLACE(Price, ',', '') AS DECIMAL(12,2)), 2) / 88.52,
    Mileage_Run = CAST(REPLACE(Mileage_Run, ',', '') AS UNSIGNED INTEGER),
    Price = ROUND(CAST(REPLACE(Price, ',', '') AS DECIMAL(12,2)), 2);
    """)
    conn.execute(sql)
    conn.commit()

def create_make_model_info_table(conn,db):
    sql = text(f"""
    CREATE TABLE {db}.make_model_info (
    Make_Model_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Make TEXT NOT NULL,
    Model TEXT NOT NULL,
    Body_Type TEXT NOT NULL,
    Seating_Capacity INT NOT NULL,
    `Fuel_Tank_Capacity(l)` INT NOT NULL);
    """)
    conn.execute(sql)
    conn.commit()

def insert_into_make_model_info(conn,db,db_table):
    sql = text(f"""
    INSERT INTO {db}.make_model_info (Make, Model, Body_Type, Seating_Capacity, `Fuel_Tank_Capacity(l)`)
    SELECT DISTINCT Make, Model, Body_Type, Seating_Capacity, `Fuel_Tank_Capacity(L)`
    FROM {db}.{db_table}
    ORDER by Make ASC;
    """)
    conn.execute(sql)
    conn.commit()

def create_make_transmission_table(conn,db):
    sql = text(f"""
    CREATE TABLE {db}.transmission_info (
	Transmission_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Transmission TEXT NOT NULL,
    Transmission_Type  TEXT NOT NULL);
    """)
    conn.execute(sql)
    conn.commit()

def insert_into_transmission_info(conn,db,db_table):
    sql = text(f"""
    INSERT INTO {db}.transmission_info (Transmission, Transmission_Type)
    SELECT DISTINCT Transmission, Transmission_Type
    FROM {db}.{db_table}
    ORDER by Transmission ASC;
    """)
    conn.execute(sql)
    conn.commit()

def create_engines_info_table(conn,db):
    sql = text(f"""
    CREATE TABLE {db}.engines_info (
	Engine_ID int not null AUTO_INCREMENT PRIMARY KEY,
    Engine_Type TEXT not null,
    Fuel_Type  TEXT not null,
    CC_Displacement INT not null,
    `Power(BHP)` TEXT not null,
    `Torque(Nm)` TEXT not null,
    `Mileage(kmpl)` TEXT not null,
    Emission TEXT not null);
    """)
    conn.execute(sql)
    conn.commit()

def insert_into_engine_info(conn,db,db_table):
    sql = text(f"""
    INSERT INTO {db}.engines_info (Engine_Type, Fuel_Type, CC_Displacement, `Power(BHP)`, `Torque(Nm)`, `Mileage(kmpl)`, Emission)
    select distinct Engine_Type, Fuel_Type, CC_Displacement, `Power(BHP)`, `Torque(Nm)`, `Mileage(kmpl)`, Emission
    FROM {db}.{db_table}
    ORDER by Engine_type ASC;
    """)
    conn.execute(sql)
    conn.commit()

def add_engine_id_key(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    ADD COLUMN Engine_ID INT,
    ADD CONSTRAINT FK_EngineInfo
    FOREIGN KEY (Engine_ID) REFERENCES engines_info(Engine_ID);
    """)
    conn.execute(sql)
    conn.commit()

def update_car_list_with_engine_id(conn,db,db_table):
    sql = text(f"""
    UPDATE {db}.{db_table} AS cl
    INNER JOIN engines_info AS ei
        ON cl.Engine_Type = ei.Engine_Type
        AND cl.Fuel_Type = ei.Fuel_Type
        AND cl.CC_Displacement = ei.CC_Displacement
        AND cl.`Torque(Nm)` = ei.`Torque(Nm)`
        AND cl.`Mileage(kmpl)` = ei.`Mileage(kmpl)`
        AND cl.Emission = ei.Emission
    SET cl.Engine_ID = ei.Engine_ID;
    """)
    conn.execute(sql)
    conn.commit()

def add_make_model_id_key(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    ADD COLUMN Make_Model_ID INT,
    ADD CONSTRAINT FK_MakeModelInfo
    FOREIGN KEY (Make_Model_ID) REFERENCES make_model_info(Make_Model_ID);
    """)
    conn.execute(sql)
    conn.commit()

def update_car_list_with_make_model_id(conn,db,db_table):
    sql = text(f"""
    UPDATE {db}.{db_table} AS cl
    INNER JOIN make_model_info AS mmi
        ON cl.Make = mmi.Make
        AND cl.Model = mmi.Model
        AND cl.Body_Type = mmi.Body_Type
        AND cl.Seating_Capacity = mmi.Seating_Capacity
        AND cl.`Fuel_Tank_Capacity(l)` = mmi.`Fuel_Tank_Capacity(l)`
    SET cl.Make_Model_ID = mmi.Make_Model_ID;
    """)
    conn.execute(sql)
    conn.commit()

def add_transmission_id_key(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    ADD COLUMN Transmission_ID INT,
    ADD CONSTRAINT FK_TransmissionInfo
    FOREIGN KEY (Transmission_ID) REFERENCES transmission_info(Transmission_ID);
    """)
    conn.execute(sql)
    conn.commit()

def update_car_list_with_transmission_id(conn,db,db_table):
    sql = text(f"""
    UPDATE {db}.{db_table} AS cl
    INNER JOIN transmission_info AS ti
        ON cl.Transmission = ti.Transmission
        AND cl.Transmission_Type = ti.Transmission_Type
    SET cl.Transmission_ID = ti.Transmission_ID;
    """)
    conn.execute(sql)
    conn.commit()

def drop_columns(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    DROP Make, DROP Model, DROP Body_Type, DROP Seating_Capacity, DROP Fuel_Type, DROP `Fuel_Tank_Capacity(L)`, DROP Engine_Type, DROP CC_Displacement,
    DROP Transmission, DROP Transmission_Type, DROP `Power(BHP)`, DROP `Torque(Nm)`, DROP `Mileage(kmpl)`, DROP Emission;
    """)
    conn.execute(sql)
    conn.commit()

def change_columns_position(conn,db,db_table):
    sql = text(f"""
    ALTER TABLE {db}.{db_table}
    MODIFY COLUMN Make_Model_ID INT AFTER  Make_Year,
    MODIFY COLUMN Engine_ID INT AFTER  Make_Model_ID,
    MODIFY COLUMN Transmission_ID INT AFTER  Engine_ID;
    """)
    conn.execute(sql)
    conn.commit()

def create_view(conn,db_table):
    sql = text(f"""
    CREATE VIEW car_details AS
    SELECT {db_table}.Car_ID, {db_table}.Car_Name, {db_table}.Make_Year, {db_table}.Color, {db_table}.Mileage_Run, {db_table}.No_of_Owners, 
    engines_info.Engine_Type, engines_info.Fuel_Type, engines_info.CC_Displacement, engines_info.`Power(BHP)`, engines_info.`Torque(Nm)`, engines_info.`Mileage(kmpl)`, engines_info.Emission,
    make_model_info.Make, make_model_info.Model, make_model_info.Body_Type, make_model_info.Seating_Capacity, make_model_info.`Fuel_Tank_Capacity(l)`,
    transmission_info.Transmission, transmission_info.Transmission_Type, {db_table}.Price
    FROM {db_table}
    INNER JOIN engines_info ON {db_table}.Engine_ID = engines_info.Engine_ID
    INNER JOIN make_model_info ON {db_table}.Make_Model_ID = make_model_info.Make_Model_ID
    INNER JOIN transmission_info ON {db_table}.Transmission_ID = transmission_info.Transmission_ID;
""")
    conn.execute(sql)
    conn.commit()