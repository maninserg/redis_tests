from factory.faker import faker
import sqlite3


NUMBERS = 100


def create_one_person():
    FAKE = faker.Faker()
    # dir(FAKE)
    first_name = FAKE.first_name()
    last_name = FAKE.last_name()
    address = FAKE.address()
    phone_number = FAKE.phone_number()
    email = FAKE.email()
    return first_name, last_name, address, phone_number, email


def generator_persons(num):
    while num > 0:
        yield create_one_person()
        num -= 1


def create_database():
    try:
        sqlite_connection = sqlite3.connect('db_persons.db')
        print('Database was created and conected')
    except sqlite3.Error as error:
        print('Error connection to database', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('Connection was closed')


def create_table():
    try:
        sqlite_connection = sqlite3.connect('db_persons.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        address VARCHAR,
        phone_number VARCHAR,
        email VARCHAR);
        '''
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        cursor.close()
        print('Table was created')
    except sqlite3.Error as error:
        print('Error of create table', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('Connection was closed')


def insert_persons_into_database():
    try:
        sqlite_connection = sqlite3.connect('db_persons.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_persons = '''INSERT INTO persons(first_name, last_name,
        address, phone_number, email) VALUES(?, ?, ?, ?, ?)'''
        for item in generator_persons(NUMBERS):
            cursor.execute(sqlite_insert_persons, item)
            sqlite_connection.commit()
        cursor.close()
        print('Persons was inserted to table')
    except sqlite3.Error as error:
        print('Error of insert to table', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('Connection was closed')


def main():
        create_database()
        create_table()
        insert_persons_into_database()


if __name__ == '__main__':
    main()
