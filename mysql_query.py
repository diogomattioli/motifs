from mysql.connector import connection
from datetime import datetime
import sys

qty = [1, 1000]

neo4j_query = ['select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on b.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2',
               'select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on a.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2',
               'select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on b.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2 and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb2 and codigo_stringdb2 = c.codigo_stringdb2) IS NOT NULL',
               'select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on b.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2 and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb1 and codigo_stringdb2 = c.codigo_stringdb2) IS NOT NULL',
               'select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on b.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2 and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb1 and codigo_stringdb2 = c.codigo_stringdb1) IS NOT NULL and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb1 and codigo_stringdb2 = c.codigo_stringdb2) IS NOT NULL',
               'select a.codigo_stringdb1, a.codigo_stringdb2, c.codigo_stringdb1, c.codigo_stringdb2 from Link a inner join Link b on a.codigo_stringdb2 = b.codigo_stringdb1 inner join Link c on b.codigo_stringdb2 = c.codigo_stringdb1 where a.codigo_stringdb1 != c.codigo_stringdb1 and a.codigo_stringdb1 != c.codigo_stringdb2 and b.codigo_stringdb1 != c.codigo_stringdb2 and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb1 and codigo_stringdb2 = c.codigo_stringdb1) IS NOT NULL and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb1 and codigo_stringdb2 = c.codigo_stringdb2) IS NOT NULL and (select codigo_stringdb1 from Link where codigo_stringdb1 = a.codigo_stringdb2 and codigo_stringdb2 = c.codigo_stringdb2) IS NOT NULL']

driver = connection.MySQLConnection(user='mattioli', password='', host='127.0.0.1', database='Proteina')
session = driver.cursor()

for query in neo4j_query:

    for j in qty:
        time = []

        print '%s - %s' % (query, j)

        for i in range(1, 11):
            start = datetime.now()
            queryrun = query + ' LIMIT %s, 1' % j;
            session.execute(queryrun)
            for record in session:
                print '%s %s' % (i, record['a.codigo_stringdb1']),
                sys.stdout.flush()
            time.append((datetime.now() - start).microseconds)

        print
        print time
        time.remove(min(time))
        time.remove(max(time))

        print '%s ms' % (sum(time) / len(time) / 1000)

        print '#' * 50

session.close()
driver.close()