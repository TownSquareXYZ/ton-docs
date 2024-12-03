# TON 스마트 컨트랙트 예시

이 페이지에서는 다양한 프로그램 소프트웨어를 위해 구현된 TON 스마트 컨트랙트 레퍼런스를 확인할 수 있습니다.

:::info
프로덕션 환경에서 사용하기 전에 컨트랙트를 철저히 테스트했는지 확인하세요. 이는 소프트웨어의 적절한 기능과 보안을 보장하기 위한 중요한 단계입니다.
:::

## FunC 스마트 컨트랙트

### 프로덕션용 컨트랙트

| 컨트랙트                                                                                                                                                                                                                                                                                                         | 설명                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| [wallet-contract](https://github.com/ton-blockchain/wallet-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/wallet-contract\&name=wallet-contract)</small>                                                                                         | Wallet v4는 v3 또는 이전 지갑을 대체하기 위해 제안된 지갑 버전입니다                                                                   |
| [liquid-staking-contract](https://github.com/ton-blockchain/liquid-staking-contract/) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/liquid-staking-contract/\&name=liquid-staking-contract)</small>                                                       | 리퀴드 스테이킹(LSt)은 모든 규모의 TON 보유자와 하드웨어 노드 운영자를 연결하여 자산 풀링을 통해 TON 블록체인 검증에 참여할 수 있게 하는 프로토콜입니다 |
| [modern_jetton](https://github.com/EmelyanenkoK/modern_jetton) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/EmelyanenkoK/modern_jetton\&name=modern_jetton)</small>                                                                                | withdraw_tons와 withdraw_jettons가 추가된 표준 제톤 구현                        |
| [highloadwallet-v3](https://github.com/ton-blockchain/highload-wallet-contract-v3)                                                                                                                                                                                                                           | 이 지갑은 암호화폐 거래소와 같이 매우 높은 비율로 트랜잭션을 보내야 하는 사용자를 위해 설계되었습니다                                                      |
| [stablecoin-contract](https://github.com/ton-blockchain/stablecoin-contract)                                                                                                                                                                                                                                 | USDt와 같은 스테이블코인에 사용되는 거버넌스가 포함된 제톤 FunC 스마트 컨트랙트                                                               |
| [governance-contract](https://github.com/ton-blockchain/governance-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/governance-contract\&name=governance-contract)</small>                                                                         | `elector-code.fc`와 `config-code.fc` 코어 TON 블록체인 컨트랙트                                                           |
| [bridge-func](https://github.com/ton-blockchain/bridge-func) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/bridge-func\&name=bridge-func)</small>                                                                                                         | TON-EVM 톤코인 브릿지                                                                                                |
| [token-bridge-func](https://github.com/ton-blockchain/token-bridge-func) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/token-bridge-func\&name=token-bridge-func)</small>                                                                                 | TON-EVM 토큰 브릿지 - FunC 스마트 컨트랙트                                                                                 |
| [lockup-wallet-contract/universal](https://github.com/ton-blockchain/lockup-wallet-contract/tree/main/universal) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/lockup-wallet-contract/tree/main/universal\&name=lockup-wallet-contract/universal)</small> | 유니버설 락업 지갑은 잠긴 코인과 제한된 코인을 저장할 수 있는 컨트랙트입니다                                                                    |
| [lockup-wallet-contract/vesting](https://github.com/ton-blockchain/lockup-wallet-contract/tree/main/vesting) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/lockup-wallet-contract/tree/main/vesting\&name=lockup-wallet-contract/vesting)</small>         | 베스팅 지갑 스마트 컨트랙트                                                                                                |
| [multisig-contract](https://github.com/ton-blockchain/multisig-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/multisig-contract\&name=multisig-contract)</small>                                                                                 | `(n, k)`-멀티시그 지갑은 `n`개의 개인키 보유자가 있는 지갑으로, 요청이 보유자의 최소 `k`개의 서명을 받으면 메시지 전송 요청을 수락합니다                           |
| [token-contract](https://github.com/ton-blockchain/token-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/token-contract\&name=token-contract)</small>                                                                                             | 대체 가능, 대체 불가능, 준대체 가능 토큰 스마트 컨트랙트                                                                              |
| [dns-contract](https://github.com/ton-blockchain/dns-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/dns-contract\&name=dns-contract)</small>                                                                                                     | `.ton` 존의 스마트 컨트랙트                                                                                             |
| [nominator-pool](https://github.com/ton-blockchain/nominator-pool) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/nominator-pool\&name=nominator-pool)</small>                                                                                             | 노미네이터 풀 스마트 컨트랙트                                                                                               |
| [single-nominator-pool](https://github.com/orbs-network/single-nominator) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/nominator-pool\&name=nominator-pool)</small>                                                                                      | 단일 노미네이터 풀 스마트 컨트랙트                                                                                            |
| [vesting-contract](https://github.com/ton-blockchain/vesting-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/vesting-contract\&name=vesting-contract)</small>                                                                                     | 베스팅 컨트랙트를 사용하면 일정 기간 동안 특정 양의 톤코인을 잠그고 점진적으로 잠금을 해제할 수 있습니다                                                    |
| [storage](https://github.com/ton-blockchain/ton/tree/master/storage/storage-daemon/smartcont) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-blockchain/ton/tree/master/storage/storage-daemon/smartcont\&name=storage)</small>                                       | TON 스토리지 제공자 및 패브릭 컨트랙트                                                                                        |

### 생태계 컨트랙트

| 컨트랙트                                                                                                                                                                                                                                                                                                                       | 설명                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [telemint](https://github.com/TelegramMessenger/telemint) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/TelegramMessenger/telemint\&name=telemint)</small>                                                                                                                             | 텔레그램 사용자명(`nft-item.fc`)과 텔레그램 번호(`nft-item-no-dns.fc`) 컨트랙트 |
| [capped-fungible-token](https://github.com/TonoxDeFi/capped-fungible-token) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/TonoxDeFi/capped-fungible-token\&name=capped-fungible-token)</small>                                                                                         | 제톤 지갑과 제톤 민터를 위한 기본 스마트 컨트랙트 구현                                                                    |
| [gusarich-airdrop](https://github.com/Gusarich/airdrop/tree/main/contracts)                                                                                                                                                                                                                                                | TON 블록체인을 위한 확장 가능한 에어드롭 시스템의 구현. 온체인에서 모든 지갑에 제톤을 분배하는 데 사용될 수 있습니다               |
| [getgems-io/nft-contracts](https://github.com/getgems-io/nft-contracts/tree/main/packages/contracts/sources) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/getgems-io/nft-contracts/tree/main/packages/contracts/sources\&name=getgems-io/nft-contracts)</small>                       | Getgems NFT 컨트랙트                                                                                   |
| [lockup-wallet-deployment](https://github.com/ton-defi-org/lockup-wallet-deployment) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-defi-org/lockup-wallet-deployment\&name=lockup-wallet-deployment)</small>                                                                       | 락업 컨트랙트 종단간 배포 및 실행                                                                                |
| [WTON](https://github.com/TonoxDeFi/WTON) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/TonoxDeFi/WTON\&name=WTON)</small>                                                                                                                                                             | 이 스마트 컨트랙트는 WTON이라 불리는 래핑된 톤코인의 구현을 제공합니다                                                          |
| [wton-contract](https://github.com/ton-community/wton-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-community/wton-contract\&name=wton-contract)</small>                                                                                                                 | wTON 컨트랙트                                                                                          |
| [contract-verifier-contracts](https://github.com/ton-community/contract-verifier-contracts) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-community/contract-verifier-contracts\&name=contract-verifier-contracts)</small>                                                         | 코드 셀 해시당 온체인 증명을 저장하는 소스 레지스트리 컨트랙트                                                                |
| [vanity-contract](https://github.com/ton-community/vanity-contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-community/vanity-contract\&name=vanity-contract)</small>                                                                                                         | 모든 컨트랙트에 대해 적합한 주소를 "채굴"할 수 있는 스마트 컨트랙트                                                            |
| [ton-config-smc](https://github.com/ton-foundation/ton-config-smc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-foundation/ton-config-smc\&name=ton-config-smc)</small>                                                                                                           | TON 블록체인에서 버전 관리되는 데이터를 저장하기 위한 단순한 컨트랙트                                                           |
| [ratelance](https://github.com/ProgramCrafter/ratelance/tree/main/contracts/func) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ProgramCrafter/ratelance/tree/main/contracts/func\&name=ratelance)</small>                                                                             | Ratelance는 잠재적 고용주와 근로자 사이의 장벽을 제거하고자 하는 프리랜서 플랫폼입니다                                               |
| [logger.fc](https://github.com/tonwhales/ton-contracts/blob/master/contracts/logger.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/tonwhales/ton-contracts/blob/master/contracts/logger.fc\&name=logger.fc)</small>                                                 | 로컬 스토리지에 데이터를 저장하는 컨트랙트                                                                            |
| [ton-nominators](https://github.com/tonwhales/ton-nominators) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/tonwhales/ton-nominators\&name=ton-nominators)</small>                                                                                                                     | Ton Whales 노미네이터 풀 소스 코드                                                                           |
| [ton-link-contract-v3](https://github.com/ton-link/ton-link-contract-v3) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-link/ton-link-contract-v3\&name=ton-link-contract-v3)</small>                                                                                               | Ton-link를 통해 스마트 컨트랙트는 데이터 보안을 유지하면서 블록체인 외부의 데이터에 접근할 수 있습니다                                      |
| [delab-team/fungible-token](https://github.com/delab-team/contracts/tree/main/fungible-token) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/delab-team/contracts/tree/main/fungible-token\&name=delab-team/fungible-token)</small>                                                     | DeLab TON 대체 가능 토큰 구현                                                                              |
| [whitelisted-wallet.fc](https://github.com/tonwhales/ton-contracts/blob/master/contracts/whitelisted-wallet.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/tonwhales/ton-contracts/blob/master/contracts/whitelisted-wallet.fc\&name=whitelisted-wallet.fc)</small> | 단순 화이트리스트 지갑 컨트랙트                                                                                  |
| [delab-team/jetton-pool](https://github.com/delab-team/contracts/tree/main/jetton-pool) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/delab-team/contracts/tree/main/jetton-pool\&name=delab-team/jetton-pool)</small>                                                                 | Jetton Pool TON 스마트 컨트랙트는 파밍 풀을 생성하기 위해 설계되었습니다                                                    |
| [ston-fi/contracts](https://github.com/ston-fi/dex-core/tree/main/contracts) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ston-fi/dex-core/tree/main/contracts\&name=ston-fi/contracts)</small>                                                                                       | Stonfi DEX 코어 컨트랙트                                                                                 |
| [onda-ton](https://github.com/0xknstntn/onda-ton) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/0xknstntn/onda-ton\&name=onda-ton)</small>                                                                                                                                             | Onda 대출 풀 - TON의 첫 번째 대출 프로토콜의 코어 스마트 컨트랙트                                                         |
| [ton-stable-timer](https://github.com/ProgramCrafter/ton-stable-timer) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ProgramCrafter/ton-stable-timer\&name=ton-stable-timer)</small>                                                                                                   | TON 안정 타이머 컨트랙트                                                                                    |
| [HipoFinance/contract](https://github.com/HipoFinance/contract) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/HipoFinance/contract\&name=HipoFinance)</small>                                                                                                                          | hTON은 TON 블록체인의 탈중앙화되고, 허가가 필요 없는, 오픈소스 리퀴드 스테이킹 프로토콜입니다                                           |

### 학습용 컨트랙트

| 컨트랙트                                                                                                                                                                                                                                                                                                                                                                | 설명                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [counter.fc](https://github.com/ton-community/blueprint/blob/main/example/contracts/counter.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-community/blueprint/blob/main/example/contracts/counter.fc\&name=counter.fc)</small>                                                                          | 주석이 포함된 카운터 스마트 컨트랙트              |
| [simple-distributor](https://github.com/ton-community/simple-distributor) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/ton-community/simple-distributor\&name=simple-distributor)</small>                                                                                                                                      | 단순 TON 배포자                        |
| [ping-pong.fc](https://github.com/tonwhales/ton-nft/blob/main/packages/nft/ping-pong/ping-pong.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/tonwhales/ton-nft/blob/main/packages/nft/ping-pong/ping-pong.fc\&name=ping-pong.fc)</small>                                                                    | 다양한 모드에서 톤코인 전송을 테스트하기 위한 단순 컨트랙트 |
| [ton-random](https://github.com/puppycats/ton-random) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/puppycats/ton-random\&name=ton-random)</small>                                                                                                                                                                              | 온체인에서 난수 생성을 도와주는 두 개의 컨트랙트       |
| [Blueprint simple contract](https://github.com/liminalAngel/1-func-project/blob/master/contracts/main.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/liminalAngel/1-func-project/blob/master/contracts/main.fc\&name=simple_contract)</small>                                                                                | 예제 스마트 컨트랙트                       |
| [Blueprint jetton_minter.fc](https://github.com/liminalAngel/func-blueprint-tutorial/blob/master/6/contracts/jetton_minter.fc) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/liminalAngel/func-blueprint-tutorial/blob/master/6/contracts/jetton_minter.fc\&name=jetton_minter.fc)</small> | 온체인에서 제톤을 민팅하기 위한 스마트 컨트랙트 예제     |
| [Simple TON DNS Subdomain manager](https://github.com/Gusarich/simple-subdomain) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/Gusarich/simple-subdomain\&name=Simple_TON_DNS_Subdomain_manager)</small>                                                                                                                        | TON DNS 서브도메인 관리자                 |
| [disintar/sale-dapp](https://github.com/disintar/sale-dapp/tree/master/func) <br /> <small>🪄 [WebIDE에서 실행](https://ide.nujan.io/?importURL=https://github.com/disintar/sale-dapp/tree/master/func\&name=disintar/sale-dapp)</small>                                                                                                                                | React + NFT 판매 DApp with FunC     |

### TON 스마트 챌린지

#### TON 스마트 챌린지 1

- https://github.com/nns2009/TON-FunC-contest-1/tree/main
- https://github.com/pyAndr3w/func-contest1-solutions
- https://github.com/crazyministr/TonContest-FunC/tree/master/func-contest1

#### TON 스마트 챌린지 2

- https://github.com/ton-blockchain/func-contest2-solutions
- https://github.com/nns2009/TON-FunC-contest-2
- https://github.com/crazyministr/TonContest-FunC/tree/master/func-contest2

#### TON 스마트 챌린지 3

- https://github.com/nns2009/TON-FunC-contest-3
- https://github.com/shuva10v/func-contest3-solutions
- https://github.com/crazyministr/TonContest-FunC/tree/master/func-contest3

#### TON 스마트 챌린지 4

- https://github.com/akifoq/tsc4 (최적화 TOP)
- https://github.com/Gusarich/tsc4
- https://github.com/Skydev0h/tsc4
- https://github.com/aSpite/tsc4-contracts (FunC 솔루션)
- [https://github.com/ProgramCrafter/tsc4](https://github.com/ProgramCrafter/tsc4/tree/c1616e12d1b449b01fdcb787a3aa8442e671371e/contracts) (FunC 솔루션)

## Fift 스마트 컨트랙트

- [CreateState.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/CreateState.fif)
- [asm-to-cpp.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/asm-to-cpp.fif)
- [auto-dns.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/auto-dns.fif)
- [complaint-vote-req.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/complaint-vote-req.fif)
- [complaint-vote-signed.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/complaint-vote-signed.fif)
- [config-proposal-vote-req.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/config-proposal-vote-req.fif)
- [config-proposal-vote-signed.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/config-proposal-vote-signed.fif)
- [create-config-proposal.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/create-config-proposal.fif)
- [create-config-upgrade-proposal.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/create-config-upgrade-proposal.fif)
- [create-elector-upgrade-proposal.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/create-elector-upgrade-proposal.fif)
- [envelope-complaint.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/envelope-complaint.fif)
- [gen-zerostate-test.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/gen-zerostate-test.fif)
- [gen-zerostate.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/gen-zerostate.fif)
- [highload-wallet-v2-one.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-one.fif)
- [highload-wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2.fif)
- [highload-wallet.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet.fif)
- [manual-dns-manage.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/manual-dns-manage.fif)
- [new-auto-dns.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-auto-dns.fif)
- [new-highload-wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-highload-wallet-v2.fif)
- [new-highload-wallet.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-highload-wallet.fif)
- [new-manual-dns.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-manual-dns.fif)
- [new-pinger.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-pinger.fif)
- [new-pow-testgiver.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-pow-testgiver.fif)
- [new-restricted-wallet.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-restricted-wallet.fif)
- [new-restricted-wallet2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-restricted-wallet2.fif)
- [new-restricted-wallet3.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-restricted-wallet3.fif)
- [new-testgiver.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-testgiver.fif)
- [new-wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet-v2.fif)
- [new-wallet-v3.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet-v3.fif)
- [new-wallet.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet.fif)
- [show-addr.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/show-addr.fif)
- [testgiver.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/testgiver.fif)
- [update-config-smc.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/update-config-smc.fif)
- [update-config.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/update-config.fif)
- [update-elector-smc.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/update-elector-smc.fif)
- [validator-elect-req.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/validator-elect-req.fif)
- [validator-elect-signed.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/validator-elect-signed.fif)
- [wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-v2.fif)
- [wallet-v3.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-v3.fif)
- [wallet.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet.fif)
- [wallet-v3-code.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-v3-code.fif)

## FunC 라이브러리와 헬퍼

- https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/crypto/elliptic-curves
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/math
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/messages
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/slices
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/strings
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/tuples
- https://github.com/TonoxDeFi/open-contracts/tree/main/contracts/utils
- https://github.com/disintar/sale-dapp/tree/master/func

## 레퍼런스 추가하기

새로운 예제 스마트 컨트랙트를 공유하고 싶다면 이 [페이지](https://github.com/ton-community/ton-docs/tree/main/docs/v3/documentation/smart-contracts/contracts-specs/examples.md)에 PR을 제출하세요.

## 참고 자료

- [스마트 컨트랙트 개발 입문](/v3/documentation/smart-contracts/overview)
- [지갑 스마트 컨트랙트 작업 방법](/v3/guidelines/smart-contracts/howto/wallet)
- [[유튜브] Ton Dev Study FunC & BluePrint 레슨](https://www.youtube.com/watch?v=7omBDfSqGfA\&list=PLtUBO1QNEKwtO_zSyLj-axPzc9O9rkmYa)
