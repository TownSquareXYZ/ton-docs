import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 자산 처리 개요

여기서 TON 전송이 어떻게 작동하는지에 대한 **간단한 개요**를 찾을 수 있습니다. TON에서 찾을 수 있는 [자산 유형](/develop/dapps/asset-processing/overview#digital-asset-types-on-ton)은 무엇인지, 다음에 읽을 [내용](/develop/dapps/asset-processing/overview#read-next)은 무엇인지, 그리고 [프로그래밍 언어를 사용하여 TON과 상호작용](/develop/dapps/asset-processing/overview#interaction-with-ton-blockchain)하는 방법도 있습니다. 다음 페이지로 넘어가기 전에 아래에 설명된 모든 정보를 이해하는 것이 좋습니다.

## 메시지와 트랜잭션 개요

TON 블록체인은 완전히 비동기적인 접근 방식을 채택하고 있으며, 전통적인 블록체인과는 다른 몇 가지 개념을 포함하고 있습니다. 특히, 블록체인과의 상호작용은 스마트 계약과 외부 세계 사이에서 비동기적으로 전송되는 [메시지](/develop/smart-contracts/guidelines/message-delivery-guarantees)들의 그래프 형태로 이루어집니다. 각 트랜잭션은 하나의 들어오는 메시지와 최대 255개의 나가는 메시지로 구성됩니다.

메시지는 3가지 유형이 있으며, 각각의 설명은 [여기](/develop/smart-contracts/messages#types-of-messages)에서 확인할 수 있습니다. 간단히 설명하면:

- [외부 메시지](/develop/smart-contracts/guidelines/external-messages):
  - `external in message`(때로는 `external message`라고도 함)는 블록체인 외부에서 블록체인 내부의 스마트 계약으로 보내진 메시지입니다.
  - `external out message`(보통 `logs message`라고 불림)는 블록체인 엔터티에서 외부 세계로 보내지는 메시지입니다.
- [내부 메시지](/develop/smart-contracts/guidelines/internal-messages)는 한 블록체인 엔터티에서 다른 엔터티로 보내지며, 디지털 자산과 임의의 데이터 일부를 포함할 수 있습니다.

일반적인 상호작용 경로는 `wallet` 스마트 계약으로 외부 메시지를 보내는 것으로 시작됩니다. 이 계약은 공개 키 암호화를 사용하여 메시지 발신자를 인증하고, 수수료 지불을 담당하며, 내부 블록체인 메시지를 보냅니다. 이 메시지 큐는 방향성 비순환 그래프 또는 트리를 형성합니다.

예를 들어:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- `Alice`는 예를 들어 [Tonkeeper](https://tonkeeper.com/)를 사용하여 `external message`를 자신의 지갑으로 보냅니다.
- `external message`는 소스가 비어 있는 (예: [Tonkeeper](https://tonkeeper.com/)처럼 어디서부터 온 메시지) `wallet A v4` 계약에 대한 입력 메시지입니다.
- `outgoing message`는 `wallet A v4` 계약의 출력 메시지이자 `wallet B v4` 계약의 입력 메시지입니다. 이때 소스는 `wallet A v4`이고, 목적지는 `wallet B v4`입니다.

결과적으로 입력 및 출력 메시지 세트를 가진 두 개의 트랜잭션이 발생합니다.

각 동작은 계약이 메시지를 입력으로 받아들이고(이에 의해 트리거됨), 이를 처리하여 출력 메시지를 생성하거나 생성하지 않는 형태로 이루어지며, 이를 `트랜잭션`이라고 합니다. 트랜잭션에 대한 자세한 내용은 [여기](/develop/smart-contracts/guidelines/message-delivery-guarantees#what-is-a-transaction)에서 확인할 수 있습니다.

이러한 `트랜잭션`은 **오랜 시간** 동안 지속될 수 있습니다. 기술적으로, 메시지 큐가 있는 트랜잭션은 블록으로 집계되어 검증자에 의해 처리됩니다. TON 블록체인의 비동기적 특성으로 인해 메시지 전송 단계에서 트랜잭션의 해시와 논리적 시간(lt)을 예측할 수 없습니다.

블록에 수락된 `트랜잭션`은 최종적이며 수정할 수 없습니다.

:::info 트랜잭션 확인
TON 트랜잭션은 한 번의 확인만으로도 되돌릴 수 없습니다. 최상의 사용자 경험을 위해서는 TON 블록체인에서 트랜잭션이 완료된 후 추가적인 블록을 기다리는 것을 피하는 것이 좋습니다. 자세한 내용은 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인할 수 있습니다.
:::

스마트 계약은 트랜잭션에 대해 여러 유형의 [수수료](/develop/smart-contracts/fees)를 지불합니다(보통은 들어오는 메시지의 잔액에서 지불되며, 이는 [메시지 모드](/develop/smart-contracts/messages#message-modes)에 따라 다릅니다). 수수료의 양은 워크체인 구성에 따라 달라지며, `masterchain`에서는 최대 수수료가 부과되고, `basechain`에서는 훨씬 낮은 수수료가 부과됩니다.

## TON의 디지털 자산 유형

TON에는 세 가지 유형의 디지털 자산이 있습니다.

- Toncoin, 네트워크의 주요 토큰입니다. 블록체인에서 모든 기본 작업에 사용되며, 예를 들어 가스 수수료를 지불하거나 검증을 위한 스테이킹에 사용됩니다.
- 계약 자산은 ERC-20/ERC-721 표준과 유사한 토큰 및 NFT와 같은 자산으로, 임의의 계약에 의해 관리되며 처리에 대한 사용자 정의 규칙이 필요할 수 있습니다. 이 처리에 대한 자세한 내용은 [NFT 처리](/develop/dapps/asset-processing/nfts) 및 [Jetton 처리](/develop/dapps/asset-processing/jettons) 문서에서 확인할 수 있습니다.
- 네이티브 토큰은 네트워크의 모든 메시지에 첨부할 수 있는 특수 자산입니다. 그러나 현재 네이티브 토큰을 발행하는 기능이 비활성화되어 사용되지 않고 있습니다.

## TON 블록체인과의 상호작용

TON 블록체인에서의 기본 작업은 TonLib을 통해 수행할 수 있습니다. TonLib은 TON 노드와 함께 컴파일할 수 있는 공유 라이브러리로, 경량 클라이언트를 위한 서버(lite servers)를 통해 블록체인과 상호작용할 수 있는 API를 제공합니다. TonLib은 모든 수신 데이터를 증명으로 확인하는 신뢰 없는(trustless) 방식을 따르므로, 신뢰할 수 있는 데이터 제공자가 필요하지 않습니다. TonLib에서 사용할 수 있는 메서드는 [TL scheme](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)에 나와 있습니다. 이 메서드는 공유 라이브러리로 사용할 수 있으며, [wrappers](/develop/dapps/asset-processing/#repositories)를 통해 사용할 수 있습니다.

## 다음 읽기

이 문서를 읽은 후에는 다음을 확인할 수 있습니다:

1. [결제 처리](/develop/dapps/asset-processing/)에서 `TON 코인`으로 작업하는 방법을 확인하세요.
2. [Jetton 처리](/develop/dapps/asset-processing/jettons)에서 `jetton`(때때로 `토큰`이라고도 함)으로 작업하는 방법을 확인하세요.
3. [NFT 처리](/develop/dapps/asset-processing/nfts)에서 `NFT`(특별한 유형의 `jetton`)로 작업하는 방법을 확인하세요.
