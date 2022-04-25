import psycopg2


def connect_to_DB():
    con = psycopg2.connect(
        database="project",
        user="postgres",
        password="Cerf2022",
        host="localhost",
        port="5432")
    cur = con.cursor()
    return (cur, con)
