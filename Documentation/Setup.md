### Setup des Projekts unter Windows

1. **Installation und Start von Docker Desktop**
   - Installieren Sie Docker Desktop auf Ihrem Windows-System von der offiziellen Docker-Website.
   - Befolgen Sie die Installationsanweisungen.
   - Stellen Sie sicher, dass Docker Desktop nach der Installation ausgeführt wird, bevor Sie mit dem nächsten Schritt fortfahren.

2. **Verwenden der Kommandozeile im Projektverzeichnis**
   - Öffnen Sie die Kommandozeile (CMD).
   - Navigieren Sie zum Projektverzeichnis, insbesondere in den Unterordner `/Project/blokusserver/`.
     - Sie können dies tun, indem Sie den Explorer öffnen, zum entsprechenden Verzeichnis navigieren, die Adressleiste anklicken, `cmd` eingeben und Enter drücken.
     - Alternativ können Sie die Kommandozeile öffnen und den `cd`-Befehl verwenden, um in das Verzeichnis zu navigieren.

3. **Ausführen von Docker Compose**
   - Im CMD-Fenster, das sich nun im Verzeichnis `/Project/blokusserver/` befindet, führen Sie den folgenden Befehl aus:
     ```shell
     docker-compose up -d
     ```
     Dieser Befehl startet die notwendigen Docker-Container im Hintergrund (dank des `-d`-Flags für "detached").
     > Hinweis: Stellen Sie sicher, dass eine `docker-compose.yml`-Datei im Verzeichnis vorhanden ist, die definiert, welche Container gestartet werden sollen.

4. **Start der Anwendung**
   - Starten Sie die Anwendung, indem Sie in das Verzeichnis `/Project/client/` wechseln.
   - Führen Sie dort die Datei `Blokus.exe` aus:
     - Öffnen Sie den Explorer, navigieren Sie zum Verzeichnis und doppelklicken Sie auf die Datei.
     - Oder verwenden Sie die Kommandozeile mit dem Befehl:
       ```shell
       start Blokus.exe
       ```
     > Beachten Sie, dass das Starten der Anwendung je nach Systemleistung und anderen Faktoren etwa 10 bis 20 Sekunden dauern kann.