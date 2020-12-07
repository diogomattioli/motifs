from datetime import datetime
from neo4j.v1 import GraphDatabase, basic_auth
import sys


qty = [1, 1000, 1000000]

neo4j_query = ['MATCH (a)-[:LINK]-(b)-[:LINK]-(c)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d',
               'MATCH (a)-[:LINK]-(b)-[:LINK]-(c), (b)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d',
               'MATCH (a)-[:LINK]-(b)-[:LINK]-(c)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d AND (b)-[:LINK]-(d)',
               'MATCH (a)-[:LINK]-(b)-[:LINK]-(c)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d AND (a)-[:LINK]-(d)',
               'MATCH (a)-[:LINK]-(b)-[:LINK]-(c)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d AND (a)-[:LINK]-(c) AND (a)-[:LINK]-(d)',
               'MATCH (a)-[:LINK]-(b)-[:LINK]-(c)-[:LINK]-(d) WHERE a <> c AND a <> d AND b <> d AND (a)-[:LINK]-(c) AND (a)-[:LINK]-(d) AND (b)-[:LINK]-(d)']

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "admin"))
session = driver.session()

for query in neo4j_query:

    for j in qty:
        time = []

        print '%s - %s' % (query, j)

        for i in range(1, 11):
            start = datetime.now()
            queryrun = query + ' RETURN a, b, c, d SKIP %s LIMIT 1' % j;
            result = session.run(queryrun)
            for record in result:
                record = None
                print i,
                sys.stdout.flush()
            time.append((datetime.now() - start))

        print
        print time
        time.remove(min(time))
        time.remove(max(time))

        print '%s ms' % (sum(time) / len(time) / 1000)

        print '#' * 50

session.close()
