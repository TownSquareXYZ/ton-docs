import Feedback from '@site/src/components/Feedback';

# Smart contract addresses

このセクションでは、TON ブロックチェーン上のスマート コントラクト アドレスの詳細について説明します。また、TON においてアクターがどのようにスマート コントラクトと同義であるかについても説明します。

## Everything is a smart contract

TON では、スマート コントラクトは [アクター モデル](/v3/concepts/dive-into-ton/ton-blockchain/blockchain-of-blockchains#single-actor) を使用して構築されます。実際、TON 上のアクターは技術的にはスマート コントラクトとして表現されます。これは、ウォレットさえも単純なアクター (およびスマート コントラクト) であることを意味します。

通常、アクターは受信メッセージを処理し、その内部状態を変更し、結果として送信メッセージを生成します。そのため、TON ブロックチェーン上のすべてのアクター (つまり、スマート コントラクト) は、他のアクターからメッセージを受信できるようにアドレスを持たなければなりません。

:::info EVM 経験
On the Ethereum Virtual Machine (EVM), addresses are completely separate from smart contracts. Feel free to learn more about the differences by reading our article ["Six unique aspects of TON Blockchain that will surprise Solidity developers"](https://blog.ton.org/six-unique-aspects-of-ton-blockchain-that-will-surprise-solidity-developers) - *Tal Kol*.
:::

## Address of smart contract

TON のスマート コントラクト アドレスは通常、次の 2 つの主要コンポーネントで構成されます。

- **(workchain_id)**: ワークチェーン ID (符号付き 32 ビット整数) を示します。

- **(account_id)** アカウントのアドレスを示します (ワークチェーンに応じて 64 ～ 512 ビット)。

このドキュメントの生アドレスの概要セクションでは、**(workchain_id, account_id)** ペアがどのように表現されるかについて説明します。

### WorkChain ID and Account ID

#### Workchain ID

[以前に見たように](/v3/concepts/dive-into-ton/ton-blockchain/blockchain-of-blockchains#workchain-blockchain-with-your-own-rules) 、 TON ブロックチェーン上で動作する「2^32」ワークチェーンはいくつでも作成できます。また、32 ビット プレフィックスのスマート コントラクト アドレスがどのように識別され、異なるワークチェーン内のスマート コントラクト アドレスにリンクされるかにも注目しました。これにより、スマート コントラクトは、TON ブロックチェーン上のさまざまなワークチェーンとの間でメッセージを送受信できるようになります。

現在、TON ブロックチェーンではマスターチェーン (workchain_id=-1) と、場合によっては基本ワークチェーン (workchain_id=0) のみが実行されています。

どちらも 256 ビットのアドレスを持っているため、workchain_id は 0 または -1 であり、ワークチェーン内のアドレスは正確に 256 ビットであると想定します。

#### Account ID

All account IDs on TON use 256-bit addresses on the Masterchain and Basechain (also referred to as the basic workchain).

In fact, an Account ID (**account_id**) is defined as the result of applying a hash function (specifically SHA-256) to a smart contract object. Every smart contract operating on the TON Blockchain stores two main components:

1. *Compiled code*. The logic of the smart contract, compiled into bytecode.
2. *Initial state*. The contract's values at the moment it is deployed on-chain.

To derive the contract's address, you calculate the hash of the **(Initial code, Initial state)** pair. We won’t explore how the [TVM](/v3/documentation/tvm/tvm-overview) works at this time, but it is important to understand that account IDs on TON follow this formula:

**account_id = hash(initial code, initial state)**

Later in this documentation, we will dive deeper into the technical specifications of the TVM and TL-B scheme. Now that we are familiar with how the **account_id** is generated and how it interacts with smart contract addresses on TON, let’s discuss Raw and User-Friendly addresses.

## アドレスの状況

各アドレスは、次のいずれかの状態になります。

- `noneexist` - このアドレスでは受け入れられたトランザクションがなかったため、データがありません (または契約が削除されました)。最初はすべての 2<sup>256</sup> アドレスがこの状態にあると言えます。
- `uninit` - アドレスには残高とメタ情報を含むデータが含まれています。この州の住所にはまだスマート コントラクト コード/永続データがありません。たとえば、アドレスが存在しない状態にあり、別のアドレスがそのアドレスにトークンを送信した場合、アドレスはこの状態になります。
- `active`  - アドレスにはスマート コントラクト コード、永続データ、残高が含まれます。この状態では、トランザクション中にいくつかのロジックを実行し、永続データを変更できます。アドレスがこの状態になるのは、アドレスが `uninit` で、state_init パラメータを持つ受信メッセージがあったときです (このアドレスをデプロイできるようにするには、`state_init` と `code` のハッシュが address に等しい必要があることに注意してください)。
- `frozen` - アドレスはいかなる操作も実行できません。この状態には前の状態のハッシュが 2 つだけ含まれています (それぞれコードと状態セル)。アドレスのストレージ料金が残高を超えると、この状態になります。凍結を解除するには、前述のハッシュといくつかの Toncoin を保存する `state_init` と `code` を含む内部メッセージを送信します。回復するのが難しい場合があるため、このような状況を許すべきではありません。アドレスの凍結を解除するプロジェクトがあり、[ここ](https://unfreezer.ton.org/)で見つけることができます。

## Raw and user-friendly addresses

TON 上のスマート コントラクト アドレスがワークチェーンとアカウント ID (特にマスターチェーンとベースチェーン) をどのように活用するかについて簡単に概要を説明した後、これらのアドレスが 2 つの主要な形式で表現されていることを理解することが重要です。

- **ローアドレス**: スマート コントラクト アドレスの元の完全な表現。
- **ユーザーフレンドリーアドレス**: ユーザーフレンドリーなアドレスは、より優れたセキュリティと使いやすさを採用した生アドレスの拡張形式です。

以下では、これら 2 つのアドレス タイプの違いについて詳しく説明し、TON でユーザー フレンドリーなアドレスが使用される理由を詳しく説明します。

### ローアドレス

未加工のスマート コントラクト アドレスは、ワークチェーン ID とアカウント ID *(workchain_id, account_id)* で構成され、次の形式で表示されます。

- [decimal workchain_id\]:[64 hexadecimal digits with account_id\]

以下に、ワークチェーン ID とアカウント ID を一緒に使用した生のスマート コントラクト アドレスの例を示します (**workchain_id** および **account_id** として表されます)。

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

アドレス文字列の先頭にある「-1」に注目してください。これは、マスターチェーンに属する *workchain_id* を示しています。

:::note
アドレス文字列では、対応する小文字 ('a'、'b'、'c'、' など) の代わりに大文字 ('A'、'B'、'C'、'D' など) を使用できます。 d'など）。
:::

#### Issues with raw addresses

ローアドレス フォームを使用すると、次の 2 つの主な問題が発生します。

1. RAW アドレス形式を使用する場合、トランザクションを送信する前にアドレスを検証してエラーを排除することはできません。
   つまり、トランザクションを送信する前に誤ってアドレス文字列の文字を追加または削除すると、トランザクションが間違った宛先に送信され、資金が失われることになります。
2. RAW アドレス形式を使用する場合、ユーザーフレンドリーなアドレスを使用するトランザクションを送信するときに使用されるような特別なフラグを追加することはできません。
   この概念をよりよく理解できるように、以下でどのフラグを使用できるかを説明します。

### User-friendly address

ユーザーフレンドリーなアドレスは、現実世界だけでなく、インターネット上 (パブリック メッセージング プラットフォームや電子メール サービス プロバイダー経由など) でアドレスを共有する TON ユーザーのエクスペリエンスを保護し、簡素化するために開発されました。

#### User-friendly address structure

ユーザーフレンドリーなアドレスは合計 36 バイトで構成され、次のコンポーネントを順番に生成することで取得されます。

1. *[flags - 1 byte]* — アドレスに固定されたフラグは、受信したメッセージに対するスマート コントラクトの反応方法を変更します。
   ユーザーフレンドリーなアドレス形式を採用するフラグ タイプは次のとおりです。

   - バウンス可能です。バウンス可能なアドレス タイプまたはバウンス不可能なアドレス タイプを示します。 (*0x11* は「バウンス可能」、*0x51* は「バウンス不可」)
   - テストネットのみです。テストネットの目的のみに使用されるアドレス タイプを示します。 *0x80* で始まるアドレスは、運用ネットワーク上で実行されているソフトウェアでは受け入れられません。
   - UrlSafe。アドレスに対して URL セーフとして定義されている非推奨のフラグを示します。すべてのアドレスは URL セーフとみなされます。
2. *\[workchain_id - 1 byte]* — ワークチェーン ID (*workchain_id*) は、符号付き 8 ビット整数 *workchain_id* によって定義されます。\
   (BaseChain の場合は *0x00*、MasterChain の場合は *0xff*)
3. *\[account_id - 32 バイト]* — アカウント ID は、([ビッグエンディアン](https://www.freecodecamp.org/news/what-is-endianness-big-endian-vs-little) で構成されます。 -endian/)) ワークチェーン内の 256 ビット アドレス。
4. *\[address verification - 2 bytes]*  — ユーザーフレンドリーなアドレスでは、アドレス検証は前の 34 バイトの CRC16-CCITT 署名で構成されます。 ([例](https://github.com/andreypfau/ton-kotlin/blob/ce9595ec9e2ad0eb311351c8a270ef1bd2f4363e/ton-kotlin-crypto/common/src/crc32.kt))
   実際、ユーザーフレンドリーなアドレスの検証に関する考え方は、ユーザーがアクセスできないようにするためにすべてのクレジット カードで使用されている [Luhn アルゴリズム](https://en.wikipedia.org/wiki/Luhn_algorithm) に非常に似ています。存在しないカード番号を誤って入力した場合。

これら 4 つの主要コンポーネントの追加は、合計で「1 + 1 + 32 + 2 = 36」バイト (ユーザーフレンドリーなアドレスあたり) を意味します。

ユーザーフレンドリーなアドレスを生成するには、開発者は次のいずれかを使用して 36 バイトすべてをエンコードする必要があります。

- *base64* (つまり、数字、ラテン文字の大文字と小文字、「/」と「+」を含む)
- *base64url* (「/」と「+」の代わりに「_」と「-」を使用)

このプロセスが完了すると、スペースなしの 48 文字の長さのユーザーフレンドリーなアドレスの生成が完了します。

:::info DNS アドレスフラッグス
TON では、mywallet.ton などの DNS アドレスが、生のユーザーフレンドリーなアドレスの代わりに使用されることがあります。 DNS アドレスはユーザーフレンドリーなアドレスで構成されており、開発者が TON ドメイン内の DNS レコードからすべてのフラグにアクセスできるようにする必要なフラグがすべて含まれています。
:::

#### User-friendly address encoding examples

たとえば、「テスト ギバー」スマート コントラクト (テストネット マスターチェーンに常駐し、要求した人に 2 つのテスト トークンを送信する特別なスマート コントラクト) は、次の生のアドレスを使用します。

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

上記の「テスト提供者」の生のアドレスは、使いやすいアドレス形式に変換する必要があります。これは、次のように、base64 または Base64url 形式 (以前に紹介した) のいずれかを使用して取得されます。

- `kf/8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15+KsQHFLbKSMiYIny` (base64)
- `kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiyIny` (base64url)

:::info
両方の形式 (*base64* と *base64url*) が有効であり、受け入れる必要があることに注意してください。
:::

#### Bounceable vs non-bounceable addresses

バウンス可能アドレス フラグの背後にある中心的な考え方は、送信者の資金のセキュリティです。

たとえば、宛先のスマート コントラクトが存在しない場合、またはトランザクション中に問題が発生した場合、メッセージは送信者に「返送」され、トランザクションの元の価値 (すべての送金手数料とガス手数料を差し引いた) の残りが構成されます。 ）。
バウンス可能なアドレスに関しては、具体的には次のとおりです。

1. **bounceable=false** フラグは通常、受信者がウォレットであることを意味します。
2. **bounceable=true** フラグは通常、独自のアプリケーション ロジック (DEX など) を備えたカスタム スマート コントラクトを示します。この例では、セキュリティ上の理由から、バウンス不可能なメッセージは送信されるべきではありません。

[非バウンス可能メッセージ](/v3/documentation/smart-contracts/message-management/non-bounceable-messages) について理解を深めるために、ドキュメントでこのトピックの詳細を読んでください。

#### Armored base64 representations

TON ブロックチェーンに関連する追加のバイナリ データは、同様の「装甲化された」base64 ユーザーフレンドリーなアドレス表現を採用しています。これらは、バイト タグの最初の 4 文字に応じて互いに区別されます。たとえば、256 ビットの Ed25519 公開キーは、最初に以下のプロセスを順番に使用して 36 バイトのシーケンスを作成することによって表されます。

- *0x3E* 形式を使用した 1 バイトのタグは公開キーを示します。
- *0xE6* 形式を使用した 1 バイトのタグは、Ed25519 公開鍵を示します。
- Ed25519 公開鍵の標準バイナリ表現を含む 32 バイト
- 前の34バイトのCRC16-CCITTのビッグエンディアン表現を含む2バイト

結果の 36 バイトのシーケンスは、標準的な方法で 48 文字の Base64 または Base64url 文字列に変換されます。たとえば、Ed25519 公開鍵「E39ECDA0A7B0C60A7107EC43967829DBE8BC356A49B9DFC6186B3EAC74B5477D」（通常は「0xE3、0x9E、...、0x7D」などの 32 バイトのシーケンスで表されます）は、 「アーマード」表現は次のようになります。

`Pubjns2gp7DGCnEH7EOWeCnb6Lw1akm538YYaz6sdLVHfRB2`

### Converting user-friendly addresses and raw addresses

ユーザーフレンドリーで生のアドレスを変換する最も簡単な方法は、次のようないくつかの TON API およびその他のツールのいずれかを使用することです。

- [ton.org/address](https://ton.org/address)
- [dton.io API method](https://dton.io/api/address/0:867ac2b47d1955de6c8e23f57994fad507ea3bcfe2a7d76ff38f29ec46729627)
- [メインネット上での toncenter API methods](https://toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)
- [テストネット上での toncenter API methods](https://testnet.toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)

さらに、JavaScript を使用してウォレットのユーザーフレンドリーな生のアドレスを変換するには、次の 2 つの方法があります。

- [ton.js を使用してアドレスをユーザーフレンドリーな形式またはRAWの形式に変換します。](https://github.com/ton-org/ton-core/blob/main/src/address/Address.spec.ts)
- [tonweb を使用してアドレスをユーザーフレンドリーな形式またはRAWの形式に変換します。](https://github.com/toncenter/tonweb/tree/master/src/utils#address-class)

[SDK](/v3/guidelines/dapps/apis-sdks/sdk) を使用して同様のメカニズムを利用することもできます。

### Address examples

TON アドレスの詳細な例については、[TON クックブック](/v3/guidelines/dapps/cookbook#working-with-contracts-addresses) をご覧ください。

## 考えられる問題

TON ブロックチェーンを操作する場合、TON コインを「uninit」ウォレット アドレスに転送することの影響を理解することが重要です。このセクションでは、そのようなトランザクションがどのように処理されるかを明確にするために、さまざまなシナリオとその結果の概要を説明します。

### Toncoin を Uninit アドレスに転送するとどうなりますか?

#### `state_init` が含まれた取引

トランザクションに「state_init」（ウォレットまたはスマートコントラクトのコードとデータで構成されます）を含める場合、スマート コントラクトは、提供された `state_init` を使用して最初にデプロイされます。デプロイメント後、受信メッセージは、すでに初期化されているアカウントへの送信と同様に処理されます。

#### `state_init`および`bounce`フラグが設定されていないトランザクション

メッセージは「uninit」スマート コントラクトに配信できず、送信者に返送されます。消費したガス料金を差し引いた残りの金額が送り主のアドレスに返送されます。

#### `state_init`と`bounce`フラグが設定されていないトランザクション

メッセージは配信できませんが、送信者に返送されることはありません。代わりに、ウォレットがまだ初期化されていない場合でも、送信された金額が受信アドレスに入金され、残高が増加します。これらは、アドレス所有者がスマート ウォレット コントラクトを展開し、その後残高にアクセスできるようになるまで、そこに保存されます。

#### 正しく行う方法

ウォレットをデプロイする最良の方法は、「bounce」フラグをクリアして、そのアドレス (まだ初期化されていない) に TON を送信することです。このステップの後、所有者は、現在の初期化されていないアドレスにある資金を使用してウォレットを展開および初期化できます。このステップは通常、最初のウォレット操作時に発生します。

### TON ブロックチェーンは誤ったトランザクションに対する保護を実装

TON ブロックチェーンでは、標準のウォレットとアプリは、[こちら](#bounceable-vs-non-bounceable-addresses) で説明されているバウンス可能アドレスと非バウンス可能アドレスを使用して、初期化されていないアドレスへのトランザクションの複雑さを自動的に管理します。ウォレットが初期化されていないアドレスにコインを送信する場合、バウンス可能なアドレスとバウンス不可能なアドレスの両方に返送せずにコインを送信するのが一般的です。

バウンス可能/非バウンス形式のアドレスをすぐに取得する必要がある場合は、[ここ](https://ton.org/address/) で行うことができます。

### カスタム製品に対する責任

TON ブロックチェーン上でカスタム製品を開発している場合は、同様のチェックとロジックを実装することが不可欠です。

資金を送金する前に、アプリケーションで受信者のアドレスが初期化されているかどうかを確認してください。
アドレスの状態に基づいて、カスタム アプリケーション ロジックを備えたユーザー スマート コントラクトのバウンス可能アドレスを使用して、資金が確実に返されるようにします。ウォレットにはバウンス不可能なアドレスを使用してください。

<Feedback />

