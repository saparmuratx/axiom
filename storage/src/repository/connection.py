from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from src.config import settings


auth_provider = PlainTextAuthProvider(username=settings.CASSANDRA_USER, password=settings.CASSANDRA_PASSWORD)

cluster = Cluster(contact_points=[settings.CASSANDRA_HOST], port=9042, auth_provider=auth_provider)
session = cluster.connect(settings.CASSANDRA_KEYSPACE)

keyspaces = session.execute("SELECT * FROM system_schema.keyspaces;")

print("KEYSPACES:\n")
for row in keyspaces:
    print(row)


# print("TABLES:\n")
# tables = session.execute("SELECT * FROM system_schema.tables;")
# for row in tables:
#     print(row.keyspace_name, row.table_name)


print("VIEWS:\n")
views = session.execute("SELECT * FROM system_schema.views;")
for row in views:
    print(row)

print("ROLES:\n")
roles = session.execute("select * from system_auth.roles")
for row in roles:
    print(row)
