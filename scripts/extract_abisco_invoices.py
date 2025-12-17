#!/usr/bin/env python3
"""
Extrahiert alle Rechnungen aus der Abisco-Datenbank
und bereitet sie für den Import in ABA Ninja vor.
"""

import psycopg2
import json
from datetime import datetime

# Datenbankverbindung (als postgres user via peer auth)
import subprocess
import os

# Verwende subprocess um als postgres user zu verbinden
conn_string = "dbname=abisco_db"
conn = psycopg2.connect(conn_string, user="postgres")

cur = conn.cursor()

# Extrahiere alle Rechnungen mit vollständigen Details
query = """
SELECT 
    r.rechnungsnummer,
    r.rechnungsdatum,
    r.redundant_endpreis_brutto / 100.0 as betrag_brutto,
    r.redundant_endpreis_netto / 100.0 as betrag_netto,
    r.bezahlt / 100.0 as bezahlt,
    r.komplett_bezahlt::text,
    r.faelligkeit,
    r.skontodatum,
    r.skonto::text,
    r.skonto_wert / 100.0 as skonto_prozent,
    r.kundennummer,
    r.belegrabatt / 100.0 as rabatt,
    r.mitarbeiter,
    k.kundennummer as kunde_nr,
    a.name as kunde_name,
    a.name_zusatz,
    a.strasse,
    a.plz,
    a.ort,
    a.land,
    a.email,
    a.telefon_gesch,
    a.mobil
FROM kundenrechnungen r
LEFT JOIN kundendaten k ON r.kundennummer = k.kundennummer
LEFT JOIN adressen a ON a.id = (
    SELECT kunde_adressid FROM kundendaten WHERE kundennummer = r.kundennummer LIMIT 1
)
WHERE r.kundennummer >= 10000
ORDER BY r.rechnungsnummer;
"""

cur.execute(query)
rechnungen = cur.fetchall()

print(f"✅ {len(rechnungen)} Rechnungen gefunden\n")

# Speichere Rechnungen
invoices_data = []

for row in rechnungen:
    invoice = {
        "rechnungsnummer": row[0],
        "rechnungsdatum": str(row[1]) if row[1] else None,
        "betrag_brutto": float(row[2]) if row[2] else 0.0,
        "betrag_netto": float(row[3]) if row[3] else 0.0,
        "bezahlt": float(row[4]) if row[4] else 0.0,
        "komplett_bezahlt": row[5] == 'T',
        "faelligkeit": str(row[6]) if row[6] else None,
        "skontodatum": str(row[7]) if row[7] else None,
        "skonto": row[8] == 'T',
        "skonto_prozent": float(row[9]) if row[9] else 0.0,
        "kundennummer": row[10],
        "rabatt": float(row[11]) if row[11] else 0.0,
        "mitarbeiter": row[12],
        "kunde": {
            "kundennummer": row[13],
            "name": row[14],
            "name_zusatz": row[15],
            "strasse": row[16],
            "plz": row[17],
            "ort": row[18],
            "land": row[19],
            "email": row[20],
            "telefon": row[21],
            "mobil": row[22]
        }
    }
    
    # Hole Positionen
    cur.execute("""
        SELECT 
            artikelnummer,
            bezeichnung,
            menge / 100.0,
            einzelpreis / 100.0,
            redundant_endpreis / 100.0,
            mwst_satz / 100.0
        FROM verkaufspositionen
        WHERE rechnungsid = (
            SELECT rechnungsid FROM kundenrechnungen WHERE rechnungsnummer = %s LIMIT 1
        )
        ORDER BY positionsnummer
    """, (row[0],))
    
    positionen = cur.fetchall()
    invoice["positionen"] = [
        {
            "artikelnummer": p[0],
            "bezeichnung": p[1],
            "menge": float(p[2]) if p[2] else 0.0,
            "einzelpreis": float(p[3]) if p[3] else 0.0,
            "gesamtpreis": float(p[4]) if p[4] else 0.0,
            "mwst_satz": float(p[5]) if p[5] else 0.0
        }
        for p in positionen
    ]
    
    invoices_data.append(invoice)

# Speichere als JSON
with open('/home/ubuntu/Swiss21/data/abisco_invoices_export.json', 'w', encoding='utf-8') as f:
    json.dump(invoices_data, f, indent=2, ensure_ascii=False)

print(f"✅ Daten gespeichert in: /home/ubuntu/Swiss21/data/abisco_invoices_export.json")

# Erstelle Markdown-Übersicht
with open('/home/ubuntu/Swiss21/data/RECHNUNGEN_UEBERSICHT.md', 'w', encoding='utf-8') as f:
    f.write("# Abisco Rechnungen - Übersicht\n\n")
    f.write(f"**Exportiert am**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"**Anzahl Rechnungen**: {len(invoices_data)}\n\n")
    
    # Statistiken
    total_brutto = sum(inv['betrag_brutto'] for inv in invoices_data)
    total_bezahlt = sum(inv['bezahlt'] for inv in invoices_data)
    total_offen = total_brutto - total_bezahlt
    anzahl_bezahlt = sum(1 for inv in invoices_data if inv['komplett_bezahlt'])
    anzahl_offen = len(invoices_data) - anzahl_bezahlt
    
    f.write("## Statistiken\n\n")
    f.write(f"- **Gesamtbetrag (brutto)**: CHF {total_brutto:,.2f}\n")
    f.write(f"- **Bereits bezahlt**: CHF {total_bezahlt:,.2f}\n")
    f.write(f"- **Noch offen**: CHF {total_offen:,.2f}\n")
    f.write(f"- **Anzahl bezahlt**: {anzahl_bezahlt}\n")
    f.write(f"- **Anzahl offen**: {anzahl_offen}\n\n")
    
    # Tabelle
    f.write("## Alle Rechnungen\n\n")
    f.write("| Nr | Datum | Kunde | Betrag (CHF) | Bezahlt | Status | Fälligkeit |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    
    for inv in invoices_data:
        status = "✅ Bezahlt" if inv['komplett_bezahlt'] else "❌ Offen"
        kunde_name = inv['kunde']['name'] if inv['kunde'] else "Unbekannt"
        f.write(f"| {inv['rechnungsnummer']} | {inv['rechnungsdatum']} | {kunde_name} | "
                f"{inv['betrag_brutto']:,.2f} | {inv['bezahlt']:,.2f} | {status} | {inv['faelligkeit']} |\n")
    
    f.write("\n## Details pro Rechnung\n\n")
    
    for inv in invoices_data:
        f.write(f"### Rechnung {inv['rechnungsnummer']}\n\n")
        f.write(f"**Datum**: {inv['rechnungsdatum']}  \n")
        f.write(f"**Fälligkeit**: {inv['faelligkeit']}  \n")
        
        if inv['kunde']:
            f.write(f"**Kunde**: {inv['kunde']['name']}  \n")
            f.write(f"**Kundennummer**: {inv['kunde']['kundennummer']}  \n")
            f.write(f"**Adresse**: {inv['kunde']['strasse']}, {inv['kunde']['plz']} {inv['kunde']['ort']}  \n")
            f.write(f"**E-Mail**: {inv['kunde']['email']}  \n")
        
        f.write(f"**Betrag (netto)**: CHF {inv['betrag_netto']:,.2f}  \n")
        f.write(f"**Betrag (brutto)**: CHF {inv['betrag_brutto']:,.2f}  \n")
        f.write(f"**Bezahlt**: CHF {inv['bezahlt']:,.2f}  \n")
        f.write(f"**Status**: {'✅ Vollständig bezahlt' if inv['komplett_bezahlt'] else '❌ Offen'}  \n\n")
        
        if inv['positionen']:
            f.write("**Positionen**:\n\n")
            f.write("| Artikel | Bezeichnung | Menge | Einzelpreis | Gesamt | MwSt |\n")
            f.write("|---|---|---|---|---|---|\n")
            for pos in inv['positionen']:
                f.write(f"| {pos['artikelnummer']} | {pos['bezeichnung']} | {pos['menge']} | "
                        f"{pos['einzelpreis']:,.2f} | {pos['gesamtpreis']:,.2f} | {pos['mwst_satz']}% |\n")
        
        f.write("\n---\n\n")

print(f"✅ Übersicht erstellt: /home/ubuntu/Swiss21/data/RECHNUNGEN_UEBERSICHT.md")

cur.close()
conn.close()

print("\n✅ Export abgeschlossen!")
