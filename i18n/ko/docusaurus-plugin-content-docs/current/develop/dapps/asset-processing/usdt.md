'@site/src/components/button'에서 버튼 가져오기

# USDT 처리

## 테더

스테이블코인은 안정적인 가격을 유지하기 위해 법정화폐나 금과 같은 다른 자산에 가치가 1:1로 고정된 암호화폐의 일종입니다. 최근까지 이더리움 토큰을 [bridge.ton.org](bridge.ton.org)로 브릿지한 ERC-20 래핑 토큰인 jUSDT 토큰이 있었습니다. 그러나 [18.04.2023](https://t.me/toncoin/824)에 [Tether](https://tether.to/en/)라는 회사에서 발행한 **네이티브** USD₮ 토큰이 공개 출시되었습니다. USD₮ 출시 후 jUSDT는 두 번째 우선순위 토큰으로 이동했지만 여전히 USD₮의 대체 또는 추가 토큰으로 서비스에서 사용되고 있습니다.

톤 블록체인에서 USD₮는 [제톤 에셋](/개발/앱/자산-처리/제톤)으로 지원됩니다.

:::info
테더의 USD₮ 토큰을 TON 블록체인에 통합하려면 컨트랙트 주소를 사용하세요:
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>자산 SDK</Button>
<Button href="https://docs.ton.org/develop/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>젯톤 처리</Button>

## TON에서 USD₮의 장점

### 원활한 텔레그램 통합

[USD₮ on TON](https://ton.org/borderless)은 텔레그램에 원활하게 통합되어, 사용자 친화적인 경험을 제공하며, TON이 USDt 거래를 위한 가장 편리한 블록체인으로 자리매김할 것입니다. 이 통합은 텔레그램 사용자들의 디파이를 단순화하여, 접근성과 이해도를 높여줄 것입니다.

### 거래 수수료 절감

이더리움 USD₮ 송금에 소요되는 수수료는 네트워크 부하에 따라 동적으로 계산됩니다. 그렇기 때문에 트랜잭션 비용이 많이 발생할 수 있습니다.

```cpp
transaction_fee = gas_used * gas_price
```

- 'gas_used'는 트랜잭션 실행 중에 사용된 가스 양입니다.
- 가스 1단위에 대한 `가스_가격` 가격(동적으로 계산된 Gwei)

반면에 TON 블록체인에서 USD₮를 송금하는 평균 수수료는 현재 약 0.0145 TON입니다. TON 가격이 100배 상승하더라도 거래 비용은 [매우 저렴하게 유지됩니다](/개발/스마트 컨트랙트/수수료#평균-거래-비용). TON의 핵심 개발팀은 Tether의 스마트 컨트랙트를 최적화하여 다른 어떤 제톤보다 3배 더 저렴하게 만들었습니다.

### 속도와 확장성

TON의 높은 처리량과 빠른 확인 시간 덕분에 USD₮ 거래를 그 어느 때보다 빠르게 처리할 수 있습니다.

## 고급 세부 정보

:::caution 중요

중요 [권장 사항](/개발/앱/자산 처리/제톤#제톤-지갑 처리)을 참조하세요.
:::

## 참고 항목

- [결제 처리](/개발/앱/자산 처리/)
