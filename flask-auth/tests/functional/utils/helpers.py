from contextlib import contextmanager


@contextmanager
def conn_context(conn):
    yield conn
    conn.close()
