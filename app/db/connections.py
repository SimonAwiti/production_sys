import os
import psycopg2


from app.db.schemas import queries
from werkzeug.security import generate_password_hash

def dbconnection():
    """making a connection to the db"""
    DATABASE_URL = "postgres://meikytsarrxidw:6ce13506bf9e101a731c315693b808a3d91969d17174d8858d783c185ed619ff@ec2-3-230-106-126.compute-1.amazonaws.com:5432/da606t2hkcecu6"
    return psycopg2.connect(DATABASE_URL)


def initializedb():
    try:
        """starting the database"""
        connection = dbconnection()
        connection.autocommit = True

        """activate cursor"""
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()

        """Generate the default admin and add to db"""
        gen_admin = """
                INSERT INTO
                admin (name, email, phone, password, isadmin)
                VALUES ('mainadmin', 'admin12@gmail.com', '0722663340', '%s', true)
                ON CONFLICT (email) DO NOTHING;
                """%(generate_password_hash('passadmin'))
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(gen_admin)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("DB Error")
        print(error)
