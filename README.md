# Credits and Debits Expen

## Overview

This document outlines the structure and formulas used in the Credits and Debits sheets to manage and maintain balances based on amounts earned and spent.

### Credits Sheet

#### Columns

* Name: The name of the person.
* Date: The date of the event.
* Start time: The start time of the event.
* End time: The end time of the event.
* Amount made: The amount earned, calculated based on the duration.
* Balance: The cumulative balance after accounting for earnings and spendings.
* Duration: The duration of the event in hours.

##### Formulas

* Amount made:
* = G2 * 20
This formula calculates the amount earned based on the duration of the event.
* Balance:
* =IFERROR(SUMIFS(E$2:E2, A$2:A2, A2) - SUMIFS(Debits!C:C, Debits!A:A, A2, Debits!B:B, "<=" & B2), E2)
This formula calculates the cumulative balance by summing the amounts made and subtracting the amounts spent up to the current date.
* Duration:
* = (HOUR(D2) + MINUTE(D2)/60 + SECOND(D2)/3600) - (HOUR(C2) + MINUTE(C2)/60 + SECOND(C2)/3600)
This formula calculates the duration of the event in hours.

### Debits Sheet

Columns:

* Name: The name of the person.
* Date: The date of the spending.
* Amount spent: The amount spent.
* Balance: The updated balance after spending.
Formulas:
* Balance:
* =IFERROR(INDEX(Credits!F:F, MATCH(A2 & MAXIFS(Credits!B:B, Credits!A:A, A2, Credits!B:B, "<=" & B2), Credits!A:A & Credits!B:B, 0)) - SUMIF(A$2:A2, A2, C$2:C2), -C2)
This formula fetches the latest balance from the�Credits�sheet and subtracts the cumulative amount spent.


## README på Svenska

### Översikt

Detta dokument beskriver strukturen och formlerna som används i Credits och Debits bladen för att hantera och upprätthålla saldon baserat på intjänade och spenderade belopp.

### Credits Sheet

#### Kolumner

* **Namn**: Personens namn.
* **Datum**: Datum för händelsen.
* **Starttid**: Starttid för händelsen.
* **Sluttid**: Sluttid för händelsen.
* **Intjänat belopp**: Intjänat belopp, beräknat baserat på varaktigheten.
* **Saldo**: Det kumulativa saldot efter att ha tagit hänsyn till intäkter och utgifter.
* **Varaktighet**: Händelsens varaktighet i timmar.

#### Formler

* **Intjänat belopp**:
* `= G2 * 20`
* Denna formel beräknar det intjänade beloppet baserat på händelsens varaktighet.
* **Saldo**:
* `=IFERROR(SUMIFS(E$2:E2, A$2:A2, A2) - SUMIFS(Debits!C:C, Debits!A:A, A2, Debits!B:B, "<=" & B2), E2)`
* Denna formel beräknar det kumulativa saldot genom att summera de intjänade beloppen och subtrahera de spenderade beloppen fram till det aktuella datumet.
* **Varaktighet**:
* `= (HOUR(D2) + MINUTE(D2)/60 + SECOND(D2)/3600) - (HOUR(C2) + MINUTE(C2)/60 + SECOND(C2)/3600)`
* Denna formel beräknar händelsens varaktighet i timmar.

### Debits Sheet

#### Kolumner

* **Namn**: Personens namn.
* **Datum**: Datum för utgiften.
* **Spenderat belopp**: Det spenderade beloppet.
* **Saldo**: Det uppdaterade saldot efter utgiften.

#### Formler

* **Saldo**:
* `=IFERROR(INDEX(Credits!F:F, MATCH(A2 & MAXIFS(Credits!B:B, Credits!A:A, A2, Credits!B:B, "<=" & B2), Credits!A:A & Credits!B:B, 0)) - SUMIF(A$2:A2, A2, C$2:C2), -C2)`
* Denna formel hämtar det senaste saldot från Credits bladet och subtraherar det kumulativa spenderade beloppet.

### Titlar i Båda Bladen

#### Credits Sheet

* Namn
* Datum
* Starttid
* Sluttid
* Intjänat belopp
* Saldo
* Varaktighet

#### Debits Sheet

* Namn
* Datum
* Spenderat belopp
* Saldo
