import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 자산 처리 개요

여기에서는 [TON 전송이 어떻게 작동하는지](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions), TON에서 어떤 [자산 유형](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton)을 찾을 수 있는지([다음](/v3/documentation/dapps/assets/overview#read-next)에서 읽을 내용) 그리고 프로그래밍 언어를 사용하여 [TON과 상호작용하는 방법](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain)에 대한 **간단한 개요**를 확인할 수 있습니다. 다음 페이지로 넘어가기 전에 아래에서 설명하는 모든 정보를 이해하는 것이 좋습니다.

## 메시지와 트랜잭션 개요

완전히 비동기 방식을 구현하는 TON 블록체인은 기존 블록체인에서는 흔하지 않은 몇 가지 개념을 포함합니다. 특히 블록체인과의 모든 참여자 상호작용은 스마트 컨트랙트와 외부 세계 사이에서 비동기적으로 전송되는 [메시지](/v3/documentation/smart-contracts/message-management/messages-and-transactions) 그래프로 구성됩니다. 각 트랜잭션은 하나의 수신 메시지와 최대 255개의 발신 메시지로 구성됩니다.

[여기](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages)에서 자세히 설명된 3가지 유형의 메시지가 있습니다. 간단히 말하면:

- [외부 메시지](/v3/documentation/smart-contracts/message-management/external-messages):
  - `외부 수신 메시지`(때때로 그냥 `외부 메시지`라고 함)는 블록체인 *외부*에서 블록체인 *내부*의 스마트 컨트랙트로 전송되는 메시지입니다.
  - `외부 발신 메시지`(일반적으로 `로그 메시지`라고 함)는 *블록체인 엔티티*에서 *외부 세계*로 전송됩니다.
- [내부 메시지](/v3/documentation/smart-contracts/message-management/internal-messages)는 한 *블록체인 엔티티*에서 *다른 엔티티*로 전송되며, 일정 금액의 디지털 자산과 임의의 데이터를 포함할 수 있습니다.

모든 상호작용의 일반적인 경로는 `지갑` 스마트 컨트랙트로 전송되는 외부 메시지로 시작됩니다. 이 컨트랙트는 공개키 암호화를 사용하여 메시지 발신자를 인증하고, 수수료 지불을 담당하며, 내부 블록체인 메시지를 전송합니다. 해당 메시지 큐는 방향성 비순환 그래프 또는 트리를 형성합니다.

예시:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- `Alice`는 예를 들어 [Tonkeeper](https://tonkeeper.com/)를 사용하여 자신의 지갑에 `외부 메시지`를 보냅니다.
- `외부 메시지`는 출처가 없는(예: [Tonkeeper](https://tonkeeper.com/)와 같은) `wallet A v4` 컨트랙트의 입력 메시지입니다.
- `발신 메시지`는 `wallet A v4` 컨트랙트의 출력 메시지이자 `wallet A v4` 출처와 `wallet B v4` 목적지를 가진 `wallet B v4` 컨트랙트의 입력 메시지입니다.

결과적으로 입력 및 출력 메시지 세트가 있는 2개의 트랜잭션이 있습니다.

컨트랙트가 메시지를 입력으로 받고(이에 의해 트리거됨), 처리하고, 발신 메시지를 출력으로 생성하거나 생성하지 않는 각 작업을 `트랜잭션`이라고 합니다. 트랜잭션에 대해 자세히 알아보려면 [여기](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction)를 참조하세요.

이러한 `트랜잭션`은 **장기간** 지속될 수 있습니다. 기술적으로, 메시지 큐가 있는 트랜잭션은 검증자가 처리하는 블록으로 집계됩니다. TON 블록체인의 비동기적 특성으로 인해 메시지를 보내는 단계에서 **트랜잭션의 해시와 lt(논리적 시간)를 예측할 수 없습니다**.

블록에 승인된 `트랜잭션`은 최종적이며 수정할 수 없습니다.

:::info 트랜잭션 확인
TON 트랜잭션은 단 한 번의 확인 후에 되돌릴 수 없습니다. 최상의 사용자 경험을 위해, 트랜잭션이 TON 블록체인에서 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)를 참조하세요.
:::

스마트 컨트랙트는 트랜잭션에 대해 여러 유형의 [수수료](/v3/documentation/smart-contracts/transaction-fees/fees)를 지불합니다(일반적으로 수신 메시지의 잔액에서, 동작은 [메시지 모드](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes)에 따라 다름). 수수료 금액은 워크체인 구성에 따라 다르며 `마스터체인`에서는 최대 수수료가, `베이스체인`에서는 상당히 낮은 수수료가 적용됩니다.

## TON의 디지털 자산 유형

TON에는 세 가지 유형의 디지털 자산이 있습니다.

- Toncoin, 네트워크의 주요 토큰입니다. 가스 수수료 지불이나 검증을 위한 스테이킹과 같은 모든 기본 블록체인 작업에 사용됩니다.
- 토큰과 NFT와 같은 컨트랙트 자산으로, ERC-20/ERC-721 표준과 유사하며 임의의 컨트랙트에 의해 관리되므로 처리에 사용자 지정 규칙이 필요할 수 있습니다. [NFT 처리](/v3/guidelines/dapps/asset-processing/nft-processing/nfts)와 [Jetton 처리](/v3/guidelines/dapps/asset-processing/jettons) 문서에서 처리에 대한 자세한 정보를 확인할 수 있습니다.
- 네이티브 토큰은 네트워크의 모든 메시지에 첨부할 수 있는 특별한 종류의 자산입니다. 하지만 새로운 네이티브 토큰을 발행하는 기능이 닫혀 있어 현재 이 자산은 사용되지 않습니다.

## TON 블록체인과의 상호작용

TON 블록체인의 기본 작업은 TonLib를 통해 수행할 수 있습니다. 이는 TON 노드와 함께 컴파일되어 라이트 서버(라이트 클라이언트용 서버)를 통해 블록체인과 상호작용하기 위한 API를 제공하는 공유 라이브러리입니다. TonLib는 모든 수신 데이터에 대한 증명을 확인하는 무신뢰 방식을 따르므로 신뢰할 수 있는 데이터 제공자가 필요하지 않습니다. TonLib에서 사용할 수 있는 메소드는 [TL 스키마](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)에 나열되어 있습니다. 이들은 [래퍼](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks)를 통해 공유 라이브러리로 사용할 수 있습니다.

## 다음 내용

이 글을 읽은 후에는 다음을 확인할 수 있습니다:

1. `TON 코인` 작업 방법을 알아보려면 [결제 처리](/v3/guidelines/dapps/asset-processing/payments-processing)
2. `제톤`(때로는 `토큰`이라고 함) 작업 방법을 알아보려면 [제톤 처리](/v3/guidelines/dapps/asset-processing/jettons)
3. `NFT`(`제톤`의 특별한 유형) 작업 방법을 알아보려면 [NFT 처리](/v3/guidelines/dapps/asset-processing/nft-processing/nfts)
