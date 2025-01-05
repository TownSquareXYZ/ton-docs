# Adresy inteligentnych kontraktów

Ta sekcja opisuje specyfikę adresów inteligentnych kontraktów na blockchainie TON. Wyjaśnimy również, w jaki sposób aktorzy są synonimami inteligentnych kontraktów na TON.

## Wszystko jest inteligentnym kontraktem

W TON inteligentne kontrakty są budowane przy użyciu modelu [Actor model](/learn/overviews/ton-blockchain#single-actor). W rzeczywistości aktorzy w TON są technicznie reprezentowani jako inteligentne kontrakty. Oznacza to, że nawet Państwa portfel jest prostym aktorem (i inteligentnym kontraktem).

Zazwyczaj aktorzy przetwarzają przychodzące wiadomości, zmieniają swój stan wewnętrzny i w rezultacie generują wiadomości wychodzące. Dlatego też każdy aktor (tj. inteligentny kontrakt) na blockchainie TON musi mieć adres, aby móc odbierać wiadomości od innych aktorów.

:::info DOŚWIADCZENIE Z EVM
W maszynie wirtualnej Ethereum (EVM) adresy są całkowicie oddzielone od inteligentnych kontraktów. Proszę dowiedzieć się więcej o różnicach, czytając nasz artykuł ["Sześć unikalnych aspektów TON Blockchain, które zaskoczą programistów Solidity"] (https://blog.ton.org/six-unique-aspects-of-ton-blockchain-that-will-surprise-solidity-developers) autorstwa Tal Kol.
:::

## Adres inteligentnego kontraktu

Adresy inteligentnych kontraktów działających na TON zazwyczaj składają się z dwóch głównych komponentów:

- **(workchain_id)**: oznacza identyfikator łańcucha roboczego (32-bitowa liczba całkowita ze znakiem).

- **(account_id)** oznacza adres konta (64-512 bitów, w zależności od łańcucha roboczego).

W sekcji przeglądu nieprzetworzonych adresów w tej dokumentacji omówimy, jak prezentują się pary **(workchain_id, account_id)**.

### Identyfikator łańcucha roboczego i identyfikator konta

#### Identyfikator łańcucha roboczego

[Jak widzieliśmy wcześniej](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules), możliwe jest utworzenie aż `2^32` łańcuchów roboczych działających na TON Blockchain. Zauważyliśmy również, w jaki sposób 32-bitowe prefiksy adresów inteligentnych kontraktów identyfikują i są powiązane z adresami inteligentnych kontraktów w różnych łańcuchach roboczych. Pozwala to inteligentnym kontraktom na wysyłanie i odbieranie wiadomości do i z różnych łańcuchów roboczych na TON Blockchain.

Obecnie w TON Blockchain działa tylko Masterchain (workchain_id=-1) i okazjonalnie podstawowy workchain (workchain_id=0).

Oba mają 256-bitowe adresy, dlatego zakładamy, że workchain_id wynosi 0 lub -1, a adres w łańcuchu roboczym ma dokładnie 256 bitów.

#### Identyfikator konta

Wszystkie identyfikatory kont w TON wykorzystują 256-bitowe adresy w łańcuchach Masterchain i Basechain (lub podstawowym łańcuchu roboczym).

W rzeczywistości identyfikator konta **(account_id)** zdefiniowano jako funkcje skrótu dla obiektów inteligentnych kontraktów (w szczególności SHA-256). Każdy inteligentny kontrakt działający na TON Blockchain przechowuje dwa główne komponenty. Należą do nich:

1. Skompilowany kod_. Logika inteligentnego kontraktu skompilowana w postaci kodu bajtowego.
2. *Stan początkowy*. Wartości kontraktu w momencie jego wdrożenia w łańcuchu.

Wreszcie, aby dokładnie wyprowadzić adres kontraktu, konieczne jest obliczenie skrótu odpowiadającego parze **(kod początkowy, stan początkowy)** obiektu. W tej chwili nie będziemy zagłębiać się w to, jak działa [TVM](/learn/tvm-instructions/tvm-overview), ale ważne jest, aby zrozumieć, że identyfikatory kont w TON są określane za pomocą tego wzoru:
:
**account_id = hash(kod początkowy, stan początkowy)**.

Z czasem, w całej tej dokumentacji, zagłębimy się w specyfikacje techniczne i przegląd schematu TVM i TL-B. Teraz, gdy jesteśmy zaznajomieni z generowaniem **account_id** i ich interakcją z adresami inteligentnych kontraktów w TON, wyjaśnijmy adresy Raw i User-Friendly.

## Adresy państwowe

Każdy adres może znajdować się w jednym z możliwych stanów:

- `nonexist` - nie było żadnych zaakceptowanych transakcji na tym adresie, więc nie ma on żadnych danych (lub umowa została usunięta). Możemy powiedzieć, że początkowo wszystkie adresy<sup>2256</sup> są w tym stanie.
- `uninit` - adres ma pewne dane, które zawierają saldo i meta informacje. W tym stanie adres nie ma jeszcze żadnego kodu inteligentnego kontraktu/trwałych danych. Adres wchodzi w ten stan, na przykład, gdy nie istniał, a inny adres wysłał do niego tokeny.
- `active` - adres posiada kod inteligentnego kontraktu, trwałe dane i saldo. W tym stanie może wykonać pewną logikę podczas transakcji i zmienić swoje trwałe dane. Adres wchodzi w ten stan, gdy był `uninit` i nadeszła wiadomość z parametrem state_init (proszę zauważyć, że aby móc wdrożyć ten adres, hash z `state_init` i `code` musi być równy adresowi).
- `frozen` - adres nie może wykonywać żadnych operacji, ten stan zawiera tylko dwa skróty poprzedniego stanu (odpowiednio komórki kodu i stanu). Gdy ładunek pamięci adresu przekroczy jego saldo, przechodzi on w ten stan. Aby go odmrozić, można wysłać wewnętrzną wiadomość z `state_init` i `code`, które przechowują hashe opisane wcześniej i trochę Toncoin. Odzyskanie go może być trudne, więc nie należy dopuszczać do takiej sytuacji. Istnieje projekt odblokowania adresu, który można znaleźć [tutaj] (https://unfreezer.ton.org/).

## Surowe i przyjazne dla użytkownika adresy

Po przedstawieniu krótkiego przeglądu tego, w jaki sposób adresy inteligentnych kontraktów w TON wykorzystują łańcuchy robocze i identyfikatory kont (w szczególności dla Masterchain i Basechain), ważne jest, aby zrozumieć, że adresy te są wyrażane w dwóch głównych formatach:

- **Surowe adresy**: Oryginalna pełna reprezentacja adresów inteligentnych kontraktów.
- **Adresy przyjazne dla użytkownika**: Adresy przyjazne dla użytkownika to ulepszony format surowego adresu, który zapewnia lepsze bezpieczeństwo i łatwość użytkowania.

Poniżej wyjaśnimy więcej na temat różnic między tymi dwoma typami adresów i zagłębimy się w to, dlaczego adresy przyjazne dla użytkownika są używane w TON.

### Nieprzetworzony adres

Nieprzetworzone adresy inteligentnych kontraktów składają się z identyfikatora łańcucha roboczego i identyfikatora konta *(workchain_id, account_id)* i są wyświetlane w następującym formacie:

- [decimal workchain_id\]:[64 cyfry szesnastkowe z account_id\].

Poniżej znajduje się przykład nieprzetworzonego adresu inteligentnego kontraktu przy użyciu identyfikatora łańcucha roboczego i identyfikatora konta (wyrażonego jako **workchain_id** i **account_id**):

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

Proszę zauważyć `-1` na początku ciągu adresu, który oznacza *workchain_id* należący do Masterchain.

:::note
Wielkie litery (takie jak "A", "B", "C", "D" itp.) mogą być używane w ciągach adresowych zamiast ich małych odpowiedników (takich jak "a", "b", "c", "d" itp.).
:::

#### Problemy z surowymi adresami

Korzystanie z formularza Raw Address wiąże się z dwoma głównymi problemami:

1. W przypadku korzystania z nieprzetworzonego formatu adresu nie jest możliwa weryfikacja adresów w celu wyeliminowania błędów przed wysłaniem transakcji.
   Oznacza to, że jeśli przypadkowo dodadzą lub usuną Państwo znaki w ciągu adresowym przed wysłaniem transakcji, zostanie ona wysłana do niewłaściwego miejsca docelowego, co spowoduje utratę środków.
2. Podczas korzystania z nieprzetworzonego formatu adresu niemożliwe jest dodanie specjalnych flag, takich jak te używane podczas wysyłania transakcji, które wykorzystują adresy przyjazne dla użytkownika.
   Aby pomóc Państwu lepiej zrozumieć tę koncepcję, poniżej wyjaśnimy, które flagi mogą być używane.

### Adres przyjazny dla użytkownika

Przyjazne dla użytkownika adresy zostały opracowane w celu zabezpieczenia i uproszczenia doświadczenia użytkowników TON, którzy udostępniają adresy w Internecie (na przykład na publicznych platformach komunikacyjnych lub za pośrednictwem swoich dostawców usług poczty elektronicznej), a także w świecie rzeczywistym.

#### Przyjazna dla użytkownika struktura adresów

Przyjazne dla użytkownika adresy składają się łącznie z 36 bajtów i są uzyskiwane poprzez wygenerowanie następujących składników w kolejności:

1. Flagi przypięte do adresów zmieniają sposób, w jaki inteligentne kontrakty reagują na otrzymaną wiadomość.
   Typy flag, które wykorzystują przyjazny dla użytkownika format adresu obejmują:

   - isBounceable. Oznacza typ adresu bounceable lub non-bounceable. (*0x11* dla "bounceable", *0x51* dla "non-bounceable")
   - isTestnetOnly. Oznacza typ adresu używany wyłącznie do celów sieci testowej. Adresy zaczynające się od *0x80* nie powinny być akceptowane przez oprogramowanie działające w sieci produkcyjnej.
   - isUrlSafe. Oznacza przestarzałą flagę, która jest zdefiniowana jako URL-safe dla adresu. Wszystkie adresy są wtedy uważane za bezpieczne pod względem adresu URL.
2. *\[workchain_id - 1 bajt]* - Identyfikator łańcucha roboczego (*workchain_id*) jest zdefiniowany przez podpisaną 8-bitową liczbę całkowitą *workchain_id*.\
   (*0x00* dla BaseChain, *0xff* dla MasterChain)
3. Identyfikator konta składa się z ([big-endian](https://www.freecodecamp.org/news/what-is-endianness-big-endian-vs-little-endian/)) 256-bitowego adresu w łańcuchu roboczym.
4. Weryfikacja adresu - 2 bajty]_ - W adresach przyjaznych dla użytkownika weryfikacja adresu składa się z podpisu CRC16-CCITT z poprzednich 34 bajtów. ([Przykład](https://github.com/andreypfau/ton-kotlin/blob/ce9595ec9e2ad0eb311351c8a270ef1bd2f4363e/ton-kotlin-crypto/common/src/crc32.kt))
   W rzeczywistości idea weryfikacji adresów przyjaznych dla użytkownika jest dość podobna do [algorytmu Luhna](https://en.wikipedia.org/wiki/Luhn_algorithm), który jest używany na wszystkich kartach kredytowych, aby uniemożliwić użytkownikom omyłkowe wprowadzenie nieistniejących numerów kart.

Dodanie tych 4 głównych składników oznacza, że: `1 + 1 + 32 + 2 = 36` bajtów łącznie (na adres przyjazny dla użytkownika).

Aby wygenerować adres przyjazny dla użytkownika, programista musi zakodować wszystkie 36 bajtów za pomocą jednego z nich:

- *base64* (tj. z cyframi, dużymi i małymi literami alfabetu łacińskiego, '/' i '+')
- *base64url* (z '_' i '-' zamiast '/' i '+')

Po zakończeniu tego procesu generowany jest przyjazny dla użytkownika adres o długości 48 znaków bez odstępów.

:::info FLAGI ADRESU DNS
W TON adresy DNS, takie jak mywallet.ton, są czasami używane zamiast surowych i przyjaznych dla użytkownika adresów. W rzeczywistości adresy DNS składają się z adresów przyjaznych dla użytkownika i zawierają wszystkie wymagane flagi, które umożliwiają programistom dostęp do wszystkich flag z rekordu DNS w domenie TON.
:::

#### Przyjazne dla użytkownika przykłady kodowania adresów

Przykładowo, inteligentny kontrakt "test giver" (specjalny inteligentny kontrakt rezydujący w łańcuchu głównym testnet, który wysyła 2 tokeny testowe do każdego, kto o nie poprosi) korzysta z następującego surowego adresu:

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

Powyższy nieprzetworzony adres "dawcy testu" musi zostać przekonwertowany na przyjazną dla użytkownika formę adresu. Uzyskuje się to za pomocą formularzy base64 lub base64url (które wprowadziliśmy wcześniej) w następujący sposób:

- `kf/8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15+KsQHFLbKSMiYIny` (base64)
- `kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny` (base64url)

:::info
Proszę zauważyć, że obie formy (*base64* i *base64url*) są poprawne i muszą zostać zaakceptowane!
:::

#### Adresy odrzucające i nieodrzucające

Główną ideą stojącą za flagą adresu zwrotnego jest bezpieczeństwo funduszy nadawcy.

Na przykład, jeśli docelowy inteligentny kontrakt nie istnieje lub jeśli wystąpi jakiś problem podczas transakcji, wiadomość zostanie "odbita" z powrotem do nadawcy i będzie stanowić pozostałą część pierwotnej wartości transakcji (pomniejszoną o wszystkie opłaty za przelew i gaz). Gwarantuje to, że nadawca nie straci środków, które zostały przypadkowo wysłane na adres, który nie może zaakceptować transakcji.

W szczególności w odniesieniu do adresów odrzucających:

1. Flaga **bounceable=false** zazwyczaj oznacza, że odbiornik jest portfelem.
2. Flaga **bounceable=true** zazwyczaj oznacza niestandardowy inteligentny kontrakt z własną logiką aplikacji (na przykład DEX). W tym przykładzie wiadomości nie podlegające bounceable nie powinny być wysyłane ze względów bezpieczeństwa.

Proszę przeczytać więcej na ten temat w naszej dokumentacji, aby lepiej zrozumieć [non-bouncable messages] (/develop/smart-contracts/guidelines/non-bouncable-messages).

#### Reprezentacje bazy pancernej64

Dodatkowe dane binarne związane z TON Blockchain wykorzystują podobne "pancerne", przyjazne dla użytkownika reprezentacje adresów base64. Różnią się one od siebie w zależności od pierwszych 4 znaków ich znacznika bajtowego. Na przykład 256-bitowe klucze publiczne Ed25519 są reprezentowane przez utworzenie najpierw 36-bajtowej sekwencji przy użyciu poniższego procesu w kolejności:

- Jednobajtowy znacznik w formacie *0x3E* oznacza klucz publiczny
- Jednobajtowy znacznik w formacie *0xE6* oznacza klucz publiczny Ed25519
- 32 bajty zawierające standardową reprezentację binarną klucza publicznego Ed25519
- 2 bajty zawierające reprezentację big-endian CRC16-CCITT poprzednich 34 bajtów

Wynikowa 36-bajtowa sekwencja jest konwertowana na 48-znakowy ciąg base64 lub base64url w standardowy sposób. Na przykład klucz publiczny Ed25519 `E39ECDA0A7B0C60A7107EC43967829DBE8BC356A49B9DFC6186B3EAC74B5477D` (zwykle reprezentowany przez sekwencję 32 bajtów, takich jak:  `0xE3, 0x9E, ..., 0x7D`) przedstawia się poprzez "pancerną" reprezentację w następujący sposób:

`Pubjns2gp7DGCnEH7EOWeCnb6Lw1akm538YYaz6sdLVHfRB2`

### Konwersja adresów przyjaznych dla użytkownika i adresów nieprzetworzonych

Najprostszym sposobem konwersji przyjaznych dla użytkownika i nieprzetworzonych adresów jest użycie jednego z kilku interfejsów API TON i innych narzędzi, w tym:

- [ton.org/address](https://ton.org/address)
- [dton.io API method](https://dton.io/api/address/0:867ac2b47d1955de6c8e23f57994fad507ea3bcfe2a7d76ff38f29ec46729627)
- [metody API toncenter w sieci głównej](https://toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)
- [metody API toncenter w testnet](https://testnet.toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)

Ponadto istnieją dwa sposoby konwertowania przyjaznych dla użytkownika i nieprzetworzonych adresów portfeli za pomocą JavaScript:

- [Konwersja adresu z/do postaci przyjaznej dla użytkownika lub nieprzetworzonej przy użyciu ton.js](https://github.com/ton-org/ton-core/blob/main/src/address/Address.spec.ts)
- [Proszę przekonwertować adres z/do postaci przyjaznej dla użytkownika lub nieprzetworzonej za pomocą tonweb](https://github.com/toncenter/tonweb/tree/master/src/utils#address-class)

Możliwe jest również wykorzystanie podobnych mechanizmów za pomocą [SDK](/develop/dapps/apis/sdk).

### Przykłady adresów

Więcej przykładów na temat adresów TON można znaleźć w książce kucharskiej [TON Cookbook] (/develop/dapps/cookbook#working-with-contracts-addresses).

## Możliwe problemy

Podczas interakcji z blockchainem TON kluczowe jest zrozumienie konsekwencji przesyłania monet TON na adresy portfeli `uninit`. W tej sekcji przedstawiono różne scenariusze i ich wyniki, aby zapewnić jasność co do sposobu obsługi takich transakcji.

### Co się stanie, gdy przeleją Państwo Toncoin na niezainicjowany adres?

#### Transakcja z włączonym `state_init`

Jeśli dołączą Państwo `state_init` (który składa się z kodu i danych portfela lub inteligentnego kontraktu) do swojej transakcji. Inteligentny kontrakt jest najpierw wdrażany przy użyciu dostarczonego `state_init`. Po wdrożeniu, przychodząca wiadomość jest przetwarzana, podobnie jak w przypadku wysyłania na już zainicjalizowane konto.

#### Transakcja bez ustawionej flagi `state_init` i `bounce`

Wiadomość nie może zostać dostarczona do inteligentnego kontraktu `uninit` i zostanie odesłana z powrotem do nadawcy. Po odjęciu zużytych opłat za gaz, pozostała kwota jest zwracana na adres nadawcy.

#### Transakcja bez ustawionej flagi `state_init` i `bounce`

Wiadomość nie może zostać dostarczona, ale nie zostanie odesłana do nadawcy. Zamiast tego wysłana kwota zostanie przelana na adres odbiorcy, zwiększając jego saldo, nawet jeśli portfel nie został jeszcze zainicjowany. Będą one tam przechowywane, dopóki posiadacz adresu nie wdroży kontraktu inteligentnego portfela, a następnie będzie mógł uzyskać dostęp do salda.

#### Jak zrobić to dobrze

Najlepszym sposobem na wdrożenie portfela jest wysłanie pewnej ilości TON na jego adres (który nie jest jeszcze zainicjowany) z wyczyszczoną flagą `bounce`. Po tym kroku właściciel może wdrożyć i zainicjować portfel przy użyciu środków na bieżącym niezainicjalizowanym adresie. Ten krok zwykle ma miejsce przy pierwszej operacji portfela.

### Blockchain TON zapewnia ochronę przed błędnymi transakcjami

W blockchainie TON standardowe portfele i aplikacje automatycznie zarządzają złożonością transakcji na niezainicjowane adresy za pomocą adresów bounceable i non-bounceable, które są opisane [tutaj] (#bounceable-vs-non-bounceable-addresses). Powszechną praktyką portfeli podczas wysyłania monet na niezainicjowane adresy jest wysyłanie monet zarówno na adresy bounceable, jak i non-bounceable bez zwrotu.

Jeśli istnieje potrzeba szybkiego uzyskania adresu w formie odbijającej/nieodbijającej, można to zrobić [tutaj](https://ton.org/address/).

### Odpowiedzialność za produkty niestandardowe

Jeśli opracowują Państwo niestandardowy produkt na blockchainie TON, konieczne jest wdrożenie podobnych kontroli i logiki:

Przed wysłaniem środków należy upewnić się, że aplikacja weryfikuje, czy adres odbiorcy został zainicjowany.
W oparciu o stan adresu, proszę używać adresów odrzucających dla inteligentnych kontraktów użytkownika z niestandardową logiką aplikacji, aby zapewnić zwrot środków. W przypadku portfeli proszę używać adresów niepodlegających odrzuceniu.
