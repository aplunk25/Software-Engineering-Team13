# Sofware-Engineering-Team13
Team 13 Repo for Software Engineering Spring 2026
Aplunk25 | Alex Plunk 
Jortiz2003 | Jose Ortiz
loganc01 | Logan Camp 
Milesh2002 | Miles Schlutermann 


HOW TO RUN PROGRAM:

1. Download files from GitHub
2. chmod +x Script.sh
3. ./Script.sh
4. venv/bin/activate in the directory that venv is located (preferably it opens in the directory with Photon files)
5. Open two terminal windows, in one, with venv active, run python3 UDP_Server.py
6. In the other with venv active as well, run python3 python-pg.py, the splash screen will show and then in the terminal it will ask to choose a network, after choosing it will launch the player entry terminal
7. Follow the input


Other Important Info: 
To view the current players database, do psql -U student -d photon -h 127.0.0.1 and password student. 
Next do SELECT * FROM players;  to view the players added. 
