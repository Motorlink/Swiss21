# Swiss21 - Server-Setup & Infrastruktur

**Datum**: 17. Dezember 2024  
**Server**: 185.229.91.116 (37366.hostserv.eu)  
**Projekt**: Swiss21 - Abisco ↔ ABA Ninja Integration  
**Verantwortlich**: Manus AI

---

## 1. Übersicht

Dieses Dokument beschreibt die vollständig **isolierte und sichere Infrastruktur**, die für das **Swiss21-Projekt** auf dem Server 185.229.91.116 eingerichtet wurde. Ziel ist die strikte Trennung von Bank- und Rechnungsdaten von anderen Anwendungen (z.B. `swiss-connect`).

## 2. Dedizierter User: `swiss21`

Ein dedizierter Linux-User `swiss21` wurde erstellt, um die Anwendung zu verwalten und auszuführen.

### User-Details

| Attribut | Wert |
|---|---|
| **Username** | `swiss21` |
| **Passwort** | `MaxundLeo1517##Swiss21` |
| **Home-Verzeichnis** | `/home/swiss21` |
| **Shell** | `/bin/bash` |

### Berechtigungen

Der User `swiss21` hat folgende Berechtigungen:

- **Sudo-Rechte**: Kann System-Operationen mit `sudo` ausführen.
  - `sudo usermod -aG sudo swiss21`
- **Docker-Rechte**: Kann Docker-Container verwalten (sobald Docker installiert ist).
  - `sudo usermod -aG docker swiss21`
- **Besitzrechte**: Ist Besitzer aller Swiss21-Projektverzeichnisse.
  - `sudo chown -R swiss21:swiss21 /opt/swiss21`

## 3. Isolierte Verzeichnisstruktur

Eine komplett getrennte Verzeichnisstruktur wurde unter `/opt/swiss21` angelegt.

### Struktur

```
/opt/swiss21/
├── app/                    # Anwendungscode (Git Repository)
│   └── Swiss21/           # Geklontes Repository
├── data/                   # Datenbank-Daten (isoliert, NICHT in Git)
├── logs/                   # Log-Dateien (isoliert, NICHT in Git)
├── backups/                # Backup-Dateien (isoliert, NICHT in Git)
├── certs/                  # SSL-Zertifikate (isoliert, NICHT in Git)
└── SERVER_CREDENTIALS.md   # Sichere Credentials (isoliert, NICHT in Git)
```

### Berechtigungen

- **Besitzer**: `swiss21:swiss21`
- **Rechte**: `750` (rwxr-x---)
  - `swiss21` (User): Voller Zugriff (Lesen, Schreiben, Ausführen)
  - `swiss21` (Gruppe): Lese- und Ausführungsrechte
  - **Andere**: Kein Zugriff

## 4. Sichere Credentials-Verwaltung

Alle sensiblen Daten (Passwörter, API-Keys, etc.) werden **ausschließlich auf dem Server** in der Datei `SERVER_CREDENTIALS.md` gespeichert.

### Details

- **Datei**: `/opt/swiss21/SERVER_CREDENTIALS.md`
- **Besitzer**: `swiss21:swiss21`
- **Rechte**: `600` (rw-------) - Nur der User `swiss21` kann die Datei lesen und schreiben.
- **Inhalt**: Server-Zugang, API-Keys, Datenbank-Passwörter, etc.
- **Status**: **NIEMALS IN GITHUB!**

## 5. GitHub Repository & `.gitignore`

Das `Motorlink/Swiss21` Repository wurde nach `/opt/swiss21/app/Swiss21` geklont.

### `.gitignore`

Die `.gitignore`-Datei wurde erweitert, um sicherzustellen, dass **keine sensiblen Daten** versehentlich committet werden:

```gitignore
# Server Credentials (NIEMALS committen!)
SERVER_CREDENTIALS.md
*_CREDENTIALS.md
*.pem
*.key
*.crt

# Sensitive Data
backups/
certs/
*.sql
*.db
*.sqlite
*.sqlite3

# SSH Keys
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub
*.ppk
```

## 6. Docker-Setup (Vorbereitung)

### Docker-Netzwerk

Ein eigenes, isoliertes Docker-Netzwerk wird für Swiss21 erstellt, um die Container vom `swiss-connect`-Netzwerk zu trennen.

```bash
docker network create swiss21_network
```

### `docker-compose.yml`

Eine separate `docker-compose.yml` wird in `/opt/swiss21/` erstellt, die dieses Netzwerk verwendet.

```yaml
version: '3.8'

services:
  swiss21-app:
    build: ./app/Swiss21
    container_name: swiss21_app
    restart: always
    volumes:
      - ./app/Swiss21:/app
      - ./logs:/app/logs
    ports:
      - "8228:8228"  # Webisco-Port
    networks:
      - swiss21_network
    env_file:
      - ./app/Swiss21/.env

  # Optional: Datenbank
  # swiss21-db:
  #   image: postgres:15
  #   container_name: swiss21_db
  #   restart: always
  #   volumes:
  #     - ./data:/var/lib/postgresql/data
  #   networks:
  #     - swiss21_network
  #   environment:
  #     - POSTGRES_USER=swiss21
  #     - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  #     - POSTGRES_DB=swiss21

networks:
  swiss21_network:
    external: true
```

## 7. Nächste Schritte

1. ✅ **Infrastruktur erstellt**
2. ⏳ **Docker installieren** (falls noch nicht geschehen)
3. ⏳ **Docker-Netzwerk erstellen**
4. ⏳ **`.env`-Datei erstellen** auf dem Server mit den echten Credentials
5. ⏳ **`docker-compose.yml` erstellen**
6. ⏳ **Anwendung deployen** mit `docker compose up -d`
7. ⏳ **DNS & SSL konfigurieren**

---

**Die Infrastruktur ist nun bereit für das Deployment. Alle Daten sind sicher und isoliert.**
