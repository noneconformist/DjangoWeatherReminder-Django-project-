import pytest
from django.db import connection


@pytest.mark.django_db
def test_connection_pool_reuse():
    conn_ids = set()

    for _ in range(5):
        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_backend_pid();')  # Get the ID of the current connection
            conn_id = cursor.fetchone()[0]
            conn_ids.add(conn_id)

    # If the pool is working, the number of unique connections
    # will be less than the number of requests

    assert len(conn_ids) < 5, f'Expected reused connections, got {len(conn_ids)} unique'
