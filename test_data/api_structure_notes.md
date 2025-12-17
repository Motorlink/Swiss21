# ABA Ninja Invoice API - Struktur-Notizen

## Problem
Die Invoice API erwartet ein `documents` Array, aber die genaue Struktur ist in der Dokumentation nicht vollständig sichtbar.

## Beobachtungen
1. Request muss `{"documents": [...]}` enthalten
2. Die Dokumentation zeigt Properties wie:
   - receiver
   - paymentInstructions
   - positions
   - cashDiscounts

## Nächste Schritte
- Beispiel-Request aus der Dokumentation extrahieren
- Oder: Reverse-Engineering durch Trial & Error
- Oder: OpenAPI Spec herunterladen und analysieren

## Status
- Kunde erfolgreich erstellt: `e6592469-5215-481d-b354-2227b75a6ad5`
- Rechnung noch nicht erstellt (Schema-Fehler)
