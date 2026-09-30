# 6 Welche Stolpersteine traten auf?

## 6.1 Die erste Software passte nicht zum Server

Die zunächst eingesetzte Software vLLM ist für große Rechenzentren mit sehr großen Grafikkarten gebaut. Auf einem Server mit einer einzelnen Karte und 20 GB Grafikspeicher zeigten sich drei Probleme:

**Neue Modelle wurden nicht voll unterstützt.** Für das Modell Gemma 4 hatte vLLM keine eigene Unterstützung und wich auf eine deutlich langsamere Ersatzlösung aus. Die verfügbare komprimierte Fassung des Modells war zudem mit rund 24 GB größer als der gesamte Grafikspeicher.

**Speicher wurde fest reserviert.** vLLM belegt beim Start einen festen Anteil des Grafikspeichers, hier 92 %. Sprachmodell, Embedding-Modell und das Modell zum Sortieren von Suchergebnissen ließen sich deshalb nicht nebeneinander betreiben.

**Viele Teile, viele Fehlerquellen.** Mehrere einzelne Dienste mit einem Vermittler davor führten wiederholt zu Zeitüberschreitungen und Verbindungsfehlern.

Die Umstellung auf Ollama hat alle drei Probleme für diesen Einsatzzweck gelöst.

## 6.2 Rechte lassen sich nicht in der Modellsoftware abbilden

**Das Problem.** In der ersten Anbindung (Stufe 1, Kapitel 5.4) waren die Modelle und die Wissensdatenbank direkt miteinander verbunden: vLLM für die Modelle, Chroma als Wissensdatenbank, davor ein gemeinsamer Zugang (LiteLLM). Der Versuch, Zugriffsrechte direkt in dieser Software festzulegen, scheiterte: Diese Programme kennen weder Benutzer noch Gruppen. Wer überhaupt Zugang hatte, konnte grundsätzlich jede Wissenssammlung abfragen.

Für eine Verwaltung ist das nicht tragbar. Wissen ist dort fast immer an einen Personenkreis gebunden:

- Personalangelegenheiten gehören nur in die Personalabteilung.
- Interne Dienstanweisungen eines Fachbereichs sind nicht für alle bestimmt.
- Die Wissensablage für Auszubildende soll anders aufbereitet sein als das Fachwissen der Sachbearbeitung.
- Eine Fachanwendung wie der Schadensmelder braucht nur ihr eigenes Wissen – und soll auch nur darauf zugreifen können.

Ein gemeinsamer Zugangsschlüssel kann das nicht leisten. Er unterscheidet nur zwischen „darf alles“ und „darf nichts“. Dasselbe gilt für den Auth-Proxy (Kapitel 5.7): Er schützt die Modelle, kennt aber keine Wissenssammlungen und keine Personen.

**Der Lösungsweg: Open WebUI als Vermittlungsschicht (Middleware).** Statt die Rechte in der Modellsoftware nachzubauen, wurde Open WebUI zwischen Nutzende und Modelle gesetzt (Kapitel 5.5). Open WebUI ist nicht nur eine Chat-Oberfläche, sondern verwaltet Konten, Gruppen und Wissenssammlungen und prüft bei jeder Anfrage, wer fragt und worauf diese Person zugreifen darf. Erst danach geht die Anfrage an das Modell.

| Anfrage kommt von … | Weg | Was geprüft wird |
|---|---|---|
| Mitarbeitenden im Browser | Nginx → **Open WebUI** → Auth-Proxy → Ollama | Anmeldung, Gruppenzugehörigkeit, freigegebene Modellprofile und Wissenssammlungen |
| Fachanwendung mit Wissen | Nginx → **Open WebUI** (API-Schlüssel) → Auth-Proxy → Ollama | wie oben – die Anwendung hat ein eigenes Konto und damit genau die Rechte dieses Kontos |
| Fachanwendung ohne Wissen | VPN → Auth-Proxy → Ollama | Schlüssel, freigegebenes Modell, keine Verwaltungsbefehle |

Die Rechte werden damit an genau einer Stelle gepflegt, in einer Software, die dafür gebaut ist. Die Bausteine dahinter bleiben einfach: Ollama rechnet nur, der Auth-Proxy schützt nur.

**Wie Open WebUI den Zugriff einzelner Personen beschränkt.**

| Baustein | Wirkung |
|---|---|
| **Konten** | Jede Person meldet sich mit eigenem Konto an. Neue Konten sind gesperrt, bis die Administration sie freischaltet. |
| **Gruppen** | Konten werden Gruppen zugeordnet, etwa „Bauamt“, „Personal“ oder „Auszubildende“. |
| **Wissenssammlungen** | Jede Sammlung ist entweder privat, für einzelne Gruppen freigegeben oder öffentlich. Lese- und Schreibrechte lassen sich getrennt vergeben: Wer pflegt, muss nicht dieselbe Person sein, die nutzt. |
| **Modellprofile** | Ein Profil verbindet ein Basismodell mit einer Arbeitsanweisung und einer oder mehreren Wissenssammlungen, etwa „Assistent Bauamt“. Das Profil ist nur für die berechtigten Gruppen sichtbar. |
| **Berechtigungen je Gruppe** | Pro Gruppe lässt sich festlegen, ob eigene Dokumente hochgeladen, eigene Sammlungen angelegt oder API-Schlüssel erzeugt werden dürfen. |

So sieht die Personalabteilung ihr Profil mit dem Personalwissen, die Auszubildenden sehen ihre Wissensablage, und keine der beiden Gruppen sieht das Wissen der anderen – obwohl alle dasselbe Modell auf demselben Server nutzen.

**Wie Open WebUI den API-Zugriff rechtemäßig steuert.** Fachanwendungen greifen nicht mit einem Generalschlüssel zu, sondern wie eine Person:

1. Für jede Fachanwendung wird ein eigenes Dienstkonto angelegt und einer Gruppe zugeordnet.
2. Für dieses Konto wird ein API-Schlüssel erzeugt.
3. Die Anwendung sendet ihre Anfragen über die standardisierte Schnittstelle von Open WebUI (kompatibel zur weit verbreiteten OpenAI-Schnittstelle, sodass viele vorhandene Anwendungen ohne Umbau angebunden werden können).
4. Open WebUI behandelt die Anfrage mit genau den Rechten dieses Kontos: Die Anwendung sieht nur die für ihre Gruppe freigegebenen Modellprofile und Wissenssammlungen.

Daraus ergeben sich mehrere Vorteile:

- **Geringste Rechte:** Jede Anwendung bekommt nur, was sie braucht. Der Schadensmelder kommt nicht an Personalwissen.
- **Einzeln widerrufbar:** Wird eine Anwendung abgeschaltet oder ein Schlüssel bekannt, wird genau dieser Schlüssel gesperrt; alle anderen laufen weiter.
- **Nachvollziehbar:** Anfragen sind einem Konto zugeordnet, nicht einem anonymen gemeinsamen Schlüssel.
- **Einheitlich:** Für Menschen und Anwendungen gelten dieselben Regeln. Wer eine Wissenssammlung für eine Gruppe freigibt, gibt sie damit auch den Anwendungen dieser Gruppe frei.
- **Zusätzlich eingrenzbar:** Die Administration kann API-Schlüssel insgesamt abschalten, auf bestimmte Gruppen beschränken und festlegen, welche Funktionen der Schnittstelle mit einem Schlüssel erreichbar sind.

**Was dabei zu beachten ist.** Die Rechte gelten nur, solange jeder Zugriff über Open WebUI läuft. Die Wissensdatenbank liegt deshalb innerhalb von Open WebUI und ist von außen nicht erreichbar, Ollama nur intern (Kapitel 4.4). Der direkte Weg über den Auth-Proxy bleibt Anwendungen vorbehalten, die kein Wissen aus der Datenbank brauchen. Die Administration sieht technisch alle Sammlungen; die Zahl der Administratorkonten ist daher klein zu halten. Die Modellprofile je Zielgruppe sind auf einem Testsystem erprobt; auf dem produktiven Server folgt die Übertragung mit dem Ausbau der Testgruppe (Kapitel 4.4).

**Aufwand.** Der Umbau auf Open WebUI als Vermittlungsschicht kostete rund zwei zusätzliche Wochen, einschließlich Neuinstallation der Plattform. Der Aufwand hat sich gelohnt: Ohne diese Schicht wäre eine Wissensdatenbank nur für Inhalte möglich, die alle sehen dürfen. Anderen Kommunen empfehlen wir, die Rechteschicht von Anfang an einzuplanen, statt sie nachträglich einzuziehen.

## 6.3 Ständig neue Modelle

Während der Projektlaufzeit erschienen laufend neue, frei verfügbare Modelle, darunter Gemma 4. Jedes neue Modell warf die Frage auf, ob es besser ist, und erforderte neue Tests. Die Modellauswahl und das wiederholte Testen haben am meisten Zeit gekostet. Hinzu kommt, dass Modellversion, Kompression und Betriebssoftware die Ergebnisse beeinflussen; alles muss sauber dokumentiert werden, damit Ergebnisse vergleichbar bleiben.

## 6.4 Immer nur ein größeres Modell zur Zeit

Auf 20 GB Grafikspeicher passt jeweils ein größeres Modell. Mehrere Modelle gleichzeitig anzubieten, etwa ein schnelles für einfache Fragen und ein starkes für juristische Texte, ist auf diesem Server nicht möglich. Daraus entstanden das Werkzeug zum Modellwechsel und die Modellfreigabe im Auth-Proxy.

## 6.5 Verarbeitungsumfang muss ausdrücklich eingestellt werden

Die Voreinstellungen der Programme lassen oft nur kurze Texte zu. Für Verwaltungstexte mit Quellen aus der Wissensdatenbank reicht das nicht. Der Umfang muss ausdrücklich erhöht werden (hier auf 16.384 Token, rund 20 Seiten) und auf dem gesamten Weg zusammenpassen; sonst werden Texte unbemerkt gekürzt.

## 6.6 Vorhandene Dokumente aufbereiten

Vorhandene Dokumentationen liegen in vielen Formaten und Qualitäten vor. Sie so aufzubereiten, dass das System passende Stellen zuverlässig findet, war aufwendiger als erwartet. Werkzeuge helfen bei der Umwandlung, ersetzen aber nicht die inhaltliche Durchsicht (Kapitel 5.9). MarkItDown überträgt Texte getreu, liest eingescannte Seiten aber erst mit einer zusätzlichen Texterkennung (hier Tesseract) und verliert bei komplizierten Layouts Struktur. Solche Dokumente müssen nachbearbeitet oder neu erfasst werden. obsidian-llm-wiki ordnet verstreutes Wissen, doch die Seiten schreibt ein Sprachmodell. Jede Seite muss deshalb fachlich geprüft werden, bevor sie in die Wissensdatenbank kommt.

## 6.7 Lieferzeiten für eigene Hardware

Eigene Server mit Grafikkarte hätten den Start um Monate verzögert. Die Option bleibt für eine spätere Phase bestehen.

## 6.8 Zu wenige Testfälle aus der Praxis

Für den Test mit dem Schadensmelder standen nur 12 echte Meldungen zur Verfügung. Das reicht für keine belastbare Aussage. Aussagekräftige Vergleiche brauchen ausreichend viele, praxisnahe Testfälle.

---
[← Kapitel 5](05-arbeitspakete-und-vorgehen.md) · [Übersicht](README.md) · [Kapitel 7 →](07-foerderliche-faktoren.md)
