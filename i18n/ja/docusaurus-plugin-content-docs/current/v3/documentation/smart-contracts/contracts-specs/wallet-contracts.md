import Feedback from '@site/src/components/Feedback';

import ConceptImage from '@site/src/components/conceptImage';
import ThemedImage from '@theme/ThemedImage';

# Wallet contracts

You may have heard about different versions of wallets on TON Blockchain. But what do these versions actually mean, and how do they differ?

この記事では、TONウォレットの様々なバージョンと変更について説明します。

:::info
Before we start, there are some terms and concepts that you should be familiar with to fully understand the article:

- [メッセージ管理](/v3/documentation/smart-contracts/message-management/messages-and-transactions)は、ウォレットの主な機能だからです。
- [FunC language](/v3/documentation/smart-contracts/func/overview), because we will heavily rely on implementations made using it.
  :::

## 共通概念

この緊張を解くには、まず、ウォレットはTONエコシステムにおける特定のエンティティではないことを理解する必要があります。ウォレットはコードとデータからなるスマート・コントラクトに過ぎず、その意味ではTONの他のアクター（つまりスマート・コントラクト）と同等です。

Like your own custom smart contract, or any other one, wallets can receive external and internal messages, send internal messages and logs, and provide `get methods`.
So the question is: what functionality do they provide and how it differs between versions?

各ウォレットのバージョンは、標準的な外部インターフェイスを提供するスマートコントラクトの実装と考えることができ、異なる外部クライアントが同じ方法でウォレットと対話することができます。FunC言語とFift言語によるこれらの実装は、メインのTONモノレポで見つけることができます：

- [トン/クリプト/スマートコント/](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/)

## ベーシックな財布

### ウォレットV1

これは最もシンプルなものです。一度に4つのトランザクションを送ることができるだけで、サインとseqno以外には何もチェックしません。

ウォレットのソースコード：

- [ton/crypto/smartcont/wallet-code.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet.fif)

このバージョンは、いくつかの大きな問題があるため、通常のアプリでは使われていません：

- 契約書からseqnoと公開鍵を取り出す簡単な方法がありません。
- `Valid_until`チェックがないので、トランザクションの確認が遅すぎるということはありません。

The first issue was fixed in `V1R2` and `V1R3`. The `R` stands for **revision**. Usually, revisions are just small updates that only add get methods; you can find all of those in the changes history of `new-wallet.fif`. Hereinafter, we will consider only the latest revisions.

とはいえ、後続の各バージョンは前のバージョンの機能を受け継いでいるため、後のバージョンに役立てるためにも、やはりそれにこだわるべきでしょう。

#### 永続メモリ・レイアウト

- <b>seqno</b>：32ビット長のシーケンス番号。
- <b>公開鍵</b>：256ビット長の公開鍵。

#### 外部メッセージの本文レイアウト

1. データ
  - <b>署名</b>：512ビット長のed25519署名。
  - <b>msg-seqno</b>: 32ビット長のシーケンス番号。
  - <b>(0-4)mode</b>：各メッセージの送信モードを定義する最大4つの8ビット長の整数。
2. メッセージを含むセルへの最大4つの参照。

ご覧のように、ウォレットの主な機能は、外部からTONブロックチェーンと通信する安全な方法を提供することです。seqno`メカニズムはリプレイ攻撃から保護し、`Ed25519署名\`はウォレット機能への認可されたアクセスを提供します。これらのメカニズムは[外部メッセージ](/v3/documentation/smart-contracts/message-management/external-messages)のドキュメントページで詳しく説明されており、外部メッセージを受け取るスマートコントラクトの間ではごく一般的なものなので、それぞれのメカニズムについて詳しく説明することはしません。ペイロードデータは、セルへの最大4つの参照と、対応するモードの数で構成され、[send_raw_message(cell msg, int mode)](/v3/documentation/smart-contracts/func/docs/stdlib#send_raw_message) メソッドに直接転送されます。

:::caution
ウォレットは、あなたがウォレットを通して送信する内部メッセージのバリデーションを提供しないことに注意してください。[内部メッセージのレイアウト](http://localhost:3000/v3/documentation/smart-contracts/message-management/sending-messages#message-layout)に従ってデータをシリアライズするのはプログラマー（つまり外部クライアント）の責任です。
:::

#### 終了コード

| 終了コード | 説明                     |
| ----- | ---------------------- |
| 0x21  | `seqno`チェックに失敗しました。    |
| 0x22  | `Ed25519署名`のチェックに失敗した。 |
| 0x0   | 標準的な正常終了コード。           |

:::info
[TVM](/v3/documentation/tvm/tvm-overview)には[standart exit codes](/v3/documentation/tvm/tvm-exit-codes)があるので(`0x0`もその一つ)、例えば[gas](https://docs.ton.org/develop/smart-contracts/fees)を使い切ると`0xD`コードが表示されます。
:::

#### メソッドを取得する

1. int seqno() は、現在保存されている seqno を返します。
2. int get_public_key は、現在保存されている公開鍵を返します。

### 財布 V2

ウォレットのソースコード：

- [ton/crypto/smartcont/wallet-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc)

このバージョンでは `valid_until` パラメータが導入された。これは、トランザクションの確認が遅すぎることを防ぐために、トランザクションに期限を設定するために使用します。また、このバージョンには `V2R2` で追加された公開鍵の get-method がありません。

以前のバージョンとの違いはすべて `valid_until` 機能を追加した結果です。新しい終了コード `0x23` が追加され、valid_until のチェックに失敗したことを示します。さらに、外部メッセージボディレイアウトに新しいUNIX-timeフィールドが追加され、トランザクションの制限時間が設定された。すべての get メソッドに変更はありません。

#### 外部メッセージの本文レイアウト

1. データ
  - <b>署名</b>：512ビット長のed25519署名。
  - <b>msg-seqno</b>: 32ビット長のシーケンス番号。
  - <b>有効期限</b>：32ビット長のUnix時間整数。
  - <b>(0-4)mode</b>：各メッセージの送信モードを定義する最大4つの8ビット長の整数。
2. メッセージを含むセルへの最大4つの参照。

### ウォレット V3

このバージョンでは `subwallet_id` パラメータが導入され、同じ公開鍵を使用して複数のウォレットを作成できるようにないました（そのため、1つのシードフレーズだけで複数のウォレットを持つことができる）。以前と同様に、`V3R2` では公開鍵の get-method が追加されただけです。

ウォレットのソースコード：

- [ton/crypto/smartcont/wallet3-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)

基本的に、`subwallet_id` はデプロイ時にコントラクトの状態に追加される番号に過ぎません。TONのコントラクトアドレスはその状態とコードのハッシュなので、ウォレットアドレスは異なる`subwallet_id`で変更されます。このバージョンは現在最も広く使われています。ほとんどのユースケースをカバーし、クリーンでシンプルで、以前のバージョンとほとんど変わりません。すべての get メソッドは変わりません。

#### 永続メモリレイアウト

- <b>seqno</b>：32ビットのシーケンス番号。
- <b>サブウォレット</b>：32ビットサブウォレットID。
- <b>公開鍵</b>：256ビットの公開鍵。

#### 外部メッセージのレイアウト

1. データ
  - <b>署名</b>512ビットのED25519署名。
  - <b>サブウォレットID</b>：32ビットのサブウォレットID。
  - <b>msg-seqno</b>: 32ビットのシーケンス番号。
  - <b>有効期限</b>：32ビットUNIX時間整数。
  - <b>(0-4)mode</b>：各メッセージの送信モードを定義する最大4つの8ビット整数。
2. メッセージを含むセルへの最大4つの参照。

#### 終了コード

| 終了コード | 説明                              |
| ----- | ------------------------------- |
| 0x23  | トランザクションの確認が遅すぎた。               |
| 0x23  | `Ed25519署名`のチェックに失敗した。          |
| 0x21  | `seqno`のチェックに失敗した。              |
| 0x22  | `subwallet-id`が保存されているものと一致しない。 |
| 0x0   | 標準的な正常終了コード。                    |

### ウォレット V4

このバージョンは、以前のバージョンの機能をすべて保持しているが、非常に強力なもの、`プラグイン`を導入しています。

ウォレットのソースコード：

- [トン・ブロックチェーン／ウォレット契約](https://github.com/ton-blockchain/wallet-contract)

この機能により、開発者はユーザーのウォレットと連動する複雑なロジックを実装することができる。例えば、あるDAppが特定の機能を使うために、ユーザーに毎日少額のコインを支払うよう要求することがある。この場合、ユーザーはトランザクションに署名することで、自分のウォレットにプラグインをインストールする必要がある。そしてプラグインは、外部メッセージによって要求されると、毎日コインを宛先アドレスに送る。

#### プラグイン

プラグインは基本的にTON上の他のスマートコントラクトであり、開発者が自由に実装できる。ウォレットとの関係では、プラグインは単に、ウォレットの永続メモリ内の[辞書](/v3/documentation/smart-contracts/func/docs/dictionaries)に格納されたスマートコントラクトのアドレスです。これらのプラグインは、ウォレットに内部メッセージを送信することで、資金を要求したり、"許可リスト "から削除したりすることができます。

#### 永続メモリ・レイアウト

- <b>seqno</b>：32ビット長のシーケンス番号。
- <b>サブワレットID</b>：32ビット長のサブウォレットID。
- <b>公開鍵</b>：256ビット長の公開鍵。
- <b>plugins</b>: プラグインを含む辞書（空でもよい）

#### 社内メッセージの受信

以前のバージョンのウォレットはすべて、内部メッセージを受け取るための簡単な実装を持っていました。つまり、空の recv_internal メソッドを持っていたのです。しかし、前述したように、ウォレットの4番目のバージョンでは、利用可能な操作が2つ追加されている。内部メッセージ・ボディのレイアウトを見てみよう：

- <b>op-code?</b>:32ビット長のオペレーションコード。これはオプションのフィールドです。メッセージ本文に32ビット未満を含むメッセージ、不正なオペコード、またはプラグインとして登録されていない送信者アドレスは、以前のウォレットバージョンと同様に、単純な転送とみなされます。
- <b>クエリーID</b>：64ビット長整数。このフィールドはスマート・コントラクトの動作には影響しない。コントラクト間のメッセージの連鎖を追跡するために使われる。

1. op-code = 0x706c7567、資金運用要求コード。
  - <b>トンコイン</b>：VARUINT16 要求されたトンコインの量。
  - <b>extra_currencies</b>：要求された追加通貨の量を含む辞書 (空でもよい)。
2. op-code = 0x64737472, 「許可リスト」からのプラグイン送信者の削除を要求する。

#### 外部メッセージの本文レイアウト

- <b>署名</b>：512ビット長のed25519署名。
- <b>サブウォレットID</b>：32ビット長のサブウォレットID。
- <b>有効期限</b>：32ビット長のUnix時間整数。
- <b>msg-seqno</b>: 32ビット長のシーケンス整数。
- <b>オペコード</b>：32ビット長のオペレーションコード。

1. op-code = 0x0、単純な送信。
  - <b>(0-4)mode</b>：各メッセージの送信モードを定義する最大4つの8ビット長の整数。
  - <b>(0-4)messages</b>:メッセージを含むセルへの最大4つの参照。
2. op-code = 0x1、プラグインをデプロイしてインストールする。
  - <b>workchain</b>: 8ビット長整数。
  - <b>残高</b>：VARUINT16 toncoins 初期残高の金額。
  - <b>state-init</b>：プラグインの初期状態を含むセル参照。
  - <b>ボディ</b>：ボディを含むセル参照。
3. op-code = 0x2/0x3、プラグインのインストール/削除。
  - <b>wc_n_address</b>：8ビット長のworkchain_id + 256ビット長のプラグインアドレス。
  - <b>残高</b>：VARUINT16 toncoins 初期残高の金額。
  - <b>クエリーID</b>：64ビット長整数。

ご覧のように、4番目のバージョンでは、以前のバージョンと同様に `0x0` オペコードを通して標準的な機能を提供している。0x2`と`0x3` の操作では、プラグインの辞書を操作することができる。0x2` の場合は、そのアドレスを持つプラグインを自分でデプロイする必要があることに注意してほしい。対照的に、`0x1` オペコードは state_init フィールドを使用してデプロイ処理を行う。

:::tip
If `state_init` doesn't make much sense from its name, take a look at the following references:

- [アドレスイントンブロックチェーン](/v3/documentation/smart-contracts/addresses#workchain-id-and-account-id)
- [デプロイメッセージの送信](/v3/documentation/smart-contracts/func/cookbook#how-to-send-a-deploy-message-with-stateinit-only-with-stateinit-and-body)
- [internal-message-layout](/v3/documentation/smart-contracts/message-management/sending-messages#message-layout)
  :::

#### 終了コード

| 終了コード | 説明                                                                                          |
| ----- | ------------------------------------------------------------------------------------------- |
| 0x24  | `valid_until`チェックに失敗しましました。                                                                 |
| 0x23  | `Ed25519署名`のチェックに失敗しました。                                                                    |
| 0x21  | `seqno`チェックに失敗し、リプライ保護が作動しました。                                                              |
| 0x22  | `subwallet-id`が保存されているものと一致しません。                                                            |
| 0x27  | プラグイン辞書の操作に失敗しました (0x1-0x3 recv_external op-codes)。 |
| 0x50  | 資金要求に十分な資金がありません。                                                                           |
| 0x0   | 標準的な正常終了コード                                                                                 |

#### メソッドを取得する

1. int seqno() は、現在保存されている seqno を返します。
2. int get_public_key() 現在保存されている公開鍵を返します。
3. int get_subwallet_id() 現在のサブウォレット ID を返します。
4. int is_plugin_installed(int wc, int addr_hash) 定義されたワークチェーンIDとアドレスハッシュを持つプラグインがインストールされているかどうかをチェックします。
5. タプル get_plugin_list() はプラグインのリストを返します。

### ウォレット V5

It is the most modern wallet version at the moment, developed by the Tonkeeper team, aimed at replacing V4 and allowing arbitrary extensions. <br></br>
<ThemedImage
alt=""
sources={{
light: '/img/docs/wallet-contracts/wallet-contract-V5.png?raw=true',
dark: '/img/docs/wallet-contracts/wallet-contract-V5_dark.png?raw=true',
}}
/> <br></br><br></br><br></br>
The V5 wallet standard offers many benefits that improve the experience for both users and merchants. V5 supports gas-free transactions, account delegation and recovery, subscription payments using tokens and Toncoin, and low-cost multi-transfers. In addition to retaining the previous functionality (V4), the new contract allows you to send up to 255 messages at a time.

ウォレットのソースコード：

- [ton-blockchain/wallet-contract-v5](https://github.com/ton-blockchain/wallet-contract-v5)

TL-B方式：

- [ton-blockchain/wallet-contract-v5/types.tlb](https://github.com/ton-blockchain/wallet-contract-v5/blob/main/types.tlb)

:::caution
以前のウォレットバージョンの仕様とは対照的に、このウォレットバージョンのインターフェースの実装が比較的複雑であるため、[TL-B](/v3/documentation/data-formats/tlb/tl-b-language)スキームに依存することにします。それぞれについて、いくつかの説明を提供します。とはいえ、基本的な理解はまだ必要であり、ウォレットのソースコードと組み合わせれば十分でしょう。
:::

#### 永続メモリ・レイアウト

```
contract_state$_
    is_signature_allowed:(## 1)
    seqno:#
    wallet_id:(## 32)
    public_key:(## 256)
    extensions_dict:(HashmapE 256 int1) = ContractState;
```

ご覧のように、`ContractState`は以前のバージョンと比べて大きな変更はありません。主な違いは、新しい `is_signature_allowed` という1ビットのフラグで、署名と保存されている公開鍵によるアクセスを制限したり許可したりします。この変更の重要性については後のトピックで説明します。

#### 認証プロセス

```
signed_request$_             // 32 (opcode from outer)
  wallet_id:    #            // 32
  valid_until:  #            // 32
  msg_seqno:    #            // 32
  inner:        InnerRequest //
  signature:    bits512      // 512
= SignedRequest;             // Total: 688 .. 976 + ^Cell

internal_signed#73696e74 signed:SignedRequest = InternalMsgBody;

internal_extension#6578746e
    query_id:(## 64)
    inner:InnerRequest = InternalMsgBody;

external_signed#7369676e signed:SignedRequest = ExternalMsgBody;
```

メッセージの実際のペイロードである `InnerRequest` に入る前に、まず認証プロセスにおいてバージョン5が以前のバージョンとどのように異なるかを見てみましょう。InternalMsgBody`コンビネータには、内部メッセージを通してウォレットアクションにアクセスする2つの方法が記述されています。一つ目の方法は、バージョン4から既に馴染みのある方法です。`extensions_dict\`に保存されている、以前に登録した拡張機能としての認証です。2つ目の方法は、外部からのリクエストと同様に、保存された公開鍵と署名による認証です。

一見、これは不要な機能のように思えるかもしれないが、実際には、ウォレットの拡張インフラに属さない外部サービス（スマートコントラクト）を通じてリクエストを処理できるようにするもので、V5の重要な機能です。ガスフリー取引はこの機能に依存しています。

単純に資金を受け取るという選択肢もあることに注意してください。実質的には、認証プロセスをパスしない内部メッセージの受信はすべて送金とみなされます。

#### 行動

まず最初に注目すべきは `InnerRequest` で、これは認証プロセスですでに見たものであります。以前のバージョンとは対照的に、外部メッセージも内部メッセージも、署名モードの変更（つまり `is_signature_allowed` フラグ）を除けば、同じ機能にアクセスできます。

```
out_list_empty$_ = OutList 0;
out_list$_ {n:#}
    prev:^(OutList n)
    action:OutAction = OutList (n + 1);

action_send_msg#0ec3c86d mode:(## 8) out_msg:^(MessageRelaxed Any) = OutAction;

// Extended actions in V5:
action_list_basic$_ {n:#} actions:^(OutList n) = ActionList n 0;
action_list_extended$_ {m:#} {n:#} action:ExtendedAction prev:^(ActionList n m) = ActionList n (m+1);

action_add_ext#02 addr:MsgAddressInt = ExtendedAction;
action_delete_ext#03 addr:MsgAddressInt = ExtendedAction;
action_set_signature_auth_allowed#04 allowed:(## 1) = ExtendedAction;

actions$_ out_actions:(Maybe OutList) has_other_actions:(## 1) {m:#} {n:#} other_actions:(ActionList n m) = InnerRequest;
```

最初の `OutList` はセル参照のオプションのチェーンで、各セルにはメッセー ジモードによって導かれるメッセージ送信リクエストが含まれます。2番目の `ActionList` は1ビットのフラグである `has_other_actions` によって導かれます。最初の2つの拡張アクションである `action_add_ext` と `action_delete_ext` についてはすでによく知られています。3番目の `action_set_signature_auth_allowed` は公開鍵による認証を制限または許可するもので、ウォレットとやり取りする唯一の方法は拡張機能です。この機能は、秘密鍵を紛失したり漏洩したりした場合に非常に重要になります。

:::info
これは[c5](/v3/documentation/tvm/tvm-overview#result-of-tvm-execution)TVMレジスタを通して実現された結果です。技術的には、空の `OutAction` と `ExtendedAction` を指定してリクエストすることもできますが、その場合は単に資金を受け取るのと同じことになります。
:::

#### 終了コード

| 終了コード | 説明                                                                               |
| ----- | -------------------------------------------------------------------------------- |
| 0x84  | 無効化された状態で署名による認証を試みます。                                                           |
| 0x85  | `seqno`チェックに失敗しました。                                                              |
| 0x86  | `wallet-id`が保存されているものと一致しません。                                                    |
| 0x87  | `Ed25519署名`のチェックに失敗しました。                                                         |
| 0x88  | `valid-until`チェックに失敗しました。                                                        |
| 0x89  | 外部メッセージに対して `send_mode` に +2 ビット (エラーを無視する) が設定されていることを強制します。 |
| 0x8A  | `外部署名`のプレフィックスが受信したものと一致しません。                                                    |
| 0x8B  | 拡張機能の追加操作は成功しませんでした。                                                             |
| 0x8C  | 拡張機能の削除操作は成功しませんでした。                                                             |
| 0x8D  | サポートされていない拡張メッセージ接頭辞                                                             |
| 0x8E  | 拡張機能辞書が空の状態で、署名による認証を無効にしようとしました。                                                |
| 0x8F  | すでに設定されている状態にシグネチャを設定しようとしました。                                                   |
| 0x90  | 署名が無効になっているときに最後の拡張機能を削除しようとしました。                                                |
| 0x91  | エクステンションのワークチェーンが間違っています。                                                        |
| 0x92  | 外部メッセージで署名モードを変更しようとしました。                                                        |
| 0x93  | 無効な `c5`、`action_send_msg` の検証に失敗しました。                                           |
| 0x0   | 標準的な正常終了コード。                                                                     |

:::danger
`0x8E`、`0x90`、`0x92`のウォレット終了コードは、ウォレット機能へのアクセスを失わないようにするためのものであることに注意してください。それでもなお、ウォレットは保存された拡張アドレスが実際に TON に存在するかどうかをチェックしないことを覚えておくべきです。また、空の拡張子辞書と制限された署名モードからなる初期データでウォレットをデプロイすることもできます。その場合でも、最初の拡張機能を追加するまでは、公開鍵を通してウォレットにアクセスすることができます。ですから、これらのシナリオには注意してください。
:::

#### メソッドを取得する

1. int is_signature_allowed() は、格納されている `is_signature_allowed` フラグを返します。
2. int seqno() は、現在保存されている seqno を返します。
3. int get_subwallet_id() 現在のサブウォレット ID を返します。
4. int get_public_key() 現在保存されている公開鍵を返します。
5. cell get_extensions() は、extensions 辞書を返します。

#### Preparing for gasless transactions

As was said, before v5, the wallet smart contract allowed the processing of internal messages signed by the owner. This also allows you to make gasless transactions, e.g., payment of network fees when transferring USDt in USDt itself. The common scheme looks like this:

![画像](/img/gasless.jpg)

:::tip
その結果、この機能を提供するサービス（[Tonkeeper's Battery](https://blog.ton.org/tonkeeper-releases-huge-update#tonkeeper-battery)など）が登場することになります。このサービスは、ユーザーに代わって取引手数料をTONで支払うが、手数料はトークンで請求します。
:::

#### フロー

1. USDtを送信する場合、ユーザーは2つのUSDt送金を含む1つのメッセージに署名します：
  1. 米ドルで受取人の住所へ送金
  2. 少額のUSDtを同サービスに譲渡
2. この署名されたメッセージは、HTTPSによってオフチェーンでサービス・バックエンドに送信されます。サービスバックエンドはこれをTONブロックチェーンに送信し、ネットワーク手数料としてTonコインを支払います。

ガスレスバックエンドAPIのベータ版は[tonapi.io/api-v2](https://tonapi.io/api-v2)で入手可能です。ウォレットアプリを開発していて、これらの方法についてフィードバックがある場合は、[@tonapitech](https://t.me/tonapitech) チャットで共有してください。

ウォレットのソースコード：

- [ton-blockchain/wallet-contract-v5](https://github.com/ton-blockchain/wallet-contract-v5)

## 特別な財布

基本的なウォレットの機能だけでは不十分な場合があります。そのため、`high-load`、`lockup`、`restricted`などの特殊なウォレットがあります。

見てみましょう。

### Highload wallets

短期間に多くのメッセージを扱う場合、高負荷ウォレットと呼ばれる特別なウォレットが必要になります。詳しくは[記事](/v3/documentation/smart-contracts/contracts-specs/highload-wallet)を読んでください。

### ロックアップウォレット

もしあなたが何らかの理由で、時間が経つ前にコインを引き出すことなく、しばらくウォレットにコインを閉じ込めておく必要があるなら、ロックアップウォレットをご覧ください。

ウォレットから何も引き出せない時間を設定することができます。また、アンロック期間を設定することで、設定した期間中にコインを使用できるようにカスタマイズすることもできます。

例：100万コインを保持するウォレットを作成し、10年間の権利確定期間を設定することができます。クリフ期間を1年に設定すると、ウォレットが作成されてから最初の1年間は資金がロックされます。その後、アンロック期間を1ヶ月に設定することができ、1'000'000 TON / 120ヶ月 = ~8333 TON\`が毎月アンロックされます。

ウォレットのソースコード：

- [ton-blockchain/lockup-wallet-contract](https://github.com/ton-blockchain/lockup-wallet-contract)

### 制限付き財布

このウォレットの機能は、通常のウォレットと同じように動作しますが、あらかじめ定義された1つの宛先アドレスのみに送金を制限することです。このウォレットを作成するときに送金先を設定すると、そのアドレスにしか送金できなくなります。ただし、バリデーションコントラクトへの送金は可能なので、このウォレットでバリデーターを実行することもできます。

ウォレットのソースコード：

- [エメリヤーエンコK/指名契約/制限付き財布](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)

## 結論

ご覧のように、TONには様々なバージョンのウォレットがあります。しかし、ほとんどの場合、必要なのは`V3R2`または`V4R2`だけです。また、定期的な資金ロック解除のような追加機能が必要な場合は、特別なウォレットを使用することもできます。

## See also

- [ウォレット・スマートコントラクトを使う](/v3/guidelines/smart-contracts/howto/wallet)
- [基本的な財布の情報源](https://github.com/ton-blockchain/ton/tree/master/crypto/smartcont)
- [バージョンに関するより詳細な技術的説明](https://github.com/toncenter/tonweb/blob/master/src/contract/wallet/WalletSources.md)
- [ウォレットV4のソースと詳細説明](https://github.com/ton-blockchain/wallet-contract)
- [ロックアップウォレットのソースと詳細な説明](https://github.com/ton-blockchain/lockup-wallet-contract)
- [制限付き財布ソース](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)
- [トンでのガス抜き取引](https://medium.com/@buidlingmachine/gasless-transactions-on-ton-75469259eff2)

<Feedback />

