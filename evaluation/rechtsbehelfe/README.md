# Benchmark: Korrektur fehlerhafter Rechtsbehelfsbelehrungen

## Methode

- **Testfälle:** zwei fehlerhafte Rechtsbehelfsbelehrungen, siehe [testfaelle.md](testfaelle.md)
- **Prompt:** für alle Modelle identisch, siehe [prompt.md](prompt.md)
- **Umfang:** 100 Anfragen je Modell
- **Bewertung:** manuell, nach zwei Kennzahlen
  1. Fehler erkannt bzw. beseitigt
  2. korrektes Endergebnis (vollständig richtige Belehrung)

## Laufzeitumgebungen

| Modell | Umgebung |
|---|---|
| Llama 3.2 3B | vLLM auf Hetzner GEX44 |
| Qwen3-14B | vLLM auf Hetzner GEX44 |
| Gemma 4 26B-A4B | Ollama (nativer Dienst) auf Hetzner GEX44 |
| Cloud kommerziell (GPT-5.6, Claude) | Cloud-API, ausschließlich mit den fiktiven Testfällen |

Die Ergebnisse stehen im Zwischenbericht, Kapitel 4.6.
