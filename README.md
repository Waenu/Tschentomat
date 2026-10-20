# TSCHENT-O-MAT

Preisrechner für die Familie, Chalet Tschenten, Adelboden.

## Preise oder Nächte ändern

1. Auf GitHub die Datei `einstellungen.json` öffnen.
2. Oben rechts auf den Stift (Edit) klicken.
3. Nur die Zahlen ändern, dazu `version` und `gueltigAb` anpassen.
4. Rechts oben auf «Commit changes…» und danach auf «Commit changes» klicken.
5. Nach etwa einer Minute sehen alle die neuen Werte.

| Eintrag | Bedeutung |
|---|---|
| `famPausch` | Familie pro Nacht |
| `gast` | Gast pro Nacht (eigenes Zimmer) |
| `gastZimmer` | Gast im selben Zimmer wie Sohn oder Tochter, pro Nacht |
| `famAnteil` | Familie pro Nacht, wenn Sohn oder Tochter das Zimmer mit einem Gast teilt |
| `reinigung` | Reinigung pro Aufenthalt |
| `sparEin` | Reduktion pro Nacht, wenn Zimmer 1 abgeschlossen bleibt |
| `sparMaxPers` | Bis so viele Personen insgesamt kann Zimmer 1 abgeschlossen bleiben |
| `minNaechte` / `maxNaechte` | Kleinste und grösste Anzahl Nächte |
| `maxPersonen` | Personen mit Bett |
