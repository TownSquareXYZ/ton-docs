import Feedback from '@site/src/components/Feedback';

import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Asset processing overview

Here you can find a **short overview** on [how TON transfers work](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions), what [asset types](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton) can you find in TON (and what about will you read [next](/v3/documentation/dapps/assets/overview#read-next)) and how to [interact with ton](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain) using your programming language, it's recommended to understand all information, discovered below, before going to the next pages.

## Przegląd wiadomości i transakcji

Embodying a fully asynchronous approach, TON Blockchain involves a few concepts which are uncommon to traditional blockchains. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred [messages](/v3/documentation/smart-contracts/message-management/messages-and-transactions) between smart contracts and/or the external world. Each transaction consists of one incoming message and up to 255 outgoing messages.

There are 3 types of messages, that are fully described [here](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages). To put it briefly:

- [external message](/v3/documentation/smart-contracts/message-management/external-messages):
  - "Zewnętrzna wiadomość" (czasami nazywana po prostu "zewnętrzną wiadomością") to wiadomość, która jest wysyłana z *zewnątrz* blockchaina do inteligentnego kontraktu *wewnątrz* blockchaina.
  - `external out message` (zwykle nazywana `logs message`) jest wysyłana z *blockchain entity* do *świata zewnętrznego*.
- [internal message](/v3/documentation/smart-contracts/message-management/internal-messages) is sent from one *blockchain entity* to *another*, can carry some amount of digital assets and arbitrary portion of data.

Wspólna ścieżka każdej interakcji rozpoczyna się od zewnętrznej wiadomości wysłanej do inteligentnego kontraktu `wallet`, który uwierzytelnia nadawcę wiadomości za pomocą kryptografii klucza publicznego, przejmuje opłatę i wysyła wewnętrzne wiadomości blockchain. Kolejka wiadomości tworzy kierunkowy graf acykliczny lub drzewo.

Na przykład:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- Alice`użyje np. [Tonkeeper](https://tonkeeper.com/), aby wysłać`zewnętrzną wiadomość\` do swojego portfela.
- `external message` is the input message for `wallet A v4` contract with empty source (a message from nowhere, such as [Tonkeeper](https://tonkeeper.com/)).
- "Wiadomość wychodząca" to wiadomość wyjściowa dla kontraktu "Portfel A v4" i wiadomość wejściowa dla kontraktu "Portfel B v4" ze źródłem "Portfel A v4" i miejscem docelowym "Portfel B v4".

W rezultacie istnieją 2 transakcje z zestawem komunikatów wejściowych i wyjściowych.

Each action, when contract take message as input (triggered by it), process it and generate or not generate outgoing messages as output, called `transaction`. Read more about transactions [here](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction).

Te "transakcje" mogą obejmować **długi okres czasu**. Technicznie rzecz biorąc, transakcje z kolejkami wiadomości są agregowane w bloki przetwarzane przez walidatory. Asynchroniczny charakter TON Blockchain **nie pozwala przewidzieć hasha i lt (czasu logicznego) transakcji** na etapie wysyłania wiadomości.

Transakcja zaakceptowana do bloku jest ostateczna i nie może być modyfikowana.

:::info Potwierdzenie transakcji
Transakcje TON są nieodwracalne po jednym potwierdzeniu. Aby uzyskać najlepsze wrażenia użytkownika, zaleca się unikanie czekania na dodatkowe bloki po sfinalizowaniu transakcji na blockchainie TON. Więcej informacji znajdą Państwo w dokumencie [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

Smart contracts pay several types of [fees](/v3/documentation/smart-contracts/transaction-fees/fees) for transactions (usually from the balance of an incoming message, behavior depends on [message mode](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes)). Amount of fees depends on workchain configs with maximal fees on `masterchain` and substantially lower fees on `basechain`.

## Typy zasobów cyfrowych w TON

TON posiada trzy rodzaje zasobów cyfrowych.

- Toncoin, główny token sieci. Jest on używany do wszystkich podstawowych operacji na blockchainie, na przykład do uiszczania opłat za gaz lub stakowania w celu walidacji.
- Contract assets, such as tokens and NFTs, which are analogous to the ERC-20/ERC-721 standards and are managed by arbitrary contracts and thus can require custom rules for processing. You can find more info on it's processing in [process NFTs](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) and [process Jettons](/v3/guidelines/dapps/asset-processing/jettons) articles.
- Natywny token, który jest specjalnym rodzajem aktywów, które można dołączyć do dowolnej wiadomości w sieci. Aktywa te nie są jednak obecnie używane, ponieważ funkcja wydawania nowych tokenów natywnych jest zamknięta.

## Interaction with TON Blockchain

Basic operations on TON Blockchain can be carried out via TonLib. It is a shared library which can be compiled along with a TON node and expose APIs for interaction with the blockchain via so-called lite servers (servers for lite clients). TonLib follows a trustless approach by checking proofs for all incoming data; thus, there is no necessity for a trusted data provider. Methods available to TonLib are listed [in the TL scheme](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). They can be used either as a shared library via [wrappers](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks).

## Czytaj dalej

Po przeczytaniu tego artykułu mogą Państwo sprawdzić:

1. [Payments processing](/v3/guidelines/dapps/asset-processing/payments-processing) to get how to work with `TON coins`
2. [Jetton processing](/v3/guidelines/dapps/asset-processing/jettons) to get how to work with `jettons` (sometime called `tokens`)
3. [NFT processing](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) to get how to work with `NFT` (that is the special type of `jetton`)

<Feedback />

