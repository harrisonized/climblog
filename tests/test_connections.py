import unittest
import pandas.io.sql as pd_sql
from climblog.etc.paths import postgres_connection_uri


class TestConnections(unittest.TestCase):

    def test_postgres_connection(self):
        """Connect to postgres"""
        query = """
        SELECT data_type
        FROM information_schema.columns
        LIMIT 1
        ;
        """
        self.assertIsNotNone(pd_sql.read_sql(query, postgres_connection_uri))


if __name__ == '__main__':
    unittest.main()
