#!/usr/bin/env python3
"""Meldet neue Luecken (2-3 freie Naechte zwischen zwei Buchungen) als GitHub-Issue, damit in
PriceLabs reagiert werden kann. Gemeldet werden Luecken ausserhalb der Selbstreinigungs-Zeiten
(dort ist die Familienstaffel nicht moeglich; einstellungen.json: selbstReinigung) sowie Luecken
in den Monaten aus lueckeSperrMonate. Die Familie kann diese erst lueckeVorlaufTage vor Beginn buchen.
Jede Luecke wird nur einmal gemeldet (Dedupe ueber den Issue-Titel, auch geschlossene).
Ohne GITHUB_TOKEN laeuft das Skript im Probelauf und gibt nur aus."""
import json, os, sys, urllib.request
from datetime import date, datetime, timedelta

cfg = json.load(open("einstellungen.json", encoding="utf-8"))
monate = cfg.get("lueckeSperrMonate", [])
ruhe = cfg.get("selbstReinigung", [])
vorlauf = cfg.get("lueckeVorlaufTage", 4)
n_min = cfg.get("minNaechte", 2)
n_max = cfg.get("lueckeMax", 3)
heute = date.today()
belegt = sorted(datetime.strptime(k, "%Y-%m-%d").date() for k in json.load(open("belegt.json", encoding="utf-8"))["belegt"])

def in_ruhe(d):
    md = d.strftime("%m-%d")
    return any(a <= md <= e for a, e in ruhe)

luecken = []
for a, b in zip(belegt, belegt[1:]):
    n = (b - a).days - 1
    start = a + timedelta(days=1)
    if cfg.get("keinCheckinSonntag", True) and start.weekday() == 6:   # Sonntag: kein Check-in bei Airbnb
        start += timedelta(days=1)
        n -= 1
    ende = b - timedelta(days=1)
    staffel_zeit = in_ruhe(start) and in_ruhe(ende)
    if n_min <= n <= n_max and start >= heute and (start.month in monate or not staffel_zeit):
        luecken.append((start, b, n))

def titel(start, ende, n):
    return "Lücke %s bis %s (%d Nächte): PriceLabs prüfen" % (start.strftime("%d.%m.%Y"), ende.strftime("%d.%m.%Y"), n)

token = os.environ.get("GITHUB_TOKEN")
repo = os.environ.get("GITHUB_REPOSITORY")
api = "https://api.github.com/repos/%s/issues" % repo

def call(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
        headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "User-Agent": "luecken-bot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

if not luecken:
    print("Keine meldepflichtigen Lücken")
    sys.exit(0)
bekannt = set()
if token and repo:
    page = 1
    while True:
        liste = call(api + "?state=all&per_page=100&page=%d" % page)
        bekannt |= {i["title"] for i in liste if "pull_request" not in i}
        if len(liste) < 100:
            break
        page += 1
for start, b, n in luecken:
    t = titel(start, b, n)
    if t in bekannt:
        print("Schon gemeldet:", t)
        continue
    text = ("Zwischen zwei Buchungen sind %d Nächte frei: erste freie Nacht %s, Abreise der nächsten Buchung am %s.\n\n"
            "Airbnb-Mindestaufenthalt in PriceLabs für diese Tage bei Bedarf auf %d Nächte senken. "
            "Im Tschent-O-Mat ist die Lücke für die Familie bis %d Tage vor Beginn gesperrt.") % (n, start.strftime("%d.%m.%Y"), b.strftime("%d.%m.%Y"), n, vorlauf)
    if token and repo:
        call(api, {"title": t, "body": text})
        print("Gemeldet:", t)
    else:
        print("PROBELAUF, würde melden:", t)
