#!/usr/bin/env python3
"""Holt den Airbnb-Kalender (iCal) und schreibt die belegten Naechte nach belegt.json.
Der Link steht als Secret AIRBNB_ICAL bei GitHub und wird nie ausgegeben oder gespeichert.
Bei jedem Fehler bleibt die bisherige belegt.json unveraendert."""
import json, os, re, sys, urllib.request
from datetime import date, datetime, timedelta

url = os.environ.get("ICAL_URL", "").strip()
if not url:
    sys.exit("Secret AIRBNB_ICAL fehlt oder ist leer.")
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (belegung-bot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8", "replace")
except Exception as e:
    sys.exit("Kalender konnte nicht geladen werden: " + type(e).__name__)
if "BEGIN:VCALENDAR" not in text:
    sys.exit("Antwort ist kein iCal-Kalender.")

text = re.sub(r"\r?\n[ \t]", "", text)  # gefaltete Zeilen zusammenfuegen

def tag(zeile):
    m = re.search(r":(\d{8})", zeile)
    return datetime.strptime(m.group(1), "%Y%m%d").date() if m else None

heute = date.today()
bis = heute + timedelta(days=800)
naechte = set()
for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
    von = ende = None
    for z in block.splitlines():
        if z.startswith("DTSTART"):
            von = tag(z)
        elif z.startswith("DTEND"):
            ende = tag(z)
    if not von:
        continue
    if not ende or ende <= von:
        ende = von + timedelta(days=1)
    d = von
    while d < ende:  # DTEND ist der Abreisetag und selbst keine belegte Nacht
        if heute - timedelta(days=1) <= d <= bis:
            naechte.add(d.isoformat())
        d += timedelta(days=1)

neu = {"_hinweis": "Wird automatisch aus dem Airbnb-Kalender erzeugt. Nicht von Hand aendern.", "belegt": sorted(naechte)}
alt = None
try:
    alt = json.load(open("belegt.json", encoding="utf-8"))
except Exception:
    pass
if alt != neu:
    with open("belegt.json", "w", encoding="utf-8") as f:
        json.dump(neu, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("belegt.json aktualisiert:", len(naechte), "belegte Naechte")
else:
    print("Keine Aenderung:", len(naechte), "belegte Naechte")
