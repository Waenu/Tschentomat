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
| `reinigungSelbst` | Reinigung, wenn die Familie selbst reinigt und frische Wäsche mitbringt (0 = gratis) |
| `selbstReinigung` | Zeiten (jedes Jahr gleich), in denen die Familie selbst reinigen darf. Format `[["11-01","12-18"]]` (Monat-Tag von, bis). Weitere Zeiträume mit Komma anfügen |
| `sparEin` | Reduktion pro Nacht, wenn Zimmer 1 abgeschlossen bleibt |
| `sparMaxPers` | Bis so viele Personen insgesamt kann Zimmer 1 abgeschlossen bleiben |
| `minNaechte` / `maxNaechte` | Kleinste und grösste Anzahl Nächte |
| `maxPersonen` | Personen mit Bett |
| `iban` / `bank` | Konto für die Überweisung, wird im Ergebnis angezeigt |
| `zahlTage` | Frist in Tagen nach dem letzten Ferientag |
| `lueckeMax` | Freie Nächte zwischen zwei Belegungen bis zu dieser Zahl gelten als Lücke (Airbnb-Mindestaufenthalt minus 1) |
| `lueckeVorlaufTage` | Lücken ausserhalb der Selbstreinigungs-Zeiten (dort ist die Familienstaffel nicht möglich) sind für die Familie erst so viele Tage vor Beginn der Lücke buchbar, vorher gesperrt |
| `lueckeSperrMonate` | Monate (Liste), in denen Lücken für die Familie immer gesperrt sind (violett, nie freigegeben). Massgebend ist der Monat der ersten Nacht der Lücke |
| `lueckeMaxPersonen` | Ganze Lücke: höchstens so viele Personen mit Bett, zusätzlich `lueckeMaxKleinkinder` Kleinkind(er) im Kinderbettchen. Dazu: keine Gäste, nur Zimmer 2, eigene Wäsche, Reinigung 240 |
| `lueckeRabatt` | Prozent Rabatt auf die Übernachtungen, wenn die ganze Lücke gebucht wird (Reinigung bleibt gleich) |
| `hochsaisonMonate` | Ganze Monate, die jedes Jahr gelb markiert werden. Februar ist `[2]`, mehrere zum Beispiel `[2, 7]` |
| `spitzenzeiten` | Zeiten, in denen nur zu hohen Preisen vermietet wird (zum Beispiel Skirennen). Rot markiert, ohne Familienpreis: nur «Preis auf Anfrage». Format: `[["2027-01-15","2027-01-17","Skirennen"]]` (von, bis, Name) |
| `hochsaison` | Zeiträume, die gelb markiert werden. Format: `[["2026-12-19","2027-01-03"], ["2027-02-06","2027-02-20"]]` (von, bis, beide eingeschlossen) |

## Belegung aus Airbnb

- Die Datei `belegt.json` wird alle 3 Stunden automatisch aus dem Airbnb-Kalender erzeugt (Reiter «Actions», «Belegung aktualisieren»). Nicht von Hand ändern.
- Der Airbnb-Link steht nur als geheimer Eintrag `AIRBNB_ICAL` unter Settings, Secrets and variables, Actions.
- Von Hand starten: Reiter «Actions», «Belegung aktualisieren», «Run workflow».
