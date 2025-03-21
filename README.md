# Skrypt do mutowania/odmutowywania dźwięku za pomocą skrótów klawiszowych

Ten skrypt w Pythonie umożliwia mutowanie i odmutowywanie dźwięku w systemie Windows za pomocą skrótów klawiszowych.

## Wymagania

* Python 3.x
* Biblioteki: `keyboard`, `pycaw`, `comtypes`

## Instalacja

1.  Zainstaluj wymagane biblioteki:

    ```bash
    pip install keyboard pycaw comtypes
    ```

2.  Skopiuj kod skryptu do pliku Python o nazwie `switch.py`.

## Użycie

1.  Uruchom skrypt z wiersza poleceń:

    ```bash
    python switch.py
    ```

2.  Użyj skrótów klawiszowych:
    * `Ctrl + Alt + M`: Mutuj/odmutuj dźwięk
    * `Ctrl + Alt + Q`: Zakończ skrypt

## Opis działania

Skrypt używa biblioteki `pycaw` do sterowania głośnością systemu Windows. Biblioteka `keyboard` jest używana do obsługi skrótów klawiszowych.

Po uruchomieniu skrypt działa w tle i nasłuchuje skróty klawiszowe. Naciśnięcie `Ctrl + Alt + M` powoduje mutowanie lub odmutowywanie dźwięku, a naciśnięcie `Ctrl + Alt + Q` kończy działanie skryptu.

## Uwagi

* Upewnij się, że masz uprawnienia administratora, aby skrypt mógł sterować głośnością.
* Skróty klawiszowe można dostosować, modyfikując zmienne `mute_hotkey` i `quit_hotkey` w kodzie skryptu.
* Skrypt działa w systemie Windows.