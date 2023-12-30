#!/bin/sh

# Starten Sie den Server im Hintergrund
python3 manage.py runserver 0.0.0.0:8000 &

# Führen Sie die Migration aus
python3 manage.py migrate

# Warten Sie auf den Server-Prozess, um zu beenden
wait %1