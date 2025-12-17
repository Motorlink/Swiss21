# Testrechnung-Analyse: MT Transport GmbH

**Datum**: 17. Dezember 2024  
**Quelle**: Abisco via Webisco-Schnittstelle  
**Status**: ✅ **ERFOLGREICH ABGERUFEN!**

---

## 🎉 Erfolg! Rechnung gefunden

Die Testrechnung wurde erfolgreich von Abisco abgerufen. Hier ist die **vollständige Datenstruktur**:

---

## 📊 Rechnungs-Stammdaten

| Feld | Wert | Beschreibung |
|---|---|---|
| **Belegnummer** | `RE1` | Rechnungsnummer |
| **Belegdatum** | `2025-12-17` | Rechnungsdatum |
| **Fälligkeitsdatum** | `2025-12-17` | Zahlungsfrist |
| **Erstellt** | `2025-12-17 12:06:13` | Erstellzeitpunkt |
| **Typ** | `rechnung` | Belegtyp |
| **Status** | `verrechnet` | Rechnungsstatus |
| **ID** | `1` | Interne Beleg-ID |

### **Preise**
| Feld | Wert |
|---|---|
| **Endpreis netto** | `24,12 EUR` |
| **Endpreis brutto** | `25,26 EUR` |
| **Komplett bezahlt** | `F` (Nein) |

### **Zahlungsinformationen**
| Feld | Wert | Anmerkung |
|---|---|---|
| **Zahlungsart** | `0` | Nicht definiert |
| **Fälligkeitsdatum** | `2025-12-17` | ⚠️ Heute! (sehr kurze Frist) |
| **Skonto** | - | Nicht angegeben |
| **Skontodatum** | - | Nicht angegeben |

---

## 👤 Kundendaten

### **MT Transport GmbH**

| Feld | Wert |
|---|---|
| **Kundennummer** | `10000` ✅ |
| **Firmenname** | `MT Transport GmbH` |
| **Anrede** | `Firma` |
| **Straße** | `Lorenweg 22` |
| **PLZ** | `8610` |
| **Ort** | `Uster` |
| **Land** | `DEU` (Deutschland) |
| **E-Mail** | `info@mt-transport.ch` ✅ |
| **Telefon** | *(leer)* |

**Wichtig**: E-Mail-Adresse ist vorhanden → Rechnungsversand möglich!

---

## 🔗 Beziehung zum Auftrag

### **Belegverlauf** ⭐

Die Rechnung hat einen vollständigen Belegverlauf:

1. **Auftrag** (ID: 1, Typ: `auftrag`)
2. **Rechnung** (ID: 1, Typ: `rechnung`)

**Auftragsnummer**: `A1` (in den Positionen referenziert)

---

## 📦 Rechnungspositionen

### **Position 1: Ölfilter**

| Feld | Wert |
|---|---|
| **Artikelnummer** | `HU7020Z` |
| **Beschreibung** | `Ölfilter` |
| **Hersteller** | `Mann & Hummel` |
| **Herstellernummer** | `HU 7020 z` |
| **Menge** | `1` |
| **Einzelpreis netto** | `14,12 EUR` |
| **Einzelpreis brutto** | `15,26 EUR` |
| **Positionspreis netto** | `14,12 EUR` |
| **Positionspreis brutto** | `15,26 EUR` |
| **MwSt** | `8,1%` |
| **Lieferdatum** | `2025-12-17` |
| **Status** | `geliefert` |
| **Skontierbarkeit** | `100%` |
| **Auftragsnummer** | `A1` ✅ |
| **Rechnungsnummer** | `RE1` |

**Zusätzliche Eigenschaften**:
- Paketfähig: Ja
- Sperrgut: Nein
- Gefahrgut: Nein
- Einzelgewicht: 80g

### **Position 2: Zustellpauschale**

| Feld | Wert |
|---|---|
| **Beschreibung** | `Zustellpauschale` |
| **Typ** | `zustellung` |
| **Menge** | `1` |
| **Einzelpreis netto** | `10,00 EUR` |
| **Einzelpreis brutto** | `10,00 EUR` |
| **Positionspreis netto** | `10,00 EUR` |
| **Positionspreis brutto** | `10,00 EUR` |
| **MwSt** | `0%` |
| **Lieferdatum** | `2025-12-17` |
| **Status** | `geliefert` |
| **Skontierbarkeit** | `0%` (nicht skontierbar) |
| **Auftragsnummer** | `A1` ✅ |
| **Rechnungsnummer** | `RE1` |

---

## ✅ Was funktioniert

### **Vollständig vorhanden**:
- ✅ Rechnungsnummer (`RE1`)
- ✅ Rechnungsdatum (`2025-12-17`)
- ✅ **Auftragsnummer** (`A1`) - in Positionen
- ✅ **Belegverlauf** (Auftrag → Rechnung)
- ✅ Kundennummer (`10000`)
- ✅ **E-Mail-Adresse** (`info@mt-transport.ch`)
- ✅ Vollständige Adresse
- ✅ Alle Positionen mit Details
- ✅ MwSt-Sätze (8,1% und 0%)
- ✅ Preise (netto, brutto)
- ✅ Fälligkeitsdatum

---

## ⚠️ Was fehlt oder auffällig ist

### **Fehlende Daten**:
- ❌ **Skonto** - Nicht angegeben (Felder leer)
- ❌ **Skontodatum** - Nicht angegeben
- ❌ **Telefonnummer** - Leer
- ❌ **Bestellnummer** - Leer
- ❌ **Mitarbeiter** - Leer
- ❌ **Rechnungsnummer** (als separates Feld) - Leer (nur `belegnummer="RE1"`)

### **Auffälligkeiten**:
- ⚠️ **Land**: `DEU` (Deutschland), aber E-Mail `.ch` (Schweiz) und Ort `Uster` (Schweiz)
- ⚠️ **Fälligkeitsdatum** = Rechnungsdatum (keine Zahlungsfrist!)
- ⚠️ **Währung**: Wahrscheinlich EUR (wegen Land DEU), aber nicht explizit angegeben

---

## 🚀 Was Swiss21 damit machen kann

### **1. Rechnung in ABA Ninja erstellen**

```python
{
  "invoice_number": "RE1",
  "invoice_date": "2025-12-17",
  "due_date": "2025-12-17",
  "reference": "A1",  # Auftragsnummer
  "customer": {
    "customer_number": "10000",
    "company_name": "MT Transport GmbH",
    "street": "Lorenweg 22",
    "zip": "8610",
    "city": "Uster",
    "country": "DE",
    "email": "info@mt-transport.ch"
  },
  "line_items": [
    {
      "description": "Ölfilter",
      "article_number": "HU7020Z",
      "quantity": 1,
      "unit_price": 14.12,
      "vat_rate": 8.1,
      "total": 15.26
    },
    {
      "description": "Zustellpauschale",
      "quantity": 1,
      "unit_price": 10.00,
      "vat_rate": 0,
      "total": 10.00
    }
  ],
  "total_net": 24.12,
  "total_gross": 25.26
}
```

### **2. QR-Code generieren**

- **Betrag**: 25,26 EUR (oder CHF?)
- **Referenz**: RE1 oder A1
- **IBAN**: (aus Konfiguration)

### **3. E-Mail versenden**

- **An**: info@mt-transport.ch
- **Betreff**: "Rechnung RE1 - MT Transport GmbH"
- **Anhang**: PDF mit QR-Code
- **Text**: "Fällig bis: 17.12.2025" (⚠️ heute!)

---

## 📝 Erkenntnisse für Integration

### **Funktioniert**:
1. ✅ Datenabfrage via `beleganfrage` funktioniert
2. ✅ Alle wichtigen Daten sind vorhanden
3. ✅ Auftragsnummer ist in Positionen enthalten
4. ✅ Belegverlauf zeigt Auftrag → Rechnung
5. ✅ E-Mail-Adresse für Versand vorhanden

### **Zu beachten**:
1. ⚠️ **Jahr 2025** - Nicht 2024!
2. ⚠️ **Skonto fehlt** - Muss in Abisco konfiguriert werden?
3. ⚠️ **Fälligkeitsdatum** = Rechnungsdatum - Unrealistisch kurz
4. ⚠️ **Währung** - Muss geklärt werden (EUR oder CHF?)
5. ⚠️ **Land-Inkonsistenz** - DEU vs. Schweiz

### **Nächste Schritte**:
1. ✅ **Datenstruktur ist klar** - Integration kann beginnen
2. 🔧 **Zahlungsbedingungen in Abisco prüfen** - Skonto, Fälligkeitsfrist
3. 🔧 **Währung klären** - EUR oder CHF?
4. 🔧 **Land korrigieren** - Schweiz statt Deutschland?

---

## 🎯 Fazit

**Die Testrechnung wurde erfolgreich abgerufen!** 🎉

Alle **essentiellen Daten** sind vorhanden:
- Rechnungsnummer, Datum, Kunde, Positionen, Preise, E-Mail

Die **Integration ist machbar** und kann jetzt implementiert werden!

**Einzige Anpassungen nötig**:
- Zahlungsbedingungen in Abisco konfigurieren (Skonto, Fälligkeitsfrist)
- Währung klären
- Ggf. Kundendaten korrigieren (Land)
