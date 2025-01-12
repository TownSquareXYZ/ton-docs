# TON HTTP 기반 API

:::tip

블록체인에 연결하는 방법에는 여러 가지가 있습니다:

1. **RPC 데이터 제공자 또는 다른 API**: 대부분의 경우, 안정성과 보안에 *의존*해야 합니다.
2. ADNL 연결: [라이트서버](/participate/run-nodes/liteserver)에 연결합니다. 접근이 불가능할 수도 있지만, 일정 수준의 검증(라이브러리에 구현됨)을 통해 거짓 정보를 제공할 수 없습니다.
3. Tonlib 바이너리: 라이트서버에 연결하는 방식으로, 모든 장점과 단점이 적용되지만, 동적으로 로드되는 외부에서 컴파일된 라이브러리를 포함합니다.
4. 오프체인 전용: 이러한 SDK는 셀을 생성하고 직렬화할 수 있으며, 이를 API에 전송할 수 있습니다.

:::

## 장점 및 단점

- ✅ 익숙하고 빠른 시작에 적합하여 TON을 처음 접하는 모든 사람에게 완벽합니다.

- ✅ 웹 지향적입니다. 웹에서 TON 스마트 계약의 데이터를 로드하고 메시지를 보낼 수 있습니다.

- ❌ 단순화된 방식입니다. 인덱싱된 TON API가 필요한 정보를 받을 수 없습니다.

- ❌ HTTP 미들웨어. 서버가 블록체인 데이터를 [머클 증명](/develop/data-formats/proofs)으로 보강하여 진위 여부를 검증하지 않는 한, 서버 응답을 완전히 신뢰할 수 없습니다.

## 모니터링

- [status.toncenter](https://status.toncenter.com/) - 지난 시간 동안 활성화된 모든 전체 네트워크 노드와 검증자를 보여주며, 다양한 통계를 제공합니다.
- [Tonstat.us](https://tonstat.us/) - 모든 TON 관련 API의 상태를 실시간으로 보여주는 Grafana 기반 대시보드를 제공하며, 데이터는 5분마다 업데이트됩니다.
- [tonqueues.vladimirlebe.dev](https://tonqueues.vladimirlebe.dev/) - TPS 등의 다양한 통계를 보여주는 실시간 Grafana 기반 대시보드를 제공합니다.

## RPC 노드

- [GetBlock Nodes](https://getblock.io/nodes/ton/) — GetBlocks 노드를 사용하여 dApp을 연결하고 테스트하십시오.
- [TON Access](https://www.orbs.com/ton-access/) - The Open Network (TON)를 위한 HTTP API.
- [Toncenter](https://toncenter.com/api/v2/) — API를 사용하여 빠르게 시작할 수 있는 커뮤니티 호스팅 프로젝트. (API 키 받기 [@tonapibot](https://t.me/tonapibot))
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - Docker 전체 노드 및 Toncenter API.
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) — 자체 RPC 노드 실행.
- [nownodes.io](https://nownodes.io/nodes) — NOWNodes 전체 노드 및 blockbook 탐색기를 API를 통해 제공.
- [Chainbase](https://chainbase.com/chainNetwork/TON) — The Open Network를 위한 노드 API 및 데이터 인프라.

## 인덱서

### Toncenter TON 인덱스

인덱서는 특정 필터로 Jetton 지갑, NFT, 거래를 나열할 수 있으며, 특정 항목만 검색할 수 있습니다.

- 공개 TON 인덱스를 사용할 수 있습니다: 테스트 및 개발은 무료이며, [프리미엄](https://t.me/tonapibot)은 프로덕션용 - [toncenter.com/api/v3/](https://toncenter.com/api/v3/).
- [Worker](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba) 및 [TON Index API wrapper](https://github.com/toncenter/ton-indexer)를 사용하여 자체 TON 인덱스 실행.

### Anton

Go 언어로 작성된 Anton은 Apache Licence 2.0 하에 제공되는 오픈 소스 The Open Network 블록체인 인덱서입니다. Anton은 개발자가 블록체인 데이터를 접근하고 분석할 수 있도록 확장 가능하고 유연한 솔루션을 제공합니다. 우리의 목표는 개발자와 사용자가 블록체인의 사용 방식을 이해할 수 있도록 돕고, 개발자가 자신의 계약을 추가하고 자신의 메시지 스키마를 우리의 탐색기에 추가할 수 있도록 하는 것입니다.

- [프로젝트 GitHub](https://github.com/tonindexer/anton) - 자체 인덱서 실행
- [Swagger API 문서](https://github.com/tonindexer/anton), [API 쿼리 예제](https://github.com/tonindexer/anton/blob/main/docs/API.md) - 사용 및 학습을 위한 문서 및 예제
- [Apache Superset](https://github.com/tonindexer/anton) - 데이터 보기용

### GraphQL 노드

GraphQL 노드는 인덱서 역할도 합니다.

- [tvmlabs.io](https://ton-testnet.tvmlabs.dev/graphql) (작성 시점에서 TON 테스트넷 전용) - 다양한 거래/블록 데이터 및 필터링 방법 제공
- [dton.io](https://dton.io/graphql) - 계약 데이터를 "Jetton 여부", "NFT 여부" 플래그로 보강하여 제공하며, 거래를 에뮬레이트하고 실행 추적을 받을 수 있습니다.

## 기타 API

- [TonAPI](https://docs.tonconsole.com/tonapi/api-v2) - 스마트 계약의 저수준 세부사항을 걱정하지 않고도 사용자에게 간소화된 경험을 제공하도록 설계된 API.
