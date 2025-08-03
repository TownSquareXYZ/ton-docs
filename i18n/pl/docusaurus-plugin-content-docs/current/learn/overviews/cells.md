# Komórki jako magazyn danych

Wszystko w TON jest przechowywane w komórkach. Komórka jest strukturą danych zawierającą:

- do **1023 bitów** danych (nie bajtów!)
- do **4 odniesień** do innych komórek

Bity i referencje nie są mieszane (są przechowywane oddzielnie). Odwołania cykliczne są zabronione: dla dowolnej komórki, żadna z komórek potomnych nie może mieć tej oryginalnej komórki jako odwołania.

W ten sposób wszystkie komórki tworzą skierowany graf acykliczny (DAG). Oto dobry obrazek ilustrujący:

Ukierunkowany graf acykliczny](/img/docs/dag.png)

## Typy komórek

Obecnie istnieje 5 rodzajów komórek: *zwykłe* i 4 *egzotyczne*.
Egzotyczne typy są następujące:

- Przycięta komórka gałęzi
- Komórka referencyjna biblioteki
- Komórka Merkle proof
- Komórka aktualizacji Merkle

:::tip
Więcej informacji na temat egzotycznych komórek można znaleźć w: [**TVM Whitepaper, Section 3**](https://ton.org/tvm.pdf).
:::

## Smaki komórkowe

Komórka jest nieprzezroczystym obiektem zoptymalizowanym pod kątem kompaktowego przechowywania.

W szczególności deduplikuje dane: jeśli istnieje kilka równoważnych podkomórek, do których odwołują się różne gałęzie, ich zawartość jest przechowywana tylko raz. Nieprzezroczystość oznacza jednak, że komórki nie można bezpośrednio modyfikować ani odczytywać. Istnieją zatem 2 dodatkowe wersje komórek:

- *Builder* dla częściowo skonstruowanych komórek, dla których można zdefiniować szybkie operacje dołączania ciągów bitów, liczb całkowitych, innych komórek i odwołań do innych komórek.
- *Slice* dla "wyciętych" komórek reprezentujących pozostałą część częściowo przeanalizowanej komórki lub wartość (podkomórkę) znajdującą się wewnątrz takiej komórki i wyodrębnioną z niej za pomocą instrukcji parsowania.

Kolejna specjalna odmiana komórek jest używana w TVM:

- *Continuation* dla komórek zawierających kody operacyjne (instrukcje) dla TON Virtual Machine, proszę zobaczyć [TVM bird's-eye overview](/learn/tvm-instructions/tvm-overview).

## Serializacja danych do komórek

Każdy obiekt w TON (wiadomość, kolejka wiadomości, blok, cały stan blockchain, kod kontraktu i dane) serializuje się do komórki.

Proces serializacji jest opisany przez schemat TL-B: formalny opis tego, jak ten obiekt może być serializowany do *Builder* lub jak przeanalizować obiekt danego typu z *Slice*.
TL-B dla komórek jest taki sam jak TL lub ProtoBuf dla strumieni bajtów.

Jeśli chcą Państwo dowiedzieć się więcej na temat (de)serializacji komórek, proszę przeczytać artykuł [Cell & Bag of Cells](/develop/data-formats/cell-boc).

## Proszę zobaczyć również

- [Język TL-B](/develop/data-formats/tl-b-language)
