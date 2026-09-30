# 2 Was soll das Ergebnis im Februar 2027 sein?

Am Ende soll eine erprobte und dokumentierte Lösung stehen, mit der eine Kommunalverwaltung Sprachmodelle auch für personenbezogene Daten datenschutzkonform einsetzen kann, und dazu Empfehlungen, die andere Kommunen übernehmen können. Drei Leitprinzipien gelten:

**In eigener Hoheit.** Die von der KI verarbeiteten Daten verlassen die eigene bzw. vertraglich abgesicherte Infrastruktur nicht.

**Experimentell.** Erprobt wird offen, was im Verwaltungsalltag taugt und wo die Grenzen liegen. Beides wird dokumentiert.

**Offen und teilbar.** Erkenntnisse, Konfigurationen und Werkzeuge werden als Open Source veröffentlicht, sodass andere sie frei nutzen können.

## 2.1 Ergebnisse zum Projektende

| Ergebnis | Inhalt |
|---|---|
| Referenzlösung | Eine dokumentierte und per Skript nachbaubare Serverlösung mit Sprachmodellen, Rechteverwaltung und abgesicherter Schnittstelle für Fachanwendungen |
| Modell- und Architekturempfehlung | Vergleich frei verfügbarer und kommerzieller Modelle an echten Verwaltungsaufgaben |
| Wirtschaftlichkeitsbetrachtung | Vergleich der Betriebsmodelle eigene Hardware, gemieteter Server, Dienstleister (Managed bzw. SaaS) und Cloud-Dienst, einschließlich der nötigen Servergröße |
| Anwendung Wissensmanagement | Assistenten, die Prozesswissen der Mitarbeitenden erfassen und als Wiki aufbereiten (Phase 3) |
| Open Source | Installationsskripte, Konfigurationen, Prompts und Testfälle im öffentlichen GitHub-Repository |
| Handlungsempfehlungen | Erfahrungen und Empfehlungen für andere Kommunen |
| Abschlussbericht | Bericht an die Entwicklungsagentur Rheinland-Pfalz e.V. |

## 2.2 Phase 3: Wissensmanagement und Wiki (Oktober bis Dezember 2026)

Phase 3 konzentriert sich auf einen Anwendungsfall: Wissen, das bisher nur in den Köpfen der Mitarbeitenden steckt, soll erfasst und für alle nutzbar gemacht werden. Dafür arbeiten mehrere spezialisierte Assistenten zusammen. Einer führt kurze Interviews mit den Mitarbeitenden; wie oft und wie hartnäckig er fragt und in welcher Form, ist einstellbar. Ein zweiter schreibt aus den Antworten Wiki-Artikel. Ein dritter nimmt die Artikel in die Wissensdatenbank auf, damit die Sprachmodelle sie bei Antworten berücksichtigen. Jeder Artikel wird von den Mitarbeitenden geprüft und freigegeben, bevor er erscheint.

Die Anwendung wird selbst entwickelt und mit einer Gruppe von Testanwenderinnen und Testanwendern erprobt. Dabei wird auch ermittelt, bei welchen Einstellungen die Mitarbeitenden am zufriedensten sind. Wenn Zeit bleibt, wird zusätzlich geprüft, ob sich aus Prozessbeschreibungen automatisch Prozessmodelle im Standard BPMN 2.0 erzeugen lassen.

## 2.3 Erweiterung: Interviews im persönlichen Gespräch

Ergänzend soll in Phase 3 das Produkt SpeechMind eingesetzt werden, um Interviews mit Mitarbeitenden im persönlichen Gespräch zu führen. Die von SpeechMind erstellten Protokolle bilden die Grundlage für die weitere Aufbereitung im Wissensmanagement. Wenn die Kapazitäten es zulassen, sollen perspektivisch auch eigene Lösungen mit dem Spracherkennungsmodell Whisper auf eigener Hardware erprobt werden.

## 2.4 Phase 4: Bündeln, dokumentieren, teilen (Januar bis Februar 2027)

Die Ergebnisse aller Phasen werden zusammengeführt, ausgewertet, im GitHub-Repository veröffentlicht und als Handlungsempfehlungen aufbereitet. Der Abschlussbericht an die Entwicklungsagentur Rheinland-Pfalz e.V. schließt das Projekt ab.

---
[← Kapitel 1](01-stand-projektbeginn.md) · [Übersicht](README.md) · [Kapitel 3 →](03-soll-stand-september-2026.md)
