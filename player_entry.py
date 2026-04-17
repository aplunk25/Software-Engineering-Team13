#!/usr/bin/env python3
"""
Entry Terminal - Player Entry System (Tkinter GUI)
Two teams with ID Number and Codename columns
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import psycopg2
from psycopg2 import sql
from UDP_Client import send_packet
from Countdown_timer import CountdownTimer
from play_action import launch_play_action

HARDWARE_TEAM_PAIR = {}  # Global dictionary to store hardware ID to team mapping
HARDWARE_TEAM_PAIR_FILE = "hardware_team.json"


class Team:
    def __init__(self, name: str, color: str, max_players: int = 20):
        self.name = name
        self.color = color
        self.players = [["", ""] for _ in range(max_players)]

    def add_player(self, index: int, id_number: str, codename: str = ""):
        if 0 <= index < len(self.players):
            self.players[index] = [id_number, codename]

    def remove_player(self, index: int):
        if 0 <= index < len(self.players):
            self.players[index] = ["", ""]

    def get_player_count(self):
        return sum(1 for p in self.players if p[0])


class EntryTerminal:
    def __init__(self, root, pg_config):
        self.root = root
        self.root.title("Entry Terminal")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")
        self.hardware_id = tk.StringVar()

        self.pg_config = dict(pg_config)

        self.table_name = "players"
        self.id_column = "id"
        self.codename_column = "codename"
        self._ensure_table()

        self.teams = [
            Team("RED TEAM", "#8B0000", 20),
            Team("GREEN TEAM", "#006400", 20)
        ]

        self.current_team = 0
        self.current_slot = 0
        self.current_column = 0

        self.game_mode = "Standard public mode"

        self.entry_widgets = {0: [], 1: []}

        self.create_ui()

    def _ensure_table(self):
        """Create the players table if it doesn't exist."""
        try:
            with psycopg2.connect(**self.pg_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS players (
                            id INTEGER PRIMARY KEY,
                            codename TEXT NOT NULL,
                            team INTEGER NOT NULL DEFAULT 0
                        );
                    """)

                    # FRIEND VERSION SCHEMA LINE RESTORED
                    cur.execute("""
                        ALTER TABLE players ADD COLUMN IF NOT EXISTS team INTEGER NOT NULL DEFAULT 0;
                    """)

                conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def _db_upsert(self, pid: int, codename: str, team: int = 0):
        with psycopg2.connect(**self.pg_config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM players WHERE id = %s;", (pid,))
                cur.execute(
                    "INSERT INTO players (id, codename, team) VALUES (%s, %s, %s);",
                    (pid, codename, team)
                )
            conn.commit()

    def _db_delete(self, pid: int):
        q = sql.SQL("DELETE FROM {t} WHERE {idc} = %s;").format(
            t=sql.Identifier(self.table_name),
            idc=sql.Identifier(self.id_column),
        )
        with psycopg2.connect(**self.pg_config) as conn:
            with conn.cursor() as cur:
                cur.execute(q, (pid,))
            conn.commit()

    def save_row(self, team_idx: int, slot_idx: int):
        try:
            id_entry, codename_entry, _, checkbox_var = self.entry_widgets[team_idx][slot_idx]
        except Exception:
            return

        id_str = id_entry.get().strip()
        code = codename_entry.get().strip()

        if not id_str and not code:
            checkbox_var.set(False)
            return

        if not id_str.isdigit():
            messagebox.showerror("Input Error", "Equipment ID must be numeric.")
            return

        pid = int(id_str)

        if not code:
            code = self.lookup_codename(id_str).strip()
            if code:
                codename_entry.delete(0, tk.END)
                codename_entry.insert(0, code)

        if not code:
            return

        if checkbox_var.get() and id_str and code:
            self.create_hardware_id_popup(team_idx)

        try:
            self._db_upsert(pid, code, team_idx)
            checkbox_var.set(True)

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def create_ui(self):
        title_frame = tk.Frame(self.root, bg="#1a1a2e", height=80)
        title_frame.pack(fill=tk.X, pady=(10, 0))
        title_frame.pack_propagate(False)

        subtitle_label = tk.Label(
            title_frame,
            text="Edit Current Game",
            font=("Courier", 20, "bold"),
            bg="#1a1a2e",
            fg="#00bfff"
        )
        subtitle_label.pack()

        content_frame = tk.Frame(self.root, bg="#1a1a2e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for team_idx in range(2):
            team_frame = tk.Frame(content_frame, bg="#1a1a2e")
            team_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

            self.create_team_panel(team_frame, team_idx)

        self.create_footer()

    def create_team_panel(self, parent, team_idx):
        team = self.teams[team_idx]

        header_frame = tk.Frame(parent, bg=team.color, height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame,
            text=team.name,
            font=("Courier", 14, "bold"),
            bg=team.color,
            fg="white"
        )
        header_label.pack(expand=True)

        col_header_frame = tk.Frame(parent, bg="#2a2a3e")
        col_header_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(col_header_frame, text="", width=3, bg="#2a2a3e", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Label(col_header_frame, text="ID Number", width=20, bg="#2a2a3e", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Label(col_header_frame, text="Codename", width=20, bg="#2a2a3e", fg="white").pack(side=tk.LEFT, padx=2)

        roster_container = tk.Frame(parent, bg="#1a1a2e")
        roster_container.pack(fill=tk.BOTH, expand=True, pady=5)

        canvas = tk.Canvas(roster_container, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(roster_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for i in range(20):
            self.create_player_row(scrollable_frame, team_idx, i)

    def create_player_row(self, parent, team_idx, slot_idx):
        team = self.teams[team_idx]

        row_frame = tk.Frame(parent, bg="#2a2a3e", bd=1, relief=tk.SOLID)
        row_frame.pack(fill=tk.X, pady=1, padx=2)

        slot_frame = tk.Frame(row_frame, bg="#2a2a3e")
        slot_frame.pack(side=tk.LEFT, padx=5, pady=3)

        checkbox_var = tk.BooleanVar(value=False)

        tk.Label(slot_frame, text=str(slot_idx), bg="#2a2a3e", fg="white", width=2).pack(side=tk.LEFT)

        id_entry = tk.Entry(row_frame, bg="#1a1a2e", fg="white", insertbackground="white", width=20)
        id_entry.pack(side=tk.LEFT, padx=2)

        codename_entry = tk.Entry(row_frame, bg="#1a1a2e", fg="white", insertbackground="white", width=20)
        codename_entry.pack(side=tk.LEFT, padx=2)

        delete_btn = tk.Button(
            row_frame,
            text="✕",
            bg="#8B0000",
            fg="white",
            command=lambda: self.delete_player(team_idx, slot_idx)
        )
        delete_btn.pack(side=tk.LEFT, padx=2)

        self.entry_widgets[team_idx].append((id_entry, codename_entry, row_frame, checkbox_var))

    def delete_player(self, team_idx, slot_idx):
        id_entry, codename_entry, _, checkbox_var = self.entry_widgets[team_idx][slot_idx]
        id_str = id_entry.get().strip()

        if id_str.isdigit():
            self._db_delete(int(id_str))

        id_entry.delete(0, tk.END)
        codename_entry.delete(0, tk.END)
        checkbox_var.set(False)

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#1a1a2e")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        buttons_frame = tk.Frame(footer_frame, bg="#1a1a2e")
        buttons_frame.pack()

        functions = [
            ("F1\nEdit Game", self.edit_game),
            ("F2\nGame\nParameters", self.game_parameters),
            ("F3\nPreEntered\nGames", self.preentered_games),
            ("F5\nStart\nGames", self.start_games),
            ("F7\n\n", None),
            ("F8\nView\nGame", self.view_game),
            ("F10\nFlick\nSync", self.flick_sync),
            ("F12\nClear\nGame", self.clear_game)
        ]

        for label, command in functions:
            tk.Button(
                buttons_frame,
                text=label,
                bg="#2a2a3e",
                fg="white",   # FIXED AS REQUESTED
                activeforeground="white",
                command=command if command else lambda: None
            ).pack(side=tk.LEFT, padx=5)

    def clear_game(self):
        result = messagebox.askyesno("Clear Game", "Are you sure?")
        if result:
            try:
                with psycopg2.connect(**self.pg_config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("DELETE FROM players;")  # RESTORED
                    conn.commit()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

            for team_idx in range(2):
                for id_entry, codename_entry, _, checkbox_var in self.entry_widgets[team_idx]:
                    id_entry.delete(0, tk.END)
                    codename_entry.delete(0, tk.END)
                    checkbox_var.set(False)

    def lookup_codename(self, id_number):
        return ""

    def create_hardware_id_popup(self, team_idx):
        popup = tk.Toplevel(self.root)
        popup.title("Hardware ID")

        frame = tk.Frame(popup)
        frame.pack()

        entry = tk.Entry(frame, textvariable=self.hardware_id)
        entry.pack()

        tk.Button(
            frame,
            text="Submit",
            command=lambda: self.send_hardware_id(popup, team_idx)
        ).pack()

    def send_hardware_id(self, popup, team_idx):
        h_id = self.hardware_id.get().strip()
        if h_id.isdigit():
            HARDWARE_TEAM_PAIR[int(h_id)] = "RED" if team_idx == 0 else "GREEN"
            with open(HARDWARE_TEAM_PAIR_FILE, "w") as f:
                json.dump(HARDWARE_TEAM_PAIR, f)
            send_packet(int(h_id))
        popup.destroy()

    def edit_game(self): pass
    def game_parameters(self): pass
    def preentered_games(self): pass
    def start_games(self): pass
    def view_game(self): pass
    def flick_sync(self): pass


def entry_terminal(root_or_config, pg_config=None):
    root = tk.Tk() if pg_config is None else root_or_config
    EntryTerminal(root, pg_config if pg_config else root_or_config)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    entry_terminal(root, {"dbname": "photon", "user": "student", "host": "localhost", "port": 5432})
    root.mainloop()
