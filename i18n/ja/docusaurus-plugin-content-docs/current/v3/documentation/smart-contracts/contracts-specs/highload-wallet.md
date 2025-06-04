import Feedback from '@site/src/components/Feedback';

# Highload wallet contracts

When working with many messages in a short period, there is a need for special wallet called Highload wallet. Highload wallet v2 was the main wallet on TON for a long time, but you had to be very careful with it. Otherwise, you could [lock all funds](https://t.me/tonstatus/88).

format@@0(https://github.com/ton-blockchain/Highload-wallet-contract-v3)の登場により、この問題はコントラクトアーキテクチャレベルで解決され、ガス消費量が少なくなりました。 この章では、Highload Wallet V3の基本と覚えておくべき重要なニュアンスについて説明します。

## Highload wallet v3

このウォレットは、非常に高いレートでトランザクションを送信する必要がある人のために作られています。例えば、暗号交換が挙げられます。

- [ソースコード](https://github.com/ton-blockchain/Highload-wallet-contract-v3)

Highload v3 への与えられた外部メッセージ (転送要求) には以下が含まれています:

- 最上位のセル内のシグネチャ（512ビット）。その他のパラメータはそのセルの参照にあります。
- subwallet ID (32 bits)
- refとして送信するためのメッセージ (送信されるシリアル化された内部メッセージ)
- メッセージの送信モード (8 ビット)
- composite query ID - "shift" の 13 ビット と "bit number" の 10 ビット しかし102ビットまでしかできないのは 1023ではなく、最後のこのような使用可能なクエリID(8388605)も緊急事態のために予約されており、通常は使用しないでください。
- 作成日時、またはメッセージのタイムスタンプです。
- タイムアウト

タイムアウトはパラメータとしてHighloadに保存され、すべてのリクエストのタイムアウトに対してチェックされるので、すべてのリクエストのタイムアウトは同じです。 メッセージは、Highload ウォレットに到着した時点のタイムアウトよりも古くない必要があります。 または、`created_at > now() - timeout` が必要です。 クエリIDは、少なくともタイムアウトのためのリプレイ保護のために保存され、おそらく2\*タイムアウトまで保存されます。 しかしタイムアウトより長く保管するべきではありません サブウォレットIDはウォレットに保存されているものと照合されます。 内部refのハッシュはウォレットの公開鍵に対する署名とともにチェックされます。

Highload v3は、任意の外部メッセージから1つのメッセージしか送信できませんが、特別なオペコードを使用してメッセージを自分自身に送信することができます。 内部メッセージを呼び出す際にアクションセルを設定できるようにします 効果的に、1つの外部メッセージにつき最大254件のメッセージを送信することができます(これらの254の中で、別のメッセージが再びHighload Walletに送信された場合の方が多いでしょう)。

ハイロードv3は、すべてのチェックがパスすると、クエリID(リプレイ保護)を常に保存します。 しかし、メッセージは、以下を含むがこれらに限定されないいくつかの条件のために送信されない可能性があります:

- **state init**（必要に応じてメッセージを含み、Highloadウォレットからの内部メッセージの後にアクションセルを設定するために特別なオペコードを使用して送信することができます。)
- 残高が足りません
- 不正なメッセージ構造 (外部からのメッセージを含む - 外部メッセージのみが外部メッセージから直接送信されます。)

Highload v3 は、同じ `query_id` と `created_at` を含む複数の外部を決して実行しません。与えられた `query_id` を忘れるまで、`created_at`条件は、そのようなメッセージが実行されないようにします。 これにより、`query_id` と `created_at` が Highload v3 への転送リクエストの "primary key" になります。

クエリIDを繰り返す(増分)場合、ビット数を最初に繰り返す方が安くなります(手数料に費やされるTONの面で)。 そしてシフトの時のように通常の数字を増やしています 最後のクエリ ID (緊急クエリ ID について覚えておいてください - 上記参照) に達した後、クエリ ID を 0 にリセットできます。 ただし、Highloadのタイムアウト期間がまだ過ぎていない場合 リプレイ保護辞書がいっぱいになりタイムアウトが終わるまで待たなければならない

## ウォレット v2 をハイロードする

:::danger
従来の契約では、Highload wallet v3を使用することをお勧めします。
:::

このウォレットは、短時間で何百ものトランザクションを送信する必要がある人のために作られています。例えば、暗号交換が挙げられます。

これにより、1つのスマートコントラクト通話で最大254トランザクションを送信できます。 また、seqnoの代わりにリプレイ攻撃を解決するために少し異なるアプローチを使用しています。 このウォレットを何度も呼び出して数千の取引を1秒で送ることができます。

:::caution 制限事項
ハイロードウォレットを扱う場合、以下の制限をチェックして考慮する必要があります。
:::

1. 現在、**契約ストレージのサイズ**は65535セル以下でなければいけません。
 old_queriesのサイズがこの制限を超えると、ActionPhaseで例外がスローされ、トランザクションは失敗します。
 失敗したトランザクションは再生されるかもしれません。
2. ガスのリミットについて。現在、**ガスの上限**は1'000'000GASユニットです。 つまり、
 古いクエリを1つのtxでどれだけきれいにするかに制限があります。 期限切れのクエリの数が多い場合、コントラクトは停止します。

That means that it is not recommended to set too high expiration date:
the number of queries during expiration time span should not exceed 1000.

Also, the number of expired queries cleaned in one transaction should be below 100.

## How to

[Highload Walletチュートリアル](/v3/guidelines/smart-contracts/howto/wallet#-high-load-wallet-v3) の記事を読むこともできます。

ウォレットのソースコード:

- [ton/crypto/smartcont/Highload-wallet-v2-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-highload-wallet-v2.fif)

<Feedback />

