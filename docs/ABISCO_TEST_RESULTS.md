# Abisco/Webisco Test-Ergebnisse

**Datum**: 17. Dezember 2024  
**Server**: 82.220.91.37  
**Admin-ID**: 5zHaOvoDzfp97DtimphCrAX  
**Version**: 55

---

## Verbindungstest ✅

### Server-Erreichbarkeit
- **Port 8228 (HTTP)**: ✅ OFFEN
- **Port 9229 (HTTPS)**: ✅ OFFEN
- **Authentifizierung**: ✅ Erfolgreich mit Admin-ID

### Webisco-Version
- **Version**: 55
- **Status**: Aktiv und funktionsfähig

---

## Kundensuche-Tests

### Problem: "Es muss ein Suchmuster angegeben werden"

Alle Kundensuche-Versuche liefern denselben Fehler:
```xml
<webisco utcoffset="+1" 
         errormessage="Es muss ein Suchmuster angegeben werden." 
         timestamp="2025-12-17 11:50:46" 
         type="response" 
         version="55"/>
```

### Getestete Varianten

#### 1. Direkter Suchbegriff
```xml
<kundensuche>
  <suchbegriff>10000</suchbegriff>
</kundensuche>
```
**Ergebnis**: ❌ "Es muss ein Suchmuster angegeben werden"

#### 2. Wildcard-Muster
```xml
<kundensuche>
  <suchbegriff>*10000*</suchbegriff>
</kundensuche>
```
**Ergebnis**: ❌ "Es muss ein Suchmuster angegeben werden"

#### 3. Kundennummer-Tag
```xml
<kundensuche>
  <kundennummer>10000</kundennummer>
</kundensuche>
```
**Ergebnis**: ❌ "Es muss ein Suchmuster angegeben werden"

#### 4. Name-Tag
```xml
<kundensuche>
  <name>10000</name>
</kundensuche>
```
**Ergebnis**: ❌ "Es muss ein Suchmuster angegeben werden"

---

## Mögliche Ursachen

1. **Dokumentation unvollständig**: Die Webisco-Dokumentation zeigt kein vollständiges Beispiel für `kundensuche`
2. **Spezielle Syntax erforderlich**: Möglicherweise wird ein spezielles Format erwartet
3. **Zusätzliche Parameter**: Eventuell sind weitere Parameter erforderlich
4. **Abisco-Konfiguration**: Die Kundensuche könnte in Abisco deaktiviert oder eingeschränkt sein

---

## Alternative: Beleganfrage

Die `beleganfrage`-Ressource funktioniert besser für den Zugriff auf Kundendaten, da Belege (Aufträge, Rechnungen) immer Kundeninformationen enthalten.

### Empfohlener Ansatz

**Statt Kundensuche** → **Beleganfrage mit Kundennummer-Filter**:

```xml
<beleganfrage>
  <typ>auftrag</typ>
  <von>2024-01-01</von>
  <bis>2025-12-31</bis>
</beleganfrage>
```

Dann in der Antwort nach `kundennummer=10000` filtern.

---

## Nächste Schritte

1. ✅ **Beleganfrage testen** - Aufträge/Rechnungen abrufen
2. ⏳ **Abisco-Dokumentation prüfen** - Gibt es spezielle Kundensuche-Syntax?
3. ⏳ **Support kontaktieren** - Falls Kundensuche weiterhin nicht funktioniert
4. ✅ **Alternative Route**: Über Belege auf Kundendaten zugreifen

---

**Fazit**: Die Verbindung funktioniert, aber die `kundensuche`-Ressource benötigt weitere Klärung. Für die Integration können wir über `beleganfrage` auf Kundendaten zugreifen.
