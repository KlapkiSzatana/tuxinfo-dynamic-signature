# TuxInfo Dynamic Signature

Minimalistyczna, automatycznie generowana sygnatura PNG do forum TuxInfo.

## Jak działa

- Edytujesz `config.json` (tytuł, autor, status i opcjonalny link).
- GitHub Actions uruchamia generator i tworzy `signature.png`.
- Workflow publikuje obrazek w repozytorium.
- W sygnaturze forum używasz stałego adresu do obrazka.


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
