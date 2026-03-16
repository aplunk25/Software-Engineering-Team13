import psycopg2
from psycopg2 import sql
import UDP_Client
from splashscreen import SplashScreen 
from player_entry import entry_terminal
from Countdown_timer import CountdownTimer


# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

def read_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            return int(s)
        print("Please enter a numeric equipment id.")

# def edit_player(cursor, conn):
#     print("\n--- EDIT PLAYER ---")
#     pid = read_int("Enter Equipment ID to edit: ")
#     new_codename = input("Enter NEW codename: ").strip()

#     cursor.execute("""
#         UPDATE players
#         SET codename = %s
#         WHERE id = %s;
#     """, (new_codename, pid))

#     conn.commit()

#     if cursor.rowcount == 0:
#         print(f"No player found with id {pid}.")
#         return None

#     print("Player updated successfully.")
#     return pid

# def show_player(cursor, pid):
#     cursor.execute("""
#         SELECT id, codename
#         FROM players
#         WHERE id = %s;
#     """, (pid,))
#     row = cursor.fetchone()

#     if row is None:
#         print("Player not found.")
#         return

#     print("\nPLAYER INFO:")
#     print("-----------------------------")
#     print(f"Equipment ID: {row[0]}")
#     print(f"Codename:     {row[1]}")
#     print("-----------------------------\n")



# def read_int(prompt: str) -> int:
#     while True:
#         s = input(prompt).strip()
#         if s.isdigit():
#             return int(s)
#         print("Please enter a numeric equipment id.")




# try:

#     # connect to server network 
#     server_addr = select_network()
#     print("Using UDP server:", server_addr)


#     # Connect to PostgreSQL
#     conn = psycopg2.connect(**connection_params)
#     cursor = conn.cursor()

#     # Execute a query
#     cursor.execute("SELECT version();")

#     # Fetch and display the result
#     version = cursor.fetchone()
#     print(f"Connected to - {version}")

#     # Example: creating a table
#     #cursor.execute('''
#     #    CREATE TABLE IF NOT EXISTS employees (
#     #        id SERIAL PRIMARY KEY,
#     #        name VARCHAR(100),
#     #        department VARCHAR(50),
#     #        salary DECIMAL
#     #    );
#     #''')
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS players (
#             id INTEGER PRIMARY KEY,
#             codename TEXT NOT NULL
#         );
#     """)

#     # Adding two players to database via terminal input
#     # print("\nAdd TWO players to the game:\n")

#     # for i in range(1, 3):
#     #     print(f"--- Player {i} ---")
#     #     pid = read_int("Equipment ID: ")
#     #     codename = input("Codename: ").strip()

#     #     cursor.execute("""
#     #         INSERT INTO players (id, codename)
#     #         VALUES (%s, %s)
#     #     """, (pid, codename))
#     #     conn.commit()

#     #     print(f"Saved Player {i}: ({pid}, {codename})")


    
    

#     # Commit the changes
#     conn.commit()

#     # Fetch and display data from the table
#     cursor.execute("SELECT * FROM players;")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

# except Exception as error:
#     print(f"Error connecting to PostgreSQL database: {error}")

# finally:
    # Close the cursor and connection
    # if cursor:
    #    cursor.close()
    # if conn:
    #    conn.close()
def run_app():
    try:
		
        # connect to server network
        UDP_Client.configure_server()
        print("Using UDP server:", UDP_Client.SERVER_ADDRESS)

        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                codename TEXT NOT NULL
            );
        """)
        conn.commit()

        cursor.close()
        conn.close()

        # Launch GUI using SAME db config
        entry_terminal(connection_params)
        
        

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
#  SplashScreen(on_close=run_app, image_path="logo.jpg", duration_ms=3000).show()
    SplashScreen(on_close=run_app,
                image_path="logo.jpg",
                duration_ms=3000).show()
    




