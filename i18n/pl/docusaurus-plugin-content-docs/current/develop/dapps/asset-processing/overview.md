import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Przegląd przetwarzania zasobów

Tutaj znajdą Państwo **krótki przegląd** [jak działają przelewy TON](/develop/dapps/asset-processing/overview#overview-on-messages-and-transactions), jakie [typy aktywów](/develop/dapps/asset-processing/overview#digital-asset-types-on-ton) można znaleźć w TON (i o czym będą Państwo czytać [next](/develop/dapps/asset-processing/overview#read-next)) oraz jak [wchodzić w interakcję z ton](/develop/dapps/asset-processing/overview#interaction-with-ton-blockchain) przy użyciu języka programowania, zalecamy zapoznanie się ze wszystkimi informacjami, które znajdą Państwo poniżej, przed przejściem do następnych stron.

## Przegląd wiadomości i transakcji

Ucieleśniając w pełni asynchroniczne podejście, TON Blockchain obejmuje kilka koncepcji, które są niespotykane w tradycyjnych blockchainach. W szczególności, każda interakcja dowolnego aktora z blockchainem składa się z grafu asynchronicznie przesyłanych [wiadomości] (/develop/smart-contracts/guidelines/message-delivery-guarantees) pomiędzy inteligentnymi kontraktami i/lub światem zewnętrznym. Każda transakcja składa się z jednej wiadomości przychodzącej i do 512 wiadomości wychodzących.

Istnieją 3 rodzaje wiadomości, które są w pełni opisane [tutaj](/develop/smart-contracts/messages#types-of-messages). Krótko mówiąc:

- [wiadomość zewnętrzna](/develop/smart-contracts/guidelines/external-messages):
  - "Zewnętrzna wiadomość" (czasami nazywana po prostu "zewnętrzną wiadomością") to wiadomość, która jest wysyłana z *zewnątrz* blockchaina do inteligentnego kontraktu *wewnątrz* blockchaina.
  - `external out message` (zwykle nazywana `logs message`) jest wysyłana z *blockchain entity* do *świata zewnętrznego*.
- [wiadomość wewnętrzna] (/develop/smart-contracts/guidelines/internal-messages) jest wysyłana z jednego podmiotu *blockchain* do *innego*, może zawierać pewną ilość zasobów cyfrowych i dowolną porcję danych.

Wspólna ścieżka każdej interakcji rozpoczyna się od zewnętrznej wiadomości wysłanej do inteligentnego kontraktu `wallet`, który uwierzytelnia nadawcę wiadomości za pomocą kryptografii klucza publicznego, przejmuje opłatę i wysyła wewnętrzne wiadomości blockchain. Kolejka wiadomości tworzy kierunkowy graf acykliczny lub drzewo.

Na przykład:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- Alice`użyje np. [Tonkeeper](https://tonkeeper.com/), aby wysłać`zewnętrzną wiadomość\` do swojego portfela.
- `external message` to wiadomość wejściowa dla kontraktu `wallet A v4` z pustym źródłem (wiadomość znikąd, taka jak [Tonkeeper](https://tonkeeper.com/)).
- "Wiadomość wychodząca" to wiadomość wyjściowa dla kontraktu "Portfel A v4" i wiadomość wejściowa dla kontraktu "Portfel B v4" ze źródłem "Portfel A v4" i miejscem docelowym "Portfel B v4".

W rezultacie istnieją 2 transakcje z zestawem komunikatów wejściowych i wyjściowych.

Każda akcja, gdy umowa przyjmuje wiadomość jako dane wejściowe (wyzwalane przez nią), przetwarza ją i generuje lub nie generuje wiadomości wychodzących jako dane wyjściowe, zwane `transakcją`. Proszę przeczytać więcej o transakcjach [tutaj](/develop/smart-contracts/guidelines/message-delivery-guarantees#what-is-a-transaction).

Te "transakcje" mogą obejmować **długi okres czasu**. Technicznie rzecz biorąc, transakcje z kolejkami wiadomości są agregowane w bloki przetwarzane przez walidatory. Asynchroniczny charakter TON Blockchain **nie pozwala przewidzieć hasha i lt (czasu logicznego) transakcji** na etapie wysyłania wiadomości.

Transakcja zaakceptowana do bloku jest ostateczna i nie może być modyfikowana.

:::info Potwierdzenie transakcji
Transakcje TON są nieodwracalne po jednym potwierdzeniu. Aby uzyskać najlepsze wrażenia użytkownika, zaleca się unikanie czekania na dodatkowe bloki po sfinalizowaniu transakcji na blockchainie TON. Więcej informacji znajdą Państwo w dokumencie [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

Inteligentne kontrakty płacą kilka rodzajów [opłat](/develop/smart-contracts/fees) za transakcje (zwykle z salda przychodzącej wiadomości, zachowanie zależy od [trybu wiadomości](/develop/smart-contracts/messages#message-modes)). Wysokość opłat zależy od konfiguracji łańcucha roboczego z maksymalnymi opłatami na `masterchain` i znacznie niższymi opłatami na `basechain`.

## Typy zasobów cyfrowych w TON

TON posiada trzy rodzaje zasobów cyfrowych.

- Toncoin, główny token sieci. Jest on używany do wszystkich podstawowych operacji na blockchainie, na przykład do uiszczania opłat za gaz lub stakowania w celu walidacji.
- Aktywa kontraktowe, takie jak tokeny i NFT, które są analogiczne do standardów ERC-20/ERC-721 i są zarządzane przez dowolne kontrakty, a zatem mogą wymagać niestandardowych reguł przetwarzania. Więcej informacji na temat ich przetwarzania znajdą Państwo w artykułach [process NFTs](/develop/dapps/asset-processing/nfts) i [process Jettons](/develop/dapps/asset-processing/jettons).
- Natywny token, który jest specjalnym rodzajem aktywów, które można dołączyć do dowolnej wiadomości w sieci. Aktywa te nie są jednak obecnie używane, ponieważ funkcja wydawania nowych tokenów natywnych jest zamknięta.

## Interakcja z blockchainem TON

Podstawowe operacje na TON Blockchain mogą być wykonywane za pośrednictwem TonLib. Jest to biblioteka współdzielona, którą można skompilować wraz z węzłem TON i udostępnić interfejsy API do interakcji z blockchainem za pośrednictwem tak zwanych serwerów lite (serwerów dla klientów lite). TonLib stosuje podejście bez zaufania, sprawdzając dowody dla wszystkich przychodzących danych; w związku z tym nie ma potrzeby korzystania z zaufanego dostawcy danych. Metody dostępne dla TonLib są wymienione [w schemacie TL] (https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). Mogą być one używane jako biblioteka współdzielona poprzez [wrappers](/develop/dapps/asset-processing/#repositories).

## Czytaj dalej

Po przeczytaniu tego artykułu mogą Państwo sprawdzić:

1. [Przetwarzanie płatności](/develop/dapps/asset-processing/), aby dowiedzieć się, jak pracować z `TON coins`.
2. [Przetwarzanie Jetton](/develop/dapps/asset-processing/jettons), aby dowiedzieć się, jak pracować z `jettons` (czasami nazywanymi `tokens`).
3. [Przetwarzanie NFT](/develop/dapps/asset-processing/nfts), aby dowiedzieć się, jak pracować z `NFT` (czyli specjalnym typem `jetton`).
