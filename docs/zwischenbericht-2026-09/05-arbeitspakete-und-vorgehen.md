# 5 Welche Arbeitspakete wurden bisher erledigt? Und wie wurde dabei vorgegangen?

Dieses Kapitel beschreibt den Weg vom leeren Server zur heutigen Lösung. Die Lösung entstand in drei Stufen; jede Stufe hat ein konkretes Problem der vorherigen gelöst.

> **Die Ergebnisse sind reproduzierbar.** Installationsskripte, Konfigurationen, der selbst entwickelte Auth-Proxy, Prüfaufträge und Testfälle sind im GitHub-Repository [Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise) veröffentlicht. Wiki-Kern und Verarbeitungskette der Wissensablage (Kapitel 5.11) folgen mit dem Abschlussbericht. Dieser Bericht beschreibt, **was** gemacht wurde und **warum**; das Repository enthält, **wie** es technisch umgesetzt ist. Es richtet sich an die IT-Fachleute, die die Lösung aufbauen.

## 5.1 Team, Aufwand und Vorgehensweise

Die Lösung haben zwei Personen aufgebaut: der Digitalbeauftragte und ein Fachinformatiker der IT. Bis zur Rechteverwaltung über Open WebUI flossen rund 60 Arbeitsstunden in den Aufbau, einschließlich erster Versuche für die Oberfläche der Wissensablage. Seitdem ist weiterer Aufwand hinzugekommen, der nicht gesondert erfasst wurde.

Gearbeitet wurde überwiegend mit den offiziellen Anleitungen der eingesetzten Open-Source-Projekte. KI-Assistenten (ChatGPT, Codex und die eigenen Modelle) wurden nur punktuell genutzt.

## 5.2 Zeitleiste

| Zeitraum | Schritt |
|---|---|
| April 2026 | Gemieteter GPU-Server steht dem Projekt zur Verfügung; Vorarbeiten |
| Ende Juni 2026 | Grafikkartentreiber installiert, Beginn des Betriebs eigener Modelle |
| Mitte Juli 2026 | **Stufe 1:** erste Modelle laufen mit der Software vLLM |
| Ende Juli 2026 | **Stufe 2:** Neuaufbau mit Open WebUI als Schicht für Konten und Rechte |
| September 2026 | **Stufe 3:** Umstieg auf die Software Ollama, eigener Auth-Proxy, privates Netz für Fachanwendungen |
| Mitte September 2026 | Freigabe für erste Testnutzerinnen und Testnutzer |

Bis zum ersten laufenden Modell vergingen rund zwei Wochen, bis zur funktionierenden Rechteverwaltung weitere zwei Wochen.

## 5.3 Arbeitspaket 1: Infrastruktur und Betriebsmodelle

**Entscheidung.** Eigene Hardware im Haus kam für den Start nicht in Frage, weil die Lieferzeiten für Grafikkarten einer kurzfristigen Umsetzung entgegenstanden. Gewählt wurde ein gemieteter Server beim deutschen Anbieter Hetzner, Modell GEX44. Den Ausschlag gaben der bereits bestehende Auftragsverarbeitungsvertrag, weitere dort betriebene Dienste der Verwaltung und die gute Erfahrung mit dem Anbieter.

| Merkmal | Hetzner GEX44 |
|---|---|
| Rechenleistung | Intel Core i5-13500 (14 Kerne), 64 GB Arbeitsspeicher |
| Grafikkarte | NVIDIA RTX 4000 SFF Ada mit 20 GB Grafikspeicher |
| Datenspeicher | 2 × 1,92 TB, gespiegelt gegen Ausfall einer Platte |
| Kosten | rund 232 €/Monat zzgl. rund 114 € einmalig (Stand Anfang August 2026) |

Als zweites Betriebsmodell wurde ein Testzugang bei Orgasoft Kommunal genutzt (Kapitel 4.5).

## 5.4 Arbeitspaket 2: Stufe 1 – erste Modelle mit vLLM (Juni bis Juli)

**Vorgehen.** Der erste Ansatz folgte dem ursprünglichen Konzept: die Software vLLM, die für hohe Leistung ausgelegt ist, direkt auf dem Server. Für jedes Modell lief ein eigener Dienst – je einer für Llama 3.2, Qwen3-14B, das Bildmodell BakLLaVA, das Embedding-Modell und ein Modell zum Sortieren von Suchergebnissen. Ein vorgeschalteter Vermittler (LiteLLM) fasste sie unter einer gemeinsamen Schnittstelle zusammen. Als Wissensdatenbank diente Chroma.

**Ergebnis.** Die Modelle liefen; in dieser Stufe entstanden die Testergebnisse für Llama 3.2 und Qwen3-14B (Kapitel 4.6).

**Problem.** Für die Verwaltung fehlte etwas Grundlegendes: Unterschiedliche Wissensbestände ließen sich nicht unterschiedlichen Personenkreisen mit unterschiedlichen Rechten bereitstellen. vLLM und Chroma kennen keine Benutzer.

## 5.5 Arbeitspaket 3: Stufe 2 – Open WebUI als Rechteschicht (Ende Juli)

**Vorgehen.** Beim Ausprobieren von Open WebUI entstand der Ansatz, die Software nicht nur als Oberfläche, sondern als Vermittlungsschicht zwischen Nutzenden und Modellen zu verwenden. Open WebUI verwaltet Konten und Gruppen, legt Wissenssammlungen an und verbindet sie mit Modellprofilen, die sich auf bestimmte Gruppen beschränken lassen. Diese Profile stehen auch Fachanwendungen zur Verfügung. Die Rechteverwaltung liegt damit in einer Software, die dafür gebaut ist.

Die Plattform wurde daraufhin neu installiert. Open WebUI läuft seitdem als Container (ein abgeschlossenes, leicht aktualisierbares Softwarepaket). Davor sitzt der Webserver Nginx, der die Verbindung mit einem kostenlosen Zertifikat von Let's Encrypt verschlüsselt. Open WebUI selbst ist von außen nicht direkt erreichbar.

**Im Repository:** Start des Containers in [`setup/bin/llm-webui-run`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/bin/llm-webui-run), Webserver-Konfiguration in [`setup/files/nginx-site.conf`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/files/nginx-site.conf).

## 5.6 Arbeitspaket 4: Stufe 3 – Umstieg auf Ollama (September)

**Anlass.** Mit dem neuen Modell Gemma 4 stieß vLLM auf dem Server an Grenzen (Einzelheiten in Kapitel 6.1).

**Entscheidung.** Die Modelle laufen seitdem mit der Software Ollama. Ollama ist einfacher zu betreiben, lädt Modelle bei Bedarf und gibt den Speicher wieder frei. Es wird direkt auf dem Server betrieben, nicht in einem Container, und ist nur intern erreichbar.

**Wichtige Einstellungen.** Jedes Modell verarbeitet bis zu 16.384 Token auf einmal. Ein Modell bleibt zehn Minuten nach der letzten Anfrage im Speicher und wird dann entladen. Neben dem Sprachmodell darf das Embedding-Modell gleichzeitig geladen sein.

**Ergebnis.** Gemma 4 läuft vollständig auf der Grafikkarte, belegt rund 14,8 GB und lässt etwa 5 GB Reserve. Die Testergebnisse für Gemma 4 (Kapitel 4.6) entstanden in dieser Stufe.

**Im Repository:** Installation und Einstellungen in [`setup/steps/20-ollama.sh`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/steps/20-ollama.sh), Laden der Modelle in [`setup/steps/30-models.sh`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/steps/30-models.sh).

## 5.7 Arbeitspaket 5: Abgesicherte Schnittstelle für Fachanwendungen

**Anlass.** Fachanwendungen sollen die Modelle auch direkt nutzen können, ohne Umweg über die Weboberfläche. Die Software Ollama selbst prüft aber weder, wer zugreift, noch was angefragt wird.

**Abgrenzung.** Dieser direkte Weg ist für Anwendungen gedacht, die kein Wissen aus der Datenbank brauchen. Anwendungen, die auf Wissenssammlungen zugreifen, werden wie Personen über ein eigenes Dienstkonto in Open WebUI angebunden, damit die Gruppenrechte greifen (Kapitel 6.2).

**Lösung.** Zwischen Open WebUI und Ollama sitzt ein selbst entwickelter Auth-Proxy, ein kleines Programm mit rund 200 Zeilen, das wie ein Türsteher arbeitet:

| Aufgabe | Umsetzung |
|---|---|
| Zugang | Nur mit gültigem Schlüssel; ohne Schlüssel darf nur Open WebUI selbst zugreifen |
| Schutz | Anfragen an die Modelle sind erlaubt; Modelle laden, kopieren oder löschen ist gesperrt |
| Freigabe | Nur das freigegebene Sprachmodell und das Embedding-Modell sind sichtbar und nutzbar |
| Tempo | Antworten werden sofort Wort für Wort weitergegeben, nicht erst am Ende |
| Datenschutz | Protokolliert werden Zeitpunkt, Art der Anfrage, Modell und Ergebnis, keine Inhalte |
| Erreichbarkeit | Nur intern und über ein privates, verschlüsseltes Netz (VPN, hier Tailscale), nie öffentlich |

**Im Repository:** Quellcode in [`setup/files/llm-proxy.py`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/files/llm-proxy.py), Einrichtung in [`setup/steps/50-proxy.sh`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/steps/50-proxy.sh) und [`setup/steps/80-tailscale.sh`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/steps/80-tailscale.sh).

## 5.8 Arbeitspaket 6: Modellauswahl und Modellbetrieb

**Auswahl.** Neben den eingesetzten Modellen standen Phi-4, Llama 3.1 und BakLLaVA zur Wahl. Die Kriterien waren gutes Deutsch, ausreichende Geschwindigkeit auf dem vorhandenen Server und mindestens 16.000 Token Verarbeitungsumfang.

**Modell wechseln.** Auf 20 GB Grafikspeicher passt jeweils ein größeres Modell. Ein kleines Werkzeug gibt ein anderes Modell frei, entfernt die übrigen aus dem Speicher und lädt das neue vorab, damit die erste Anfrage nicht warten muss. Open WebUI zeigt danach automatisch nur das freigegebene Modell an; ein Neustart ist nicht nötig.

**Aktualisieren.** Open WebUI wird per Skript aktualisiert, das vorher die Datenbank mit allen Konten und Einstellungen sichert.

**Im Repository:** [`setup/bin/llm-model-switch`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/bin/llm-model-switch) und [`setup/bin/llm-webui-update`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/bin/llm-webui-update).

## 5.9 Arbeitspaket 7: Wissensdatenbank aufbauen

Vorhandene Dokumente liegen in vielen Formaten vor, etwa PDF, Word oder Webseiten. Für die Wissensdatenbank werden sie zunächst in einfache Textdateien (Markdown) umgewandelt. Markdown ist reiner Text mit wenigen Zeichen für Überschriften, Listen und Tabellen. Sprachmodelle können es besonders gut verarbeiten, und die Gliederung eines Dokuments bleibt erhalten. So findet die Wissensdatenbank später passende Abschnitte zuverlässiger als in einem unaufbereiteten PDF.

Erprobt wurden zwei Werkzeuge mit unterschiedlichem Zweck, beide mit guten Ergebnissen.

**Microsoft MarkItDown – Dokumente umwandeln.** MarkItDown ist ein kostenloses Open-Source-Werkzeug von Microsoft (MIT-Lizenz). Es wandelt Dateien in Markdown um und behält dabei Überschriften, Listen, Tabellen und Verweise bei.

| Merkmal | MarkItDown |
|---|---|
| Aufgabe | Umwandlung, ohne Inhalte zu verändern: Aus einem Gesetzestext wird derselbe Gesetzestext als Markdown |
| Eingabeformate | u. a. PDF, Word, Excel, PowerPoint, Webseiten (HTML), CSV, JSON, XML, E-Books, ZIP-Archive |
| Bedienung | über die Kommandozeile, z. B. `markitdown gemo.pdf > gemo.md`, oder als Baustein in eigenen Skripten (Python); viele Dateien lassen sich so in einem Durchgang umwandeln |
| Datenschutz | Die Grundfunktionen laufen vollständig auf dem eigenen Rechner, ohne KI und ohne Internet |
| Grenzen | Eingescannte Seiten ohne hinterlegten Text liest MarkItDown erst mit einer zusätzlichen Texterkennung; bei komplizierten Layouts, etwa mehrspaltigen Seiten oder verschachtelten Tabellen, geht Struktur verloren |

MarkItDown bietet optional Zusatzfunktionen über Cloud-Dienste an, etwa Microsoft Azure für die Texterkennung in Scans oder die Bildbeschreibung über OpenAI. Diese Zusatzfunktionen wurden bewusst nicht genutzt, weil dabei Inhalte den eigenen Server verlassen würden. Für eingescannte Unterlagen wurde stattdessen die frei verfügbare Texterkennung Tesseract eingebunden, die vollständig lokal arbeitet (Kapitel 5.11). Für die Sammlung Verwaltungsrecht war MarkItDown das passende Werkzeug: Die Gesetze liegen als Text-PDF oder Webseite vor und sollen unverändert in die Wissensdatenbank.

**obsidian-llm-wiki – Wissen zu einem Wiki verdichten.** obsidian-llm-wiki setzt einen anderen Ansatz um, das sogenannte „LLM-Wiki“. Es wandelt Dokumente nicht nur um, sondern lässt ein Sprachmodell daraus ein verknüpftes Nachschlagewerk schreiben. Die Ergebnisse sind Markdown-Dateien, die sich mit dem kostenlosen Notizprogramm Obsidian lesen und bearbeiten lassen.

| Merkmal | obsidian-llm-wiki |
|---|---|
| Aufgabe | Aufbereitung: Das Modell erkennt in Notizen und Dokumenten die wichtigen Begriffe, Zuständigkeiten und Abläufe und legt zu jedem eine eigene Wiki-Seite an |
| Ergebnis | Wiki-Seiten mit Querverweisen, z. B. von „Posteingang“ auf „Fristenkontrolle“ und „Zuständigkeiten“; die Ausgangsdokumente bleiben unverändert |
| Weiterpflege | Neue Dokumente werden in die vorhandenen Seiten eingearbeitet, statt ein zweites, widersprüchliches Dokument danebenzulegen |
| Datenschutz | Kann mit einem Modell auf dem eigenen Server (Ollama) betrieben werden; Cloud-Anbieter sind möglich, kommen für interne Inhalte aber nicht in Frage |
| Grenzen | Die Seiten schreibt ein Sprachmodell. Sie können Fehler oder Lücken enthalten und müssen vor der Freigabe fachlich geprüft werden |

Dieser Ansatz passt zu Wissen, das verstreut in Notizen, E-Mails und Einzeldokumenten steckt, etwa Abläufe im Posteingang oder am Empfang. Er ist die Vorstufe für Phase 3, in der der Interview-Assistent Wissen erfragt und daraus Wiki-Artikel entstehen (Kapitel 2.2).

**Welches Werkzeug wofür?**

| Ausgangslage | Werkzeug |
|---|---|
| Fertige, verbindliche Texte (Gesetze, Satzungen, Dienstanweisungen), die wörtlich erhalten bleiben müssen | MarkItDown |
| Verstreutes Erfahrungswissen, das erst geordnet und verknüpft werden muss | obsidian-llm-wiki |

**Übernahme in die Wissensdatenbank.** Die Markdown-Dateien werden in Open WebUI als Wissenssammlung hochgeladen. Open WebUI zerlegt sie in Abschnitte und lässt sie vom Embedding-Modell auf dem eigenen Server übersetzen. Wer die Sammlung sehen darf, wird dabei über die Gruppenrechte festgelegt (Kapitel 6.2).

## 5.10 Arbeitspaket 8: Modellvergleich

**Testfälle.** Als Aufgabe dienten zwei fehlerhafte Rechtsbehelfsbelehrungen:

1. **„4 Wochen“ statt „1 Monat“.** Vorgeschrieben ist eine Monatsfrist (§ 70 Abs. 1 VwGO). Der Fehler ist schwer zu erkennen, weil „4 Wochen“ im Alltag oft wie „ein Monat“ verwendet wird. Eine abweichende Fristangabe macht die Belehrung unrichtig (§ 58 Abs. 2 VwGO); die Widerspruchsfrist beträgt dann ein Jahr.
2. **Fristbeginn „ab Bescheiddatum“ statt „nach Bekanntgabe“.** Die Frist beginnt mit der Bekanntgabe, nicht mit dem Datum des Bescheids. Auch das führt zur Jahresfrist.

**Prüfauftrag.** Alle Modelle erhielten denselben Auftrag: die Belehrung auf den richtigen Rechtsbehelf, Fristdauer, Fristbeginn, vollständige Formangaben, zuständige Behörde und irreführende Zusätze zu prüfen und eine Fehlerliste mit Begründung und Norm, die Rechtsfolge und einen Korrekturvorschlag auszugeben.

**Durchführung.** Jedes Modell erhielt 100 Anfragen. Bewertet wurde von Hand nach zwei Kennzahlen: Wurde der Fehler erkannt bzw. beseitigt, und stand am Ende eine vollständig korrekte Belehrung? Llama 3.2 und Qwen3-14B liefen noch in Stufe 1, Gemma 4 in Stufe 3. Die kommerziellen Cloud-Modelle erhielten ausschließlich diese erfundenen Testfälle.

**Behebes.** Für die Einordnung von Bürgermeldungen wurden alle bis dahin eingegangenen Meldungen anonymisiert und mit der Arbeitsanweisung der Anwendung über den Testzugang des Dienstleisters verarbeitet.

**Im Repository:** Prüfauftrag im Wortlaut und Testfälle unter [`evaluation/rechtsbehelfe/`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/tree/main/evaluation/rechtsbehelfe). Andere Kommunen können den Test damit unverändert mit eigenen Modellen wiederholen.

## 5.11 Arbeitspaket 9: Wissensablage für Auszubildende

**Anlass.** Die neuen Auszubildenden brauchten zum Ausbildungsbeginn verlässliche Anleitungen für den zentralen Posteingang und Rechnungseingang sowie für den zentralen Empfang und die Infotheke. Dieses Wissen lag bisher vor allem in Notizen und Handzetteln der Sachbearbeitung vor, uneinheitlich und über viele Unterlagen verteilt.

**Vorgehen: vom Handzettel zur Wiki-Seite.** Die Anleitungen entstanden in einer Verarbeitungskette, die die in Kapitel 5.9 beschriebenen Werkzeuge kombiniert:

| Schritt | Werkzeug | Ergebnis |
|---|---|---|
| 1. Sammeln | – | Notizen und Handzettel der Sachbearbeitung, eingescannt |
| 2. Texterkennung und Umwandlung | Microsoft MarkItDown mit der Texterkennung Tesseract (OCR), beide lokal | Einheitliche Markdown-Dateien aus den gescannten Seiten |
| 3. Verdichten | obsidian-llm-wiki mit Gemma 4 auf dem eigenen Server | Geordnete, verknüpfte Anleitungen je Ablauf, z. B. „Rechnungen scannen“ |
| 4. Prüfen und freigeben | Sachbearbeitung | Fachlich abgenommene Anleitungen |
| 5. Ablegen | Wiki-Kern („Wikicore“) | Nach Fachbereich getrennte Markdown-Dateien, Zugriff nur nach Anmeldung |

Die Reihenfolge folgt aus den Stärken der Werkzeuge: MarkItDown liest eingescannte Seiten nur mit zusätzlicher Texterkennung (Kapitel 5.9); deshalb wurde Tesseract eingebunden. obsidian-llm-wiki ist genau für verstreutes Erfahrungswissen gedacht, das erst geordnet und verknüpft werden muss. Die gesamte Kette läuft ohne Cloud-Dienste: Texterkennung und Umwandlung lokal, das Sprachmodell auf dem eigenen Server. Auch interne Arbeitsnotizen verlassen damit die eigene Infrastruktur nicht.

**Erfahrung.** Die Kette zeigt, dass sich vorhandenes, unstrukturiertes Wissen in nutzbare Anleitungen überführen lässt. Die Sachbearbeiterinnen und Sachbearbeiter haben jede erzeugte Seite fachlich abgenommen, wie es für Texte eines Sprachmodells nötig ist (Kapitel 6.6). Die Auszubildenden haben anschließend erfolgreich mit den Anleitungen gearbeitet.

**Ausblick.** In Phase 3 kommt als zweite Quelle der Interview-Assistent hinzu, der Wissen im Gespräch erfragt. Wiki-Kern und Verarbeitungskette werden zusammen mit ihm im Abschlussbericht dokumentiert und im Repository veröffentlicht.

## 5.12 Nachbau mit dem GitHub-Repository

Die Serverlösung ist mit dem Repository [Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise) reproduzierbar. Die Installation ist in zehn Schritte gegliedert, die ein einziges Skript nacheinander ausführt. Alle Einstellungen stehen in einer zentralen Konfigurationsdatei; jeder Schritt prüft seine Voraussetzungen und kann gefahrlos wiederholt werden. Am Ende prüft das Skript automatisch, ob alle Schutzmechanismen greifen.

| Schritt | Was passiert | Datei im Repository |
|---|---|---|
| 0 | Voraussetzungen prüfen, Zugangsschlüssel erzeugen | `setup/steps/00-preflight.sh` |
| 1 | Treiber für die Grafikkarte installieren, danach Neustart | `setup/steps/10-nvidia.sh` |
| 2 | Ollama einrichten, nur intern erreichbar | `setup/steps/20-ollama.sh` |
| 3 | Sprachmodelle und Embedding-Modell herunterladen | `setup/steps/30-models.sh` |
| 4 | Container-Umgebung (Docker) mit eigenem internen Netz | `setup/steps/40-docker.sh` |
| 5 | Auth-Proxy und Werkzeug zum Modellwechsel | `setup/steps/50-proxy.sh` |
| 6 | Open WebUI starten | `setup/steps/60-openwebui.sh` |
| 7 | Webserver mit verschlüsselter Verbindung | `setup/steps/70-nginx-tls.sh` |
| 8 | Optional: privates Netz (VPN) für Fachanwendungen | `setup/steps/80-tailscale.sh` |
| 9 | Automatische Prüfung von Funktion und Sicherheit | `setup/steps/90-verify.sh` |

**Was die IT dafür braucht:** einen Server mit NVIDIA-Grafikkarte und dem Betriebssystem Debian 13, eine eigene Internetadresse (Domain) und einen Auftragsverarbeitungsvertrag mit dem Anbieter. Die Anleitung für IT-Fachleute steht in [`setup/README.md`](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise/blob/main/setup/README.md).

---
[← Kapitel 4](04-ist-stand-september-2026.md) · [Übersicht](README.md) · [Kapitel 6 →](06-stolpersteine.md)
