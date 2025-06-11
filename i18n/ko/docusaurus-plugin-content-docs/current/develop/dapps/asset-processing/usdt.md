import Button from '@site/src/components/button'

# USDT 처리

## Tether

스테이블코인은 가격을 안정적으로 유지하기 위해 금이나 법정화폐와 같은 다른 자산에 1:1로 연동된 암호화폐의 일종입니다. 최근까지는 jUSDT라는 토큰이 있었는데, 이는 이더리움의 ERC-20 토큰을 래핑하여 <a href="https://bridge.ton.org" target="_blank">bridge.ton.org</a>를 통해 브릿지된 것이었습니다. 하지만 [2023년 4월 18일](https://t.me/toncoin/824)에 **네이티브** USD₮ 토큰이 <a href="https://tether.to/en/" target="_blank">Tether</a>라는 회사에서 발행되며 공개적으로 출시되었습니다. USD₮가 출시된 후, jUSDT는 우선순위가 낮아졌지만 여전히 대체재 또는 추가 옵션으로 서비스에서 사용되고 있습니다.

TON 블록체인에서는 USD₮가 [Jetton 자산](/develop/dapps/asset-processing/jettons)으로 지원됩니다.

:::info
TON 블록체인에서 Tether의 USD₮ 토큰을 통합하려면 아래의 계약 주소를 사용하세요:
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>자산 SDK</Button>
<Button href="https://docs.ton.org/develop/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>Jetton 처리</Button>
<Button href="https://github.com/ton-community/tma-usdt-payments-demo?tab=readme-ov-file#tma-usdt-payments-demo" colorType={'secondary'} sizeType={'sm'}>TMA USDT 결제 데모</Button>

## TON에서의 USD₮ 장점

### 텔레그램과의 매끄러운 통합

[TON에서의 USD₮](https://ton.org/borderless)은 텔레그램과 원활하게 통합되어, TON을 USD₮ 거래에 가장 편리한 블록체인으로 만드는 사용자 친화적인 경험을 제공합니다. 이 통합을 통해 텔레그램 사용자가 DeFi를 더 쉽게 접근하고 이해할 수 있게 됩니다.

### 낮은 트랜잭션 수수료

이더리움에서의 USD₮ 전송에 소비되는 수수료는 네트워크 부하에 따라 동적으로 계산됩니다. 이 때문에 트랜잭션 수수료가 높아질 수 있습니다.

```cpp
transaction_fee = gas_used * gas_price
```

- 'gas_used'는 거래 실행 중에 사용된 가스 양입니다.
- `gas_price`는 Gwei 단위로 계산된 1단위 가스의 가격이며, 동적으로 계산됩니다.

반면, TON 블록체인에서 USD₮를 전송하는 데 드는 평균 수수료는 현재 약 0.0145 TON입니다. TON의 가격이 100배 상승하더라도 거래는 여전히 [초저가](/develop/smart-contracts/fees#average-transaction-cost)로 유지될 것입니다. TON의 핵심 개발 팀은 Tether의 스마트 계약을 최적화하여 다른 Jetton보다 세 배 더 저렴하게 만들었습니다.

### 속도와 확장성

TON의 높은 처리량과 빠른 확인 시간 덕분에 USD₮ 거래가 그 어느 때보다 빠르게 처리될 수 있습니다.

## 고급 세부 정보

:::caution 중요

중요 [권장 사항](/개발/앱/자산 처리/제톤#제톤-지갑 처리)을 참조하세요.
:::

## 참고 항목

- [결제 처리](/develop/dapps/asset-processing/)
