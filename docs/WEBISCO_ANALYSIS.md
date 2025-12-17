# Webisco-Schnittstellenanalyse für Abisco Integration

## Übersicht

**Webisco** ist die XML-basierte HTTP-Schnittstelle für das Abisco Warenwirtschaftssystem. Die Schnittstelle ermöglicht die Kommunikation mit Abisco über Port 8228 mittels HTTP-POST.

**Protokoll-Version**: 55  
**Abisco-Version**: ab 8.8.23  
**Stand**: 24.10.2025

## Wichtiger Lizenzhinweis

⚠️ Die Webisco-Schnittstelle darf **ausschließlich für Client-Implementierungen** verwendet werden. Eine Implementierung als Server oder Dienst ist ausdrücklich untersagt und wird als Markenverletzung angesehen. Für die Implementierung auf Server-Seite ist die Schnittstelle **"Abisco-Connect"** vorgesehen.

## Kommunikation mit dem Webisco-Daemon

### Verbindungsdetails

- **Port**: 8228
- **Protokoll**: HTTP-POST
- **Format**: XML mit UTF-8 Encoding
- **Content-Type**: text/html; charset="utf-8"

### Verfügbare Ressourcen

| Ressource | Beschreibung |
|-----------|--------------|
| `config` | Liefert kundenspezifische Grundkonfigurationen |
| `artikelanfrage` | Liefert Artikel nach bestimmten Suchkriterien |
| `beleganfrage` | Liefert existierende Kundenbelege |
| `belegbemerkung` | Fügt eine Bemerkung zu einem bestehenden Beleg hinzu |
| `createauftrag` | **Erzeugt einen Auftrag in Abisco** |
| `createkunde` | Erzeugt einen neuen Kunden in Abisco |
| `kundensuche` | Liefert Kundendaten anhand von Suchmustern |
| `positionsanfrage` | Liefert existierende Positionen für eventuelle Rückgaben |
| `removeauftrag` | Löscht einen bestehenden Auftrag |
| `tourfahrtanfrage` | Liefert die nächsten Tourfahrten für einen Kunden |
| `updatekunde` | Ändert die Daten eines existierenden Kunden |
| `zahlung` | Fügt eine Anzahlung zu einem Auftrag hinzu |
| `zugangsdaten` | Sendet dem Kunden seine Zugangsdaten |

## Webisco-Envelope Struktur

Alle Anfragen und Antworten verwenden einen standardisierten Envelope:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="21" username="testuser" password="geheim" type="request">
  <content>
    [...Anfrage-Daten...]
  </content>
</webisco>
```

### Envelope-Attribute

| Attribut | Typ | Pflicht | Bedeutung |
|----------|-----|---------|-----------|
| `version` | #ZAHL | ✓ | Die Versionsnummer des Protokolls |
| `adminid` | #TEXT | | Eine von Abisco vergebene eindeutige ID |
| `username` | #TEXT | ✓ | Der Benutzername (oder Kundennummer) des Kunden |
| `password` | #TEXT | ✓ | Das Passwort des Kunden |
| `type` | #ENUM | ✓ | "request" bei Anfragen des Clients, "response" bei Antworten vom Server |
| `errormessage` | #TEXT | | Wird vom Server bei Bedarf mit einer Fehlermeldung belegt |

## Datentypen

| Datentyp | Beschreibung |
|----------|--------------|
| `#TEXT` | Zeichenfolge beliebiger Länge |
| `#ZAHL` | Ganzzahl (Integer) |
| `#GKZ` | Gleitkommazahl (Double), Komma als Dezimaltrennzeichen |
| `#PREIS` | Preis in Euro, Komma als Dezimaltrennzeichen |
| `#PROZENT` | Prozentzahl mit maximal zwei Nachkommastellen, Komma als Dezimaltrennzeichen |
| `#MENGE` | Menge mit maximal zwei Nachkommastellen, Komma als Dezimaltrennzeichen |
| `#BOOL` | Wahrheitswert ("T" = True, "F" = False) |
| `#DATUM` | Datum in der Form "YYYY-MM-DD" |
| `#ZEIT` | Zeitangabe in der Form "HH:MM:SS" |
| `#DATUMZEIT` | Zeitstempel in der Form "YYYY-MM-DD HH:MM:SS" |
| `#ENUM` | Ein Aufzählungstyp vom Typ #TEXT |

## Auftragserstellung (createauftrag)

### Auftragstypen

- `anfrage` - Anfrage
- `bestellung` - Bestellung
- `streckenbestellung` - Streckenbestellung (nur mit Admin-ID)
- `multiplexer` - Für transparente Weiterleitungen an Lieferantensysteme

### Auftrags-XML-Struktur

```xml
<auftrag>
  <typ>#TEXT</typ>
  <bemerkung>#TEXT</bemerkung>
  <ersatzartikel>#BOOL</ersatzartikel>
  <bestellername>#TEXT</bestellername>
  <bestellnummer>#TEXT</bestellnummer>
  <wunschlieferdatum>#DATUM</wunschlieferdatum>
  <wunschfilialid>#ZAHL</wunschfilialid>
  <versandadressdaten>#TEXT</versandadressdaten>
  <belegrabatt>#PROZENT</belegrabatt>
  <belegrabattname>#TEXT</belegrabattname>
  <kommission>#TEXT</kommission>
  <kostenstelle>#TEXT</kostenstelle>
  <multiplexerlieferantid>#ZAHL</multiplexerlieferantid>
  <referer>#TEXT</referer>
  <refererinfo>#TEXT</refererinfo>
  <auslandsmwst>#BOOL</auslandsmwst>
  <positionsids>#TEXT</positionsids>
  
  <position>...</position>
  <zustellgebuehr>...</zustellgebuehr>
  <sonderkosten>...</sonderkosten>
  <tourfahrt>...</tourfahrt>
  <zahlungsart>...</zahlungsart>
  <gutschein>...</gutschein>
  <rechnungsadresse>...</rechnungsadresse>
  <lieferadresse>...</lieferadresse>
</auftrag>
```

### Position-Struktur

```xml
<position>
  <id>#ZAHL</id>
  <artikelid>#ZAHL</artikelid>
  <menge>#MENGE</menge>
  <mwst>#PROZENT</mwst>
  <einzelpreis_netto>#PREIS</einzelpreis_netto>
  <einzelpreis_brutto>#PREIS</einzelpreis_brutto>
  <listenpreis>#PREIS</listenpreis>
  <beschreibung>#TEXT</beschreibung>
  <zusatztext>#TEXT</zusatztext>
  <bemerkung>#TEXT</bemerkung>
  <quellbelegnummer>#TEXT</quellbelegnummer>
</position>
```

### Wichtige Felder für Rechnungserstellung

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `typ` | #TEXT | "bestellung" für Rechnungen |
| `referer` | #TEXT | **Wichtig**: Internet-Service der den Auftrag initiiert (z.B. "http://www.plattformname.com"). Der Referer ist wichtig, wenn die Bestellungen ihrer Plattform später als solche für eine weitere Verarbeitung identifiziert werden können sollen. |
| `rechnungsadresse` | | Rechnungsadresse des Auftrags |
| `lieferadresse` | | Lieferadresse des Auftrags |
| `zahlungsart` | | Zahlungsart des Auftrags (nur eine pro Auftrag möglich) |

### Rechnungsadresse / Lieferadresse

```xml
<rechnungsadresse> oder <lieferadresse>
  <anrede>#TEXT</anrede>
  <vorname>#TEXT</vorname>
  <name>#TEXT</name>
  <zusatz>#TEXT</zusatz>
  <strasse>#TEXT</strasse>
  <plz>#TEXT</plz>
  <ort>#TEXT</ort>
  <land>#ENUM</land>
  <telefon>#TEXT</telefon>
  <telefax>#TEXT</telefax>
  <email>#TEXT</email>
  <lieferanrede>#TEXT</lieferanrede>
  <ustidnr>#TEXT</ustidnr>
  <steuernummer>#TEXT</steuernummer>
</rechnungsadresse>
```

**Wichtig**: Die E-Mail-Adresse muss eine gültige E-Mail-Adresse sein und **keine sonstigen Zeichen** enthalten.

## Kundenverwaltung

### Kunde anlegen (createkunde)

```xml
<kunde>
  <login>#TEXT</login>
  <password>#TEXT</password>
  <endverbraucher>#BOOL</endverbraucher>
  <kundengruppe>#TEXT</kundengruppe>
  <steuerfrei>#BOOL</steuerfrei>
  <preisrundung>#BOOL</preisrundung>
  <zahlungsbedingung>#ZAHL</zahlungsbedingung>
  
  <rechnungsadresse>...</rechnungsadresse>
  <lieferadresse>...</lieferadresse>
</kunde>
```

### Kunde aktualisieren (updatekunde)

Um ein bereits angelegtes Kundenkonto zu ändern, muss im Envelope entweder der entsprechende Benutzername und das alte Kennwort oder die Admin-ID des Webisco-Dienstes übergeben werden. Im Content muss sich ein Kunden-XML befinden, das die neuen Daten beinhaltet. Der Login kann nachträglich nicht wieder geändert werden.

**HTTP-Header**: Ressource `updatekunde`

## Relevante Informationen für Swiss21 Integration

### 1. Auftragserstellung in Abisco

- Ressource: `createauftrag`
- Auftragstyp: `bestellung`
- Erforderliche Daten:
  - Kundendaten (Login/Passwort oder Admin-ID)
  - Rechnungsadresse mit gültiger E-Mail
  - Positionen mit Artikeln
  - Zahlungsart
  - Referer (Plattform-Identifikation)

### 2. Datenfluss

```
Abisco (Rechnung erstellen) 
  → Webisco createauftrag (XML über HTTP-POST Port 8228)
  → Swiss21 (Daten empfangen)
  → ABA Ninja API (Rechnung in ABA Ninja erstellen)
  → QR-Code generieren
  → E-Mail mit Rechnung + QR-Code + Twint-Link versenden
```

### 3. Wichtige Hinweise

- **Admin-ID**: Für die Integration sollte eine Admin-ID verwendet werden, um Kundenpasswörter nicht prüfen zu müssen
- **Referer**: Muss gesetzt werden, um Bestellungen der Plattform später identifizieren zu können
- **E-Mail-Validierung**: Die E-Mail-Adresse muss gültig sein und keine Sonderzeichen enthalten
- **Encoding**: Alle XML-Dokumente müssen UTF-8 encoding verwenden

### 4. Unterstützte Dateiformate

Laut Dokumentation unterstützt Abisco über Webisco:
- **XML** (Hauptformat für alle Anfragen/Antworten)
- **Text-basierte Daten** (#TEXT, #ZAHL, #PREIS, etc.)

Für Rechnungs-PDFs und QR-Codes müssen diese separat generiert werden (nicht Teil der Webisco-Schnittstelle).
