# Kuketz (DE) — Empfehlungsecke proposal + forum feedback post

**STATUS: DRAFT — needs native review before posting.** Machine-assisted
German; a native speaker must review before anything is submitted. This
community audits claims hard (they WILL open the network tab and read the
CSP) — every sentence below must stay literally true. The nano-gpt.com
dependency is disclosed in the first paragraph of both texts, deliberately.
Plan ref: `plan-q3-distribution.md` Phase 2, language wave 1 (DE).

Two separate texts:
1. Proposal for the **Empfehlungsecke** (Kuketz's recommendation corner,
   maintained on Codeberg — file the proposal per the repo's contribution
   flow at submit time).
2. A separate **forum post** on forum.kuketz-blog.de asking for feedback —
   NOT a promo post; the ask is "prüft das bitte kritisch".

---

## 1. Empfehlungsecke proposal (Codeberg)

**Titel:** Vorschlag: nanoodle — Node-Editor für KI-Workflows, komplett
clientseitig

**Vorab-Offenlegung:** Ich bin der Entwickler. Und die wichtigste
Einschränkung zuerst: Die KI-Modelle selbst laufen **nicht** lokal, sondern
über die API von nano-gpt.com mit einem eigenen API-Schlüssel
(Pay-per-Call). Wer ein vollständig lokales Werkzeug sucht, ist hier falsch
— das soll dieser Vorschlag nicht verschleiern.

**Was es ist:** nanoodle (https://nanoodle.com/de/) ist ein Node-Graph-
Editor für KI-Workflows (Text, Bild, Video, Audio), der vollständig im
Browser läuft. Workflows lassen sich als eigenständige Einzeldatei-
HTML-Apps exportieren oder als URL teilen.

**Warum ich glaube, dass es zu den Kriterien passt:**

- **Open Source:** MIT-Lizenz, vollständige Commit-Historie öffentlich:
  https://github.com/nanoodlecom/nanoodle
- **Kein Tracking:** Null Analytics, keine Werbe- oder Statistik-Dienste.
  Das ist nicht nur Policy, sondern per Content-Security-Policy erzwungen:
  Die CSP erlaubt keine Dritt-Origins (Fonts, CDNs, Tracker — nichts).
  Prüfbar in den Response-Headern und in der Datei `_headers` im Repository.
- **Kein Konto:** Registrierung existiert nicht. Editor, Teilen und Export
  funktionieren ohne Schlüssel; nur das Ausführen von Modellen braucht den
  eigenen API-Schlüssel.
- **Clientseitig:** Kein Backend. Persistenz liegt in IndexedDB im Browser;
  geteilte Links kodieren den Graphen im URL-Fragment (der Teil hinter `#`
  wird nie an einen Server übertragen). Der API-Schlüssel verbleibt im
  Browser des Nutzers.
- **Selbst hostbar:** Die Seite ist statisch; Self-Hosting bedeutet, ein
  Verzeichnis auf einen beliebigen Webserver zu kopieren.

**Die ehrlichen Grenzen:**

- Abhängigkeit von einem kommerziellen API-Anbieter (nano-gpt.com). Prompts
  und Eingaben gehen zur Inferenz an dessen Server — für die Bewertung der
  Datensparsamkeit ist das der entscheidende Punkt. Der Anbieter erlaubt
  Guthaben ohne Konto, u. a. per Kryptowährung; eine eigene Bewertung des
  Anbieters kann und will ich hier nicht ersetzen.
- Die Modelle sind Cloud-Modelle, keine lokalen.
- Pay-per-Call: Jede Ausführung kostet Geld (eine Kostenschätzung wird vor
  dem Ausführen angezeigt); nanoodle selbst schlägt nichts auf und
  verdient ggf. über ein offengelegtes Referral-Programm des Anbieters.

Wenn die Abhängigkeit vom externen KI-Anbieter ein Ausschlusskriterium für
die Empfehlungsecke ist, akzeptiere ich das selbstverständlich — dann
betrachtet diesen Vorschlag bitte als Transparenzübung.

---

## 2. Forum post (forum.kuketz-blog.de) — „Feedback erbeten"

**Titel:** Feedback erbeten: Browser-Node-Editor für KI-Workflows ohne
Tracking — bitte kritisch prüfen

Hallo zusammen,

ich bin der Entwickler von nanoodle und stelle das Projekt hier bewusst
zur kritischen Prüfung vor, nicht als Werbung. Die zwei wichtigsten Fakten
zuerst:

1. **Es ist Open Source (MIT)** und läuft komplett clientseitig — kein
   Server, kein Konto, keinerlei Analytics.
2. **Aber:** Die KI-Inferenz läuft über die API von nano-gpt.com mit
   eigenem Schlüssel (Pay-per-Call). Eingaben verlassen zur Ausführung den
   Browser in Richtung dieses Anbieters. Wer das für sich ausschließt,
   braucht nicht weiterzulesen.

Was es tut: Node-Graph-Editor für KI-Workflows (Text/Bild/Video/Audio) im
Browser; Export als eigenständige Einzeldatei-HTML-App; Teilen per URL,
wobei der Graph im URL-Fragment steckt und nie an einen Server übertragen
wird.

Warum ich glaube, dass es dieses Forum interessieren könnte: Die
Datenschutz-Behauptungen sind technisch nachprüfbar statt nur behauptet —

- CSP ohne Dritt-Origins (Response-Header ansehen; `connect-src` ist auf
  den API-Anbieter beschränkt)
- keine Cookies, kein Fingerprinting, kein Analytics-Code im Quelltext
  (https://github.com/nanoodlecom/nanoodle — die `_headers`-Datei zeigt
  dieselbe CSP im Quellcode)
- Netzwerk-Tab bleibt leer, bis man selbst einen Workflow ausführt

Deutsche Oberfläche: https://nanoodle.com/de/

Was ich mir wünsche: Zerpflückt es. Wenn jemand im Netzwerk-Tab, in der
CSP oder im Quellcode etwas findet, das meinen Aussagen widerspricht,
möchte ich das erfahren und fixen. Auch Meinungen zur grundsätzlichen
Architektur-Entscheidung (kein lokales Modell, dafür null eigene
Datenhaltung) sind willkommen.

Offenlegung: Ich verdiene ggf. über das Referral-Programm des
API-Anbieters, wenn jemand darüber ein Guthaben anlegt. Kein Abo, kein
Aufschlag auf API-Preise, keine Datenverwertung.

Danke fürs kritische Draufschauen!

---

**Submission notes (EN, not part of the posts):**
- Forum post goes up FIRST; only file the Empfehlungsecke proposal after
  the forum thread has run a few days without uncovering a real problem.
- Check the Empfehlungsecke repo's current submission format on Codeberg
  before filing (issue vs. PR) — do not guess the template.
- Log both in `growth/shares.md`.
