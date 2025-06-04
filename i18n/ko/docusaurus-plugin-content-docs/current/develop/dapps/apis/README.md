# API 유형

**고가용성 블록체인 API는 TON에서 유용한 애플리케이션을 안전하고 편리하며 빠르게 개발하는 핵심 요소입니다.**

- [TON HTTP API](/develop/dapps/apis/toncenter) — _인덱싱된 블록체인 정보_를 다룰 수 있는 API.
- [TON ADNL API](/develop/dapps/apis/adnl) — ADNL 프로토콜을 기반으로 TON과 통신하는 안전한 API.

## Toncenter APIs

- [TON Index](https://toncenter.com/api/v3/) - TON Index는 전체 노드에서 데이터를 수집하여 PostgreSQL 데이터베이스에 저장하고 인덱싱된 블록체인에 대한 편리한 API를 제공합니다.
- [toncenter/v2](https://toncenter.com/) - 이 API는 TON 블록체인에 대한 HTTP 액세스를 가능하게 하며, 계정 및 지갑 정보 조회, 블록 및 트랜잭션 조회, 블록체인으로 메시지 전송, 스마트 계약의 get 메서드 호출 등을 지원합니다.

## 타사 API

- [tonapi.io](https://docs.tonconsole.com/tonapi/api-v2) - 계정, 트랜잭션, 블록에 대한 기본 데이터를 제공하는 빠른 인덱스 API로, NFT, 경매, Jettons, TON DNS, 구독과 같은 애플리케이션별 데이터도 제공합니다. 또한 트랜잭션 체인에 대한 주석 데이터를 제공합니다.
- [dton.io](https://dton.io/graphql/) - 계정, 트랜잭션, 블록에 대한 데이터를 제공하는 GraphQL API로, NFT, 경매, Jettons, TON DNS와 같은 애플리케이션별 데이터도 제공합니다.
- [ton-api-v4](https://mainnet-v4.tonhubapi.com) - CDN에서 공격적인 캐싱을 통해 속도에 중점을 둔 또 다른 라이트 API입니다.
- [docs.nftscan.com](https://docs.nftscan.com/reference/ton/model/asset-model) - TON 블록체인을 위한 NFT API.
- [evercloud.dev](https://ton-mainnet.evercloud.dev/graphql) - TON에서 기본 쿼리를 위한 GraphQL API.
- [everspace.center](https://everspace.center/toncoin) - TON 블록체인에 액세스하기 위한 간단한 RPC API.

## 추가 API

### Toncoin 환율 APIs

- https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Cusd%2Crub
- https://coinmarketcap.com/api/documentation/v1/
- https://apiguide.coingecko.com/getting-started

### 주소 변환 API

:::info
로컬 알고리즘을 통해 주소를 변환하는 것이 좋습니다. 자세한 내용은 문서의 [Addresses](/learn/overviews/addresses) 섹션을 참조하세요.
:::

#### 친숙한 주소에서 원시 형태로 변환

/api/v2/unpackAddress

Curl

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/unpackAddress?address=EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB' \
-H 'accept: application/json'
```

응답 본문

```curl
{
"ok": true,
"result": "0:29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563"
}
```

#### 친숙한 주소에서 원시 형태로 변환

/api/v2/packAddress

Curl

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/packAddress?address=0%3A29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563' \
-H 'accept: application/json'
```

응답 본문

```json
{
  "ok": true,
  "result": "EQApAj3rEnJJSxEjEHVKrH3QZgto/MQMOmk8l72azaXlY1zB"
}
```

## 참고 항목

- [TON HTTP API](/develop/dapps/apis/toncenter)
- [SDK 목록](/develop/dapps/apis/sdk)
- [TON 지침서](/develop/dapps/cookbook)
