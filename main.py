import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import psycopg2

# splash screen -> player entry
def open_player_entry():
    splash_screen.destroy()

    # Define connection parameters
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
        # 'password': 'student',
        # 'host': 'localhost',
        # 'port': '5432'
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Execute a query to check the connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to - {version}")

        # Ensure 'players' table has a unique constraint on 'id' column
        cursor.execute('''
            ALTER TABLE players ADD CONSTRAINT IF NOT EXISTS unique_player_id UNIQUE (id);
        ''')
        conn.commit()

        # Insert sample data (Ensure no duplicates)
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        ''', ('500', 'BhodiLi'))
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        ''', ('232', 'Spark'))

        # Commit the changes
        conn.commit()

        # Fetch and display data from the table to check insertion
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

    # Create window
    player_entry = tk.Tk()
    player_entry.title("Player Entry Screen")
    player_entry.configure(background="black")
   
    # Set size of the window
    player_entry.geometry("800x600")
   
    # 2 columns for teams
    for i in range(2):
        player_entry.columnconfigure(i, weight=2)
   
    # Red Label
    red_team_label = tk.Label(player_entry, text="RED TEAM", bg="darkred", fg="white", font=("Arial", 16,))
    red_team_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
   
    # Green Label
    green_team_label = tk.Label(player_entry, text="GREEN TEAM", bg="darkgreen", fg="white", font=("Arial", 16))
    green_team_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    # Frame for Red Team
    red_team_frame = tk.Frame(player_entry, bg="darkred")
    red_team_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
   
    # Frame for Green Team
    green_team_frame = tk.Frame(player_entry, bg="darkgreen")
    green_team_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


    red_team_entries = []
    green_team_entries = []

    # Red players (19 players)
    for i in range(19):
        player_label = tk.Label(red_team_frame, text=f"{i+1}", bg="darkred", fg="white", font=("Arial", 12))
        player_label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
       
        id_entry = tk.Entry(red_team_frame, font=("Arial", 12), width=20)
        id_entry.grid(row=i, column=1, padx=5, pady=2)

        codename_entry = tk.Entry(red_team_frame, font=("Arial", 12), width=20)
        codename_entry.grid(row=i, column=2, padx=5, pady=2)

        red_team_entries.append((id_entry, codename_entry))

    # Green players (19 players)
    for i in range(19):
        player_label = tk.Label(green_team_frame, text=f"{i+1}", bg="darkgreen", fg="white", font=("Arial", 12))
        player_label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
       
        id_entry = tk.Entry(green_team_frame, font=("Arial", 12), width=20)
        id_entry.grid(row=i, column=1, padx=5, pady=2)

        codename_entry = tk.Entry(green_team_frame, font=("Arial", 12), width=20)
        codename_entry.grid(row=i, column=2, padx=5, pady=2)

        green_team_entries.append((id_entry, codename_entry))

    # Adding new player input fields and button
    add_player_label = tk.Label(player_entry, text="Add New Player", bg="black", fg="white", font=("Arial", 16))
    add_player_label.grid(row=2, column=0, columnspan=2, pady=10)

    id_entry = tk.Entry(player_entry, font=("Arial", 12), width=20)
    id_entry.grid(row=3, column=0, padx=5, pady=5)
    id_entry.insert(0, "Enter Player ID")  # Placeholder text

    codename_entry = tk.Entry(player_entry, font=("Arial", 12), width=40)
    codename_entry.grid(row=3, column=1, padx=5, pady=5)
    codename_entry.insert(0, "Enter Player Codename")  # Placeholder text

    add_player_button = tk.Button(player_entry, text="Add Player", command=lambda: add_player(id_entry.get(), codename_entry.get()), font=("Arial", 12), bg="darkgreen", fg="white")
    add_player_button.grid(row=4, column=0, columnspan=2, pady=10)

    populate_players(red_team_frame, green_team_frame)

    player_entry.mainloop()

# Function to add a player to the database
def add_player(player_id, codename):
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Check if the player ID already exists
        cursor.execute('''
            SELECT id FROM players WHERE id = %s;
        ''', (player_id,))
        result = cursor.fetchone()

        if result:
            print(f"Player with ID {player_id} already exists!")
        else:
            # Insert the new player if not already in the database
            cursor.execute('''
                INSERT INTO players (id, codename)
                VALUES (%s, %s);
            ''', (player_id, codename))
            conn.commit()

        populate_players(red_team_frame, green_team_frame)

    except Exception as error:
        print(f"Error inserting player: {error}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# to get players to show up in GUI
def populate_players(red_team_frame, green_team_frame):
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Fetch players from the database
        cursor.execute("SELECT * FROM players;")
        players = cursor.fetchall()

        # Debugging: Print players fetched from the database
        print(players)

        # Clear the frames before repopulating
        for widget in red_team_frame.winfo_children():
            widget.destroy()

        for widget in green_team_frame.winfo_children():
            widget.destroy()

        # Populate Red Team 
        for i, player in enumerate(players[:19]):
            player_label = tk.Label(red_team_frame, text=f"{i+1}. {player[1]}", bg="darkred", fg="white", font=("Arial", 12))
            player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

        # Populate Green Team 
        for i, player in enumerate(players[19:]):
            player_label = tk.Label(green_team_frame, text=f"{i+1}. {player[1]}", bg="darkgreen", fg="white", font=("Arial", 12))
            player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

    except Exception as error:
        print(f"Error fetching players: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# splash screen window
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.configure(background="black")

# size of window
splash_screen.geometry("800x600")

# splash screen image
image = Image.open("logo.jpg")
logo = ImageTk.PhotoImage(image)
logo_label = tk.Label(splash_screen, image=logo)
logo_label.pack()

# displayed for 3 seconds, then show player entry screen
splash_screen.after(3000, open_player_entry)

splash_screen.mainloop()
