import Feedback from '@site/src/components/Feedback';

import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Asset processing overview

ここでは、[TONの転送がどのように機能するか](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions)についての**短い概要**を見ることができます。どのような[アセットタイプ](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton)がTONで見つかるか(そして[次に](/v3/documentation/dapps/assets/overview#read-next)を読むか)、そしてあなたのプログラミング言語を使ってどのように[tonとやりとりする](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain)か、 次のページに進む前に、以下のすべての情報を理解することをお勧めします。

## メッセージとトランザクションの概要

完全に非同期的なアプローチを体現するTON Blockchainには、伝統的なブロックチェーンには珍しいいくつかの概念が含まれています。 特に あらゆるアクターとブロックチェーンの相互作用は、スマートコントラクトおよび/または外部の世界間で非同期に転送される [messages](/v3/documentation/smart-contracts/message-management/messages-and-transactions)のグラフで構成されています。 各トランザクションは、1つの受信メッセージと最大255の送信メッセージで構成されています。

メッセージには [here](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages) の3種類があります。簡単に言うと、

- [external message](/v3/documentation/smart-contracts/message-management/external-messages):
  - `external in message` (場合によっては`external message`と呼ばれます) はブロックチェーンの*外側*からブロックチェーン内\*スマートコントラクトに送信されるメッセージです。
  - `external out message` (通常は`logs message`) は*ブロックチェーンエンティティ*から*outside world*に送信されます。
- [internal message](/v3/documentation/smart-contracts/message-management/internal-messages) が *ブロックチェーンエンティティ*から*別のエンティティ*に送信されると、ある量のデジタル資産と任意のデータを運ぶことができます。

このスマートコントラクトは公開鍵暗号を使ってメッセージ送信者を認証し、料金の支払いを担当し、ブロックチェーン内部のメッセージを送信します。そのメッセージのキューは、方向性のある非周期的なグラフ、つまりツリーを形成します。

例:

![](/img/docs/asset-processing/alicemsg.svg)

- `Alice` は e.g [Tonkeeper](https://tonkeeper.com/) を使ってウォレットに `external message` を送信します。
- `external message`は、空のソースを持つ`wallet A v4`コントラクトの入力メッセージです（ [Tonkeeper](https://tonkeeper.com/)など、どこからもメッセージがありません）。
- `output message`は`wallet A v4`コントラクトの出力メッセージで、`wallet A v4`ソースと`wallet B v4`宛先を持つ`wallet B v4`コントラクトのメッセージを入力します。

結果として、入力と出力メッセージのセットを持つ2つのトランザクションが存在します。

それぞれのアクションは、コントラクトが(トリガーされた)入力としてメッセージを取得した場合、それを処理し、`transaction` と呼ばれる出力として送信メッセージを生成または生成しません。 取引 [here](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction) についてもっと読む。

`トランザクション`は**長期間**に及ぶことがあります。技術的には、メッセージのキューを持つトランザクションは、バリデータが処理するブロックに集約されます。TONブロックチェーンの非同期的な性質は、**メッセージを送信する段階で**トランザクションのハッシュとLT（論理時間）を予測することはできません。

ブロックに受け入れられた `transaction` は最終的なものであり、変更することはできません。

:::info トランザクションの承認
TONの取引は、たった1回の確認で元に戻せなくなります。最高のユーザーエクスペリエンスのためには、TONブロックチェーン上でトランザクションが確定したら、追加のブロックを待たないことが推奨されます。詳しくは[Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)をお読みください。
:::

スマートコントラクトは、トランザクションに対していくつかのタイプの [fees](/v3/documentation/smart-contracts/transaction-fees/fees)を支払います。通常、受信メッセージの残高からの動作は[message mode](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes)に依存します。 手数料の額は、 `masterchain` に対する最大手数料のワークチェーン設定と、 `basechain` に対する手数料が実質的に低くなります。

## TONのデジタル資産タイプ

TONには3種類のデジタル資産があります。

- Toncoin、ネットワークのメイントークンは、ブロックチェーン上のすべての基本的な操作に使用されます。例えば、ガス料金を支払ったり、検証のためにステーキングしたりできます。
- トークンやNFTなどのコントラクトアセット ERC-20/ERC-721 規格に類似しており、任意の契約によって管理されているため、処理にはカスタムルールが必要になる可能性があります。 [process NFTs](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) および [process Jettons](/v3/guidelines/dapps/asset-processing/jettons) の記事に詳しい情報があります。
- ネイティブトークンは、ネットワーク上のあらゆるメッセージに添付できる特別な種類のアセットです。しかし、新しいネイティブトークンを発行する機能が閉鎖されたため、これらのアセットは現在使用されていません。

## Interaction with TON Blockchain

TONブロックチェーンに対する基本的な操作は、TonLibを介して行うことができます。TonLibはTONノードと一緒にコンパイルできる共有ライブラリで、いわゆるライトサーバー（ライトクライアント用のサーバー）を介してブロックチェーンとやりとりするためのAPIを公開します。TonLibは、すべての受信データの証明をチェックするトラストレスアプローチに従っているため、信頼できるデータプロバイダーは必要ありません。TonLibで利用可能なメソッドは[TLスキーム](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)に記載されています。これらのメソッドは、[ラッパー](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks)を介して共有ライブラリとして使用することができます。

## 次を読む

本記事を読んだ後、以下の確認をお勧めします：

1. [Payments processing](/v3/guidelines/dapps/asset-processing/payments-processing) を使って、`TON coins`の使い方を学びましょう。
2. [Jetton processing](/v3/guidelines/dapps/asset-processing/jettons) を使って、`tokens`（いつかは`tokens`と呼ばれます）
3. [NFT processing](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) を使って、 `NFT` (これは特殊なタイプの `jetton`)を扱う方法を得ることができます。

<Feedback />

