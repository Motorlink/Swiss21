# 🎯 LÖSUNG GEFUNDEN! POST-Endpunkt für Kunden

**Datum:** 2025-12-17  
**Quelle:** ABA Ninja API-Dokumentation

---

## ✅ DER RICHTIGE ENDPUNKT:

```
POST /accounts/{accountUuid}/addresses/v2/addresses
```

**NICHT** `/companies` sondern `/addresses`!

---

## Request Body Schema

```json
{
  "type": "company",
  "customer_number": "string",
  "name": "string",
  "id_number": "string",
  "vat_number": "string",
  "currency_code": "string",
  "language": "string",
  "contact_persons": [],
  "tags": [],
  "contacts": [],
  "addresses": [],
  "private_notes": "string",
  "automatic_dunning": boolean,
  "payment_terms": integer
}
```

### Pflichtfelder:
- `type`: `"company"` (für Firmen) oder `"person"` (für Privatpersonen)
- `customer_number`: Kundennummer (String)
- `name`: Firmenname (String)

### Optionale Felder:
- `id_number`: UID-Nummer
- `vat_number`: MwSt-Nummer
- `currency_code`: Währung (z.B. "CHF")
- `language`: Sprache (z.B. "de")
- `contact_persons`: Array von Ansprechpartnern
- `tags`: Array von Tags
- `contacts`: Array von Kontaktmethoden (Email, Telefon, etc.)
- `addresses`: Array von Adressen
- `private_notes`: Private Notizen
- `automatic_dunning`: Automatisches Mahnwesen (Boolean)
- `payment_terms`: Zahlungsziel in Tagen (Enum: -1, 7, 10, 14, 15, 20, 30, 60, 90)

---

## Response

**201 Address created**

```json
{
  "data": {
    "type": "company",
    "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
    "customer_number": "string",
    "name": "string",
    ...
  }
}
```

---

## Fehler-Codes

- **400**: Fehler (z.B. ungültige Daten)
- **409**: Conflict (z.B. Kundennummer bereits vergeben)

---

## Warum hat `/companies` nicht funktioniert?

Der Endpunkt `/addresses/v2/companies` ist nur für:
- GET (Liste/Einzeln)
- PATCH (Update)
- DELETE

Zum **ERSTELLEN** muss man `/addresses/v2/addresses` verwenden!

---

## Nächster Schritt

Test mit Kunde 10001 (Sinanovic Garage)
