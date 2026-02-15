import psycopg2
from psycopg2 import sql
from UDP_Client import select_network, send_packet  

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

def read_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            return int(s)
        print("Please enter a numeric equipment id.")


try:

    # connect to server network 
    server_addr = select_network()
    print("Using UDP server:", server_addr)


    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")

    # Fetch and display the result
    version = cursor.fetchone()
    print(f"Connected to - {version}")

    # Example: creating a table
    #cursor.execute('''
    #    CREATE TABLE IF NOT EXISTS employees (
    #        id SERIAL PRIMARY KEY,
    #        name VARCHAR(100),
    #        department VARCHAR(50),
    #        salary DECIMAL
    #    );
    #''')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            codename TEXT NOT NULL
        );
    """)

    # Adding two players to database
    print("\nAdd TWO players to the database:\n")

    for i in range(1, 3):
        print(f"--- Player {i} ---")
        pid = read_int("Equipment ID: ")
        codename = input("Codename: ").strip()

        cursor.execute("""
            INSERT INTO players (id, codename)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE
            SET codename = EXCLUDED.codename;
        """, (pid, codename))
        conn.commit()

        print(f"Saved Player {i}: ({pid}, {codename})")

        send_packet(str(pid))
        print()

    # Commit the changes
    conn.commit()

    # Fetch and display data from the table
    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()








