import Button from '@site/src/components/button'

# USDT 처리

## 테더

스테이블코인은 가치가 법정화폐나 금과 같은 자산에 1:1로 고정된 암호화폐입니다. 최근까지 bridge.ton.org를 통해 브리지된 ERC-20 이더리움 토큰인 jUSDT가 있었습니다. 하지만 2023년 4월 18일 Tether사가 발행한 **네이티브** USD₮ 토큰이 공개 출시되었습니다. USD₮ 출시 이후 jUSDT는 2순위로 밀렸지만 여러 서비스에서 USD₮의 대안이나 보완으로 계속 사용되고 있습니다.

TON 블록체인에서 USD₮는 [제톤 자산](/v3/guidelines/dapps/asset-processing/jettons)으로 지원됩니다.

:::info
TON 블록체인에서 Tether의 USD₮ 토큰을 통합하려면 다음 컨트랙트 주소를 사용하세요:
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>Assets SDK</Button>
<Button href="/v3/guidelines/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>제톤 처리</Button>
<Button href="https://github.com/ton-community/tma-usdt-payments-demo?tab=readme-ov-file#tma-usdt-payments-demo" colorType={'secondary'} sizeType={'sm'}>TMA USDT 결제 데모</Button>

## TON의 USD₮ 장점

### 원활한 텔레그램 통합

[TON의 USD₮](https://ton.org/borderless)는 텔레그램과 원활하게 통합되어 독보적인 사용자 경험을 제공하며, TON을 USDt 거래에 가장 편리한 블록체인으로 자리매김합니다. 이 통합으로 텔레그램 사용자들의 DeFi 접근성이 향상됩니다.

### 낮은 거래 수수료

이더리움 USD₮ 전송 수수료는 네트워크 부하에 따라 동적으로 계산됩니다. 이로 인해 거래 비용이 높아질 수 있습니다.

```cpp
transaction_fee = gas_used * gas_price
```

- `gas_used`는 거래 실행에 사용된 가스량입니다.
- `gas_price`는 Gwei 단위로 동적 계산되는 가스 단위 비용입니다.

반면 TON 블록체인에서 USD₮ 전송 평균 수수료는 현재 약 0.0145 TON입니다. TON 가격이 100배 상승해도 거래는 [매우 저렴하게](/v3/documentation/smart-contracts/transaction-fees/fees#average-transaction-cost) 유지됩니다. TON 핵심 개발팀은 테더의 스마트 컨트랙트를 최적화하여 다른 제톤보다 3배 저렴하게 만들었습니다.

### 더 빠르고 확장 가능

TON의 높은 처리량과 빠른 확인 시간으로 USD₮ 거래가 그 어느 때보다 빠르게 처리됩니다.

## 고급 세부사항

:::caution 중요

중요 [권장사항](/v3/guidelines/dapps/asset-processing/jettons)을 참조하세요.
:::

## 참고

- [결제 처리](/v3/guidelines/dapps/asset-processing/payments-processing)
