# Webisco Auftragsimport - Machbarkeitsstudie

**Datum:** 17.12.2025  
**Projekt:** Swiss21 - Abisco zu ABA Ninja Migration  
**Thema:** Theoretische Analyse: Aufträge über Webisco-Schnittstelle in Abisco reimportieren

---

## 🎯 Ziel

Prüfen, ob die 116 bestehenden Aufträge aus der Abisco-Datenbank über die **Webisco-Schnittstelle** neu in Abisco angelegt werden können - als Vorbereitung für den Export nach ABA Ninja.

---

## ✅ Erkenntnisse

### 1. **Webisco unterstützt Auftragserstellung**

**Ressource:** `createauftrag`  
**Endpunkt:** `POST http://www.webisco.de:8228/createauftrag`  
**Format:** XML über HTTP-POST  
**Protokoll-Version:** 55 (Abisco 8.8.23)

**Auftragstypen:**
- `anfrage` - Anfrage
- `bestellung` - Bestellung ✅ **Empfohlen**
- `streckenbestellung` - Streckenbestellung (nur mit Admin-ID)
- `multiplexer` - Für Lieferantensysteme

---

### 2. **Zugangsdaten vorhanden**

**Authentifizierung erfolgt über:**
- `username` = Kundennummer
- `password` = Kundenpasswort

**Konkrete Zugangsdaten:**

| Kundennummer | Firmenname | Username | Password | Aufträge |
|--------------|------------|----------|----------|----------|
| 10000 | MT Transport GmbH | 10000 | aachen5446 | 2 |
| 10001 | Sinanovic Garage | 10001 | sales123 | 2 |
| 10002 | Truck Center Regensdorf AG | 10002 | sales123 | 1 |
| 10003 | Endkunde | 10003 | sales123 | 8 |
| 10004 | AB Automobile | 10004 | sales123 | 1 |
| 10005 | Eko Performance | 10005 | sales123 | 1 |
| 10006 | Hüseyin Kuzu | 10006 | sales123 | 1 |
| 10007 | Car Lounge 83 GmbH | 10007 | sales123 | 1 |
| 10009 | TESTKUNDE | 10009 | sales123 | 1 |
| 10010 | Barverkauf Twindt | 10010 | sales123 | 1 |
| 10011 | yannick schwart | 10011 | sales123 | 1 |
| 10012 | dvse468 | 10012 | sales123 | 1 |
| 10014 | sales | 10014 | sales123 | 1 |
| 10015 | DIAMAS Group AG | 10015 | sales123 | 87 |
| 10016 | Norline AG | 10016 | sales123 | 1 |
| 10017 | AVS Garage AG | 10017 | sales123 | 5 |
| 10022 | ISTANBUL GARAGE | 10022 | sales123 | 1 |

**Gesamt:** 17 Kunden mit 116 Aufträgen

---

### 3. **XML-Struktur für createauftrag**

#### Envelope (Authentifizierung)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="21" username="10000" password="aachen5446" type="request">
  <content>
    <!-- Auftrag hier -->
  </content>
</webisco>
```

#### Auftragskopf (`<auftrag>`)

**Pflichtfelder:**
- `typ` - Auftragstyp (z.B. "bestellung")

**Optionale Felder:**
- `bemerkung` - Freitext
- `bestellername` - Name für Rückfragen
- `bestellnummer` - Bestellnummer des Kunden
- `wunschlieferdatum` - Gewünschtes Lieferdatum (#DATUM: YYYY-MM-DD)
- `wunschfilialid` - Filiale (#ZAHL)
- `referer` - Internet-Service URL (#TEXT) ⚠️ **WICHTIG!**
- `belegrabatt` - Endrabatt (#PROZENT)
- `versandadressdaten` - Versandadresse (#TEXT)

#### Artikelposition (`<position>`)

**Pflichtfelder:**
- `artikelid` - Die interne Artikel-ID von Abisco (#ZAHL) ✅ **MUSS aus DB kommen!**

**Optionale Felder:**
- `menge` - Menge (#MENGE, max 2 Nachkommastellen)
- `mwst` - Mehrwertsteuersatz (#PROZENT)
- `einzelpreis_netto` - Nettopreis (#PREIS)
- `einzelpreis_brutto` - Bruttopreis (#PREIS)
- `listenpreis` - Listenpreis ohne MwSt (#PREIS)
- `beschreibung` - Artikelbeschreibung (#TEXT)
- `bemerkung` - Positionsbemerkung (#TEXT)

---

## 📋 Beispiel: Auftrag 2 (Kunde 10000)

### Basisdaten

```
Auftragsnummer: 2
Kundennummer: 10000 (MT Transport GmbH)
Datum: 2025-09-08
Betrag Netto: CHF 176.92
Betrag Brutto: CHF 191.25
Status: 26 (Abgeschlossen)
```

### XML-Anfrage (theoretisch)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="21" username="10000" password="aachen5446" type="request">
  <content>
    <auftrag typ="bestellung">
      <bestellername>MT Transport GmbH</bestellername>
      <bestellnummer>REIMPORT-AUFTRAG-2</bestellnummer>
      <wunschlieferdatum>2025-09-08</wunschlieferdatum>
      <wunschfilialid>1</wunschfilialid>
      <bemerkung>Reimport von Auftrag 2 aus Abisco-Datenbank für Migration zu ABA Ninja</bemerkung>
      <referer>http://abisco-migration.swiss21.local</referer>
      
      <!-- ARTIKELPOSITIONEN FEHLEN NOCH -->
      <!-- Müssen aus verkaufspositionen-Tabelle extrahiert werden -->
      
      <position>
        <artikelid>ARTIKEL_ID_HIER</artikelid>
        <menge>1.00</menge>
        <einzelpreis_netto>176.92</einzelpreis_netto>
        <einzelpreis_brutto>191.25</einzelpreis_brutto>
        <listenpreis>158.97</listenpreis>
        <mwst>8.1</mwst>
        <beschreibung>Artikelbeschreibung aus DB</beschreibung>
      </position>
      
    </auftrag>
  </content>
</webisco>
```

### HTTP-Request

```
POST /createauftrag HTTP/1.1
Host: www.webisco.de:8228
Connection: Keep-Alive
Content-Type: text/xml; charset=UTF-8
Content-Length: [Länge des XML]

[XML-Inhalt hier]
```

---

## ⚠️ Offene Fragen & Herausforderungen

### 1. **Artikelpositionen fehlen**

**Problem:** Die genaue Datenbank-Struktur für Artikelpositionen ist komplex.

**Lösung:** SQL-Query muss entwickelt werden, um:
- `artikelid` (Pflicht!)
- `herstellernummer`
- `beschreibung`
- `menge`
- `einzelpreis` (netto/brutto)
- `listenpreis`
- `mwst`
- `bemerkung`

aus der `verkaufspositionen`-Tabelle zu extrahieren.

### 2. **Datentyp-Konvertierung**

**Problem:** Abisco speichert Preise als Integer (Cent), Webisco erwartet Decimal (Euro).

**Beispiel:**
- DB: `17692` → Webisco: `176.92`
- DB: `19125` → Webisco: `191.25`

**Lösung:** Division durch 100 bei der Extraktion.

### 3. **Duplikate vermeiden**

**Problem:** Wenn Aufträge über Webisco neu angelegt werden, entstehen **neue** Aufträge in Abisco!

**Risiko:**
- ❌ Doppelte Aufträge
- ❌ Falsche Auftragsnummern
- ❌ Verwirrung im System

**Empfehlung:** 
- ⚠️ **NICHT für Reimport in Abisco verwenden!**
- ✅ **Nur für neue Web-Bestellungen gedacht!**

### 4. **Lizenzrechtlicher Hinweis**

Aus der Webisco-Dokumentation (Seite 2):

> "Die Webisco-Schnittstelle darf ausschließlich für Client-Implementierungen verwendet werden. Eine Implementierung als Server oder Dienst ist ausdrücklich untersagt und wird als Markenverletzung angesehen."

**Interpretation:**
- ✅ OK: Kunden bestellen über Webshop
- ❌ NICHT OK: Automatisierter Server-zu-Server Import
- ⚠️ **Mit Admin-ID möglicherweise erlaubt** (unklar)

---

## 🎯 Empfehlung

### ❌ **NICHT empfohlen: Webisco für Reimport**

**Gründe:**
1. Webisco ist für **neue Bestellungen** gedacht, nicht für Datenmigrationen
2. Es würden **neue Aufträge** entstehen, nicht die alten aktualisiert
3. Lizenzrechtlich fragwürdig
4. Komplex und fehleranfällig

### ✅ **Empfohlen: Direkter Export nach ABA Ninja**

**Besserer Weg:**
1. Aufträge **direkt aus Abisco-Datenbank** lesen
2. Über **ABA Ninja API** importieren:
   - `POST /documents/v2/quotes` (Angebote)
   - `POST /documents/v2/contract_notes` (Auftragsbestätigungen)
3. Kein Umweg über Webisco
4. Keine Duplikate
5. Saubere Migration

---

## 📊 Zusammenfassung

| Kriterium | Webisco-Reimport | Direkter ABA Ninja Import |
|-----------|------------------|---------------------------|
| **Technisch möglich** | ✅ Ja | ✅ Ja |
| **Zugangsdaten vorhanden** | ✅ Ja | ✅ Ja (API-Token) |
| **Duplikate** | ❌ Risiko hoch | ✅ Keine |
| **Lizenzkonform** | ⚠️ Unklar | ✅ Ja |
| **Komplexität** | 🔴 Hoch | 🟢 Mittel |
| **Empfehlung** | ❌ Nicht empfohlen | ✅ **Empfohlen** |

---

## 🚀 Nächste Schritte (falls gewünscht)

Falls du trotzdem Webisco testen möchtest:

1. **SQL-Query entwickeln** für Artikelpositionen
2. **Python-Skript erstellen** für XML-Generierung
3. **Test mit Auftrag 2** durchführen
4. **Ergebnis prüfen** in Abisco
5. **Bei Erfolg:** Weitere Aufträge importieren

**Aber:** Ich empfehle den direkten Weg über ABA Ninja API! 🎯

---

**Status:** ✅ Machbarkeitsstudie abgeschlossen  
**Ergebnis:** Technisch möglich, aber nicht empfohlen  
**Empfehlung:** Direkter Import in ABA Ninja
