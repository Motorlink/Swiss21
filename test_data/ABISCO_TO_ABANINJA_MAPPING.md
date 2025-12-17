# Abisco → ABA Ninja Daten-Mapping

## Analyse der existierenden ABA Ninja Rechnung

### Wichtige Erkenntnisse aus der existierenden Rechnung:

1. **receiver** benötigt BEIDE:
   - `addressUuid`: "ad08bb56-373d-48df-b906-e994cb27eaf9"
   - `companyUuid`: "e6592469-5215-481d-b354-2227b75a6ad5"

2. **paymentInstructions** verwendet:
   - `bankAccountUuid` statt direkter IBAN
   - Die IBAN wird über das Bankkonto referenziert

3. **positions** Struktur:
   - `kind`: "product"
   - `unitCode`: "C62" (Stück)
   - `unitUuid`: "fb9abcdc-534c-434f-9ac3-6d51182febc1"
   - `vatUuid`: "1c414ea5-f38e-4d73-ad7b-2a3072c2a4b6" (für 8.1%)
   - `singlePrice`: Einzelpreis
   - `positionTotal`: Gesamtpreis der Position
   - `discount`: { "percentage": 0 }

4. **documentTotal**: Zahl (Skonto in Prozent)

5. **documentDiscount**: { "percentage": 0 }

6. **cashDiscounts**: Array mit Skonto-Bedingungen

---

## Daten-Mapping: Abisco → ABA Ninja

### Rechnungskopf

| Abisco | ABA Ninja | Beispiel |
|--------|-----------|----------|
| `rechnungsnummer` | `reference` oder `title` | "RE1" |
| `auftragsnummer` | `reference` | "A1" |
| `datum` | `invoiceDate`, `deliveryDate` | "2025-12-17" |
| `faelligkeitsdatum` | `dueDate` | "2026-01-16" |
| - | `currencyCode` | "CHF" |
| - | `pricesIncludeVat` | false |
| - | `isTemplate` | false |
| `skonto` | `cashDiscounts[].percentage` | 2 |
| `skontodatum` | `cashDiscounts[].days` | 10 |
| `gesamtbetrag` | `documentTotal` | 0 (Skonto %) |

### Kunde (receiver)

| Abisco | ABA Ninja | Beispiel |
|--------|-----------|----------|
| - | `addressUuid` | "ad08bb56-373d-48df-b906-e994cb27eaf9" |
| - | `companyUuid` | "e6592469-5215-481d-b354-2227b75a6ad5" |

**WICHTIG**: Beide UUIDs müssen angegeben werden!

### Zahlungsinformationen

| Abisco | ABA Ninja | Beispiel |
|--------|-----------|----------|
| IBAN (manuell) | `paymentInstructions.bankAccountUuid` | "3e2f38d3-c957-4ecc-b1d0-ae563b3fab7b" |

**WICHTIG**: Nicht direkt IBAN, sondern `bankAccountUuid`!

### Positionen

| Abisco | ABA Ninja | Beispiel |
|--------|-----------|----------|
| Position-Nr | `positionNumber` | 1 |
| - | `kind` | "product" |
| `artikelnummer` | `productNumber` | "HU7020Z" |
| `beschreibung` | `productDescription` | "Ölfilter" |
| `menge` | `quantity` | 1 |
| `einzelpreis` | `singlePrice` | 14.12 |
| - | `positionTotal` | 14.12 |
| - | `unitCode` | "C62" |
| - | `unitUuid` | "fb9abcdc-534c-434f-9ac3-6d51182febc1" |
| `mwst` (8.1%) | `vatUuid` | "1c414ea5-f38e-4d73-ad7b-2a3072c2a4b6" |
| - | `discount` | { "percentage": 0 } |

---

## Fehlende Informationen, die wir noch brauchen:

1. ✅ **addressUuid** - Gefunden: "ad08bb56-373d-48df-b906-e994cb27eaf9"
2. ✅ **companyUuid** - Gefunden: "e6592469-5215-481d-b354-2227b75a6ad5"
3. ❓ **bankAccountUuid** - Muss ermittelt werden
4. ❓ **unitUuid** für "Stück" - Gefunden: "fb9abcdc-534c-434f-9ac3-6d51182febc1"
5. ❓ **vatUuid** für verschiedene MwSt-Sätze:
   - 8.1%: "1c414ea5-f38e-4d73-ad7b-2a3072c2a4b6"
   - 0%: ?
   - 7.7%: ?

---

## Nächste Schritte:

1. Bank-Account UUID ermitteln
2. Unit UUIDs für verschiedene Einheiten ermitteln
3. VAT UUIDs für alle MwSt-Sätze ermitteln
4. Script mit korrekter Struktur erstellen
