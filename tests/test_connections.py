import unittest
from climblog.apps.auth.connections import postgres_connection


class TestConnections(unittest.TestCase):

    def test_postgres_connection(self):
        """Connect to postgres"""
        connection_uri = postgres_connection()
        self.assertIsNotNone(connection_uri)


if __name__ == '__main__':
    unittest.main()
