# KI-Sprachmodelle in der kommunalen Verwaltung – datenschutzkonform und selbst betrieben

Beitrag der **Verbandsgemeinde Otterbach-Otterberg** zum Projekt „KI-Sprachmodelle in der kommunalen
Verwaltung“ der Entwicklungsagentur Rheinland-Pfalz e.V. (Juni 2026 – Februar 2027).

Ziel ist, KI auch für sensible, personenbezogene Daten nutzbar zu machen – mit offenen Sprachmodellen
auf eigener bzw. vertraglich abgesicherter Infrastruktur. Mit diesem Repository ist die Lösung
vollständig reproduzierbar.

| Zielgruppe | Einstieg |
|---|---|
| **IT-Fachleute** | [`setup/README.md`](setup/README.md) – Installation per Skript auf einem eigenen GPU-Server |
| **Verantwortliche in der Verwaltung** | [Zwischenbericht](docs/zwischenbericht-2026-09/) – Vorgehen, Ergebnisse, Kosten, Empfehlungen |

## Architektur

```
Browser ──HTTPS──► Nginx ──► Open WebUI (Docker) ──► Auth-Proxy ──► Ollama ──► NVIDIA-GPU
                                                        ▲
                             API-Clients (über VPN, mit Token)
```

| Schicht | Komponente | Aufgabe |
|---|---|---|
| Zugang | Nginx + Let's Encrypt | HTTPS, einziger öffentlicher Einstieg |
| Middleware | Open WebUI | Konten, Gruppen, Modellprofile, Wissenssammlungen, Vektordatenbank |
| API-Schicht | Auth-Proxy (Python) | Token, Modellfreigabe, Schreibschutz, Streaming |
| Inferenz | Ollama (systemd) | Sprach- und Embedding-Modelle, nur lokal erreichbar |
| Hardware | Hetzner GEX44 | NVIDIA RTX 4000 SFF Ada, 20 GB |

## Schnellstart

```bash
git clone https://github.com/Verbandsgemeinde-Otterbach-Otterberg/ki-onpremise.git
cd ki-onpremise/setup && sudo ./install.sh
```

Details: [`setup/README.md`](setup/README.md)

## Inhalt

| Ordner | Inhalt |
|---|---|
| [`docs/zwischenbericht-2026-09/`](docs/zwischenbericht-2026-09/) | Zwischenbericht (September 2026) |
| [`setup/`](setup/) | Installationsskripte, Auth-Proxy, Konfigurationsvorlage, Admin-Werkzeuge |
| [`evaluation/`](evaluation/) | Testfälle, Prompts und Methodik der Modellvergleiche |
| [`tools/`](tools/) | Prüfung auf Geheimnisse, Architekturbild, Erzeugung der Word-Fassung |

## Lizenz

- Quellcode und Konfigurationen: [MIT](LICENSE)
- Dokumentation und Berichte: [CC BY 4.0](LICENSE-docs.md)

Verwendete Modelle unterliegen ihren jeweiligen Lizenzen (u. a. Llama Community License, Gemma Terms of Use, Apache 2.0).

## Kontakt

Verbandsgemeinde Otterbach-Otterberg · Dominik Tröster, Digitalbeauftragter
