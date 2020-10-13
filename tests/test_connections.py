import unittest
import pandas.io.sql as pd_sql
from climblog.apps.auth.connections import postgres_connection


class TestConnections(unittest.TestCase):

    def test_postgres_connection(self):
        """Connect to postgres"""
        connection_uri = postgres_connection()
        query = """
        SELECT data_type
        FROM information_schema.columns
        LIMIT 1
        ;
        """
        self.assertIsNotNone(pd_sql.read_sql(query, connection_uri))


if __name__ == '__main__':
    unittest.main()
