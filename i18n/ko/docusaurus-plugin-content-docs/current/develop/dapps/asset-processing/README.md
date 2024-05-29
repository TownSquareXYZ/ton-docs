import Button from '@site/src/components/button';

# 처리 글로벌 개요

이 페이지에는 TON 블록체인에서 디지털 자산을 처리(전송 및 수락)하는 방법을 설명하는 개요와 구체적인 세부 정보가 포함되어 있습니다.

:::info 거래 확인
TON 트랜잭션은 한 번만 확인하면 되돌릴 수 없습니다. 최상의 사용자 경험을 위해 TON 블록체인에서 트랜잭션이 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [캐치체인.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

## 모범 사례

### 톤코인

#### 톤코인 입금

:::info
더 나은 성능을 위해 여러 개의 메모 입금 지갑을 설정하는 것이 좋습니다.
:::

- [메모 예치금](https://github.com/toncenter/examples/blob/main/deposits.js)

#### 톤코인 인출

- [일괄 출금](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)

- [인출](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- [상세 정보](/개발/앱/자산 처리 #글로벌 개요)

### 제튼

- [제톤 프로세싱](/개발/앱/자산 처리/제톤) 읽기

## CEX를 위한 준비된 솔루션

### 토나피 임베드

토나피 임베디드 - 입출금과 함께 작동하도록 설계된 온프레미스 솔루션으로, 고성능의 가벼운 배포를 보장합니다.

- 모든 톤 라이트서버에서 실행되는 신뢰 없는 시스템.
- 톤코인 및 제톤에 대한 입금 및 출금도 유지합니다.
- TF 코어 팀에서 제공하는 권장 MEMO 입금 및 고부하 출금 가이드라인에 따라 개발된 솔루션입니다.

협조가 필요한 경우 [@tonrostislav](https://t.me/tonrostislav)로 문의하시기 바랍니다.

## TON 커뮤니티 제작

#### GO

- [고바이크](https://github.com/gobicycle/bicycle) - 사용자 잔액 보충 및 블록체인 계정으로 결제 송금에 중점을 둔 서비스입니다. 톤과 제톤 모두 지원됩니다. 이 서비스는 개발자가 직면할 수 있는 수많은 함정(제톤에 대한 모든 확인, 올바른 작동 상태 확인, 메시지 재전송, 블록체인이 샤드에 의해 분할될 때 높은 부하 시 성능)을 염두에 두고 작성되었습니다. 새로운 결제에 대한 간단한 HTTP API, 래빗 및 웹훅 알림을 제공합니다.
- [GO 예시](https://github.com/xssnick/tonutils-go#how-to-use)

#### 자바스크립트

ton.js SDK 사용(TON 커뮤니티에서 지원):

- [키 쌍, 지갑 만들기 및 지갑 주소 받기](https://github.com/toncenter/examples/blob/main/common.js)
- [지갑 만들기, 잔액 확인하기, 송금하기](https://github.com/ton-community/ton#usage)

#### Python

톤디케이 라이브러리 사용(톤웹과 유사):

- [지갑 초기화, 지갑 배포를 위한 외부 메시지 생성](https://github.com/tonfactory/tonsdk#create-mnemonic-init-wallet-class-create-external-message-to-deploy-the-wallet)

## 글로벌 개요

완전한 비동기식 접근 방식을 구현하는 TON 블록체인은 기존 블록체인에서 흔히 볼 수 없는 몇 가지 개념을 포함합니다. 특히, 모든 주체와 블록체인의 각 상호작용은 스마트 콘트랙트 및/또는 외부 세계 간에 비동기적으로 전송되는 메시지 그래프로 구성됩니다. 모든 상호작용의 일반적인 경로는 외부 메시지를 '지갑' 스마트 콘트랙트로 전송하는 것으로 시작되며, 지갑은 공개 키 암호화를 사용하여 메시지 발신자를 인증하고 수수료 지불을 담당하며 내부 블록체인 메시지를 전송합니다. 따라서 TON 네트워크에서의 트랜잭션은 블록체인과 사용자의 상호작용이 아니라 메시지 그래프의 노드, 즉 스마트 컨트랙트가 메시지를 수락하고 처리한 결과이며, 이는 새로운 메시지의 출현으로 이어질 수도 있고 그렇지 않을 수도 있습니다. 상호작용은 임의의 수의 메시지와 트랜잭션으로 구성될 수 있으며 장기간에 걸쳐 진행될 수 있습니다. 기술적으로 메시지 대기열이 있는 트랜잭션은 유효성 검사기에 의해 처리되는 블록으로 집계됩니다. TON 블록체인의 비동기적 특성 \*\*으로 인해 메시지를 보내는 단계에서 트랜잭션의 해시 및 lt(논리적 시간)\*\*를 예측할 수 없습니다. 블록에 승인된 트랜잭션은 최종적이며 수정할 수 없습니다.

**각 내부 블록체인 메시지는 한 스마트 컨트랙트에서 다른 스마트 컨트랙트로 전달되는 메시지로, 일정량의 디지털 자산과 임의의 데이터 일부를 담고 있습니다.**

스마트 컨트랙트 가이드라인에서는 32개의 이진 0으로 시작하는 데이터 페이로드를 사람이 읽을 수 있는 텍스트 메시지로 취급할 것을 권장합니다. 지갑과 라이브러리 등 대부분의 소프트웨어는 이 규격을 지원하며, 톤코인과 함께 텍스트 코멘트를 전송하고 다른 메시지에 코멘트를 표시할 수 있습니다.

스마트 콘트랙트는 **거래 수수료**(보통 수신 메시지의 잔액에서)와 콘트랙트에 저장된 코드와 데이터에 대한 **저장 수수료**를 지불합니다. 수수료는 워크체인 구성에 따라 달라지며, '마스터체인'의 수수료는 최대이고 '베이스체인'의 수수료는 상당히 낮습니다.

![](/img/docs/asset-processing/msg_dag_example.svg)

- 외부 메시지`는 빈 수레가 있는 `월렛 A v4\` 컨트랙트에 대한 입력 메시지(예: [톤키퍼](https://tonkeeper.com/)와 같은 출처가 불분명한 메시지)입니다.
- 발신 메시지`는 `월렛 A v4`컨트랙트에 대한 출력 메시지이며`월렛 B v4`컨트랙트에 대한 입력 메시지는`월렛 A v4`소스 및`월렛 B v4`대상을 가진`월렛 B v4\`입니다.

결과적으로 입력 및 출력 메시지 세트가 있는 2개의 트랜잭션이 있습니다.

## TON의 디지털 자산

TON에는 세 가지 유형의 디지털 자산이 있습니다.

- 네트워크의 메인 토큰인 톤코인. 가스비 지불이나 검증을 위한 스테이킹 등 블록체인의 모든 기본 작업에 사용됩니다.
- 네이티브 토큰은 네트워크의 모든 메시지에 첨부할 수 있는 특별한 종류의 자산입니다. 이러한 자산은 현재 새로운 네이티브 토큰을 발행하는 기능이 종료되어 더 이상 사용되지 않습니다.
- 토큰 및 NFT와 같은 컨트랙트 자산은 ERC-20/ERC-721 표준과 유사하며 임의의 컨트랙트에 의해 관리되므로 처리를 위해 사용자 지정 규칙이 필요할 수 있습니다. 이에 대한 자세한 내용은 [NFT 처리하기](/개발/앱/자산 처리하기/nfts) 및 [제톤 처리하기](/개발/앱/자산 처리하기/제톤) 문서에서 확인할 수 있습니다.

### 간단한 톤코인 전송

톤코인을 전송하려면 사용자는 외부 메시지, 즉 외부 세계에서 블록체인으로 보내는 메시지를 통해 특별한 `월렛` 스마트 컨트랙트에 요청을 보내야 합니다(아래 참조). 이 요청을 받으면 '지갑'은 원하는 양의 자산과 선택적 데이터 페이로드(예: 텍스트 코멘트)가 포함된 내부 메시지를 전송합니다.

## 지갑 스마트 컨트랙트

월렛 스마트 컨트랙트는 블록체인 외부의 행위자가 블록체인 엔티티와 상호작용할 수 있도록 하는 역할을 하는 TON 네트워크의 컨트랙트입니다. 일반적으로 세 가지 문제를 해결합니다:

- 소유자를 인증합니다: 소유자가 아닌 사용자의 요청에 대한 처리 및 수수료 지불을 거부합니다.
- 리플레이 보호: 예를 들어 자산을 다른 스마트 컨트랙트로 전송하는 등 하나의 요청을 반복적으로 실행하는 것을 금지합니다.
- 는 다른 스마트 컨트랙트와 임의의 상호작용을 시작합니다.

첫 번째 문제에 대한 표준 솔루션은 공개 키 암호화입니다. '지갑'은 공개 키를 저장하고 요청이 포함된 수신 메시지가 소유자만 알고 있는 해당 개인 키로 서명되었는지 확인합니다. 세 번째 문제에 대한 해결책도 일반적이며, 일반적으로 요청에는 '지갑'이 네트워크에 보내는 완전한 형태의 내부 메시지가 포함됩니다. 그러나 리플레이 보호를 위해 몇 가지 다른 접근 방식이 있습니다.

### Seqno 기반 지갑

Seqno 기반 지갑은 메시지 시퀀싱에 가장 간단한 접근 방식을 따릅니다. 각 메시지에는 '지갑' 스마트 컨트랙트에 저장된 카운터와 일치해야 하는 특수한 `seqno` 정수가 있습니다. 지갑`은 각 요청마다 카운터를 업데이트하여 하나의 요청이 두 번 처리되지 않도록 합니다. 만료 시간으로 요청을 제한하는 기능, 동일한 공개 키로 여러 개의 지갑을 보유할 수 있는 기능 등 공개적으로 사용 가능한 방식이 다른 몇 가지 `월렛`버전이 있습니다. 그러나 이러한 접근 방식의 본질적인 요구사항은 요청을 하나씩 보내야 한다는 것인데, 이는`seqno\` 순서에 공백이 생기면 이후의 모든 요청을 처리할 수 없게 되기 때문입니다.

### 고부하 지갑

이 '지갑' 유형은 만료되지 않은 처리된 요청의 식별자를 스마트 컨트랙트 스토리지에 저장하는 접근 방식을 따릅니다. 이 접근 방식에서는 모든 요청이 이미 처리된 요청과 중복되는지 검사하고, 중복이 감지되면 삭제합니다. 만료로 인해 컨트랙트는 모든 요청을 영원히 저장하지는 않지만, 만료 제한으로 인해 처리할 수 없는 요청은 제거합니다. 이 '지갑'에 대한 요청은 서로 간섭하지 않고 병렬로 전송할 수 있지만, 이 접근 방식은 요청 처리에 대한 보다 정교한 모니터링이 필요합니다.

## 블록체인과의 상호작용

톤 블록체인의 기본 작업은 톤라이브를 통해 수행할 수 있습니다. 이는 TON 노드와 함께 컴파일할 수 있는 공유 라이브러리로, 소위 라이트 서버(라이트 클라이언트용 서버)를 통해 블록체인과의 상호작용을 위한 API를 노출합니다. TonLib은 들어오는 모든 데이터에 대해 증명을 확인하는 신뢰 없는 접근 방식을 따르기 때문에 신뢰할 수 있는 데이터 제공자가 필요하지 않습니다. TonLib에서 사용할 수 있는 방법은 [TL 체계에] 나열되어 있습니다(https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). 이들은 [pyTON](https://github.com/EmelyanenkoK/pyTON) 또는 [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2)와 같은 래퍼를 통해 공유 라이브러리로 사용하거나(기술적으로는 `tonlibjson`의 래퍼입니다), `tonlib-cli`를 통해 사용할 수 있습니다.

## 지갑 배포

TonLib을 통해 지갑을 배포하려면 다음을 수행해야 합니다:

1. createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L213) 또는 해당 래퍼 함수를 통해 개인/공개 키 쌍을 생성합니다([tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)의 예). 개인 키는 로컬에서 생성되며 호스트 머신을 떠나지 않는다는 점에 유의하세요.
2. 활성화된 '지갑' 중 하나에 해당하는 [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L60) 구조를 형성합니다. 현재 `wallet.v3`, `wallet.highload.v1`, `wallet.highload.v2`를 사용할 수 있습니다.
3. getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L249) 메서드를 통해 새 '지갑' 스마트 컨트랙트의 주소를 계산합니다. 기본 리비전 `0`을 사용하고 처리 및 저장 수수료를 낮추기 위해 베이스체인 `workchain=0`에 지갑을 배포하는 것이 좋습니다.
4. 계산된 주소로 톤코인을 전송합니다. 이 주소에는 아직 코드가 없으므로 수신 메시지를 처리할 수 없으므로 `비반송` 모드로 보내야 합니다. 비반송`플래그는 처리에 실패하더라도 반송 메시지와 함께 돈을 반환하지 않아야 함을 나타냅니다. 반송 메커니즘은 실수에 대한 어느 정도의 보호 기능을 제공하므로 다른 거래, 특히 큰 금액을 송금할 때는`비반송\` 플래그를 사용하지 않는 것이 좋습니다.
5. 원하는 [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L148)을 생성합니다(예: 배포 전용 `actionNoop`). 그런 다음 [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) 및 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260)를 사용하여 블록체인과의 상호작용을 시작합니다.
6. getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L254) 메서드로 몇 초 안에 컨트랙트를 확인할 수 있습니다.

:::tip
지갑 튜토리얼](/개발/스마트 컨트랙트/튜토리얼/월렛#-지갑 배포하기)에서 자세히 알아보세요.
:::

## 수신 메시지 값

메시지가 컨트랙트에 가져오는 수신 값을 계산하려면 트랜잭션을 파싱해야 합니다. 이는 메시지가 컨트랙트에 도달할 때 발생합니다. 트랜잭션은 [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236)를 사용해 얻을 수 있습니다. 수신 지갑 트랜잭션의 경우, 올바른 데이터는 수신 메시지 1개와 발신 메시지 0개로 구성됩니다. 그렇지 않으면 외부 메시지가 지갑으로 전송되며, 이 경우 소유자가 톤코인을 사용하거나 지갑이 배포되지 않고 수신 트랜잭션이 반송됩니다.

어쨌든, 일반적으로 메시지가 컨트랙트에 가져오는 금액은 들어오는 메시지의 값에서 나가는 메시지의 값의 합에서 수수료를 뺀 값으로 계산할 수 있습니다: `value_{in_msg} - SUM(value_{out_msg}) - fee`. 기술적으로 트랜잭션 표현에는 이름에 `수수료`가 포함된 세 가지 필드, 즉 총 수수료, 저장 비용과 관련된 수수료 일부, 트랜잭션 처리와 관련된 수수료 일부가 포함됩니다. 첫 번째 항목만 사용해야 합니다.

## 계약의 거래 확인

컨트랙트의 트랜잭션은 [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236)를 사용하여 얻을 수 있습니다. 이 메서드를 사용하면 일부 '트랜잭션아이디'로부터 10개의 트랜잭션을 가져올 수 있습니다. 들어오는 모든 트랜잭션을 처리하려면 다음 단계를 따라야 합니다:

1. 최신 `last_transaction_id`는 [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L235)를 사용하여 얻을 수 있습니다.
2. 10개의 트랜잭션 목록은 `겟트랜잭션` 메서드를 통해 로드해야 합니다.
3. 이 목록에서 보이지 않는 거래는 처리해야 합니다.
4. 수신 결제는 수신 메시지에 소스 주소가 있는 트랜잭션이고, 발신 결제는 수신 메시지에 소스 주소가 없고 발신 메시지도 제시하는 트랜잭션입니다. 이러한 트랜잭션은 그에 따라 처리되어야 합니다.
5. 10개의 거래가 모두 표시되지 않으면 다음 10개의 거래를 로드하고 2,3,4,5단계를 반복해야 합니다.

## 트랜잭션 흐름 확인

트랜잭션 처리 중 메시지 흐름을 추적할 수 있습니다. 메시지 흐름은 DAG이므로 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 메서드를 사용하여 현재 트랜잭션의 입력 `in_msg` 또는 출력 `out_msgs` 메시지를 가져와서 [tryLocateResultTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_result_tx_tryLocateResultTx_get)로 들어오는 트랜잭션을 찾거나 [tryLocateSourceTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_source_tx_tryLocateSourceTx_get)로 나가는 트랜잭션을 찾으면 충분합니다.

## 결제 수락

결제 수락에는 사용자를 구분하는 방법이 다른 몇 가지 접근 방식이 있습니다.

### 송장 기반 접근 방식

첨부된 댓글을 기반으로 결제를 수락하려면 서비스는 다음을 수행해야 합니다.

1. 지갑\` 컨트랙트를 배포합니다.
2. 각 사용자에 대해 고유한 '인보이스'를 생성합니다. uuid32의 문자열 표현이면 충분합니다.
3. 사용자는 댓글로 '송장'을 첨부하여 서비스의 '지갑' 계약에 톤코인을 보내도록 안내받아야 합니다.
4. 서비스는 '지갑' 컨트랙트에 대한 getTransactions 메서드를 정기적으로 폴링해야 합니다.
5. 새 트랜잭션의 경우, 수신 메시지를 추출하고 데이터베이스와 '댓글'을 일치시킨 다음 사용자 계정에 해당 값(**수신 메시지 값** 단락 참조)을 입금해야 합니다.

## 송장

### 톤:// 링크가 있는 송장

간단한 사용자 흐름을 위해 간편한 통합이 필요한 경우 ton:// 링크를 사용하는 것이 적합합니다.
톤코인으로 일회성 결제 및 인보이스에 가장 적합합니다.

```text
ton://transfer/<destination-address>?
    [amount=<toncoin-in-nanocoins>&]
    [text=<url-encoded-utf8-comment>]
```

ton:// 링크 생성의 예입니다:

```typescript
const tonLink = `ton://transfer/${address.toString({
  urlSafe: true,
})}?amount=${amount}${text ? `&text=${encodeURIComponent(text)}` : ''}`;
```

- ✅ 간편한 통합

- 지갑을 연결할 필요가 없습니다.

- 사용자는 결제할 때마다 새로운 QR 코드를 스캔해야 합니다.

- 사용자가 거래에 서명했는지 여부를 추적할 수 없습니다.

- 사용자 주소에 대한 정보 없음

- 이러한 링크를 클릭할 수 없는 플랫폼(예: 텔레그램 데스크톱 클라이언트용 봇의 메시지)에서는 해결방법이 필요합니다.

```mdx-code-block
<Button href="https://github.com/tonkeeper/wallet-api#payment-urls"
colorType="primary" sizeType={'lg'}>
```

자세히 알아보기

```mdx-code-block
</Button>
```

### TON Connect를 사용한 송장

세션 내에서 여러 결제/거래에 서명해야 하거나 일정 시간 동안 지갑에 연결을 유지해야 하는 디앱에 가장 적합합니다.

- 지갑과 영구적인 커뮤니케이션 채널, 사용자 주소에 대한 정보 ✅ 지갑과 영구적인 커뮤니케이션 채널이 있습니다.

- ✅ 사용자는 QR 코드를 한 번만 스캔하면 됩니다.

- ✅ 사용자가 지갑에서 거래를 확인했는지 여부를 확인하고, 반환된 BOC로 거래를 추적할 수 있습니다.

- ✅ 다양한 플랫폼에 대해 기성 SDK 및 UI 키트를 사용할 수 있습니다.

- 한 번만 결제를 보내야 하는 경우, 사용자는 지갑 연결과 거래 확인이라는 두 가지 작업을 수행해야 합니다.

- ❌ 통합은 톤:// 링크보다 더 복잡합니다.

```mdx-code-block
<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
```

자세히 알아보기

```mdx-code-block
</Button>
```

## 결제 보내기

1. 서비스는 보관 수수료로 인한 계약 파기를 방지하기 위해 '지갑'을 배포하고 자금을 유지해야 합니다. 보관 수수료는 일반적으로 연간 1톤코인 미만입니다.
2. 서비스는 사용자로부터 `대상_주소`와 선택적 `댓글`을 받아야 합니다. 당분간은 동일한 (`대상_주소`, `값`, `댓글`) 설정으로 완료되지 않은 발신 결제를 금지하거나, 이전 결제가 확인된 후에만 다음 결제가 시작되도록 해당 결제의 적절한 스케줄을 설정하는 것이 좋습니다.
3. 'comment'를 텍스트로 사용하여 [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L98) 형식을 만듭니다.
4. 대상_주소`, 빈 `공개_키`, `금액`및`msg.dataText\`가 포함된 [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L108) 양식을 작성합니다.
5. 발신 메시지 집합이 포함된 [작업](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L149) 양식을 작성합니다.
6. createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) 및 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) 쿼리를 사용하여 발신 결제를 전송합니다.
7. 서비스는 `wallet` 컨트랙트에 대해 정기적으로 getTransactions 메서드를 폴링해야 합니다. 확인된 트랜잭션을 나가는 결제와 (`대상_주소`, `값`, `댓글`) 기준으로 일치시키면 결제가 완료된 것으로 표시하고, 해당 트랜잭션 해시와 lt(논리적 시간)를 감지하여 사용자에게 표시할 수 있습니다.
8. '고부하' 지갑의 'v3'에 대한 요청은 기본적으로 60초의 만료 시간을 갖습니다. 이 시간이 지나면 처리되지 않은 요청을 네트워크로 안전하게 재전송할 수 있습니다(3~6단계 참조).

## 탐색기

블록체인 탐색기는 https://tonscan.org.

탐색기에서 트랜잭션 링크를 생성하려면 서비스에서 lt(로직 시간), 트랜잭션 해시, 계정 주소(getTransactions 메서드를 통해 lt 및 txhash가 검색된 계정 주소)를 가져와야 합니다. https://tonscan.org 및 https://explorer.toncoin.org/ 에서 해당 tx에 대한 페이지를 다음 형식으로 표시할 수 있습니다:

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`
