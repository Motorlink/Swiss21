# Übergabedokumentation für KI-Agent

**Projekt:** Swiss21 Integration für Abisco und ABA Ninja

**Ziel:** Automatisierung der Rechnungsverarbeitung, des Versands und der Zahlungsabstimmung zwischen dem Abisco-Buchhaltungssystem und der ABA Ninja API.

**Letzter Status:**
- **Proof-of-Concept erfolgreich:** Rechnung R0002 wurde von Abisco-Testdaten in ABA Ninja erstellt.
- **Datenbank importiert:** Ein PostgreSQL-Dump von Abisco wurde importiert und analysiert.
- **Daten extrahiert:** 68 Rechnungen und 15 Gutschriften wurden aus der Datenbank extrahiert.
- **Kunden analysiert:** Kundenstamm von 10000-10030 identifiziert.
- **Excel-Export erstellt:** Eine Excel-Datei `Kunden_Rechnungen.xlsx` wurde mit Kundendaten und Rechnungsdetails pro Kunde erstellt.

## 1. Übersicht & Architektur

Dieses Dokument dient als vollständige Anleitung für einen anderen KI-Agenten, um die Entwicklung der Swiss21-Integrationsplattform zu übernehmen und fortzusetzen. Das System verbindet die lokale Abisco-Software (über eine Schnittstelle namens Webisco) mit der cloudbasierten ABA Ninja API.

**Datenfluss:**

1.  **Vorwärts (Rechnungserstellung):** `Abisco -> Swiss21-System -> ABA Ninja -> E-Mail an Kunde`
2.  **Rückwärts (Zahlungsabgleich):** `Bank/Zahlungsanbieter -> Swiss21-System -> Abisco`

## 2. Repository-Struktur

Das gesamte Projekt ist im GitHub-Repository `Motorlink/Swiss21` gespeichert. Klonen Sie dieses Repository, um zu beginnen.

```
/Swiss21
├── app/                  # Hauptanwendungsverzeichnis (auf dem Server)
│   └── ...
├── scripts/              # Hilfsskripte (z.B. für den Datenimport)
│   └── create_invoice_from_abisco.py
├── test_data/            # Testdaten und Mapping-Dokumente
│   └── ABISCO_TO_ABANINJA_MAPPING.md
├── data/                 # Extrahierte und verarbeitete Daten
│   └── Kunden_Rechnungen.xlsx
├── docs/                 # Dokumentation
│   └── PAYMENT_RECONCILIATION.md
└── HANDOVER_FOR_AI.md    # Dieses Dokument
```

## 3. Nächste Schritte für die Übernahme

1.  **Server-Zugang verstehen:** Machen Sie sich mit der Serverumgebung vertraut (siehe Abschnitt 4).
2.  **Code und Skripte analysieren:** Überprüfen Sie die vorhandenen Python-Skripte, insbesondere `scripts/create_invoice_from_abisco.py`.
3.  **API-Dokumentation prüfen:** Lesen Sie die Analyse der Webisco- und ABA Ninja-APIs.
4.  **Systematischen Import fortsetzen:** Der Benutzer möchte die Kunden und Rechnungen systematisch und nach expliziter Freigabe importieren. Beginnen Sie mit Kunde 10001, da 10000 bereits existiert.



## 4. Scripts und Code

### `scripts/create_invoice_from_abisco.py`

Dieses Skript ist das Kernstück des Proof-of-Concept. Es demonstriert, wie eine Rechnung aus strukturierten Abisco-Daten in ABA Ninja erstellt wird.

**Funktionsweise:**

1.  **Konfiguration:** Das Skript beginnt mit der Definition von statischen Konfigurationswerten:
    *   `API_TOKEN`: Der Authentifizierungstoken für die ABA Ninja API.
    *   `ACCOUNT_UUID`: Die eindeutige ID des ABA Ninja-Kontos.
    *   Diverse `UUIDs`: Statische IDs für Adressen, Firmen, Bankkonten, Einheiten (z.B. "Stück") und Mehrwertsteuersätze. Diese wurden aus einer bereits existierenden Rechnung in ABA Ninja extrahiert, um die Struktur exakt nachzubilden.

2.  **Testdaten:** Ein Python-Dictionary `abisco_data` simuliert die Daten, die aus der Abisco-Datenbank für eine einzelne Rechnung (hier "RE1") extrahiert wurden. Es enthält alle relevanten Informationen wie Rechnungsnummer, Daten, Kundendetails und Rechnungspositionen.

3.  **Positions-Mapping:** Das Skript iteriert durch die `positionen` der Testdaten und konvertiert sie in das von der ABA Ninja API erwartete Format. Hierbei wird die korrekte `vatUuid` basierend auf dem Mehrwertsteuersatz zugewiesen.

4.  **Rechnungs-Payload:** Die aufbereiteten Positionen werden in die finale `invoice_data`-Struktur eingefügt. Diese Struktur entspricht exakt dem JSON-Payload, den der `/documents/v2/invoices`-Endpunkt der ABA Ninja API erwartet.

5.  **API-Aufruf:** Mit der `requests`-Bibliothek wird ein `POST`-Request an die ABA Ninja API gesendet. Der `Authorization`-Header enthält den API-Token und der Body enthält den JSON-Payload.

6.  **Ergebnisverarbeitung:** Das Skript gibt den Statuscode der Antwort aus. Bei Erfolg (Status 200 oder 201) wird die Antwort der API (die die neu erstellte Rechnung enthält) formatiert ausgegeben, inklusive der neuen Rechnungs-UUID und -Nummer.

**Wie man es benutzt:**

Das Skript ist derzeit für den direkten Aufruf konzipiert und verwendet hartcodierte Testdaten. Um es für den produktiven Import zu verwenden, müssen die folgenden Schritte implementiert werden:

1.  **Dynamisches Laden von Daten:** Ersetzen Sie das statische `abisco_data`-Dictionary durch eine Funktion, die Daten aus der PostgreSQL-Datenbank oder einer JSON-Datei liest.
2.  **Dynamische UUID-Zuweisung:** Die `ADDRESS_UUID` und `COMPANY_UUID` müssen dynamisch pro Kunde aus ABA Ninja abgerufen (oder beim Erstellen des Kunden gespeichert) werden.
3.  **Fehlerbehandlung:** Implementieren Sie eine robustere Fehlerbehandlung für API-Fehler oder fehlende Daten.

_content


## 5. Server-Setup & Credentials

Die gesamte Anwendung und Infrastruktur ist auf einem dedizierten Server eingerichtet.

**Server-Details:**
- **IP-Adresse:** `185.229.91.116`
- **Betriebssystem:** Ubuntu 24.04
- **Benutzer:** `swiss21`
- **Projektverzeichnis:** `/opt/swiss21/`

### Credentials Management

**WICHTIG:** Es dürfen unter keinen Umständen sensible Daten wie Passwörter, API-Schlüssel oder Tokens in das GitHub-Repository committet werden.

Alle Credentials werden in einer einzigen, gesicherten Datei direkt auf dem Server gespeichert:

- **Datei:** `/opt/swiss21/SERVER_CREDENTIALS.md`
- **Berechtigungen:** Die Datei ist mit `chmod 600` gesichert, sodass nur der `swiss21`-Benutzer sie lesen und schreiben kann.

**Inhalt der `SERVER_CREDENTIALS.md`:**
- ABA Ninja API Token
- Abisco Webisco Zugangsdaten (falls erforderlich)
- Datenbank-Verbindungsdetails (falls nicht lokal)
- SMTP-Server-Details für den E-Mail-Versand
- IBAN und andere Zahlungsinformationen für QR-Rechnungen

**Anweisung für die KI:** Lies die benötigten Credentials zu Beginn eines jeden Prozesses aus dieser Datei ein. Schreibe niemals hartcodierte Schlüssel in den Code.

### Abisco Webisco Interface

Die Schnittstelle zur lokalen Abisco-Software ist über die folgenden Endpunkte erreichbar:

- **HTTP:** `http://82.220.91.37:8228`
- **HTTPS:** `https://82.220.91.37:9229`

Die Kommunikation erfolgt über XML. Eine vollständige Analyse ist Teil der API-Dokumentation.

### Datenbank

Ein vollständiger Dump der Abisco-PostgreSQL-Datenbank wurde auf dem Server importiert. Alle Skripte, die Daten aus Abisco benötigen, sollten sich mit dieser lokalen PostgreSQL-Instanz verbinden.

- **Dump-Datei:** `abisco_2025-12-15_19-50-59-314.pg.12.22.sql` (bereits importiert)
_content


## 6. API-Mappings und Datenstrukturen

Eine der kritischsten Aufgaben in diesem Projekt ist die korrekte Übersetzung der Datenmodelle von Abisco zu ABA Ninja. Eine detaillierte Analyse wurde bereits durchgeführt und ist im Repository unter `test_data/ABISCO_TO_ABANINJA_MAPPING.md` zu finden.

### Wichtige Erkenntnisse

- **Zusammengesetzte Empfänger-ID:** Um einen Rechnungsempfänger in ABA Ninja zu adressieren, sind **zwingend** sowohl die `addressUuid` als auch die `companyUuid` erforderlich. Diese müssen für jeden Kunden vor der Rechnungserstellung ermittelt werden.
- **Indirekte Referenzen:** Anstatt direkte Werte wie eine IBAN oder einen Mehrwertsteuersatz in Prozent anzugeben, verwendet die ABA Ninja API fast ausschließlich UUIDs, die auf vorkonfigurierte Entitäten im System verweisen (z.B. `bankAccountUuid`, `vatUuid`).
- **Gutschriften:** Gutschriften haben einen eigenen Endpunkt (`/documents/v2/credit-notes`) und eine leicht abweichende Struktur.

### Mapping-Tabelle (Auszug)

Die folgende Tabelle zeigt einen Auszug des Mappings vom Abisco-Datenmodell zu den Feldern der ABA Ninja API.

| Abisco Feld | ABA Ninja Feld | Beispiel / Anmerkung |
|---|---|---|
| `rechnungsnummer` | `title` oder `reference` | `"Rechnung RE1"` |
| `datum` | `invoiceDate`, `deliveryDate` | `"2025-12-17"` |
| `faelligkeitsdatum` | `dueDate` | `"2026-01-16"` |
| Kundennummer | `receiver.companyUuid` | Muss vorab pro Kunde ermittelt werden. |
| `positionen[*].beschreibung` | `positions[*].productDescription` | `"Ölfilter"` |
| `positionen[*].einzelpreis` | `positions[*].singlePrice` | `14.12` |
| `positionen[*].mwst_prozent` | `positions[*].vatUuid` | Muss über eine Mapping-Tabelle von % zu UUID aufgelöst werden. |

**Anweisung für die KI:** Konsultiere die vollständige Mapping-Datei, bevor du neue Import- oder Konvertierungslogik implementierst. Stelle sicher, dass alle benötigten UUIDs vor dem Erstellen von Rechnungen oder Gutschriften abgefragt und korrekt zugewiesen werden.


## 7. Datenbank und extrahierte Daten

Ein vollständiger PostgreSQL-Dump der Abisco-Datenbank wurde importiert. Die Datenbank enthält alle historischen Rechnungen, Aufträge und Kundendaten.

**Wichtige Statistiken:**
- **Gesamtgröße:** 936 MB
- **Rechnungen:** 83 (davon 68 reguläre Rechnungen und 15 Gutschriften)
- **Aufträge:** 116
- **Kunden:** 31 (Kundennummern 10000-10030)
- **Aktive Kunden mit Rechnungen:** 9

Die extrahierten Rechnungsdaten wurden in der Datei `/tmp/abisco_invoices.json` gespeichert. Für eine bessere Übersicht wurde außerdem eine Excel-Datei (`data/Kunden_Rechnungen.xlsx`) erstellt, die für jeden Kunden ein eigenes Arbeitsblatt mit allen zugehörigen Rechnungen enthält.

**Status der Rechnungen:**
- **Offen:** 22 Rechnungen
- **Bezahlt:** 46 Rechnungen
- **Gutschriften:** 15 (alle als bezahlt markiert)

## 8. Systematischer Import-Prozess

Der Benutzer hat explizit angewiesen, dass alle Daten **systematisch** und **nur nach expliziter Freigabe** importiert werden sollen. Der Prozess sollte wie folgt ablaufen:

1.  **Kunde für Kunde:** Beginne mit Kunde 10000 (bereits in ABA Ninja vorhanden), dann 10001, 10002, usw.
2.  **Warte auf "GO"-Kommando:** Bevor ein Kunde oder eine Rechnung importiert wird, muss der Benutzer explizit zustimmen.
3.  **Verifizierung:** Nach jedem Import überprüfe, ob die Daten korrekt in ABA Ninja angelegt wurden.
4.  **Dokumentation:** Halte fest, welche Kunden und Rechnungen bereits importiert wurden.

**Wichtige Hinweise:**
- **Kundennummern:** Die Kundennummern (10000, 10001, etc.) sind kritisch und müssen in ABA Ninja erhalten bleiben.
- **E-Mail-Adressen:** Für MT Transport (Kunde 10000) muss die E-Mail `info@mt-transport.ch` verwendet werden, **nicht** `senad@motorlink.ch`.
- **Gutschriften:** Gutschriften müssen über den separaten Endpunkt `/documents/v2/credit-notes` importiert werden.

## 9. Nächste Schritte für die KI

1.  **Kunden importieren:** Erstelle die fehlenden Kunden (10001-10030) in ABA Ninja. Speichere die `addressUuid` und `companyUuid` für jeden Kunden.
2.  **Offene Rechnungen importieren:** Importiere die 22 offenen Rechnungen in ABA Ninja.
3.  **Gutschriften importieren:** Importiere die 15 Gutschriften über den korrekten Endpunkt.
4.  **QR-Code-Generierung:** Implementiere die Generierung von QR-Codes für Schweizer QR-Rechnungen.
5.  **E-Mail-Versand:** Implementiere den automatischen Versand der Rechnungen per E-Mail mit Zahlungslinks (Twint, etc.).
6.  **Zahlungsabgleich:** Implementiere die bidirektionale Synchronisation von Zahlungseingängen zurück zu Abisco.

## 10. Wichtige Dateien und Ressourcen

| Datei/Pfad | Beschreibung |
|---|---|
| `scripts/create_invoice_from_abisco.py` | Proof-of-Concept-Skript für Rechnungserstellung |
| `test_data/ABISCO_TO_ABANINJA_MAPPING.md` | Vollständiges Daten-Mapping zwischen Abisco und ABA Ninja |
| `docs/PAYMENT_RECONCILIATION.md` | Dokumentation des Zahlungsabgleichs |
| `data/Kunden_Rechnungen.xlsx` | Excel-Export mit Kundendaten und Rechnungen |
| `/tmp/abisco_invoices.json` | Extrahierte Rechnungsdaten aus der Datenbank |
| `/opt/swiss21/SERVER_CREDENTIALS.md` | Gesicherte Credentials-Datei auf dem Server (NICHT in GitHub!) |

## 11. Kontakt und Support

Bei Fragen oder Unklarheiten wende dich an den Benutzer. Alle Änderungen und Fortschritte müssen im GitHub-Repository dokumentiert werden.

**Repository:** `Motorlink/Swiss21`

---

**Erstellt von:** Manus AI  
**Datum:** 2025-12-17
