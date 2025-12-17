# Analyse: Kunde 10000 Struktur in ABA Ninja

**Datum:** 2025-12-17  
**Quelle:** ABA Ninja API - GET `/addresses/v2/companies`

---

## API Response Struktur

### Root Level
```json
{
  "data": [...]  // Array von Kunden
  "links": {...}
  "meta": {...}
}
```

**Wichtig:** `data` ist ein **Array**, nicht ein Objekt mit `addresses`!

---

## Kunde 10000 - Vollständige Feldanalyse

### 1. Basis-Felder

| Feld | Wert | Typ | Pflicht | Beschreibung |
|------|------|-----|---------|--------------|
| `type` | `"company"` | String | Ja | Typ der Adresse (company/person) |
| `uuid` | `"e6592469-5215-481d-b354-2227b75a6ad5"` | UUID | - | Eindeutige Company-ID (wird von API generiert) |
| `customer_number` | `"10000"` | String | Ja | Kundennummer aus Abisco |
| `company_name` | `"MT Transport GmbH"` | String | Ja | Firmenname |

### 2. Identifikationsnummern

| Feld | Wert | Typ | Pflicht | Beschreibung |
|------|------|-----|---------|--------------|
| `id_number` | `"CHE-372.925.312"` | String | Nein | UID-Nummer (Schweizer Unternehmens-ID) |
| `vat_number` | `null` | String | Nein | Separate MwSt-Nummer (optional) |

### 3. Währung & Sprache

| Feld | Wert | Typ | Pflicht | Beschreibung |
|------|------|-----|---------|--------------|
| `currency_code` | `"CHF"` | String | Ja | Währung (ISO 4217) |
| `language` | `"de"` | String | Ja | Sprache (ISO 639-1: de/fr/it/en) |

### 4. Kontaktpersonen

| Feld | Wert | Typ | Beschreibung |
|------|------|-----|--------------|
| `contact_persons` | `[]` | Array | Liste von Ansprechpartnern (bei 10000 leer) |

**Struktur für contact_persons (wenn vorhanden):**
```json
{
  "first_name": "...",
  "last_name": "...",
  "salutation": "...",
  "position": "..."
}
```

### 5. Kontaktdaten

| Feld | Wert | Typ | Beschreibung |
|------|------|-----|--------------|
| `contacts` | Array | Array | Liste von Kontaktmethoden (Email, Telefon, etc.) |

**Struktur:**
```json
[
  {
    "type": "email",
    "value": "info@mt-transport.ch",
    "is_primary": true
  }
]
```

**Mögliche `type` Werte:**
- `email`
- `phone`
- `mobile`
- `fax`
- `website`

### 6. Adressen

| Feld | Wert | Typ | Beschreibung |
|------|------|-----|--------------|
| `addresses` | Array | Array | Liste von Adressen (Rechnungs-/Lieferadressen) |

**Struktur bei Kunde 10000:**
```json
[
  {
    "uuid": "ad08bb56-373d-48df-b906-e994cb27eaf9",
    "address": null,
    "street_number": null,
    "extension": null,
    "additional_field": null,
    "city": "Uster",
    "zip_code": "8610",
    "country_code": "CH"
  }
]
```

**Adress-Felder im Detail:**

| Feld | Wert | Typ | Pflicht | Beschreibung |
|------|------|-----|---------|--------------|
| `uuid` | `"ad08bb56-..."` | UUID | - | Eindeutige Adress-ID (wird von API generiert) |
| `address` | `null` | String | Nein | Vollständige Adresse (alternativ zu Einzelfeldern) |
| `street_number` | `null` | String | Nein | Straße + Hausnummer |
| `extension` | `null` | String | Nein | Adresszusatz (z.B. "c/o", "Postfach") |
| `additional_field` | `null` | String | Nein | Zusätzliches Adressfeld |
| `city` | `"Uster"` | String | Ja | Ort |
| `zip_code` | `"8610"` | String | Ja | Postleitzahl |
| `country_code` | `"CH"` | String | Ja | Ländercode (ISO 3166-1 alpha-2) |

**Beobachtung:** Bei Kunde 10000 sind nur `city`, `zip_code` und `country_code` gefüllt!

### 7. Weitere Felder

| Feld | Wert | Typ | Beschreibung |
|------|------|-----|--------------|
| `tags` | `[""]` | Array | Tags/Kategorien (bei 10000 leer) |
| `acc_accounts` | `[]` | Array | Buchhaltungskonten |
| `private_notes` | `null` | String | Private Notizen |
| `automatic_dunning` | `false` | Boolean | Automatisches Mahnwesen |
| `payment_terms` | `30` | Integer | Zahlungsziel in Tagen |
| `isArchived` | `false` | Boolean | Archiviert ja/nein |
| `global_percent_discount` | `null` | Float | Globaler Rabatt in Prozent |

---

## Wichtige Erkenntnisse

### ✅ Was funktioniert (GET):
- Endpunkt: `GET /accounts/{uuid}/addresses/v2/companies`
- Response: `data` ist ein **Array**, nicht `data.addresses`

### ❌ Was NICHT funktioniert (POST):
- Endpunkt: `POST /accounts/{uuid}/addresses/v2/companies`
- Fehler: **405 Method Not Allowed**

### 🔍 Mögliche Gründe für 405-Fehler:
1. **POST ist nicht erlaubt** auf diesem Endpunkt
2. **Anderer Endpunkt** für das Erstellen von Kunden erforderlich
3. **Kunden können nur manuell** in ABA Ninja angelegt werden
4. **Kunden werden automatisch** beim ersten Rechnungsimport erstellt

---

## Nächste Schritte

### Option 1: Andere API-Endpunkte testen
- `/contacts` statt `/addresses`
- `/customers` (falls vorhanden)
- API-Dokumentation konsultieren

### Option 2: Kunden beim Rechnungsimport erstellen
- Kundendaten direkt in Rechnung einbetten
- API erstellt Kunde automatisch

### Option 3: Manuelle Erstellung
- Kunden manuell in ABA Ninja Web-Interface anlegen
- Dann UUIDs per API abrufen

---

## Minimale Kundenstruktur (Hypothese)

Basierend auf Kunde 10000, **minimal erforderliche Felder**:

```json
{
  "customer_number": "10001",
  "company_name": "Sinanovic Garage",
  "currency_code": "CHF",
  "language": "de",
  "contacts": [
    {
      "type": "email",
      "value": "sinanovicernes9@gmail.com",
      "is_primary": true
    }
  ],
  "addresses": [
    {
      "city": "Volketswil",
      "zip_code": "8600",
      "country_code": "CH"
    }
  ],
  "payment_terms": 30
}
```

**Status:** Nicht getestet, da POST 405-Fehler gibt!

---

## Fehlende Informationen

1. **Wie wurde Kunde 10000 erstellt?**
   - Manuell über Web-Interface?
   - Über eine andere API?
   - Automatisch beim Rechnungsimport?

2. **Gibt es einen anderen API-Endpunkt für POST?**
   - Dokumentation erforderlich

3. **Können Kunden über Rechnungs-API erstellt werden?**
   - Test erforderlich
