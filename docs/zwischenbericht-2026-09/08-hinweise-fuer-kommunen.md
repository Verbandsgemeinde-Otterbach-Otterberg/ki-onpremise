# 8 Was sollten andere Kommunen im Blick haben?

## 8.1 Für Verantwortliche in der Verwaltung

**Es muss nicht bei null beginnen.** Die Lösung aus diesem Projekt ist mit dem GitHub-Repository [Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise](https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise) reproduzierbar. Installationsskripte, Einstellungen, Prüfaufträge und Testfälle stehen dort frei zur Verfügung. Die eigene IT kann damit direkt beginnen, statt die Lösung neu zu entwickeln.

**Mit gemieteter Hardware starten.** Eigene Server mit Grafikkarte haben lange Lieferzeiten. Ein gemieteter Server bei einem Anbieter mit Auftragsverarbeitungsvertrag ist in wenigen Tagen verfügbar und kostet in der hier genutzten Größe rund 232 € im Monat. Über eigene Hardware lässt sich später auf Grundlage echter Nutzungsdaten entscheiden.

**Frei verfügbare Modelle sind konkurrenzfähig.** Bei einer anspruchsvollen Prüfaufgabe erreichte ein frei verfügbares Modell auf dem eigenen Server 96 % korrekte Ergebnisse, die kommerziellen Spitzenmodelle 100 %. Kleine Modelle reichen für solche Aufgaben dagegen nicht.

**Personal einplanen.** Zwei Personen mit Programmier- und Linux-Kenntnissen haben die Lösung aufgebaut. Mit dem Repository verringert sich der Aufwand deutlich, ganz ohne technisches Know-how im Haus geht es aber nicht. Wer den Aufwand von Beginn an erfasst, kann ihn später in der Wirtschaftlichkeitsbetrachtung belastbar ausweisen.

**Testzugänge ohne AVV nur mit anonymisierten Daten.** Testzugänge bei Dienstleistern ohne Auftragsverarbeitungsvertrag dürfen nur mit anonymisierten oder nicht-personenbezogenen Daten genutzt werden.

**Mit praxisnahen, anspruchsvollen Aufgaben testen.** Aussagekräftig sind Aufgaben, bei denen ein Modell einen schwer erkennbaren Fehler finden muss, nicht einfache Beispielfragen. Die Prüfaufträge aus diesem Projekt können dafür übernommen werden. Ergebnisse aus wenigen Testfällen sollten als vorläufig gelten.

**Aufbereitung der Dokumente einplanen.** Damit die KI verlässlich auf eigenes Wissen zugreift, müssen vorhandene Dokumente aufbereitet werden. Das kostet Zeit und braucht fachliche Durchsicht.

**Vorhandene Notizen nutzen.** Viel Wissen steckt bereits in Notizen und Handzetteln der Sachbearbeitung. Mit lokaler Texterkennung und einem Sprachmodell auf eigenem Server lassen sich daraus strukturierte Anleitungen erzeugen, ohne bei null anzufangen. Im Projekt wurden die so erzeugten Anleitungen von der Sachbearbeitung fachlich abgenommen und von Auszubildenden erfolgreich genutzt. Die fachliche Abnahme jeder Seite bleibt dabei unverzichtbar.

**Einen konkreten Anwendungsfall wählen.** Ein echter Bedarf mit echten Nutzerinnen und Nutzern, wie hier die Wissensablage für Auszubildende, treibt ein Projekt stärker voran als eine allgemeine Erprobung.

## 8.2 Hinweise für die IT

**Rechte in die Oberfläche, nicht in die Modellsoftware.** Die Software, die die Modelle betreibt, kennt keine Benutzer. Konten, Gruppen, Wissenssammlungen und Modellprofile gehören in eine Schicht wie Open WebUI. Die Modellsoftware selbst sollte nur intern erreichbar sein.

**Schnittstellen für Fachanwendungen absichern.** Anwendungen, die auf Wissensbestände zugreifen, sollten wie Personen angebunden werden: mit eigenem Dienstkonto und eigenem Schlüssel in der Rechteschicht, damit dieselben Gruppenrechte gelten. Direkte Zugriffe auf die Modelle ohne Wissensbestände brauchen eine vorgeschaltete Prüfung mit Schlüssel, die Verwaltungsbefehle wie das Laden oder Löschen von Modellen sperrt. Der Auth-Proxy im Repository ist dafür ein erprobtes Beispiel.

**Auf einem einzelnen, kleineren Server ist Ollama einfacher als vLLM.** vLLM spielt seine Stärken auf großen Grafikkarten mit hohem Durchsatz aus. Bei 20 GB Grafikspeicher, wechselnden Modellen und neuen Modellarchitekturen war Ollama deutlich einfacher und stabiler.

**Der Grafikspeicher ist die knappe Ressource.** Er bestimmt, welche Modelle laufen und wie viele Anfragen gleichzeitig möglich sind. Modelle nach dem Prinzip „Mixture of Experts“ wie Gemma 4 verbinden hohe Qualität mit hoher Geschwindigkeit.

**Verarbeitungsumfang ausdrücklich einstellen.** Voreinstellungen sind für Verwaltungstexte oft zu klein; der eingestellte Wert muss auf dem ganzen Weg zusammenpassen.

**Container-Ports nie öffentlich freigeben.** Docker leitet öffentlich freigegebene Ports an der Firewall des Servers vorbei. Container sollten nur intern erreichbar sein und über einen Webserver nach außen gegeben werden.

> „Wir sind dort gestartet, wo wir schon standen. Dadurch konnten wir an einer echten, anspruchsvollen Aufgabe zeigen, dass ein frei verfügbares, selbst betriebenes Modell fast an die kommerzielle Spitze heranreicht, ohne dass personenbezogene Daten unsere Infrastruktur verlassen. Mit dem Repository kann jede Kommune diesen Weg nachgehen.“
>
> — Dominik Tröster, Digitalbeauftragter der Verbandsgemeinde Otterbach-Otterberg

---
[← Kapitel 7](07-foerderliche-faktoren.md) · [Übersicht](README.md)
