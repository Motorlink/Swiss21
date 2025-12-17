# Abisco → Swiss21: Verfügbare Rechnungsdaten

**Datum**: 17. Dezember 2024  
**Quelle**: Webisco-Schnittstellenbeschreibung Version 55  
**Zweck**: Übersicht aller Daten, die von Abisco an Swiss21 übertragen werden können

---

## 📋 Workflow-Klarstellung

### Prozess
1. **Rechnung in Abisco erstellen** (jeden Freitag)
2. **Abisco sendet Rechnungsdaten** automatisch an Swiss21
3. **Swiss21 empfängt Daten** und erstellt Rechnung in ABA Ninja
4. **Swiss21 generiert PDF + QR-Code** und versendet per E-Mail

---

## 🔄 Zwei Methoden zum Datenabruf

### **Methode 1: PUSH (Empfohlen für "sofort")**
- **Ressource**: `createauftrag` (mit `typ=rechnung`)
- **Trigger**: Abisco sendet automatisch nach Rechnungserstellung
- **Vorteil**: Sofortige Übertragung

### **Methode 2: PULL (Empfohlen für "jeden Freitag")**
- **Ressource**: `beleganfrage` (mit `typ=rechnung`)
- **Trigger**: Swiss21 fragt jeden Freitag ab
- **Vorteil**: Kontrollierter Zeitpunkt

---

## 📊 Verfügbare Rechnungsdaten

### **1. Beleg-Stammdaten** (aus `<beleg>`-Tag)

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **typ** | TEXT | Belegtyp | `rechnung` |
| **id** | ZAHL | Belegnummer ohne Präfix | `12345` |
| **belegnummer** | TEXT | Vollständige Belegnummer | `RE-2024-12345` |
| **belegdatum** | DATUM | Rechnungsdatum | `2024-12-15` |
| **rechnungsnummer** | ZAHL | Rechnungsnummer | `12345` |
| **faelligkeitsdatum** | DATUM | **Zahlungsfrist** | `2025-01-15` |
| **kundennummer** | ZAHL | Kundennummer | `10000` |
| **mitarbeiter** | TEXT | Bearbeiter der Rechnung | `Max Mustermann` |
| **erstellt** | DATUMZEIT | Erstellzeitpunkt | `2024-12-15 10:30:00` |
| **auftragsnummer** | TEXT | **Zugehörige Auftragsnummer** | `AUF-2024-001` |

### **2. Preise und Beträge**

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **endpreis_netto** | PREIS | Gesamtpreis ohne MwSt. | `1000.00` |
| **endpreis_brutto** | PREIS | Gesamtpreis inkl. MwSt. | `1077.00` |
| **skonto** | PROZENT | **Skonto in %** | `2.00` |
| **skonto_effektiv** | PROZENT | Effektiver Skonto | `2.00` |
| **skontodatum** | DATUM | **Skonto-Frist** | `2024-12-25` |

### **3. Beziehung zum Auftrag** ⭐

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **auftragsnummer** | TEXT | **Auftragsnummer** (aus der die Rechnung erstellt wurde) | `AUF-2024-001` |

**Wichtig**: Über die Auftragsnummer kann die vollständige Auftragshistorie nachvollzogen werden:
- Wann wurde der Auftrag erstellt?
- Welche Positionen waren ursprünglich im Auftrag?
- Gibt es Änderungen zwischen Auftrag und Rechnung?

### **4. Zahlungsinformationen**

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **bezahlt** | PREIS | Bereits bezahlter Betrag | `0.00` |
| **komplett_bezahlt** | BOOL | Ob vollständig bezahlt | `false` |
| **komplett_bezahlt_datum** | DATUM | Zahlungsdatum | - |

### **5. Status**

| Feld | Typ | Beschreibung | Mögliche Werte |
|---|---|---|---|
| **status** | TEXT | Rechnungsstatus | `aktiv`, `gelöscht`, `storniert`, `verrechnet` |
| **verrechnet** | BOOL | Ob in Rechnungsbeleg | `false` |

### **6. Kundendaten** (aus `<rechnungsadresse>`-Tag)

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **firma** | TEXT | Firmenname | `Musterfirma GmbH` |
| **anrede** | TEXT | Anrede | `Herr` / `Frau` |
| **vorname** | TEXT | Vorname | `Max` |
| **nachname** | TEXT | Nachname | `Mustermann` |
| **strasse** | TEXT | Straße | `Musterstraße 123` |
| **plz** | TEXT | Postleitzahl | `8000` |
| **ort** | TEXT | Ort | `Zürich` |
| **land** | TEXT | Land | `Schweiz` / `CH` |
| **email** | TEXT | **E-Mail-Adresse** | `max@musterfirma.ch` |
| **telefon** | TEXT | Telefonnummer | `+41 44 123 45 67` |

### **7. Rechnungspositionen** (aus `<position>`-Tags)

Jede Rechnung kann **mehrere Positionen** enthalten:

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **artikelid** | ZAHL | Interne Artikel-ID | `5001` |
| **artikelnummer** | TEXT | Artikelnummer | `ART-001` |
| **beschreibung** | TEXT | Positionsbeschreibung | `Webdesign Paket Premium` |
| **menge** | MENGE | Anzahl | `1.00` |
| **mwst** | PROZENT | **MwSt-Satz** | `7.70` |
| **einzelpreis_netto** | PREIS | Einzelpreis ohne MwSt. | `1000.00` |
| **einzelpreis_brutto** | PREIS | Einzelpreis inkl. MwSt. | `1077.00` |
| **positionspreis_netto** | PREIS | Gesamtpreis Position (netto) | `1000.00` |
| **positionspreis_brutto** | PREIS | Gesamtpreis Position (brutto) | `1077.00` |
| **skontierbarkeit** | PROZENT | **Skonto-Fähigkeit** | `100.00` |

### **8. Zusätzliche Informationen**

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **bestellnummer** | TEXT | Kundenbestellnummer | `BEST-2024-001` |
| **bestellername** | TEXT | Name des Bestellers | `Max Mustermann` |
| **kommission** | TEXT | Kommission (bei Aufträgen) | - |
| **kostenstelle** | TEXT | Kostenstelle (bei Aufträgen) | - |
| **tour** | TEXT | Tour-Information | - |

### **9. Bemerkungen**

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **bemerkung** | TEXT | Interne Bemerkung | `Wichtiger Kunde` |
| **text** | TEXT | Bemerkungstext | `Bitte pünktlich liefern` |

### **10. PDF und Anhänge**

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| **pdf** | BOOL | Ob PDF mitgeliefert werden soll | `true` |
| **pdf** (Inhalt) | BASE64 | **PDF als Base64** | `JVBERi0xLjQK...` |

---

## ✅ Was Swiss21 ERHÄLT

### **Vollständige Rechnungsdaten**
- ✅ **Rechnungsnummer** und **Datum**
- ✅ **Auftragsnummer** (Verknüpfung zum ursprünglichen Auftrag)
- ✅ **Kundendaten** (Name, Adresse, E-Mail, Telefon)
- ✅ **Alle Positionen** mit Beschreibung, Menge, Preisen
- ✅ **MwSt-Sätze** pro Position
- ✅ **Gesamtbeträge** (netto, brutto)
- ✅ **Zahlungsbedingungen**:
  - **Fälligkeitsdatum** (Zahlungsfrist)
  - **Skonto** (Prozentsatz)
  - **Skontodatum** (Skonto-Frist)
- ✅ **E-Mail-Adresse** für Versand
- ✅ **Optional**: PDF der Rechnung aus Abisco

---

## 🚀 Was Swiss21 DAMIT MACHT

### **1. Rechnung in ABA Ninja erstellen**
- Alle Rechnungsdaten übertragen
- Kunde anlegen (falls noch nicht vorhanden)
- Positionen übertragen
- MwSt korrekt zuordnen

### **2. QR-Code generieren (Swiss QR-Bill)**
- **QR-IBAN** (aus Konfiguration)
- **Betrag** (aus Rechnung)
- **Referenznummer** (aus Rechnungsnummer)
- **Zahlungsinformationen** (Fälligkeitsdatum)

### **3. PDF erstellen**
- Rechnung formatieren
- QR-Code einbetten
- Optional: Abisco-PDF verwenden

### **4. E-Mail versenden**
- **An**: Kunden-E-Mail aus Rechnung
- **Betreff**: "Rechnung RE-2024-12345"
- **Anhang**: PDF mit QR-Code
- **Link**: Twint-Direktzahlung
- **Text**: Zahlungsbedingungen (Fälligkeitsdatum, Skonto)

---

## 📅 Automatisierung: "Jeden Freitag"

### **Option A: Cron-Job auf Swiss21-Server**
```bash
# Jeden Freitag um 10:00 Uhr
0 10 * * 5 /opt/swiss21/app/Swiss21/scripts/fetch_invoices.sh
```

### **Option B: Scheduler in Swiss21-Anwendung**
- Python-Script mit `schedule` Bibliothek
- Läuft kontinuierlich und prüft jeden Freitag

### **Ablauf**
1. **Freitag 10:00 Uhr**: Swiss21 fragt Abisco ab
2. **Beleganfrage**: `typ=rechnung`, `von=letzter Freitag`, `bis=heute`
3. **Für jede neue Rechnung**:
   - Rechnung in ABA Ninja erstellen
   - QR-Code generieren
   - PDF erstellen
   - E-Mail versenden
4. **Log**: Alle verarbeiteten Rechnungen protokollieren

---

## ❓ Offene Fragen

1. **Zahlungsbedingungen-Text**: Gibt es einen speziellen Text für Zahlungsbedingungen in Abisco?
2. **Skonto-Handling**: Soll Skonto im QR-Code berücksichtigt werden?
3. **Twint-Integration**: Welcher Twint-Merchant-Account soll verwendet werden?
4. **E-Mail-Template**: Gibt es ein spezifisches E-Mail-Template?
5. **Zeitpunkt**: Genau um welche Uhrzeit am Freitag?

---

**Fazit**: Abisco liefert **ALLE** benötigten Daten für die vollständige Rechnungsverarbeitung, inklusive **Zahlungsbedingungen** (Fälligkeitsdatum, Skonto, Skontodatum)!
