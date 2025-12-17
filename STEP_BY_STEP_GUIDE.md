# Schritt-für-Schritt-Anleitung für KI-Agent

**Ziel:** Systematischer Import aller Kunden und Rechnungen von Abisco in ABA Ninja

## Vorbereitung

Bevor du mit dem Import beginnst, stelle sicher, dass du Zugriff auf folgende Ressourcen hast:

1.  **Server-Zugang:** SSH-Zugang zum Server `185.229.91.116` mit Benutzer `swiss21`.
2.  **Credentials:** Lies die Datei `/opt/swiss21/SERVER_CREDENTIALS.md` auf dem Server, um API-Token und andere sensible Daten zu erhalten.
3.  **Datenbank:** Stelle sicher, dass die PostgreSQL-Datenbank mit den Abisco-Daten verfügbar ist.
4.  **GitHub Repository:** Klone das Repository `Motorlink/Swiss21`.

## Phase 1: Kunden in ABA Ninja importieren

### Schritt 1.1: Liste aller Kunden abrufen

Rufe alle Kunden aus der Abisco-Datenbank ab, die noch nicht in ABA Ninja existieren.

**SQL-Abfrage:**
```sql
SELECT kundennummer, name, strasse, plz, ort, land, email
FROM kunden
WHERE kundennummer BETWEEN 10000 AND 10030
ORDER BY kundennummer;
```

**Ergebnis:** Eine Liste von Kunden mit ihren Stammdaten.

### Schritt 1.2: Prüfen, welche Kunden bereits in ABA Ninja existieren

Rufe die Liste aller Unternehmen aus ABA Ninja ab und vergleiche sie mit der Abisco-Liste.

**API-Endpunkt:**
```
GET https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/addresses/v2/companies
```

**Ergebnis:** Eine Liste von `companyUuid` und `customer_number` (Kundennummer).

### Schritt 1.3: Fehlende Kunden erstellen

Für jeden Kunden, der in Abisco existiert, aber nicht in ABA Ninja:

1.  **Erstelle die Adresse:**
    ```
    POST https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/addresses/v2/companies
    ```
    **Payload:**
    ```json
    {
      "addresses": [
        {
          "name": "Kundenname",
          "customer_number": "10001",
          "street": "Straße",
          "zip": "PLZ",
          "city": "Ort",
          "country_code": "CH",
          "email": "kunde@example.com"
        }
      ]
    }
    ```

2.  **Speichere die UUIDs:** Aus der Antwort erhältst du die `addressUuid` und `companyUuid`. Speichere diese in einer Mapping-Tabelle (z.B. JSON-Datei oder Datenbank), um sie später für die Rechnungserstellung zu verwenden.

3.  **Warte auf Bestätigung:** Zeige dem Benutzer die Details des erstellten Kunden und warte auf das "GO"-Kommando, bevor du mit dem nächsten Kunden fortfährst.

### Schritt 1.4: Mapping-Datei erstellen

Erstelle eine JSON-Datei `data/customer_uuid_mapping.json` mit folgendem Format:

```json
{
  "10000": {
    "addressUuid": "ad08bb56-373d-48df-b906-e994cb27eaf9",
    "companyUuid": "e6592469-5215-481d-b354-2227b75a6ad5"
  },
  "10001": {
    "addressUuid": "...",
    "companyUuid": "..."
  }
}
```

## Phase 2: Rechnungen in ABA Ninja importieren

### Schritt 2.1: Liste aller offenen Rechnungen abrufen

Rufe alle offenen Rechnungen aus der Abisco-Datenbank ab.

**SQL-Abfrage:**
```sql
SELECT rechnungsnummer, kundennummer, datum, faelligkeitsdatum, gesamtbetrag
FROM rechnungen
WHERE status = 'offen'
ORDER BY datum;
```

**Ergebnis:** Eine Liste von 22 offenen Rechnungen.

### Schritt 2.2: Rechnungsdetails und Positionen abrufen

Für jede Rechnung, rufe die zugehörigen Positionen ab:

**SQL-Abfrage:**
```sql
SELECT position_nr, artikelnummer, beschreibung, menge, einzelpreis, mwst_prozent, gesamtpreis
FROM rechnungspositionen
WHERE rechnungsnummer = 'RE1'
ORDER BY position_nr;
```

### Schritt 2.3: Rechnung in ABA Ninja erstellen

Verwende das Skript `scripts/create_invoice_from_abisco.py` als Vorlage. Für jede Rechnung:

1.  **Lade die Kundendaten:** Rufe die `addressUuid` und `companyUuid` aus der Mapping-Datei ab.
2.  **Erstelle die Positionen:** Konvertiere die Rechnungspositionen in das ABA Ninja-Format.
3.  **Sende die Rechnung:**
    ```
    POST https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/documents/v2/invoices
    ```
4.  **Verifiziere:** Prüfe die Antwort und stelle sicher, dass die Rechnung erfolgreich erstellt wurde.
5.  **Warte auf Bestätigung:** Zeige dem Benutzer die Details der erstellten Rechnung und warte auf das "GO"-Kommando.

### Schritt 2.4: Gutschriften importieren

Für Gutschriften verwende den separaten Endpunkt:

```
POST https://api.abaninja.ch/accounts/{ACCOUNT_UUID}/documents/v2/credit-notes
```

Die Struktur ist ähnlich wie bei Rechnungen, aber der Endpunkt und der Dokumenttyp sind unterschiedlich.

## Phase 3: QR-Code-Generierung

### Schritt 3.1: QR-Code-Bibliothek verwenden

Verwende die Python-Bibliothek `segno` oder `qrcode`, um Schweizer QR-Rechnungen zu generieren.

**Beispiel:**
```python
import segno

qr = segno.make_qr("QR-Code-Inhalt")
qr.save("rechnung_qr.png", scale=10)
```

### Schritt 3.2: QR-Code-Inhalt erstellen

Der QR-Code für Schweizer QR-Rechnungen muss bestimmte Informationen enthalten (IBAN, Betrag, Referenz, etc.). Konsultiere die offizielle Dokumentation für das exakte Format.

## Phase 4: E-Mail-Versand

### Schritt 4.1: SMTP-Konfiguration

Lies die SMTP-Server-Details aus `/opt/swiss21/SERVER_CREDENTIALS.md`.

### Schritt 4.2: E-Mail mit Rechnung und QR-Code versenden

Verwende die Python-Bibliothek `smtplib`, um E-Mails zu versenden.

**Beispiel:**
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

msg = MIMEMultipart()
msg['From'] = "info@mt-transport.ch"
msg['To'] = "kunde@example.com"
msg['Subject'] = "Rechnung RE1"

body = "Sehr geehrter Kunde, anbei finden Sie Ihre Rechnung."
msg.attach(MIMEText(body, 'plain'))

# QR-Code anhängen
with open("rechnung_qr.png", "rb") as f:
    img = MIMEImage(f.read())
    msg.attach(img)

server = smtplib.SMTP('smtp.example.com', 587)
server.starttls()
server.login("user", "password")
server.send_message(msg)
server.quit()
```

## Phase 5: Zahlungsabgleich

### Schritt 5.1: Zahlungseingänge von der Bank abrufen

Implementiere eine Schnittstelle, um Zahlungseingänge von der Bank oder dem Zahlungsanbieter abzurufen (z.B. über eine API oder Datei-Import).

### Schritt 5.2: Zahlungen in Abisco aktualisieren

Für jede Zahlung:

1.  **Identifiziere die Rechnung:** Verwende die Referenznummer aus der Zahlung, um die zugehörige Rechnung in Abisco zu finden.
2.  **Aktualisiere den Status:** Setze den Status der Rechnung in Abisco auf "bezahlt".
3.  **Dokumentiere:** Speichere die Zahlungsdetails (Datum, Betrag, Zahlungsart) in Abisco.

## Wichtige Hinweise

- **Warte immer auf Bestätigung:** Führe niemals automatische Massenimporte ohne explizite Freigabe durch den Benutzer durch.
- **Fehlerbehandlung:** Implementiere robuste Fehlerbehandlung für API-Fehler, Netzwerkprobleme und fehlende Daten.
- **Logging:** Protokolliere alle Aktionen (Kundenerstellung, Rechnungsimport, E-Mail-Versand) für spätere Nachvollziehbarkeit.
- **Dokumentation:** Halte alle Fortschritte und Änderungen im GitHub-Repository fest.

---

**Erstellt von:** Manus AI  
**Datum:** 2025-12-17
