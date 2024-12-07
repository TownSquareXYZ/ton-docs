# TON DNS & 도메인

TON DNS는 사람이 읽을 수 있는 도메인 이름(`test.ton` 또는 `mysite.temp.ton` 등)을 TON 스마트 컨트랙트 주소나 TON 네트워크에서 실행되는 서비스(TON Sites 등)가 사용하는 ADNL 주소 등으로 변환하는 서비스입니다.

## 표준

[TON DNS 표준](https://github.com/ton-blockchain/TIPs/issues/81)은 도메인 이름 형식, 도메인 확인 과정, DNS 스마트 컨트랙트 인터페이스, DNS 레코드 형식을 설명합니다.

## SDK

TON DNS 작업은 JavaScript SDK [TonWeb](https://github.com/toncenter/tonweb)과 [TonLib](https://ton.org/#/apis/?id=_2-ton-api)에서 구현됩니다.

```js
const address: Address = await tonweb.dns.getWalletAddress('test.ton');

// or 

const address: Address = await tonweb.dns.resolve('test.ton', TonWeb.dns.DNS_CATEGORY_WALLET);
```

또한 `lite-client`와 `tonlib-cli`는 DNS 쿼리를 지원합니다.

## 최상위 도메인

현재는 `.ton`으로 끝나는 도메인만 유효한 TON DNS 도메인으로 인식됩니다.

루트 DNS 스마트 컨트랙트 소스 코드 - https://github.com/ton-blockchain/dns-contract/blob/main/func/root-dns.fc.

이는 향후 변경될 수 있습니다. 새로운 최상위 도메인을 추가하려면 새로운 루트 스마트 컨트랙트와 [네트워크 설정 #4](https://ton.org/#/smart-contracts/governance?id=config) 변경을 위한 일반 투표가 필요합니다.

## \*.ton 도메인

\*.ton 도메인은 NFT 형태로 구현됩니다. NFT 표준을 구현하므로 일반 NFT 서비스(예: NFT 마켓플레이스)와 NFT를 표시할 수 있는 지갑과 호환됩니다.

\*.ton 도메인 소스 코드 - https://github.com/ton-blockchain/dns-contract.

.ton 도메인 리졸버는 NFT 컬렉션 인터페이스를 구현하고, .ton 도메인은 NFT 아이템 인터페이스를 구현합니다.

\*.ton 도메인의 1차 판매는 https://dns.ton.org 에서 분산화된 공개 경매를 통해 이루어집니다. 소스 코드 - https://github.com/ton-blockchain/dns.

## 서브도메인

도메인 소유자는 DNS 레코드 `sha256("dns_next_resolver")`에 서브도메인 확인을 담당하는 스마트 컨트랙트 주소를 설정하여 서브도메인을 만들 수 있습니다.

DNS 표준을 구현하는 모든 스마트 컨트랙트가 될 수 있습니다.
