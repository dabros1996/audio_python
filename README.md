# Skrypt do sterowania dźwiękiem za pomocą skrótów klawiszowych

Ten skrypt w Pythonie umożliwia sterowanie dźwiękiem i odtwarzaniem mediów w systemie Windows za pomocą globalnych skrótów klawiszowych.

## Wymagania

* Python 3.x
* Biblioteki: `keyboard`, `pycaw`, `comtypes`, `pynput`

## Instalacja

1.  Zainstaluj wymagane biblioteki:

    ```bash
    pip install keyboard pycaw comtypes pynput
    ```

2.  Skopiuj kod skryptu do pliku Python o nazwie `switch.py`.

## Użycie

1.  Uruchom skrypt z wiersza poleceń:

    ```bash
    python switch.py
    ```

2.  Użyj skrótów klawiszowych:
    * `Ctrl + Alt + M`: Mutuj/odmutuj dźwięk
    * `Ctrl + Alt + P`: Play/Pause (przełączanie odtwarzania)
    * `Ctrl + Alt + Right`: Następny utwór
    * `Ctrl + Alt + Left`: Poprzedni utwór
    * `Ctrl + Alt + Q`: Zakończ skrypt

## Opis działania

Skrypt używa następujących bibliotek:
* `pycaw` do sterowania głośnością systemu Windows
* `keyboard` do obsługi globalnych skrótów klawiszowych
* `pynput` do symulacji klawiszy multimedialnych

Po uruchomieniu skrypt działa w tle i wyświetla menu w terminalu pokazujące:
* Dostępne skróty klawiszowe
* Aktualny stan odtwarzania (Playing/Paused)
* Status działania skryptu

Funkcje:
* Mutowanie/odmutowywanie dźwięku systemowego
* Kontrola odtwarzania mediów (play/pause)
* Przełączanie między utworami (następny/poprzedni)
* Zabezpieczenie przed przypadkowym podwójnym wciśnięciem (300ms opóźnienie)
* Automatyczne żądanie uprawnień administratora

## Uwagi

* Upewnij się, że masz uprawnienia administratora, aby skrypt mógł sterować głośnością.
* Skróty klawiszowe można dostosować, modyfikując zmienne hotkey w kodzie skryptu.
* Skrypt działa w systemie Windows.