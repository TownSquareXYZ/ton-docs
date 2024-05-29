# TON DNS 및 도메인

TON DNS는 사람이 읽을 수 있는 도메인 이름(예: `test.ton` 또는 `mysite.temp.ton`)을 TON 스마트 계약 주소, TON 네트워크에서 실행되는 서비스(예: TON 사이트)에서 사용하는 ADNL 주소 등으로 변환하는 서비스입니다.

## 표준

[TON DNS 표준](https://github.com/ton-blockchain/TIPs/issues/81)은 도메인 이름의 형식, 도메인 확인 프로세스, DNS 스마트 계약의 인터페이스 및 DNS 레코드의 형식에 대해 설명합니다.

## SDK

TON DNS 작업은 자바스크립트 SDK [TonWeb](https://github.com/toncenter/tonweb) 및 [TonLib](https://ton.org/#/apis/?id=_2-ton-api)에서 구현됩니다.

```js
const address: Address = await tonweb.dns.getWalletAddress('test.ton');

// or 

const address: Address = await tonweb.dns.resolve('test.ton', TonWeb.dns.DNS_CATEGORY_WALLET);
```

또한 `lite-client` 및 `tonlib-cli`는 DNS 쿼리에서 지원됩니다.

## 첫 번째 수준 도메인

현재 '.ton'으로 끝나는 도메인만 유효한 TON DNS 도메인으로 인식됩니다.

루트 DNS 스마트 계약 소스 코드 - https://github.com/ton-blockchain/dns-contract/blob/main/func/root-dns.fc.

이는 향후 변경될 수 있습니다. 새로운 1단계 도메인을 추가하려면 새로운 루트 스마트 컨트랙트와 [네트워크 구성 #4](https://ton.org/#/smart-contracts/governance?id=config)를 변경하기 위한 일반 투표가 필요합니다.

## \*.ton 도메인

\*.ton 도메인은 NFT 형태로 구현됩니다. NFT 표준을 구현하기 때문에 일반 NFT 서비스(예: NFT 마켓플레이스) 및 NFT를 표시할 수 있는 지갑과 호환됩니다.

\*.ton 도메인 소스 코드 - https://github.com/ton-blockchain/dns-contract.

.ton 도메인 확인자는 NFT 수집 인터페이스를 구현하고 .ton 도메인은 NFT 항목 인터페이스를 구현합니다.

.ton 도메인의 1차 판매는 https://dns.ton.org 에서 탈중앙화 공개 경매를 통해 이루어집니다. 소스 코드 - https://github.com/ton-blockchain/dns.

## 하위 도메인

도메인 소유자는 하위 도메인 확인을 담당하는 스마트 계약의 주소를 DNS 레코드 `sha256("dns_next_resolver")`에 설정하여 하위 도메인을 만들 수 있습니다.

DNS 표준을 구현하는 모든 스마트 컨트랙트가 될 수 있습니다.
