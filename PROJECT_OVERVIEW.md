# Swiss21 Projekt-Übersicht

**Automatisierte Rechnungsverarbeitung zwischen Abisco und ABA Ninja**

## Projektziel

Swiss21 ist ein Integrationssystem, das die lokale Buchhaltungssoftware **Abisco** (über die Webisco-Schnittstelle) mit der cloudbasierten **ABA Ninja API** verbindet. Das System automatisiert den gesamten Prozess der Rechnungserstellung, des QR-Code-Versands und der Zahlungsabstimmung.

## Datenfluss

Das System implementiert einen bidirektionalen Datenfluss zwischen Abisco und ABA Ninja.

**Vorwärts (Rechnungserstellung):**
```
Abisco → Swiss21-System → ABA Ninja → E-Mail an Kunde
```

**Rückwärts (Zahlungsabgleich):**
```
Bank/Zahlungsanbieter → Swiss21-System → Abisco
```

## Aktueller Projektstand

### Erfolgreich abgeschlossen

1.  **GitHub Repository erstellt:** Das Repository `Motorlink/Swiss21` wurde mit vollständiger Projektstruktur angelegt.
2.  **Server-Infrastruktur:** Ein dedizierter Benutzer `swiss21` wurde auf dem Server `185.229.91.116` mit isolierter Umgebung unter `/opt/swiss21/` eingerichtet.
3.  **API-Analyse:** Vollständige Analyse der Webisco-Schnittstelle (Abisco) und der ABA Ninja API wurde dokumentiert.
4.  **Proof-of-Concept:** Rechnung R0002 wurde erfolgreich von Abisco-Testdaten in ABA Ninja erstellt.
5.  **Datenbank-Import:** Die Abisco PostgreSQL-Datenbank (936 MB) wurde importiert und enthält 83 Rechnungen, 116 Aufträge und 31 Kunden.
6.  **Datenextraktion:** 68 reguläre Rechnungen und 15 Gutschriften wurden aus der Datenbank separiert.
7.  **Kundenanalyse:** Kunden mit Nummern 10000-10030 wurden identifiziert, davon haben 9 aktive Rechnungen.
8.  **Gutschriften-Struktur:** Die Struktur für Gutschriften wurde aus ABA Ninja abgerufen und dokumentiert.
9.  **Excel-Export:** Eine umfassende Excel-Datei mit Kundendaten und Rechnungen (`Kunden_Rechnungen.xlsx`) wurde erstellt und in GitHub committed.

### Wichtige Erkenntnisse

- **Zusammengesetzte IDs:** ABA Ninja benötigt sowohl `addressUuid` als auch `companyUuid` für den Rechnungsempfänger.
- **Gutschriften:** Gutschriften verwenden einen separaten Endpunkt `/documents/v2/credit-notes` mit dem Typ `credit_note`.
- **Erfolgreiche Rechnungserstellung:** Die Erstellung von Rechnungen in ABA Ninja funktioniert einwandfrei.
- **Kundenstamm:** Kunde 10000 (MT Transport) existiert bereits in ABA Ninja.

### Nächste Schritte

1.  **Kunden importieren:** Fehlende Kunden (10001-10030) in ABA Ninja erstellen.
2.  **Offene Rechnungen importieren:** Die 22 offenen Rechnungen in ABA Ninja importieren.
3.  **Gutschriften importieren:** Die 15 Gutschriften über den korrekten Endpunkt importieren.
4.  **QR-Code-Generierung:** Implementierung der QR-Code-Generierung für Schweizer QR-Rechnungen.
5.  **E-Mail-Versand:** Automatischer Versand der Rechnungen per E-Mail mit Zahlungslinks.
6.  **Zahlungsabgleich:** Bidirektionale Synchronisation von Zahlungseingängen zurück zu Abisco.

## Wichtige Dateien

| Datei | Beschreibung |
|---|---|
| `HANDOVER_FOR_AI.md` | Vollständige Übergabedokumentation für andere KI-Agenten |
| `scripts/create_invoice_from_abisco.py` | Proof-of-Concept-Skript für Rechnungserstellung |
| `test_data/ABISCO_TO_ABANINJA_MAPPING.md` | Vollständiges Daten-Mapping |
| `docs/PAYMENT_RECONCILIATION.md` | Dokumentation des Zahlungsabgleichs |
| `data/Kunden_Rechnungen.xlsx` | Excel-Export mit Kundendaten |
| `/opt/swiss21/SERVER_CREDENTIALS.md` | Gesicherte Credentials (nur auf Server) |

## Benutzeranforderungen

- Alle Arbeiten müssen im GitHub-Repository gespeichert werden.
- Sensible Daten (Passwörter, API-Schlüssel) dürfen **niemals** in GitHub committed werden.
- Systematischer Ansatz: Kunden werden einzeln und nach expliziter Freigabe verarbeitet.
- Kundennummern sind kritisch und müssen erhalten bleiben.
- Separate Behandlung für Gutschriften (negative Beträge) vs. reguläre Rechnungen.
- E-Mail für MT Transport: `info@mt-transport.ch` (NICHT `senad@motorlink.ch`).
- Warten auf explizites "GO"-Kommando vor Import/Transfer von Daten.

## Server-Details

- **IP:** `185.229.91.116`
- **Betriebssystem:** Ubuntu 24.04
- **Benutzer:** `swiss21`
- **Projektverzeichnis:** `/opt/swiss21/`
- **Abisco Server:** `82.220.91.37:8228` (HTTP), `82.220.91.37:9229` (HTTPS)

## Technologie-Stack

- **Programmiersprache:** Python 3.11
- **Framework:** Flask (für zukünftige Web-API)
- **Datenbank:** PostgreSQL
- **APIs:** ABA Ninja API (JWT-Authentifizierung), Webisco (XML über HTTP)
- **Deployment:** Docker (geplant)
- **Abhängigkeiten:** requests, lxml, qrcode, segno, weasyprint, jinja2, schwifty, openpyxl

---

**Erstellt von:** Manus AI  
**Datum:** 2025-12-17
