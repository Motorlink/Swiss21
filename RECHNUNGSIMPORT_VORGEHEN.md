# Rechnungsimport-Vorgehen

## Datum
2025-12-17

## Ziel
Importiere alle 83 Rechnungen aus Abisco in ABA Ninja mit korrekter Kundenzuordnung.

---

## Problem & Lösung

### Problem
- Rechnungen in Abisco haben **keine Artikelpositionen**
- Nur Gesamtbeträge vorhanden
- Positionen sind bei **Aufträgen** gespeichert

### Lösung
- **Sammelposition** erstellen mit Gesamtbetrag
- **Beschreibung:** "Auftrag [Auftragsnummer]"
- Verknüpfung über Kundennummer

---

## Datenstruktur

### Rechnungen
- **Quelle:** `kundenrechnungen` Tabelle im Dump
- **Felder:**
  - `rechnungsnummer`: Eindeutige Rechnungsnummer
  - `kundennummer`: Zuordnung zum Kunden (z.B. 10000)
  - `rechnungsdatum`: Rechnungsdatum
  - `faelligkeit`: Fälligkeitsdatum
  - `betrag_netto`: Nettobetrag in CHF
  - `betrag_brutto`: Bruttobetrag in CHF
  - `bezahlt`: Bezahlter Betrag

### Aufträge
- **Quelle:** `kundenauftraege` Tabelle im Dump
- **116 Aufträge** gefunden
- Verknüpfung über `kundennummer`

### Positionen
- **Quelle:** `verkaufspositionen` Tabelle im Dump
- **Nur 1 Position** im gesamten Dump gefunden!
- Positionen sind unvollständig → **Sammelposition-Ansatz**

---

## Mapping: Abisco → ABA Ninja

### Kundenzuordnung
- **21 Kunden** mit UUID-Mapping
- **Mapping-Datei:** `/home/ubuntu/Swiss21/data/customer_uuid_mapping.json`

**Beispiel:**
```json
{
  "10000": {
    "uuid": "9841bb7e-df01-48af-80f1-9f8779ebe242",
    "name": "MT Transport GmbH",
    "company_name": "MT Transport GmbH"
  }
}
```

### Rechnungsstruktur für ABA Ninja

**API-Endpunkt:** `POST /accounts/{accountUuid}/documents/v2/invoices`

**Payload-Struktur:**
```json
{
  "address_uuid": "9841bb7e-df01-48af-80f1-9f8779ebe242",
  "invoice_number": "2",
  "invoice_date": "2025-09-08",
  "due_date": "2025-09-08",
  "positions": [
    {
      "type": "service",
      "description": "Auftrag 116",
      "quantity": 1,
      "unit_price": 191.25,
      "vat_rate": 8.1
    }
  ]
}
```

---

## Vorgehen

### Phase 1: Datenextraktion ✅
- [x] Rechnungen aus Dump extrahiert (83)
- [x] Aufträge aus Dump extrahiert (116)
- [x] Positionen aus Dump extrahiert (1)
- [x] Verknüpfung über Kundennummer

### Phase 2: Kundenzuordnung ✅
- [x] UUID-Mapping geladen
- [x] Kunde 10000 UUID ergänzt
- [x] 21 Kunden bereit

### Phase 3: Test-Import
- [ ] Rechnung 2 als Test importieren
- [ ] Validierung in ABA Ninja
- [ ] Fehlerbehandlung prüfen

### Phase 4: Vollständiger Import
- [ ] Alle 18 Rechnungen mit Positionen importieren
- [ ] Systematisch Rechnung für Rechnung
- [ ] Logging und Fehlerbehandlung

### Phase 5: Dokumentation
- [ ] Ergebnisse prüfen
- [ ] Import-Report erstellen
- [ ] GitHub commit

---

## Besonderheiten

### Sammelposition
- **Beschreibung:** "Auftrag [Auftragsnummer]"
- **Menge:** 1
- **Einzelpreis:** Gesamtbetrag der Rechnung
- **MwSt:** 8.1% (Standard CH)

### Rechnungen ohne Positionen
- **65 Rechnungen** haben keine Auftragspositionen
- Diese werden mit **generischer Sammelposition** importiert
- Beschreibung: "Sammelposition"

---

## Status
**Phase 2 abgeschlossen** - Bereit für Test-Import!
