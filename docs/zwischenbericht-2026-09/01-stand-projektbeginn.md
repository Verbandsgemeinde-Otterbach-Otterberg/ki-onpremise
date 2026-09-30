# 1 Wie war der Stand zu Projektbeginn am 1. Juni 2026?

Die Verbandsgemeinde Otterbach-Otterberg im Landkreis Kaiserslautern umfasst zwölf Ortsgemeinden mit rund 19.000 Einwohnerinnen und Einwohnern. Zielgruppe des Projekts sind die rund 100 Mitarbeitenden der Verwaltung.

## 1.1 KI im Arbeitsalltag – mit klarer Grenze

Zum Projektbeginn wurde KI in der Verwaltung bereits genutzt, allerdings ausschließlich über öffentliche Cloud-Dienste.

| Bereich | Stand am 1. Juni 2026 |
|---|---|
| Freigegebene Cloud-Dienste | DeepL, ChatGPT, Copilot, Gemini und NotebookLM, freigegeben für die EU-AI-Act-konforme Nutzung |
| Fachsoftware mit KI | Programme, die über eine Programmierschnittstelle (API) auf Cloud-Modelle wie Claude oder ChatGPT zugreifen |
| Eigenentwicklung | Schadensmelder „behebes“ für Bürgermeldungen, selbst entwickelt, mit KI-Anbindung |
| Qualifizierung | Interne Schulungsreihe „Wissenshäppchen“, parallel zum Projekt und organisatorisch getrennt |

Die Grenze war eindeutig: Personenbezogene und vertrauliche Daten dürfen nicht in öffentliche Cloud-Dienste. Mit den genutzten Diensten war eine datenschutzkonforme Verarbeitung solcher Daten nicht möglich. Gerade die Vorgänge, bei denen KI viel Arbeit abnehmen könnte, blieben deshalb außen vor. Diese Lücke ist der Ausgangspunkt des Projekts.

## 1.2 Vorarbeiten

Das Projekt startete nicht bei null.

**Anbindung und Vergleich.** Sprachmodelle waren bereits über Programmierschnittstellen an verschiedene Systeme angebunden, und kommerzielle Cloud-Modelle wurden miteinander verglichen.

**Anbindung eigener Daten.** Zwei Techniken, mit denen ein Sprachmodell auf eigene Daten und Werkzeuge zugreifen kann, waren bereits mit Cloud-Modellen erprobt: das Model Context Protocol (MCP), ein offener Standard für solche Anbindungen, und eine Vektordatenbank, in der Dokumente so abgelegt werden, dass inhaltlich passende Stellen gefunden werden.

**Selbst betriebene Modelle.** Die frei verfügbaren Modelle Qwen und Mistral wurden über einen Anbieter mit nutzungsabhängiger Abrechnung in einfachen Tests ausprobiert, ausschließlich mit nicht-sensiblen Daten.

**Prototyp des Wissens-Assistenten.** Ein bewusst einfacher Prototyp für den späteren Anwendungsfall Wissensmanagement lief mit einem großen Cloud-Modell. Er zeigte, dass Textarbeit eine Kernstärke der Modelle ist.

**Server.** Seit April 2026 steht dem Projekt ein angemieteter Server mit Grafikprozessor (GPU) beim deutschen Anbieter Hetzner zur Verfügung. Mit Hetzner besteht bereits ein Auftragsverarbeitungsvertrag (AVV). Eigene Sprachmodelle liefen darauf zum Projektbeginn noch nicht.

## 1.3 Personal und Kompetenzen

Das Projekt tragen zwei Personen: der Digitalbeauftragte und ein Fachinformatiker der IT. Programmier- und Linux-Kenntnisse waren vorhanden, Erfahrung mit dem Betrieb von KI-Servern zum Projektbeginn noch nicht.

---
[← Übersicht](README.md) · [Kapitel 2 →](02-ergebnis-februar-2027.md)
