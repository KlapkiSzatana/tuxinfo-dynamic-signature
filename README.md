# TuxInfo Dynamic Signature

Minimalistyczna, automatycznie generowana sygnatura PNG do forum TuxInfo.

## Jak działa

- Edytujesz `config.json` (tytuł, autor, status i opcjonalny link).
- GitHub Actions uruchamia generator i tworzy `signature.png`.
- Workflow publikuje obrazek w repozytorium.
- W sygnaturze forum używasz stałego adresu do obrazka.

## 1. Utwórz repozytorium

Na GitHubie utwórz publiczne repozytorium, np. `tuxinfo-dynamic-signature`.
Wgraj do niego zawartość tego katalogu, zachowując strukturę plików.

## 2. Dostosuj dane

Edytuj `config.json`, np.:

```json
{
  "label": "AKTUALNIE CZYTAM",
  "title": "Metro 2033",
  "subtitle": "Dmitry Glukhovsky",
  "status": "W trakcie",
  "footer": "TUXINFO • PERSONAL STATUS",
  "accent": "#4f8a70",
  "background": "#f5f6f4",
  "foreground": "#202522",
  "muted": "#737b76",
  "link": "https://pl.wikipedia.org/wiki/Metro_2033"
}
```

`link` jest opcjonalny. Generator zapisuje go w pliku `signature-link.txt`, aby łatwo skopiować docelowy adres. Sam obraz PNG nie jest klikalnym linkiem — jeśli forum obsługuje `[url]`, owiń `[img]` znacznikiem `[url=...]`.

## 3. Włącz GitHub Actions

Po wypchnięciu plików do GitHuba otwórz zakładkę **Actions** i włącz workflow, jeśli GitHub o to poprosi.

Workflow:
- uruchamia się po zmianie `config.json`,
- można go też uruchomić ręcznie (**Run workflow**),
- generuje `signature.png`,
- zapisuje wygenerowany obraz w repozytorium.

Przy pierwszym uruchomieniu może być potrzebne zezwolenie na zapis:
**Settings → Actions → General → Workflow permissions → Read and write permissions**.

## 4. Wstaw sygnaturę na forum

Po udanym uruchomieniu Actions adres obrazka będzie miał postać:

`https://raw.githubusercontent.com/TWOJ_LOGIN/tuxinfo-dynamic-signature/main/signature.png`

Wstaw na forum (zamień `TWOJ_LOGIN` na swój login):

```bbcode
[img]https://raw.githubusercontent.com/TWOJ_LOGIN/tuxinfo-dynamic-signature/main/signature.png[/img]
```

Jeżeli chcesz, żeby obrazek prowadził do strony książki, a forum obsługuje `[url]`:

```bbcode
[url=https://pl.wikipedia.org/wiki/Metro_2033][img]https://raw.githubusercontent.com/TWOJ_LOGIN/tuxinfo-dynamic-signature/main/signature.png[/img][/url]
```

## Aktualizacja

Zmieniasz `config.json` i robisz commit. GitHub Actions wygeneruje nowy obrazek. Po odświeżeniu cache forum/CDN nowa wersja powinna się pojawić pod tym samym adresem.

## Uwagi

- Repozytorium musi być publiczne, jeśli forum ma pobierać obrazek bez logowania.
- Obraz ma 700 × 150 px, dzięki czemu jest czytelny, ale nie zajmuje dużo miejsca.
- Nie umieszczaj w `config.json` haseł, tokenów ani prywatnych danych.
