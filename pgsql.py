import psycopg2
from config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL db server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

##connect to postgres
config = load_config()
connection = connect(config)

##create a cursor object to create table, insert record
cursor = connection.cursor()

# ## create the table
tableInfo = """
create table studentlist(id serial primary key, name varchar(20) not null, class varchar(20) not null, section varchar(5), marks integer)
"""
cursor.execute(tableInfo)

##insert some records
cursor.execute('''INSERT into studentlist values(6, 'Ram', 'Data Science', 'A', 90)''')
cursor.execute('''INSERT into studentlist values(7, 'Samira', 'Data Science', 'B', 100)''')
cursor.execute('''INSERT into studentlist values(8, 'Suhana', 'Data Science', 'A', 86)''')
cursor.execute('''INSERT into studentlist values(9, 'Vijay', 'DEVOPS', 'A', 50)''')
cursor.execute('''INSERT into studentlist values(10, 'Deepika', 'DEVOPS', 'A', 35)''')

##Display all the records
print("Display all inserted records")
cursor.execute('''SELECT * FROM studentlist''')
##fetch all rows
data = cursor.fetchall()

# Iterate over the rows and print each one
for row in data:
    print(row)
##commit your changes into the database
connection.commit()
connection.close()