# Text2Image - Python  + JavaScript (HTML, CSS)

Repozytorium zawierające **projekt kliencki**, czyli ten człon pracy magisterskiej, który odpowiada za obsługę żądań klienta.

## Instalacja pakietów

Jeżeli nie ma się zainstalowanych pakietów takich jak:

* `body-parser` (_^1.19.0_)
* `child_process` (_^1.0.2_)
* `ejs` (_^3.1.5_)
* `express` (_^4.17.1_)
* `fs` (_^0.0.1-security_)

To należy w katalogu głównym projektu (tam gdzie znajduje się plik `server.js`) wpisac komendę:
```
npm install
```
Spowoduje to doinstalowanie niezbędnych bibliotek.

## Instrukcja

Na początku należy przejść do folderu głównego projektu (tam gdzie znajduje się plik `server.js`), a następnie do sekcji pisanej w języku _Python_ (tam gdzie znajduje się plik `runtime.py`). Wówczas wystarczy użyć:
```
python runtime.py --CUDACARD={numer karty}
```
gdzie:

* `numer karty` – numer GPU, z którego będzie korzystał skrypt (możliwe opcje to `0`, `1` lub `2`).

Spowoduje to uruchomienie głównego skryptu obsługującego pliki oraz sieć _GAN_.

Kolejnym krokiem jest uruchomienie serwera dla klienta. Wykonuje się to z katalogu głównego projektu (tam gdzie znajduje się plik `server.js`) za pomocą:
```
node server.js
```

**Uwaga! Należy to zrobić w odrębnych Wierszach poleceń, bo oba skrypty działają tak długo, aż nie zostaną przerwane przez Administratora, a jednocześnie oba są wymagane do funkcjonowania serwisu.**

Na końcu już można wejść pod adres lokalny _127.0.0.1:3000_ po to by korzystać z usługi.

## Puste pliki

W niektórych katalogach znajdują się puste pliki (_init_). Służą one jedynie zachowaniu struktury plików w repozytorium _GitHub_.

**Uwaga! Po pobraniu repozytorium zalecane jest usunięcie tych plików.**

## Informacje

Autor: Cezary Pietruszyński

Promotor: dr Marek Grochowski