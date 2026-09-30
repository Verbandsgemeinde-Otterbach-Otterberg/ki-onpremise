# Testfälle

<!-- Vor Veröffentlichung juristisch gegenprüfen lassen: Zitierweise der elektronischen Form
     (§ 70 Abs. 1 VwGO verweist auf § 3a Abs. 2 VwVfG) sowie die Bewertung eines fehlenden
     Hinweises auf die elektronische Form. -->

## Testfall 1 – „4 Wochen“ statt „1 Monat“

**Fehlerhafte Belehrung**

> Gegen diesen Bescheid kann innerhalb von 4 Wochen nach Bekanntgabe Widerspruch erhoben werden.
> Der Widerspruch ist schriftlich bei der
> Verbandsgemeinde Otterbach-Otterberg, Hauptstr. 27, 67697 Otterberg
> einzulegen.

**Fehler**

- Gesetzlich vorgeschrieben ist eine Monatsfrist (§ 70 Abs. 1 VwGO), keine Wochenfrist.
- „4 Wochen“ sind 28 Tage, ein Monat kann 28, 29, 30 oder 31 Tage haben.
- Eine abweichende Fristangabe macht die Belehrung unrichtig im Sinne des § 58 Abs. 2 VwGO;
  die Widerspruchsfrist beträgt dann ein Jahr.

**Warum der Fall geeignet ist:** Der Fehler ist subtil, weil „4 Wochen“ im Alltag oft synonym
zu „1 Monat“ verwendet wird. Das Modell muss erkennen, dass Wochen und Monate im
Fristenrecht unterschiedlich behandelt werden.

## Testfall 2 – Fristbeginn „ab Bescheiddatum“ statt „nach Bekanntgabe“

**Fehlerhafte Belehrung**

> Gegen diesen Bescheid kann innerhalb eines Monats ab Bescheiddatum Widerspruch erhoben werden.
> Der Widerspruch ist schriftlich bei der
> Verbandsgemeinde Otterbach-Otterberg, Hauptstr. 27, 67697 Otterberg
> einzulegen.
>
> Bescheiddatum: 10. September 2026

**Fehler:** Die Frist beginnt mit der Bekanntgabe (Zugang), nicht mit dem Bescheiddatum.
Ein falscher Fristbeginn macht die Belehrung unrichtig und löst die Jahresfrist aus.

## Referenz (Goldstandard)

> Gegen diesen Bescheid kann innerhalb eines Monats nach Bekanntgabe Widerspruch erhoben werden.
> Der Widerspruch ist schriftlich, in elektronischer Form nach § 3a Abs. 2 des
> Landesverwaltungsverfahrensgesetzes (LVwVfG) oder zur Niederschrift bei der
> Verbandsgemeinde Otterbach-Otterberg, Hauptstr. 27, 67697 Otterberg
> einzulegen.
