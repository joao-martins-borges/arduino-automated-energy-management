import mysql
import mysql.connector
from Queues import rules

dbhost = "localhost"
user = "python"
password = "python"
dbname = "dbsensores"

def runRules():
    db = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=dbname
    )


    cursor = db.cursor()
    cursor.execute("CALL get_triggers")

    for obj in cursor:
        d = {str(obj[0]):str(obj[1])}
        rules.update(d)

    cursor.close()
