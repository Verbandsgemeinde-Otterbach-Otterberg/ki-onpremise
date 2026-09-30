# Werkzeuge

| Werkzeug | Zweck |
|---|---|
| `check-secrets.sh` | Prüft vor jedem Push auf API-Keys, Passwörter, E-Mail- und öffentliche IP-Adressen |
| `make-diagram.py` | Zeichnet das Architekturbild des Berichts (benötigt Pillow) |
| `build-docx.sh` | Erzeugt die Word-Fassung des Berichts aus den Markdown-Kapiteln (benötigt pandoc) |
| `docx/` | Titelblatt, Formatvorlage und Nachbearbeitung für die Word-Fassung |

Die Word-Fassung liegt nicht im Repository, sondern wird als Anhang an ein GitHub-Release gehängt.
