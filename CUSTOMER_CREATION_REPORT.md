# Kundenerstellung in ABA Ninja - Vollständiger Bericht

**Datum:** 2025-12-17  
**Erstellt von:** AI Assistant  
**Projekt:** Swiss21 - Abisco zu ABA Ninja Migration

---

## 📊 Zusammenfassung

| Kategorie | Anzahl | Prozent |
|-----------|--------|---------|
| **Erfolgreich erstellt** | 20 | 66.7% |
| **Bereits vorhanden** | 10 | 33.3% |
| **Fehler** | 0 | 0% |
| **Gesamt** | 30 | 100% |

---

## ✅ Erfolgreich erstellte Kunden (20)

| Nr | Kundennummer | Name | UUID |
|----|--------------|------|------|
| 1 | 10002 | Truck Center Regensdorf AG | a456efed-e92d-4126-963c-bca4ac94479d |
| 2 | 10003 | Endkunde | 81bbb9c0-a2db-433c-a055-d3c2f181e6f5 |
| 3 | 10004 | AB Automobile | 544a6767-ec36-4341-8570-79d44ffd9a68 |
| 4 | 10005 | Eko Performance | c9c26c7a-4942-409e-9487-6a97c58ea527 |
| 5 | 10006 | Hüseyin Kuzu | 85d89bdb-37f0-4972-bf88-24300f77c8d3 |
| 6 | 10007 | Car Lounge 83 GmbH | 2e5d60a3-9e85-4972-9cfe-221928f149f0 |
| 7 | 10009 | TESTKUNDE | c662e9f8-01fd-41aa-a9ab-6bbc3a9c63f7 |
| 8 | 10010 | Barverkauf Twindt | 12381746-5c4e-41c9-a9ee-d98de5857f61 |
| 9 | 10014 | sales | eddc81ac-725b-4b69-9dcc-31a74e984424 |
| 10 | 10015 | DIAMAS Group AG | 6eebf8c1-f1a7-471d-94b3-d41da0dd1eaa |
| 11 | 10016 | Norline AG | 97427366-9973-48d2-ad1b-550c6b23a511 |
| 12 | 10017 | AVS Garage AG | 20246531-fc12-4980-8859-3483c73b2043 |
| 13 | 10018 | Bachmann Autospenglerei + Spritzwerk | bcab3377-51f1-43e1-8bcf-02d766214d63 |
| 14 | 10019 | Vogt Classic | c75ea3fe-30ff-4943-a2ee-d09ca0e3b040 |
| 15 | 10020 | Sport Garage Cotardo GmbH | 5e9160c3-6015-41c9-9639-7110cd73d9ca |
| 16 | 10021 | Harper's AG | 4d6e11e1-f7b1-4041-be5e-2c908207ac25 |
| 17 | 10022 | ISTANBUL GARAGE | fa3d693a-85ec-4893-9b1f-5e1be1dc1297 |
| 18 | 10024 | Carrosserie Bräm & Bajrami GmbH | bd4d9913-4794-47ad-a0ae-0d26687e961d |
| 19 | 10026 | CARROSSERIE ÖRLIKE TL AG | d637bf10-c0f4-4a55-8d6c-c0120fc945b6 |
| 20 | 10027 | Arifi Garage (eich-pfungen ag) | b460a760-1ac3-47a8-ac69-11cca8c28936 |

---

## ⚠️ Bereits vorhandene Kunden (10)

Diese Kunden existierten bereits in ABA Ninja (manuell angelegt oder aus Tests):

| Kundennummer | Name | Grund |
|--------------|------|-------|
| 10000 | MT Transport GmbH | Manuell angelegt |
| 10001 | Sinanovic Garage | Test-Erstellung |
| 10008 | senad testkunde | Bereits vorhanden |
| 10011 | yannick schwart | Bereits vorhanden |
| 10012 | dvse468 | Bereits vorhanden |
| 10013 | dvse | Bereits vorhanden |
| 10023 | Garage Carrosserie D'Arienzo AG | Bereits vorhanden |
| 10025 | LARAG AG Rümlang | Bereits vorhanden |
| 10028 | FSF GARAGE | Bereits vorhanden |
| 10029 | EBAY | Bereits vorhanden |
| 10030 | GeppSellSoft | Bereits vorhanden |

---

## 🔧 Technische Details

### API-Endpunkt
```
POST https://api.abaninja.ch/accounts/{accountUuid}/addresses/v2/addresses
```

**Wichtig:** NICHT `/companies` sondern `/addresses`!

### Payload-Struktur

```json
{
  "type": "company",
  "customer_number": "10001",
  "name": "Firmenname",
  "currency_code": "CHF",
  "language": "de",
  "payment_terms": 30,
  "id_number": "CHE-XXX.XXX.XXX",
  "contacts": [
    {
      "type": "email",
      "value": "email@example.com",
      "primary": true
    }
  ],
  "addresses": [
    {
      "city": "Zürich",
      "zip_code": "8000",
      "country_code": "CH",
      "state": "ZH",
      "street_number": "Musterstrasse 1"
    }
  ]
}
```

### Pflichtfelder

1. **`type`**: `"company"` (für Firmen)
2. **`customer_number`**: Kundennummer (String)
3. **`name`**: Firmenname (String)
4. **`currency_code`**: Währung (z.B. "CHF")
5. **`language`**: Sprache (z.B. "de")
6. **`contacts.*.primary`**: Boolean (NICHT `is_primary`!)
7. **`addresses.*.state`**: Kanton (für CH-Adressen erforderlich!)

### Besonderheiten

1. **Land-Feld:** Muss ISO-Code sein (CH, DE, etc.), nicht "Schweiz" oder "-"
2. **Kanton-Feld:** Für CH-Adressen MUSS `state` gesetzt sein (z.B. "ZH")
3. **Adresse:** Mindestens eine Adresse erforderlich (auch Dummy-Adresse möglich)
4. **Kontakte:** `primary` statt `is_primary` verwenden

---

## 📁 Generierte Dateien

### 1. UUID-Mapping
**Pfad:** `/home/ubuntu/Swiss21/data/customer_uuid_mapping.json`

Enthält die Zuordnung Kundennummer → UUID für alle erstellten Kunden.

**Verwendung:** Für Rechnungsimport und weitere API-Operationen.

### 2. Erstellungs-Log
**Pfad:** `/home/ubuntu/Swiss21/logs/customer_creation.log`

Detailliertes Log aller Erstellungsversuche mit Erfolg/Fehler-Status.

### 3. Erstellungs-Skript
**Pfad:** `/home/ubuntu/Swiss21/scripts/create_all_customers_in_abaninja.py`

Wiederverwendbares Python-Skript für zukünftige Kundenimporte.

---

## 🔍 Lösungsweg - Wie wurde der richtige Endpunkt gefunden?

### Problem
Initiale Versuche mit `/addresses/v2/companies` gaben **405 Method Not Allowed**.

### Recherche
1. **API-Dokumentation durchsucht:** https://www.abaninja.ch/apidocs/
2. **Alle Reiter systematisch geprüft**
3. **Gefunden:** "POST Create new address for given account"

### Lösung
Der korrekte Endpunkt ist:
```
POST /addresses/v2/addresses
```

**Nicht:** `/addresses/v2/companies` (nur GET, PATCH, DELETE)

### Validierung
Erfolgreicher Test mit Kunde 10001 (Sinanovic Garage).

---

## 📝 Lessons Learned

### 1. API-Struktur
- `/companies` ist nur für GET/PATCH/DELETE
- `/addresses` ist für POST (Erstellen)
- Unterschied zwischen Abrufen und Erstellen!

### 2. Datenqualität
- CSV-Daten müssen bereinigt werden (Land-Feld)
- Fehlende Adressen mit Dummy-Daten auffüllen
- Kanton-Mapping für CH-Adressen erforderlich

### 3. Fehlerbehandlung
- 422: Validierungsfehler (Pflichtfelder prüfen!)
- 409: Konflikt (Kundennummer bereits vergeben)
- 201: Erfolg (UUID in Response)

---

## 🎯 Nächste Schritte

1. ✅ **Kunden erstellt** (20/30 neu, 10/30 bereits vorhanden)
2. ⏭️ **Rechnungen importieren** (83 Rechnungen aus Abisco)
3. ⏭️ **Aufträge importieren** (116 Aufträge aus Abisco)
4. ⏭️ **Gutschriften importieren** (15 Gutschriften)

---

## 📚 Referenzen

- **API-Dokumentation:** https://www.abaninja.ch/apidocs/
- **GitHub-Repository:** https://github.com/Motorlink/Swiss21
- **CSV-Quelle:** `/home/ubuntu/upload/kundenliste.csv`
- **Datenbank:** Abisco PostgreSQL (abisco_db)

---

**Status:** ✅ Abgeschlossen  
**Nächster Schritt:** Rechnungsimport
