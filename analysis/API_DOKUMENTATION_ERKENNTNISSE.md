# ABA Ninja API - Wichtige Erkenntnisse

**Datum:** 2025-12-17  
**Quelle:** https://www.abaninja.ch/apidocs/

---

## ❌ KRITISCHE ERKENNTNIS: POST /companies EXISTIERT NICHT!

### Verfügbare Endpunkte für `/addresses/v2/companies`:

1. ✅ **GET** `/accounts/{accountUuid}/addresses/v2/companies`
   - Liste aller Firmenadressen abrufen
   
2. ✅ **GET** `/accounts/{accountUuid}/addresses/v2/companies/{companyUuid}`
   - Einzelne Firma abrufen
   
3. ✅ **PATCH** `/accounts/{accountUuid}/addresses/v2/companies/{companyUuid}`
   - Einzelne Firma **AKTUALISIEREN**
   
4. ✅ **DELETE** `/accounts/{accountUuid}/addresses/v2/companies/{companyUuid}`
   - Einzelne Firma löschen

### ❌ **POST** existiert NICHT in der Dokumentation!

**Das erklärt den 405-Fehler ("Method Not Allowed")!**

---

## Lösung: Kunden müssen anders erstellt werden

### Möglichkeit 1: Über Rechnungs-API
Kunden werden möglicherweise **automatisch beim Erstellen einer Rechnung** angelegt, wenn die Kundendaten in der Rechnung eingebettet sind.

### Möglichkeit 2: Manuell im Web-Interface
Kunden müssen manuell in ABA Ninja angelegt werden, dann können sie über die API abgerufen und aktualisiert werden.

### Möglichkeit 3: Anderer API-Endpunkt
Es könnte einen anderen, nicht dokumentierten Endpunkt geben.

---

## Nächste Schritte

1. **Test:** Rechnung mit neuen Kundendaten erstellen → Wird Kunde automatisch angelegt?
2. **Alternative:** Kunden manuell anlegen und UUIDs per API abrufen
3. **OpenAI befragen:** Nach Best Practices für ABA Ninja Kundenimport

---

## PATCH-Struktur (für Updates)

```json
{
  "type": "company",
  "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
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
  "automatic_dunning": true,
  "payment_terms": -1
}
```

**Wichtig:** PATCH benötigt die UUID - kann also nur für **existierende** Kunden verwendet werden!
