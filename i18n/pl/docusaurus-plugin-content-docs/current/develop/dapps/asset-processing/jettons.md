import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Button from '@site/src/components/button';

# Przetwarzanie TON Jetton

:::info
Dla jasnego zrozumienia, czytelnik powinien być zaznajomiony z podstawowymi zasadami przetwarzania aktywów opisanymi w [sekcji przetwarzania płatności](/develop/dapps/asset-processing/) naszej dokumentacji.
:::

Jettony to tokeny na TON Blockchain - można je traktować podobnie do tokenów ERC-20 na Ethereum.

W tej analizie zagłębiamy się w formalne standardy wyszczególniające jetton [zachowanie](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) i [metadane](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md).
Mniej formalny przegląd architektury jetton skoncentrowany na shardingu można znaleźć w naszym wpisie na blogu
[anatomy of jettons](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons).

Należy również pamiętać, że istnieją dwa podejścia do pracy z wypłatami jetton:

- [Memo Deposits](https://github.com/toncenter/examples/blob/main/deposits-jettons.js) - Pozwala to na utrzymanie jednego portfela depozytowego, a użytkownicy dodają notatkę w celu identyfikacji przez system. Oznacza to, że nie trzeba skanować całego łańcucha bloków, ale jest to nieco mniej łatwe dla użytkowników.
- [Depozyty bez notatek](https://github.com/gobicycle/bicycle) - To rozwiązanie również istnieje, ale jest trudniejsze do zintegrowania. Możemy jednak w tym pomóc, jeśli wolą Państwo wybrać tę drogę. Proszę powiadomić nas przed podjęciem decyzji o wdrożeniu tego podejścia.

## Architektura Jetton

Standardowe tokeny w TON są wdrażane przy użyciu zestawu inteligentnych kontraktów, w tym:

- Inteligentny kontrakt [Jetton master](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-minter.fc)
- [portfel Jetton](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc) inteligentne kontrakty

<p align="center">
  <br />
    <img width="420" src="/img/docs/asset-processing/jetton_contracts.svg" alt="contracts scheme" />
      <br />
</p>

## Główny inteligentny kontrakt Jetton

Główny inteligentny kontrakt jetton przechowuje ogólne informacje o jetton (w tym całkowitą podaż, link do metadanych lub same metadane).

:::warning Proszę uważać na oszustwo Jetton

Jettony z `symbolem`==`TON` lub te, które zawierają powiadomienia systemowe, takie jak:
`ERROR`, `SYSTEM` i inne. Proszę upewnić się, że jettony są wyświetlane w interfejsie w taki sposób, że nie mogą
być mieszane z transferami TON, powiadomieniami systemowymi itp. Czasami nawet `symbol`, `name` i `image`
będą tworzone tak, by wyglądały niemal identycznie do oryginału z nadzieją na wprowadzenie użytkowników w błąd.

Aby wyeliminować możliwość oszustwa dla użytkowników TON, proszę sprawdzić **oryginalny adres jetton** (umowa główna Jetton) dla określonych typów jetton lub **śledzić oficjalne media społecznościowe projektu** lub stronę internetową, aby znaleźć **prawidłowe informacje**. Proszę sprawdzić aktywa, aby wyeliminować możliwość oszustwa za pomocą [Tonkeeper ton-assets list](https://github.com/tonkeeper/ton-assets).
:::

### Pobieranie danych Jetton

Aby pobrać bardziej szczegółowe dane Jetton, proszę użyć metody *get* kontraktu `get_jetton_data()`.

Metoda ta zwraca następujące dane:

| Nazwa                | Typ     | Opis                                                                                                                                                                                                                                                |
| -------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `total_supply`       | `int`   | całkowita liczba wydanych jettonów mierzona w niepodzielnych jednostkach.                                                                                                                                                           |
| `mintable`           | `int`   | określa, czy nowe jettony mogą zostać wybite, czy nie. Wartość ta wynosi -1 (można wybijać) lub 0 (nie można wybijać).                                                        |
| `admin_address`      | `slice` |                                                                                                                                                                                                                                                     |
| `jetton_content`     | `cell`  | dane zgodnie z [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md), proszę sprawdzić [jetton metadata parsing page](/develop/dapps/asset-processing/metadata), aby dowiedzieć się więcej. |
| `jetton_wallet_code` | `cell`  |                                                                                                                                                                                                                                                     |

Można go wywołać za pomocą [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get) lub jednego z [SDK](https://docs.ton.org/develop/dapps/apis/sdk).

<Tabs groupId="get-jetton_data">
<TabItem value="API" label="API">

> Proszę uruchomić metodę `jetton/masters` z [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get).

</TabItem>
<TabItem value="js" label="js">

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const data = await jettonMinter.getJettonData();
console.log('Total supply:', data.totalSupply.toString());
console.log('URI to off-chain metadata:', data.jettonContentUri);
```

</TabItem>
</Tabs>

### Górnik Jetton

Jak wspomniano wcześniej, jettony mogą być `mintable` lub `non-mintable`.

Jeśli nie można ich wybić, logika staje się prosta - nie ma możliwości wybicia dodatkowych tokenów. Aby wybić jettony po raz pierwszy, proszę zapoznać się ze stroną [Mint your first jetton](/develop/dapps/tutorials/jetton-minter).

Jeśli jettony mogą być bite, istnieje specjalna funkcja w [kontrakcie mintera](https://github.com/ton-blockchain/minter-contract/blob/main/contracts/jetton-minter.fc) do bicia dodatkowych jettonów. Funkcja ta może zostać wywołana poprzez wysłanie `wewnętrznej wiadomości` z określonym kodem operacyjnym z adresu administratora.

Jeśli administrator jetton chce ograniczyć tworzenie jetton, może to zrobić na trzy sposoby:

1. Jeśli nie mogą lub nie chcą Państwo zaktualizować kodu umowy, administrator musi przenieść własność z obecnego administratora na adres zerowy. Spowoduje to, że kontrakt pozostanie bez ważnego administratora, co uniemożliwi komukolwiek wybijanie jettonów. Zapobiegnie to jednak również jakimkolwiek zmianom w metadanych jettona.
2. Jeśli mają Państwo dostęp do kodu źródłowego i mogą go zmienić, można utworzyć metodę w kontrakcie, która ustawia flagę przerywającą proces wybijania po jej wywołaniu i dodać instrukcję sprawdzającą tę flagę w funkcji mint.
3. Jeśli można zaktualizować kod umowy, można dodać ograniczenia, aktualizując kod już wdrożonej umowy.

## Inteligentny kontrakt portfela Jetton

Kontrakty `portfela jettona` są używane do **wysyłania**, **odbierania** i **spalania** jettonów. Każdy kontrakt *portfela jettona* przechowuje informacje o saldzie portfela dla określonych użytkowników.
W określonych przypadkach, portfele jettona są używane dla indywidualnych posiadaczy jettona dla każdego typu jettona.

"Portfeli jetton" **nie należy mylić z portfelami** przeznaczonymi do interakcji z blockchainem i przechowywania
tylko aktywów Toncoin (np. portfele v3R2, portfele highload i inne),
które są odpowiedzialne za obsługę i zarządzanie **tylko określonym typem jetton**.

### Wdrożenie portfela Jetton

Podczas `przekazywania jettonów` między portfelami, transakcje (wiadomości) wymagają pewnej ilości TON
jako zapłaty za **opłaty gazowe** sieci i wykonanie działań zgodnie z kodem kontraktu portfela Jetton.
Oznacza to, że **odbiorca nie musi wdrażać portfela jetton przed otrzymaniem jettonów**.
Portfel Jetton odbiorcy zostanie wdrożony automatycznie, o ile nadawca posiada wystarczającą ilość TON
w portfelu, aby uiścić wymagane opłaty za gaz.

### Pobieranie adresów portfela Jetton dla danego użytkownika

Aby pobrać `adres portfela Jetton` przy użyciu `adresu właściciela` (adres portfela TON),
`kontrakt główny Jetton` udostępnia metodę get `get_wallet_address(slice owner_address)`.

<Tabs groupId="retrieve-wallet-address">
<TabItem value="api" label="API">

> Proszę uruchomić `get_wallet_address(slice owner_address)` poprzez metodę `/runGetMethod` z [Toncenter API](https://toncenter.com/api/v3/#/default/run_get_method_api_v3_runGetMethod_post).

</TabItem>
<TabItem value="js" label="js">

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const address = await jettonMinter.getJettonWalletAddress(new TonWeb.utils.Address("<OWNER_WALLET_ADDRESS>"));
// It is important to always check that wallet indeed is attributed to desired Jetton Master:
const jettonWallet = new TonWeb.token.jetton.JettonWallet(tonweb.provider, {
  address: jettonWalletAddress
});
const jettonData = await jettonWallet.getData();
if (jettonData.jettonMinterAddress.toString(false) !== new TonWeb.utils.Address(info.address).toString(false)) {
  throw new Error('jetton minter address from jetton wallet doesnt match config');
}

console.log('Jetton wallet address:', address.toString(true, true, true));
```

</TabItem>
</Tabs>

### Pobieranie danych dla określonego portfela Jetton

Aby pobrać saldo konta portfela, informacje identyfikacyjne właściciela i inne informacje związane z konkretnym kontraktem portfela jetton, należy użyć metody `get_wallet_data()` w kontrakcie portfela jetton.

Metoda ta zwraca następujące dane:

| Nazwa                | Typ       |
| -------------------- | --------- |
| `balance`            | int       |
| `właściciel`         | plasterek |
| `jetton`             | plasterek |
| `jetton_wallet_code` | komórka   |

<Tabs groupId="retrieve-jetton-wallet-data">
<TabItem value="api" label="API">

> Proszę użyć metody `/jetton/wallets` get z [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_wallets_api_v3_jetton_wallets_get), aby pobrać wcześniej zdekodowane dane portfela jetton.

</TabItem>

<TabItem value="js" label="js">

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const walletAddress = "EQBYc3DSi36qur7-DLDYd-AmRRb4-zk6VkzX0etv5Pa-Bq4Y";
const jettonWallet = new TonWeb.token.jetton.JettonWallet(tonweb.provider,{address: walletAddress});
const data = await jettonWallet.getData();
console.log('Jetton balance:', data.balance.toString());
console.log('Jetton owner address:', data.ownerAddress.toString(true, true, true));
// It is important to always check that Jetton Master indeed recognize wallet
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: data.jettonMinterAddress.toString(false)});
const expectedJettonWalletAddress = await jettonMinter.getJettonWalletAddress(data.ownerAddress.toString(false));
if (expectedJettonWalletAddress.toString(false) !== new TonWeb.utils.Address(walletAddress).toString(false)) {
  throw new Error('jetton minter does not recognize the wallet');
}

console.log('Jetton master address:', data.jettonMinterAddress.toString(true, true, true));
```

</TabItem>
</Tabs>

## Przegląd komunikacji portfeli Jetton

Komunikacja między portfelami Jetton a portfelami TON odbywa się poprzez następującą sekwencję komunikacji:

![](/img/docs/asset-processing/jetton_transfer.svg)

#### Wiadomość 0

`Nadawca -> portfel jetton nadawcy`. Wiadomość *Transfer* zawiera następujące dane:

| Nazwa                  | Typ          | Opis                                                                                                                                                                                                                                                                     |
| ---------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `query_id`             | uint64       | Umożliwia aplikacjom powiązanie ze sobą trzech typów wiadomości `Transfer`, `Powiadomienie o transferze` i `Excesses`. Aby proces ten został przeprowadzony poprawnie, zaleca się **zawsze używać unikalnego identyfikatora zapytania**. |
| `kwota`                | monety       | Całkowita kwota `ton monety`, która zostanie wysłana wraz z wiadomością.                                                                                                                                                                                 |
| `przeznaczenie`        | adres        | Adres nowego właściciela jettons                                                                                                                                                                                                                                         |
| `response_destination` | adres        | Adres portfela używany do zwracania pozostałych ton monet z wiadomością o przekroczeniu limitu.                                                                                                                                                          |
| `custom_payload`       | może komórka | Rozmiar zawsze wynosi >= 1 bit. Dane niestandardowe (które są używane przez nadawcę lub odbiorcę portfela jetton dla wewnętrznej logiki).                                                                             |
| `forward_ton_amount`   | monety       | Musi być > 0, jeśli chcesz wysłać `powiadomienie o transferze` z `przekazanym ładunkiem`. Jest to **część wartości `amount`** i **musi być mniejsza niż `amount`**.                                                                      |
| `forward_payload`      | może komórka | Rozmiar zawsze wynosi >= 1 bit. Jeśli pierwsze 32 bity = 0x0, jest to zwykła wiadomość.                                                                                                                                                  |

#### Wiadomość 2

`portfel jetton odbiorcy płatności -> odbiorca płatności`.  Wiadomość z powiadomieniem o przelewie. **Wysyłana tylko jeśli** `forward_ton_amount` **nie wynosi zero**. Zawiera następujące dane:

| Nazwa             | Typ     |
| ----------------- | ------- |
| `query_id`        | uint64  |
| `kwota`           | monety  |
| `nadawca`         | adres   |
| `forward_payload` | komórka |

Tutaj `adres nadawcy` jest adresem `portfela Jetton` Alice.

#### Wiadomość 2''

`payee's jetton wallet -> Sender`. Treść wiadomości. **Wysyłane tylko wtedy, gdy po uiszczeniu opłat pozostały jakiekolwiek monety tonowe**. Zawiera następujące dane:

| Nazwa      | Typ    |
| ---------- | ------ |
| `query_id` | uint64 |

:::tip Jettons standard
Szczegółowy opis pól kontraktu portfela jetton można znaleźć w opisie interfejsu [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) `Jetton standard`.
:::

## Proszę wysłać Jettons z komentarzami

Ten przelew wymaga kilku ton monet na **opłaty** i, opcjonalnie, **wiadomości o przelewie** (proszę sprawdzić pole kwoty przelewu).

Aby wysłać **komentarz** należy skonfigurować `forward payload`. Proszę ustawić **pierwsze 32 bity na 0x0** i dołączyć **swój tekst**.

`forward payload` jest wysyłany w wewnętrznej wiadomości `transfer notification`. Zostanie on wygenerowany tylko wtedy, gdy `forward amount` > 0.

Wreszcie, aby pobrać wiadomość `Excess`, należy ustawić `miejsce docelowe odpowiedzi`.

:::tip
Proszę sprawdzić [best practices](/develop/dapps/asset-processing/jettons#best-practices) dla przykładu *"send jettons with comments"*.
:::

## Przetwarzanie poza łańcuchem Jetton

:::info Potwierdzenie transakcji
Transakcje TON są nieodwracalne po jednym potwierdzeniu. Aby uzyskać najlepsze wrażenia użytkownika, zaleca się unikanie czekania na dodatkowe bloki po sfinalizowaniu transakcji na blockchainie TON. Więcej informacji znajdą Państwo w dokumencie [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

Istnieją dwa sposoby akceptacji Jettonów:

- w ramach \*\* scentralizowanego gorącego portfela\*\*.
- przy użyciu portfela z **oddzielnym adresem** dla **każdego indywidualnego użytkownika**.

Ze względów bezpieczeństwa zaleca się posiadanie **oddzielnych gorących portfeli** dla **oddzielnych Jettonów** (wiele portfeli dla każdego typu aktywów).

Podczas przetwarzania środków zaleca się również zapewnienie zimnego portfela do przechowywania nadwyżek środków, które nie uczestniczą w automatycznych procesach wpłat i wypłat.

### Dodawanie nowych Jettonów do przetwarzania zasobów i wstępnej weryfikacji

1. Proszę znaleźć poprawny adres [smart contract] (/develop/dapps/asset-processing/jettons#jetton-master-smart-contract).
2. Proszę pobrać [metadane](/develop/dapps/asset-processing/jettons#retrieving-jetton-data).
3. Proszę sprawdzić, czy nie ma [scam](/develop/dapps/asset-processing/jettons#jetton-master-smart-contract).

### Identyfikacja nieznanego urządzenia Jetton podczas odbierania komunikatu powiadomienia o transferze

Jeśli w Państwa portfelu zostanie odebrana wiadomość z powiadomieniem o transferze dotycząca nieznanego Jettona, oznacza to, że Państwa portfel
został utworzony w celu przechowywania konkretnego Jettona.

Adres nadawcy wewnętrznej wiadomości zawierającej treść `Transfer notification` jest adresem nowego portfela Jetton.
Nie należy go mylić z polem `sender` w powiadomieniu `Transfer notification` [body] (/develop/dapps/asset-processing/jettons#jetton-wallets-communication-overview).

1. Proszę pobrać adres główny Jetton dla nowego portfela Jetton poprzez [getting wallet data](/develop/dapps/asset-processing/jettons#retrieving-data-for-a-specific-jetton-wallet).
2. Proszę pobrać adres portfela Jetton dla swojego adresu portfela (jako właściciela) za pomocą głównego kontraktu Jetton: [Jak pobrać adres portfela Jetton dla danego użytkownika] (#retrieving-jetton-wallet-addresses-for-a-given-user)
3. Proszę porównać adres zwrócony przez główny kontrakt i rzeczywisty adres tokena portfela.
   Jeśli się zgadzają, to idealnie. Jeśli nie, to prawdopodobnie otrzymali Państwo fałszywy token.
4. Pobieranie metadanych Jetton: [Jak otrzymać metadane Jetton](#retrieving-jetton-data).
5. Proszę sprawdzić pola `symbol` i `name` pod kątem oznak oszustwa. W razie potrzeby proszę ostrzec użytkownika. [Dodawanie nowych Jettons do przetwarzania i wstępnej weryfikacji](#adding-new-jettons-for-asset-processing-and-initial-verification).

### Przyjmowanie Jettonów od użytkowników za pośrednictwem scentralizowanego portfela

:::info
Aby zapobiec wąskiemu gardłu w transakcjach przychodzących do jednego portfela, sugeruje się przyjmowanie depozytów w wielu portfelach i zwiększanie liczby tych portfeli w razie potrzeby.
:::

W tym scenariuszu usługa płatności tworzy unikalny identyfikator notatki dla każdego nadawcy, ujawniając
adres scentralizowanego portfela i wysyłane kwoty. Nadawca wysyła tokeny
na podany scentralizowany adres z obowiązkową notatką w komentarzu.

**Zalety tej metody:** ta metoda jest bardzo prosta, ponieważ nie ma żadnych dodatkowych opłat przy przyjmowaniu tokenów i są one pobierane bezpośrednio do gorącego portfela.

**Wady tej metody:** ta metoda wymaga od wszystkich użytkowników dołączenia komentarza do przelewu, co może prowadzić do większej liczby błędów wpłat (zapomniane notatki, nieprawidłowe notatki itp.), co oznacza większe obciążenie personelu pomocniczego.

Przykłady Tonweb:

1. [Przyjmowanie wpłat Jetton do indywidualnego portfela HOT z komentarzami (notatka)](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)
2. [Przykład wypłat Jettons](https://github.com/toncenter/examples/blob/main/withdrawals-jettons.js)

#### Przygotowania

1. [Proszę przygotować listę zaakceptowanych Jettonów](/develop/dapps/asset-processing/jettons#adding-new-jettons-for-asset-processing-and-initial-verification) (adresy główne Jettonów).
2. Proszę wdrożyć gorący portfel (używając v3R2, jeśli nie oczekuje się wypłat Jetton; highload v3 - jeśli oczekuje się wypłat Jetton). [Wdrożenie portfela](/develop/dapps/asset-processing/#wallet-deployment).
3. Proszę wykonać testowy transfer Jetton przy użyciu adresu gorącego portfela, aby zainicjować portfel.

#### Przetwarzanie przychodzących Jettonów

1. Proszę załadować listę zaakceptowanych Jettonów.
2. [Odzyskaj adres portfela Jetton](#retrieving-jetton-wallet-addresses-for-a-given-user) dla wdrożonego gorącego portfela.
3. Proszę pobrać adres główny Jetton dla każdego portfela Jetton za pomocą [getting wallet data] (/develop/dapps/asset-processing/jettons#retrieving-data-for-a-specific-jetton-wallet).
4. Proszę porównać adresy umów głównych Jetton z kroku 1. i kroku 3 (bezpośrednio powyżej).
   Jeśli adresy nie są zgodne, należy zgłosić błąd weryfikacji adresu Jetton.
5. Pobiera listę ostatnich nieprzetworzonych transakcji przy użyciu konta hot wallet i
   iteruje ją (sortując każdą transakcję po kolei). Proszę zobaczyć:  [Sprawdzanie transakcji kontraktu](https://docs.ton.org/develop/dapps/asset-processing/#checking-contracts-transactions).
6. Proszę sprawdzić wiadomość wejściową (in_msg) pod kątem transakcji i pobrać adres źródłowy z wiadomości wejściowej. [Przykład Tonweb](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L84)
7. Jeśli adres źródłowy jest zgodny z adresem w portfelu Jetton, należy kontynuować przetwarzanie transakcji.
   Jeśli nie, proszę pominąć przetwarzanie transakcji i sprawdzić następną transakcję.
8. Proszę upewnić się, że treść wiadomości nie jest pusta i że pierwsze 32 bity wiadomości pasują do kodu op `transfer notification` `0x7362d09c`.
   [Przykład Tonweb](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L91)
   Jeśli treść wiadomości jest pusta lub kod op jest nieprawidłowy - proszę pominąć transakcję.
9. Proszę odczytać pozostałe dane wiadomości, w tym `query_id`, `amount`, `sender`, `forward_payload`.
   [Układy wiadomości w kontraktach Jetton](#jetton-contract-message-layouts), [Przykład Tonweb](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L105)
10. Proszę spróbować pobrać komentarze tekstowe z danych `forward_payload`. Pierwsze 32 bity muszą odpowiadać
    kodowi op komentarza tekstowego `0x00000000`, a pozostałe - tekstowi zakodowanemu w UTF-8.
    [Przykład Tonweb](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L110)
11. Jeśli dane `forward_payload` są puste lub kod operacji jest nieprawidłowy - proszę pominąć transakcję.
12. Proszę porównać otrzymany komentarz z zapisanymi notatkami. Jeśli istnieje zgodność (identyfikacja użytkownika jest zawsze możliwa) - proszę wpłacić przelew.
13. Proszę zacząć od kroku 5 i powtarzać ten proces, aż przejdą Państwo przez całą listę transakcji.

### Przyjmowanie Jettonów z adresów depozytowych użytkowników

Aby akceptować Jettony z adresów depozytowych użytkowników, konieczne jest, aby usługa płatności utworzyła swój
indywidualny adres (depozyt) dla każdego uczestnika wysyłającego środki. Świadczenie usługi w tym przypadku obejmuje
wykonanie kilku równoległych procesów, w tym tworzenie nowych depozytów, skanowanie bloków w poszukiwaniu transakcji,
wypłacanie środków z depozytów do gorącego portfela i tak dalej.

Ponieważ gorący portfel może korzystać z jednego portfela Jetton dla każdego typu Jetton, konieczne jest utworzenie wielu portfeli
w celu zainicjowania wpłat. Aby utworzyć dużą liczbę portfeli, ale jednocześnie zarządzać nimi za pomocą
jednej frazy seed (lub klucza prywatnego), konieczne jest określenie innego `subwallet_id` podczas tworzenia portfela.
W TON funkcjonalność wymagana do utworzenia subportfela jest obsługiwana przez portfele w wersji v3 i wyższych.

#### Tworzenie subportfela w Tonweb

```js
const WalletClass = tonweb.wallet.all['v3R2'];
const wallet = new WalletClass(tonweb.provider, {
    publicKey: keyPair.publicKey,
    wc: 0,
    walletId: <SUBWALLET_ID>,
});
```

#### Przygotowanie

1. [Proszę przygotować listę zaakceptowanych Jettonów](#adding-new-jettons-for-asset-processing-and-initial-verification).
2. Proszę wdrożyć gorący portfel (używając v3R2, jeśli nie oczekuje się wypłat Jetton; highload v3 - jeśli oczekuje się wypłat Jetton). [Wdrożenie portfela](/develop/dapps/asset-processing/#wallet-deployment).

#### Tworzenie depozytów

1. Akceptuje żądanie utworzenia nowego depozytu dla użytkownika.
2. Proszę wygenerować nowy adres subwallet (v3R2) na podstawie seedu hot wallet. [Tworzenie subportfela w Tonweb](#creating-a-subwallet-in-tonweb)
3. Adres odbiorczy może być podany użytkownikowi jako adres używany do wpłat Jetton (jest to adres
   właściciela portfela Jetton depozytu). Inicjalizacja portfela nie jest wymagana, można to zrobić
   podczas wypłacania Jettonów z depozytu.
4. Aby uzyskać ten adres, konieczne jest obliczenie adresu portfela Jetton za pośrednictwem głównego kontraktu Jetton.
   [Jak pobrać adres portfela Jetton dla danego użytkownika] (#retrieving-jetton-wallet-addresses-for-a-given-user).
5. Proszę dodać adres portfela Jetton do puli adresów w celu monitorowania transakcji i zapisać adres subportfela.

#### Przetwarzanie transakcji

:::info Potwierdzenie transakcji
Transakcje TON są nieodwracalne po jednym potwierdzeniu. Aby uzyskać najlepsze wrażenia użytkownika, zaleca się unikanie czekania na dodatkowe bloki po sfinalizowaniu transakcji na blockchainie TON. Więcej informacji znajdą Państwo w dokumencie [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

Nie zawsze jest możliwe określenie dokładnej ilości Jettonów otrzymanych z wiadomości, ponieważ portfele Jetton
mogą nie wysyłać wiadomości `powiadomienia o transferze`, `nadwyżkach` i `przelewach wewnętrznych`. Nie są one ustandaryzowane. Oznacza to, że
nie ma gwarancji, że wiadomość `internal transfer` może zostać zdekodowana.

W związku z tym, aby określić kwotę otrzymaną w portfelu, należy zażądać sald za pomocą metody get.
Aby pobrać kluczowe dane podczas żądania sald, bloki są używane zgodnie ze stanem konta dla określonego bloku w łańcuchu.
[Przygotowanie do akceptacji bloku przy użyciu Tonweb](https://github.com/toncenter/tonweb/blob/master/src/test-block-subscribe.js).

Proces ten przebiega w następujący sposób:

1. Przygotowanie do akceptacji bloków (poprzez przygotowanie systemu do akceptacji nowych bloków).
2. Pobiera nowy blok i zapisuje poprzedni identyfikator bloku.
3. Odbieranie transakcji z bloków.
4. Proszę filtrować transakcje używane tylko z adresami z puli portfela Jetton.
5. Dekodowanie wiadomości za pomocą treści `transfer notification` w celu otrzymania bardziej szczegółowych danych, w tym adresu
   `nadawcy`, `kwoty` Jetton i komentarza. (Proszę zobaczyć: [Przetwarzanie przychodzących Jettonów](#processing-incoming-jettons))
6. Jeśli istnieje co najmniej jedna transakcja z niedekodowalnymi komunikatami out (treść komunikatu nie zawiera kodów op dla
   `powiadomienia o przelewie` i kodów op dla `przetargów`) lub bez komunikatów out obecnych na koncie
   , wówczas saldo Jetton musi zostać zażądane przy użyciu metody get dla bieżącego bloku, podczas gdy poprzedni blok
   jest używany do obliczenia różnicy sald. Teraz całkowite zmiany depozytu salda są ujawniane dzięki
   transakcjom przeprowadzanym w bloku.
7. Jako identyfikator niezidentyfikowanego transferu Jettons (bez "powiadomienia o transferze") można użyć danych transakcji
   , jeśli istnieje jedna taka transakcja lub dane bloku (jeśli kilka jest obecnych w bloku).
8. Teraz należy sprawdzić, czy saldo depozytu jest prawidłowe. Jeśli saldo depozytu jest wystarczające do zainicjowania transferu między gorącym portfelem a istniejącym portfelem Jetton, należy wypłacić Jettony, aby upewnić się, że saldo portfela zmniejszyło się.
9. Uruchomić ponownie od kroku 2 i powtórzyć cały proces.

#### Wypłaty dokonane z depozytów

Przelewy nie powinny być wykonywane z depozytu do gorącego portfela przy każdym uzupełnieniu depozytu,
ponieważ za operację przelewu pobierana jest prowizja w TON (płacona w opłatach za gaz sieciowy).
Ważne jest, aby określić pewną minimalną ilość Jettonów, które są wymagane, aby przelew
był opłacalny (a tym samym depozyt).

Domyślnie właściciele portfeli depozytowych Jetton nie są inicjowani. Dzieje się tak, ponieważ nie ma z góry określonego
wymogu uiszczania opłat za przechowywanie. Portfele depozytowe Jetton mogą być wdrażane podczas wysyłania wiadomości z ciałem
`transfer`, które następnie można natychmiast zniszczyć. Aby to zrobić, inżynier musi użyć specjalnego mechanizmu
do wysyłania wiadomości: [128 + 32](/develop/smart-contracts/messages#message-modes).

1. Pobieranie listy depozytów oznaczonych do wypłaty do gorącego portfela
2. Pobieranie zapisanych adresów właścicieli dla każdego depozytu
3. Wiadomości są następnie wysyłane na każdy adres właściciela (poprzez połączenie kilku takich wiadomości w partię) z portfela o wysokim obciążeniu
   z dołączoną kwotą TON Jetton. Jest ona określana przez dodanie opłat za inicjalizację portfela v3R2* opłat za wysłanie wiadomości z treścią `transfer` + arbitralnej kwoty TON związanej z `forward_ton_amount`
     (jeśli to konieczne). Załączona kwota TON jest określana przez dodanie opłat za inicjalizację portfela v3R2 (wartość) +
     opłat za wysłanie wiadomości z treścią `transfer` (wartość) + dowolna kwota TON
     dla `forward_ton_amount` (wartość) (jeśli to konieczne).
4. Gdy saldo na adresie stanie się niezerowe, status konta ulegnie zmianie. Proszę poczekać kilka sekund i sprawdzić status
   konta, wkrótce zmieni się on ze stanu `nonexists` na `uninit`.
5. Dla każdego adresu właściciela (ze statusem `uninit`) konieczne jest wysłanie zewnętrznej wiadomości z portfelem v3R2
   init i ciałem z wiadomością `transfer` do wpłaty do portfela Jetton = 128 + 32. Dla `transfer`,
   użytkownik musi określić adres gorącego portfela jako `destination` i `response destination`.
   Można dodać komentarz tekstowy, aby ułatwić identyfikację transferu.
6. Możliwe jest zweryfikowanie dostawy Jetton za pomocą adresu depozytowego na adres gorącego portfela przez
   , biorąc pod uwagę [przetwarzanie informacji o przychodzących Jettonach] (#processing-incoming-jettons).

### Wypłaty Jetton

:::info Ważne

Poniżej znajdą Państwo przewodnik krok po kroku, jak przetwarzać wypłaty jetton.
:::

Aby wypłacić Jettony, portfel wysyła wiadomości z treścią `transfer` do odpowiedniego portfela Jetton.
Portfel Jetton wysyła następnie Jettony do odbiorcy. W dobrej wierze ważne jest, aby dołączyć TON
jako `forward_ton_amount` (i opcjonalny komentarz do `forward_payload`), aby wywołać `powiadomienie o transferze`.
Proszę zobaczyć: [Układy wiadomości w kontraktach Jetton](#jetton-contract-message-layouts).

#### Przygotowanie

1. Proszę przygotować listę Jettonów do wypłaty: [Dodawanie nowych Jettonów do przetwarzania i wstępnej weryfikacji](#adding-new-jettons-for-asset-processing-and-initial-verification)
2. Rozpoczęto wdrażanie gorącego portfela. Zalecana jest wersja Highload v3. [Wdrożenie portfela](/develop/dapps/asset-processing/#wallet-deployment)
3. Proszę wykonać przelew Jetton przy użyciu adresu gorącego portfela, aby zainicjować portfel Jetton i uzupełnić jego saldo.

#### Przetwarzanie wypłat

1. Proszę załadować listę przetworzonych Jettonów
2. Pobieranie adresów portfela Jetton dla wdrożonego gorącego portfela: [Jak pobrać adresy portfela Jetton dla danego użytkownika] (#retrieving-jetton-wallet-addresses-for-a-given-user)
3. Proszę pobrać adresy główne Jetton dla każdego portfela Jetton: [Jak pobrać dane dla portfeli Jetton](#retrieving-data-for-a-specific-jetton-wallet).
   Wymagany jest parametr `jetton` (który jest w rzeczywistości adresem głównego kontraktu Jetton).
4. Proszę porównać adresy z umów głównych Jetton z kroku 1. i kroku 3. Jeśli adresy nie są zgodne, należy zgłosić błąd weryfikacji adresu Jetton.
5. Otrzymywane są żądania wypłaty, które faktycznie wskazują rodzaj Jetton, kwotę przelewu i adres portfela odbiorcy.
6. Proszę sprawdzić saldo portfela Jetton, aby upewnić się, że na koncie znajduje się wystarczająca ilość środków do dokonania wypłaty.
7. Proszę wygenerować [wiadomość](/develop/dapps/asset-processing/jettons#message-0).
8. W przypadku korzystania z portfela o wysokim obciążeniu zaleca się zbieranie partii wiadomości i wysyłanie jednej partii na raz w celu optymalizacji opłat.
9. Proszę zapisać czas wygaśnięcia dla wychodzących wiadomości zewnętrznych (jest to czas do pomyślnego przetworzenia wiadomości przez portfel
   , po jego upływie portfel nie będzie już akceptował wiadomości).
10. Wysłać pojedynczą wiadomość lub więcej niż jedną wiadomość (wiadomości wsadowe).
11. Pobiera listę ostatnich nieprzetworzonych transakcji na koncie hot wallet i iteruje ją.
    Więcej informacji można znaleźć tutaj: [Sprawdzanie transakcji kontraktu](/develop/dapps/asset-processing/#checking-contracts-transactions),
    [Przykład Tonweb](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43) lub
    proszę użyć metody Toncenter API `/getTransactions`.
12. Proszę sprawdzić wiadomości wychodzące na koncie.
13. Jeśli istnieje wiadomość z kodem operacyjnym `transfer`, należy ją zdekodować, aby pobrać wartość `query_id`.
    Odzyskane `query_id` należy oznaczyć jako pomyślnie wysłane.
14. Jeśli czas potrzebny na przetworzenie bieżącej zeskanowanej transakcji jest dłuższy niż
    czasu wygaśnięcia, a wiadomość wychodząca z podanym `query_id`
    nie zostanie znaleziona, wówczas żądanie powinno (jest to opcjonalne) zostać oznaczone jako wygasłe i powinno zostać bezpiecznie wysłane ponownie.
15. Proszę sprawdzić przychodzące wiadomości na koncie.
16. Jeśli istnieje wiadomość, która używa kodu operacyjnego `excesses`, wiadomość powinna zostać zdekodowana, a wartość `query_id`
    powinna zostać pobrana. Znaleziony `query_id` musi zostać oznaczony jako pomyślnie dostarczony.
17. Proszę przejść do kroku 5. Wygasłe żądania, które nie zostały pomyślnie wysłane, powinny zostać przesunięte z powrotem na listę wypłat.

## Przetwarzanie w łańcuchu Jetton

Ogólnie rzecz biorąc, aby zaakceptować i przetworzyć jettony, program obsługi wiadomości odpowiedzialny za wewnętrzne wiadomości używa kodu operacyjnego `op=0x7362d09c`.

:::info Potwierdzenie transakcji
Transakcje TON są nieodwracalne po jednym potwierdzeniu. Aby uzyskać najlepsze wrażenia użytkownika, zaleca się unikanie czekania na dodatkowe bloki po sfinalizowaniu transakcji na blockchainie TON. Więcej informacji znajdą Państwo w dokumencie [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

### Zalecenia dotyczące przetwarzania w łańcuchu

Poniżej znajduje się "lista zaleceń", które należy wziąć pod uwagę podczas **przetwarzania jettonów w łańcuchu**:

1. Proszę **identyfikować przychodzące jettony** używając ich typu portfela, a nie ich głównego kontraktu Jetton. Innymi słowy, Państwa kontrakt powinien wchodzić w interakcje (odbierać i wysyłać wiadomości) z konkretnym portfelem Jetton (a nie z jakimś nieznanym portfelem korzystającym z konkretnego głównego kontraktu Jetton).
2. Podczas łączenia portfela Jetton Wallet i Jetton Master, proszę **sprawdzić**, czy to **połączenie jest dwukierunkowe**, gdzie portfel rozpoznaje kontrakt główny i odwrotnie. Na przykład, jeśli Państwa system kontraktów otrzyma powiadomienie z portfela jetton (który uważa MySuperJetton za swój kontrakt główny), jego informacje o transferze muszą zostać wyświetlone użytkownikowi, przed wyświetleniem `symbolu`, `nazwy` i `obrazu`
   kontraktu MySuperJetton, proszę sprawdzić, czy portfel MySuperJetton używa właściwego systemu kontraktów. Z kolei jeśli Państwa system kontraktowy z jakiegoś powodu musi wysyłać jettony przy użyciu kontraktów głównych MySuperJetton lub MySuperJetton, proszę sprawdzić, czy portfel X jest portfelem używającym tych samych parametrów kontraktu.
   Dodatkowo, przed wysłaniem żądania `transfer` do X, proszę upewnić się, że rozpoznaje on MySuperJetton jako swój master.
3. **Prawdziwa moc** zdecentralizowanych finansów (DeFi) opiera się na możliwości układania protokołów jeden na drugim, jak klocki lego. Na przykład, powiedzmy, że jetton A jest zamieniany na jetton B, który z kolei jest następnie wykorzystywany jako dźwignia finansowa w ramach protokołu pożyczkowego (gdy użytkownik dostarcza płynność), który jest następnie wykorzystywany do zakupu NFT .... i tak dalej. W związku z tym proszę rozważyć, w jaki sposób umowa może służyć nie tylko użytkownikom poza łańcuchem, ale także podmiotom w łańcuchu, dołączając tokenizowaną wartość do powiadomienia o transferze, dodając niestandardowy ładunek, który można wysłać wraz z powiadomieniem o transferze.
4. \*\*Proszę pamiętać, że nie wszystkie umowy są zgodne z tymi samymi standardami. Niestety, niektóre jettony mogą być wrogie (wykorzystujące wektory ataku) i tworzone wyłącznie w celu atakowania niczego niepodejrzewających użytkowników. Ze względów bezpieczeństwa, jeśli dany protokół składa się z wielu kontraktów, proszę nie tworzyć dużej liczby portfeli jettton tego samego typu. W szczególności proszę nie wysyłać jetttonów wewnątrz protokołu pomiędzy kontraktem depozytowym, kontraktem skarbca lub kontraktem konta użytkownika itp. Atakujący mogą celowo zakłócać logikę kontraktu poprzez fałszowanie powiadomień o transferze, kwot jettona lub parametrów ładunku. Proszę zredukować potencjał ataku poprzez używanie tylko jednego portfela w systemie na jettona (dla wszystkich wpłat i wypłat).
5. Często dobrym pomysłem jest również **tworzenie subkontraktów** dla każdego zindywidualizowanego jettona, aby zmniejszyć ryzyko spoofingu adresów (na przykład, gdy wiadomość transferowa jest wysyłana do jettona B przy użyciu kontraktu przeznaczonego dla jettona A).
6. Zdecydowanie zaleca się \*\*pracę z niepodzielnymi jednostkami jetton na poziomie kontraktu. Logika związana z ułamkami dziesiętnymi jest zwykle używana do ulepszania interfejsu użytkownika aplikacji i nie jest związana z numerycznym przechowywaniem rekordów w łańcuchu.

Aby dowiedzieć się **więcej** na temat [Secure Smart Contract Programming in FunC by CertiK](https://blog.ton.org/secure-smart-contract-programming-in-func), prosimy zapoznać się z tym zasobem. Zaleca się, aby programiści **obsługiwali wszystkie wyjątki inteligentnych kontraktów**, aby nigdy nie zostały one pominięte podczas tworzenia aplikacji.

## Zalecenia dotyczące przetwarzania portfela Jetton

Ogólnie rzecz biorąc, wszystkie procedury weryfikacji stosowane do przetwarzania Jetton poza łańcuchem są odpowiednie również dla portfeli. W przypadku przetwarzania portfela Jetton nasze najważniejsze zalecenia są następujące:

1. Kiedy portfel otrzymuje powiadomienie o przelewie z nieznanego portfela jetton, bardzo ważne jest, aby zaufać portfelowi jetton i jego adresowi głównemu, ponieważ może to być złośliwa podróbka. Aby się zabezpieczyć, należy sprawdzić Jetton Master (główny kontrakt) przy użyciu podanego adresu, aby upewnić się, że procesy weryfikacji rozpoznają portfel jetton jako legalny. Po zaufaniu portfelowi i zweryfikowaniu go jako legalnego, można zezwolić mu na dostęp do sald kont i innych danych w portfelu. Jeśli Jetton Master nie rozpoznaje tego portfela, zaleca się, aby w ogóle nie inicjować ani nie ujawniać przelewów jetton i wyświetlać tylko przychodzące przelewy TON (Toncoin dołączone do powiadomień o przelewach).
2. W praktyce, jeśli użytkownik chce wejść w interakcję z Jetton, a nie z portfelem Jetton. Innymi słowy, użytkownicy wysyłają wTON/oUSDT/jUSDT, jUSDC, jDAI zamiast `EQAjN...`/`EQBLE...`
   itd. Często oznacza to, że gdy użytkownik inicjuje transfer jetton, portfel pyta odpowiedniego mastera jetton, który portfel jetton (należący do użytkownika) powinien zainicjować żądanie transferu. Ważne jest, aby **nigdy nie ufać ślepo** tym danym od Mastera (głównego kontraktu). Przed wysłaniem żądania transferu do portfela jetton, proszę zawsze upewnić się, że portfel jetton rzeczywiście należy do Jetton Master, do którego rzekomo należy.
3. **Proszę pamiętać**, że wrodzy Mistrzowie Jetton/portfele Jetton **mogą z czasem zmienić** swoje portfele/Mistrzów. Dlatego konieczne jest, aby użytkownicy dołożyli należytej staranności i sprawdzili legalność wszystkich portfeli, z którymi wchodzą w interakcję przed każdym użyciem.
4. **Zawsze proszę upewnić się**, że wyświetlają Państwo jettony w swoim interfejsie w sposób, który **nie będzie mieszał się z transferami TON**, powiadomieniami systemowymi itp. Nawet parametry `symbol`, `name` i `image`
   mogą zostać spreparowane w celu wprowadzenia użytkowników w błąd, pozostawiając poszkodowanych jako potencjalne ofiary oszustwa. Było kilka przypadków, w których złośliwe jettony były używane do podszywania się pod przelewy TON, błędy powiadomień, zarobki nagród lub ogłoszenia o zamrożeniu aktywów.
5. **Zawsze proszę zwracać uwagę na potencjalnych złośliwych aktorów**, którzy tworzą fałszywe jettony, zawsze dobrym pomysłem jest zapewnienie użytkownikom funkcji potrzebnych do wyeliminowania niechcianych jettonów w ich głównym interfejsie użytkownika.

Autorami są [kosrk](https://github.com/kosrk), [krigga](https://github.com/krigga), [EmelyanenkoK](https://github.com/EmelyanenkoK/) i [tolya-yanot](https://github.com/tolya-yanot/).

## Najlepsze praktyki

Jeśli chcą Państwo przetestować gotowe przykłady, proszę sprawdzić [SDKs](/develop/dapps/asset-processing/jettons#sdks) i spróbować je uruchomić. Poniżej znajdują się fragmenty kodu, które pomogą Państwu zrozumieć przetwarzanie jettona poprzez przykłady kodu.

### Proszę wysłać Jettons z komentarzem

<Tabs groupId="code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

<details>
<summary>
Source code
</summary>

```js
// first 4 bytes are tag of text comment
const comment = new Uint8Array([... new Uint8Array(4), ... new TextEncoder().encode('text comment')]);

await wallet.methods.transfer({
  secretKey: keyPair.secretKey,
  toAddress: JETTON_WALLET_ADDRESS, // address of Jetton wallet of Jetton sender
  amount: TonWeb.utils.toNano('0.05'), // total amount of TONs attached to the transfer message
  seqno: seqno,
  payload: await jettonWallet.createTransferBody({
    jettonAmount: TonWeb.utils.toNano('500'), // Jetton amount (in basic indivisible units)
    toAddress: new TonWeb.utils.Address(WALLET2_ADDRESS), // recepient user's wallet address (not Jetton wallet)
    forwardAmount: TonWeb.utils.toNano('0.01'), // some amount of TONs to invoke Transfer notification message
    forwardPayload: comment, // text comment for Transfer notification message
    responseAddress: walletAddress // return the TONs after deducting commissions back to the sender's wallet address
  }),
  sendMode: 3,
}).send()
```

</details>

</TabItem>
<TabItem value="tonutils-go" label="Golang">

<details>
<summary>
Source code
</summary>

```go
client := liteclient.NewConnectionPool()

// connect to testnet lite server
err := client.AddConnectionsFromConfigUrl(context.Background(), "https://ton.org/global.config.json")
if err != nil {
   panic(err)
}

ctx := client.StickyContext(context.Background())

// initialize ton api lite connection wrapper
api := ton.NewAPIClient(client)

// seed words of account, you can generate them with any wallet or using wallet.NewSeed() method
words := strings.Split("birth pattern then forest walnut then phrase walnut fan pumpkin pattern then cluster blossom verify then forest velvet pond fiction pattern collect then then", " ")

w, err := wallet.FromSeed(api, words, wallet.V3R2)
if err != nil {
   log.Fatalln("FromSeed err:", err.Error())
   return
}

token := jetton.NewJettonMasterClient(api, address.MustParseAddr("EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"))

// find our jetton wallet
tokenWallet, err := token.GetJettonWallet(ctx, w.WalletAddress())
if err != nil {
   log.Fatal(err)
}

amountTokens := tlb.MustFromDecimal("0.1", 9)

comment, err := wallet.CreateCommentCell("Hello from tonutils-go!")
if err != nil {
   log.Fatal(err)
}

// address of receiver's wallet (not token wallet, just usual)
to := address.MustParseAddr("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")
transferPayload, err := tokenWallet.BuildTransferPayload(to, amountTokens, tlb.ZeroCoins, comment)
if err != nil {
   log.Fatal(err)
}

// your TON balance must be > 0.05 to send
msg := wallet.SimpleMessage(tokenWallet.Address(), tlb.MustFromTON("0.05"), transferPayload)

log.Println("sending transaction...")
tx, _, err := w.SendWaitTransaction(ctx, msg)
if err != nil {
   panic(err)
}
log.Println("transaction confirmed, hash:", base64.StdEncoding.EncodeToString(tx.Hash))
```

</details>

</TabItem>
<TabItem value="TonTools" label="Python">

<details>
<summary>
Source code
</summary>

```py
my_wallet = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# for TonCenterClient and LsClient
await my_wallet.transfer_jetton(destination_address='address', jetton_master_address=jetton.address, jettons_amount=1000, fee=0.15) 

# for all clients
await my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jetton wallet address', jettons_amount=1000, fee=0.1)  
```

</details>

</TabItem>

<TabItem value="pytoniq" label="Python">

<details>
<summary>
Source code
</summary>

```py
from pytoniq import LiteBalancer, WalletV4R2, begin_cell
import asyncio

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
    USER_ADDRESS = wallet.address
    JETTON_MASTER_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    DESTINATION_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"

    USER_JETTON_WALLET = (await provider.run_get_method(address=JETTON_MASTER_ADDRESS,
                                                        method="get_wallet_address",
                                                        stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()]))[0].load_address()
    forward_payload = (begin_cell()
                      .store_uint(0, 32) # TextComment op-code
                      .store_snake_string("Comment")
                      .end_cell())
    transfer_cell = (begin_cell()
                    .store_uint(0xf8a7ea5, 32)          # Jetton Transfer op-code
                    .store_uint(0, 64)                  # query_id
                    .store_coins(1 * 10**9)             # Jetton amount to transfer in nanojetton
                    .store_address(DESTINATION_ADDRESS) # Destination address
                    .store_address(USER_ADDRESS)        # Response address
                    .store_bit(0)                       # Custom payload is None
                    .store_coins(1)                     # Ton forward amount in nanoton
                    .store_bit(1)                       # Store forward_payload as a reference
                    .store_ref(forward_payload)         # Forward payload
                    .end_cell())

    await wallet.transfer(destination=USER_JETTON_WALLET, amount=int(0.05*1e9), body=transfer_cell)
    await provider.close_all()

asyncio.run(main())
```

</details>

</TabItem>
</Tabs>

### Proszę zaakceptować Jetton Transfer z parsowaniem komentarzy

<Tabs groupId="parse-code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

<details>
<summary>
Source code
</summary>

```ts
import {
    Address,
    TonClient,
    Cell,
    beginCell,
    storeMessage,
    JettonMaster,
    OpenedContract,
    JettonWallet,
    Transaction
} from '@ton/ton';


export async function retry<T>(fn: () => Promise<T>, options: { retries: number, delay: number }): Promise<T> {
    let lastError: Error | undefined;
    for (let i = 0; i < options.retries; i++) {
        try {
            return await fn();
        } catch (e) {
            if (e instanceof Error) {
                lastError = e;
            }
            await new Promise(resolve => setTimeout(resolve, options.delay));
        }
    }
    throw lastError;
}

export async function tryProcessJetton(orderId: string) : Promise<string> {

    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
    });

    interface JettonInfo {
        address: string;
        decimals: number;
    }

    interface Jettons {
        jettonMinter : OpenedContract<JettonMaster>,
        jettonWalletAddress: Address,
        jettonWallet: OpenedContract<JettonWallet>
    }

    const MY_WALLET_ADDRESS = 'INSERT-YOUR-HOT-WALLET-ADDRESS'; // your HOT wallet

    const JETTONS_INFO : Record<string, JettonInfo> = {
        'jUSDC': {
            address: 'EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728', //
            decimals: 6
        },
        'jUSDT': {
            address: 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA',
            decimals: 6
        },
    }
    const jettons: Record<string, Jettons> = {};

    const prepare = async () => {
        for (const name in JETTONS_INFO) {
            const info = JETTONS_INFO[name];
            const jettonMaster = client.open(JettonMaster.create(Address.parse(info.address)));
            const userAddress = Address.parse(MY_WALLET_ADDRESS);

            const jettonUserAddress =  await jettonMaster.getWalletAddress(userAddress);
          
            console.log('My jetton wallet for ' + name + ' is ' + jettonUserAddress.toString());

            const jettonWallet = client.open(JettonWallet.create(jettonUserAddress));

            //const jettonData = await jettonWallet;
            const jettonData = await client.runMethod(jettonUserAddress, "get_wallet_data")

            jettonData.stack.pop(); //skip balance
            jettonData.stack.pop(); //skip owneer address
            const adminAddress = jettonData.stack.readAddress();


            if (adminAddress.toString() !== (Address.parse(info.address)).toString()) {
                throw new Error('jetton minter address from jetton wallet doesnt match config');
            }

            jettons[name] = {
                jettonMinter: jettonMaster,
                jettonWalletAddress: jettonUserAddress,
                jettonWallet: jettonWallet
            };
        }
    }

    const jettonWalletAddressToJettonName = (jettonWalletAddress : Address) => {
        const jettonWalletAddressString = jettonWalletAddress.toString();
        for (const name in jettons) {
            const jetton = jettons[name];

            if (jetton.jettonWallet.address.toString() === jettonWalletAddressString) {
                return name;
            }
        }
        return null;
    }

    // Subscribe
    const Subscription = async ():Promise<Transaction[]> =>{

      const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
      });

        const myAddress = Address.parse('INSERT-YOUR-HOT-WALLET'); // Address of receiver TON wallet
        const transactions = await client.getTransactions(myAddress, {
            limit: 5,
        });
        return transactions;
    }

    return retry(async () => {

        await prepare();
        const Transactions = await Subscription();

        for (const tx of Transactions) {

            const sourceAddress = tx.inMessage?.info.src;
            if (!sourceAddress) {
                // external message - not related to jettons
                continue;
            }

            if (!(sourceAddress instanceof Address)) {
                continue;
            }

            const in_msg = tx.inMessage;

            if (in_msg?.info.type !== 'internal') {
                // external message - not related to jettons
                continue;
            }

            // jetton master contract address check
            const jettonName = jettonWalletAddressToJettonName(sourceAddress);
            if (!jettonName) {
                // unknown or fake jetton transfer
                continue;
            }

            if (tx.inMessage === undefined || tx.inMessage?.body.hash().equals(new Cell().hash())) {
                // no in_msg or in_msg body
                continue;
            }

            const msgBody = tx.inMessage;
            const sender = tx.inMessage?.info.src;
            const originalBody = tx.inMessage?.body.beginParse();
            let body = originalBody?.clone();
            const op = body?.loadUint(32);
            if (!(op == 0x7362d09c)) {
                continue; // op != transfer_notification
            }

            console.log('op code check passed', tx.hash().toString('hex'));

            const queryId = body?.loadUint(64);
            const amount = body?.loadCoins();
            const from = body?.loadAddress();
            const maybeRef = body?.loadBit();
            const payload = maybeRef ? body?.loadRef().beginParse() : body;
            const payloadOp = payload?.loadUint(32);
            if (!(payloadOp == 0)) {
                console.log('no text comment in transfer_notification');
                continue;
            }

            const comment = payload?.loadStringTail();
            if (!(comment == orderId)) {
                continue;
            }
            
            console.log('Got ' + jettonName + ' jetton deposit ' + amount?.toString() + ' units with text comment "' + comment + '"');
            const txHash = tx.hash().toString('hex');
            return (txHash);
        }
        throw new Error('Transaction not found');
    }, {retries: 30, delay: 1000});
}
```

</details>

</TabItem>
<TabItem value="tonutils-go" label="Golang">

<details>
<summary>
Source code
</summary>

```go
import (
	"context"
	"fmt"
	"log"

	"github.com/xssnick/tonutils-go/address"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/tlb"
	"github.com/xssnick/tonutils-go/ton"
	"github.com/xssnick/tonutils-go/ton/jetton"
	"github.com/xssnick/tonutils-go/tvm/cell"
)

const (
	MainnetConfig   = "https://ton.org/global.config.json"
	TestnetConfig   = "https://ton.org/global.config.json"
	MyWalletAddress = "INSERT-YOUR-HOT-WALLET-ADDRESS"
)

type JettonInfo struct {
	address  string
	decimals int
}

type Jettons struct {
	jettonMinter        *jetton.Client
	jettonWalletAddress string
	jettonWallet        *jetton.WalletClient
}

func prepare(api ton.APIClientWrapped, jettonsInfo map[string]JettonInfo) (map[string]Jettons, error) {
	userAddress := address.MustParseAddr(MyWalletAddress)
	block, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		return nil, err
	}

	jettons := make(map[string]Jettons)

	for name, info := range jettonsInfo {
		jettonMaster := jetton.NewJettonMasterClient(api, address.MustParseAddr(info.address))
		jettonWallet, err := jettonMaster.GetJettonWallet(context.Background(), userAddress)
		if err != nil {
			return nil, err
		}

		jettonUserAddress := jettonWallet.Address()

		jettonData, err := api.RunGetMethod(context.Background(), block, jettonUserAddress, "get_wallet_data")
		if err != nil {
			return nil, err
		}

		slice := jettonData.MustCell(0).BeginParse()
		slice.MustLoadCoins() // skip balance
		slice.MustLoadAddr()  // skip owneer address
		adminAddress := slice.MustLoadAddr()

		if adminAddress.String() != info.address {
			return nil, fmt.Errorf("jetton minter address from jetton wallet doesnt match config")
		}

		jettons[name] = Jettons{
			jettonMinter:        jettonMaster,
			jettonWalletAddress: jettonUserAddress.String(),
			jettonWallet:        jettonWallet,
		}
	}

	return jettons, nil
}

func jettonWalletAddressToJettonName(jettons map[string]Jettons, jettonWalletAddress string) string {
	for name, info := range jettons {
		if info.jettonWallet.Address().String() == jettonWalletAddress {
			return name
		}
	}
	return ""
}

func GetTransferTransactions(orderId string, foundTransfer chan<- *tlb.Transaction) {
	jettonsInfo := map[string]JettonInfo{
		"jUSDC": {address: "EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728", decimals: 6},
		"jUSDT": {address: "EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA", decimals: 6},
	}

	client := liteclient.NewConnectionPool()

	cfg, err := liteclient.GetConfigFromUrl(context.Background(), MainnetConfig)
	if err != nil {
		log.Fatalln("get config err: ", err.Error())
	}

	// connect to lite servers
	err = client.AddConnectionsFromConfig(context.Background(), cfg)
	if err != nil {
		log.Fatalln("connection err: ", err.Error())
	}

	// initialize ton api lite connection wrapper
	api := ton.NewAPIClient(client, ton.ProofCheckPolicySecure).WithRetry()
	master, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		log.Fatalln("get masterchain info err: ", err.Error())
	}

	// address on which we are accepting payments
	treasuryAddress := address.MustParseAddr("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")

	acc, err := api.GetAccount(context.Background(), master, treasuryAddress)
	if err != nil {
		log.Fatalln("get masterchain info err: ", err.Error())
	}

	jettons, err := prepare(api, jettonsInfo)
	if err != nil {
		log.Fatalln("can't prepare jettons data: ", err.Error())
	}

	lastProcessedLT := acc.LastTxLT

	transactions := make(chan *tlb.Transaction)

	go api.SubscribeOnTransactions(context.Background(), treasuryAddress, lastProcessedLT, transactions)

	log.Println("waiting for transfers...")

	// listen for new transactions from channel
	for tx := range transactions {
		if tx.IO.In == nil || tx.IO.In.MsgType != tlb.MsgTypeInternal {
			// external message - not related to jettons
			continue
		}

		msg := tx.IO.In.Msg
		sourceAddress := msg.SenderAddr()

		// jetton master contract address check
		jettonName := jettonWalletAddressToJettonName(jettons, sourceAddress.String())
		if len(jettonName) == 0 {
			// unknown or fake jetton transfer
			continue
		}

		if msg.Payload() == nil || msg.Payload() == cell.BeginCell().EndCell() {
			// no in_msg body
			continue
		}

		msgBodySlice := msg.Payload().BeginParse()

		op := msgBodySlice.MustLoadUInt(32)
		if op != 0x7362d09c {
			continue // op != transfer_notification
		}

		// just skip bits
		msgBodySlice.MustLoadUInt(64)
		amount := msgBodySlice.MustLoadCoins()
		msgBodySlice.MustLoadAddr()

		payload := msgBodySlice.MustLoadMaybeRef()
		payloadOp := payload.MustLoadUInt(32)
		if payloadOp == 0 {
			log.Println("no text comment in transfer_notification")
			continue
		}

		comment := payload.MustLoadStringSnake()
		if comment != orderId {
			continue
		}

		// process transaction
		log.Printf("Got %s jetton deposit %d units with text comment %s\n", jettonName, amount, comment)
		foundTransfer <- tx
	}
}
```

</details>
</TabItem>

<TabItem value="pythoniq" label="Python">

<details>
<summary>
Source code
</summary>

```py
import asyncio

from pytoniq import LiteBalancer, begin_cell

MY_WALLET_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"


async def parse_transactions(provider: LiteBalancer, transactions):
    for transaction in transactions:
        if not transaction.in_msg.is_internal:
            continue
        if transaction.in_msg.info.dest.to_str(1, 1, 1) != MY_WALLET_ADDRESS:
            continue

        sender = transaction.in_msg.info.src.to_str(1, 1, 1)
        value = transaction.in_msg.info.value_coins
        if value != 0:
            value = value / 1e9

        if len(transaction.in_msg.body.bits) < 32:
            print(f"TON transfer from {sender} with value {value} TON")
            continue

        body_slice = transaction.in_msg.body.begin_parse()
        op_code = body_slice.load_uint(32)
        if op_code != 0x7362D09C:
            continue

        body_slice.load_bits(64)  # skip query_id
        jetton_amount = body_slice.load_coins() / 1e9
        jetton_sender = body_slice.load_address().to_str(1, 1, 1)
        if body_slice.load_bit():
            forward_payload = body_slice.load_ref().begin_parse()
        else:
            forward_payload = body_slice

        jetton_master = (
            await provider.run_get_method(
                address=sender, method="get_wallet_data", stack=[]
            )
        )[2].load_address()
        jetton_wallet = (
            (
                await provider.run_get_method(
                    address=jetton_master,
                    method="get_wallet_address",
                    stack=[
                        begin_cell()
                        .store_address(MY_WALLET_ADDRESS)
                        .end_cell()
                        .begin_parse()
                    ],
                )
            )[0]
            .load_address()
            .to_str(1, 1, 1)
        )

        if jetton_wallet != sender:
            print("FAKE Jetton Transfer")
            continue

        if len(forward_payload.bits) < 32:
            print(
                f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton"
            )
        else:
            forward_payload_op_code = forward_payload.load_uint(32)
            if forward_payload_op_code == 0:
                print(
                    f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and comment: {forward_payload.load_snake_string()}"
                )
            else:
                print(
                    f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and unknown payload: {forward_payload} "
                )

        print(f"Transaction hash: {transaction.cell.hash.hex()}")
        print(f"Transaction lt: {transaction.lt}")


async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()
    transactions = await provider.get_transactions(address=MY_WALLET_ADDRESS, count=5)
    await parse_transactions(provider, transactions)
    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</details>
</TabItem>
</Tabs>

## SDK

Listę SDK dla różnych języków (js, python, golang, C#, Rust itp.) można znaleźć [tutaj](/develop/dapps/apis/sdk).

## Proszę zobaczyć również

- [Przetwarzanie płatności](/develop/dapps/asset-processing/)
- [Przetwarzanie NFT na TON](/develop/dapps/asset-processing/nfts)
- [Parsowanie metadanych na TON](/develop/dapps/asset-processing/metadata)
