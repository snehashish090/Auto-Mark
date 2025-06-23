# Imports for the project
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import face_recognition
import numpy as np

from config import *
# config.py will contain the following variables
# DB_HOST = ""
# DB_USERNAME = ""
# DB_PASSWORD = ""
# DB_NAME = ""

# Predefined information for database connections

class DataBase:

    def __init__(self):
        """
        Intialization function that starts a connection pool
        """
        self.host = DB_HOST
        self.username = DB_USERNAME 
        self.password = DB_PASSWORD
        self.database = DB_NAME

        self.db_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,  # Minimum number of connections in the pool
            maxconn=10, # Maximum number of connections in the pool
            user=self.username,
            password=self.password,
            host=self.host,
            database=self.database
        )

    @contextmanager
    def get_conn(self):
        """
        Context manager to acquire a connection from the pool and ensure its release.
        Yields a connection object.
        """
        conn = None
        try:
            conn = self.db_pool.getconn()
            yield conn
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
            if conn:
                self.db_pool.putconn(conn, close=True) # Close problematic connection
            raise # Re-raise the exception after handling
        finally:
            if conn:
                self.db_pool.putconn(conn) # Always return the connection to the pool

    def _execute_query(self, conn, query, params=None, fetch_one=False, fetch_all=False):
        """
        Executes a given SQL query using a provided connection and its cursor.

        Parameters:
        - conn: The psycopg2 connection object.
        - query (str): The SQL query string.
        - params (tuple or list): Parameters for the query.
        - fetch_one (bool): If True, fetches one row after execution.
        - fetch_all (bool): If True, fetches all rows after execution.

        Returns:
        - The fetched result (single row, list of rows, or None) if fetch_one/fetch_all is True.
        - True for successful execution of non-SELECT queries, None otherwise.
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                conn.commit()
                return True # Indicate successful execution for non-SELECT queries
            
        except psycopg2.Error as e:
            conn.rollback() # Rollback in case of error
            print(f"Database error during query execution: {e}")
            return None
        
        except Exception as e:
            print(f"An unexpected error occurred during query execution: {e}")
            return None
        finally:
            cursor.close()

    def add_person(self, name:str, image_path:str):

        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]

        try:
            with self.get_conn() as conn:
                query = "INSERT INTO face_profiles (name, encoding) VALUES (%s, %s)"
                self._execute_query(conn, query, (name, encoding.tolist()))

        except Exception as ex:
            print("debug: person with name ", name, " could not be added to the database")

    def get_people(self):
        known_names = []
        known_encodings = []

        with self.get_conn() as conn:
            query = "SELECT name, encoding FROM face_profiles"
            results = self._execute_query(conn, query, fetch_all=True)

            if results:

                for name, encoding in results:
                    known_names.append(name)
                    known_encodings.append(np.array(encoding, dtype=np.float64))

            return known_names, known_encodings
        