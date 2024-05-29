# 콘텐츠 구독

TON 블록체인의 거래는 빠르고 네트워크 수수료가 낮기 때문에 스마트 컨트랙트를 통해 온체인에서 반복 결제를 처리할 수 있습니다.

예를 들어, 사용자는 디지털 콘텐츠(또는 다른 모든 콘텐츠)를 구독하고 월 1톤의 요금이 청구될 수 있습니다.

:::tip
이 콘텐츠는 버전 4의 지갑에만 해당하며, 이전 버전의 지갑에는 이 기능이 없으며 향후 버전에서도 변경될 수 있습니다.
:::

:::warning
Subscription contract requires authorization exactly once, on installation; then it can withdraw TON as it pleases. Do your own research before attaching unknown subscriptions.

반면에 사용자 모르게 구독을 설치할 수 없습니다.
:::

## 흐름 예시

- 사용자는 v4 지갑을 사용합니다. 플러그인이라고 하는 추가 스마트 컨트랙트를 통해 기능을 확장할 수 있습니다.

  기능을 확인한 후 사용자는 지갑에 대한 신뢰할 수 있는 스마트 컨트랙트(플러그인)의 주소를 승인할 수 있습니다. 그 후 신뢰할 수 있는 스마트 컨트랙트가 지갑에서 톤코인을 출금할 수 있습니다. 이는 다른 블록체인의 "무한 승인"과 유사합니다.

- 중간 구독 스마트 컨트랙트는 각 사용자와 서비스 사이에서 지갑 플러그인으로 사용됩니다.

  이 스마트 컨트랙트는 지정된 기간 내에 지정된 금액의 톤코인이 사용자의 지갑에서 한 번 이상 인출되지 않도록 보장합니다.

- 서비스 백엔드는 구독 스마트 계약에 외부 메시지를 전송하여 정기적으로 결제를 시작합니다.

- 사용자나 서비스 모두 구독이 더 이상 필요하지 않다고 판단하여 구독을 해지할 수 있습니다.

## 스마트 컨트랙트 예시

- [월렛 v4 스마트 컨트랙트 소스 코드](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc)
- [구독 스마트 계약 소스 코드](https://github.com/ton-blockchain/wallet-contract/blob/main/func/simple-subscription-plugin.fc)

## 구현

구현의 좋은 예는 [@donate](https://t.me/donate) 봇과 [Tonkeeper 지갑](https://tonkeeper.com)을 통한 텔레그램의 비공개 채널에 대한 톤코인 탈중앙화 구독입니다.
