# TON HTTP 기반 API

:::tip

블록체인에 연결하는 방법에는 여러 가지가 있습니다:

1. **RPC 데이터 공급자 또는 다른 API**: 대부분의 경우 안정성과 보안에 *의존*해야 합니다.
2. ADNL 연결: [라이트서버](/참여/런-노드/라이트서버)에 연결 중입니다. 접근이 불가능할 수도 있지만 특정 수준의 유효성 검사(라이브러리에서 구현됨)를 거치면 거짓말을 할 수 없습니다.
3. 톤라이브 바이너리: 라이트서버에도 연결하므로 모든 장점과 단점이 적용되지만 애플리케이션에는 외부에서 컴파일된 동적 로딩 라이브러리도 포함되어 있습니다.
4. 오프체인 전용. 이러한 SDK를 사용하면 셀을 생성하고 직렬화할 수 있으며, 이를 API로 전송할 수 있습니다.

:::

## 장단점

- 습관적이고 빠른 시작에 적합한 이 게임은 TON을 처음 접하는 모든 초보자에게 적합합니다.

- ✅ 웹 지향. 웹에서 TON 스마트 컨트랙트의 데이터를 로드하는 데 적합하며, 메시지를 보낼 수도 있습니다.

- 단순화. 인덱싱된 TON API가 필요한 곳에서는 정보를 수신할 수 없습니다.

- ❌ HTTP-미들웨어. 서버가 블록체인 데이터가 진짜인지 검증할 수 있도록 [머클 증명](/개발/데이터-포맷/증명)으로 블록체인 데이터를 보강하지 않는 한, 서버 응답을 완전히 신뢰할 수 없습니다.

## RPC 노드

- [겟블록 노드](https://getblock.io/nodes/ton/) - 겟블록 노드를 사용하여 디앱을 연결하고 테스트합니다.
- [TON 액세스](https://www.orbs.com/ton-access/) - 오픈 네트워크(TON)용 HTTP API입니다.
- [톤센터](https://toncenter.com/api/v2/) - API로 빠르게 시작하기 위한 커뮤니티 호스팅 프로젝트입니다. (API 키 받기 [@tonapibot](https://t.me/tonapibot))
- [톤-노드-도커](https://github.com/fmira21/ton-node-docker) - 도커 풀노드 및 톤센터 API.
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) - 자체 RPC 노드를 실행합니다.
- [nownodes.io](https://nownodes.io/nodes) - API를 통한 NOWNodes 전체 노드 및 블록북 탐색기.
- [체인베이스](https://chainbase.com/chainNetwork/TON) - 오픈 네트워크를 위한 노드 API 및 데이터 인프라.

## 인덱서

### 톤센터 톤 인덱스

인덱서는 특정 지갑을 검색할 뿐만 아니라 특정 필터별로 제트턴 지갑, NFT, 트랜잭션을 나열할 수 있습니다.

- 퍼블릭 톤 인덱스 사용 가능: 테스트 및 개발은 무료, 프로덕션용은 [프리미엄](https://t.me/tonapibot) - [toncenter.com/api/v3/](https://toncenter.com/api/v3/).
- 워커](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba) 및 [TON 인덱스 API 래퍼](https://github.com/toncenter/ton-indexer)로 자체 TON 인덱스를 실행하세요.

### GraphQL 노드

GraphQL 노드는 인덱서 역할도 합니다.

- [tvmlabs.io](https://ton-testnet.tvmlabs.dev/graphql) - 다양한 트랜잭션/블록 데이터, 필터링 방법 등이 있습니다.
- [dton.io](https://dton.io/graphql) - 파싱된 "is jetton", "is NFT" 플래그로 보강된 컨트랙트 데이터를 제공할 뿐만 아니라 트랜잭션 에뮬레이션과 실행 추적을 수신할 수 있습니다.

## 기타 API

- [TonAPI](https://docs.tonconsole.com/tonapi/api-v2) - 스마트 컨트랙트의 낮은 수준의 세부 사항에 대해 걱정하지 않고 사용자에게 간소화된 경험을 제공하도록 설계된 API입니다.
