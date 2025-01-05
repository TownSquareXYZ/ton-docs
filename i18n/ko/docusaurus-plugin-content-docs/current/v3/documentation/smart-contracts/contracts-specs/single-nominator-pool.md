import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 단일 노미네이터 풀

단일 노미네이터는 콜드 월렛을 통해 TON 블록체인의 안전한 검증을 가능하게 하는 간단한 방화벽 TON 스마트 컨트랙트입니다. 이 컨트랙트는 제3자 노미네이터의 스테이크에 의존하지 않고 자체적으로 검증할 수 있는 충분한 자체 스테이크를 보유한 TON 검증자를 위해 설계되었습니다. 단일 노미네이터만 지원하는 노미네이터 풀 스마트 컨트랙트의 대체 단순화 구현을 제공합니다. 이 구현의 장점은 공격 표면이 상당히 작아 더 안전하다는 것입니다. 이는 여러 제3자 노미네이터를 지원해야 하는 노미네이터 풀의 복잡성을 대폭 줄였기 때문입니다.

## 검증자를 위한 추천 솔루션

이 스마트 컨트랙트는 혼자서 검증할 수 있는 충분한 스테이크를 가진 TON 검증자를 위한 추천 솔루션입니다. 다른 사용 가능한 대안은 다음과 같습니다:

- 핫 월렛 사용 (검증자 노드가 해킹되면 도난을 방지하기 위해 콜드 월렛이 필요하므로 안전하지 않음)
- restricted-wallet 사용 (관리되지 않고 가스 소진 공격과 같은 해결되지 않은 공격 벡터가 있음)
- max_nominators_count = 1로 노미네이터 풀 사용 (불필요하게 복잡하고 공격 표면이 더 큼)

아래에서 [기존 대안들의 자세한 비교](#comparison-of-existing-alternatives)를 참조하세요.

## 공식 코드 해시

라이브 컨트랙트에 자금을 보내기 전에 https://verifier.ton.org 에서 확인하세요

```
pCrmnqx2/+DkUtPU8T04ehTkbAGlqtul/B2JPmxx9bo=
```

## 아키텍처

아키텍처는 노미네이터 풀 컨트랙트와 거의 동일합니다:

![image](/img/nominator-pool/single-nominator-architecture.png)

### 두 가지 역할로 구분

- *소유자* - 스테이킹에 사용되는 자금을 소유하고 단일 노미네이터로 활동하는 콜드 월렛(인터넷에 연결되지 않은 개인키)
- *검증자* - 검증자 노드에 개인키가 있는 월렛(블록은 서명할 수 있지만 스테이크에 사용된 자금은 훔칠 수 없음)

### 작업 흐름

1. *소유자*는 스테이킹을 위한 자금(\$$$)을 안전한 콜드 월렛에 보관
2. *소유자*는 *SingleNominator* 컨트랙트에 자금(\$$$)을 예치
3. *MyTonCtrl*이 인터넷에 연결된 검증자 노드에서 실행 시작
4. *MyTonCtrl*은 *Validator* 월렛을 사용하여 *SingleNominator*에게 다음 선거 사이클 참여를 지시
5. *SingleNominator*는 한 사이클 동안 스테이크(\$$$)를 *Elector*에 전송
6. 선거 사이클이 끝나고 스테이크를 회수할 수 있음
7. *MyTonCtrl*은 *Validator* 월렛을 사용하여 *SingleNominator*에게 선거 사이클에서 스테이크 회수를 지시
8. *SingleNominator*는 *Elector*로부터 이전 사이클의 스테이크(\$$$)를 회수
9. *소유자*가 검증을 계속 하고 싶은 한 4-8단계 반복
10. *소유자*는 *SingleNominator* 컨트랙트에서 자금(\$$$)을 인출하여 가져감

## 완화된 공격 벡터

- 검증자 노드는 새 블록을 서명하기 위해 핫 월렛이 필요합니다. 이 월렛은 개인키가 인터넷에 연결되어 있기 때문에 본질적으로 안전하지 않습니다. 이 키가 도난당하더라도 *Validator*는 검증에 사용된 자금을 빼낼 수 없습니다. 오직 *소유자*만이 이 자금을 인출할 수 있습니다.

- *Validator* 월렛이 도난당하더라도 *소유자*는 *SingleNominator*에게 검증자 주소를 변경하도록 지시할 수 있습니다. 이렇게 하면 공격자가 *SingleNominator*와 더 이상 상호작용하는 것을 막을 수 있습니다. 여기에는 경쟁 조건이 없으며 *소유자*가 항상 우선권을 갖습니다.

- *SingleNominator* 잔액은 주요 스테이킹 자금만 보유합니다 - 잔액은 가스 수수료로 사용되지 않습니다. 선거 사이클 참여를 위한 가스 비용은 *Validator* 월렛에 보관됩니다. 이는 검증자를 해킹한 공격자가 가스 지출 공격을 통해 원금을 소진하는 것을 막습니다.

- *SingleNominator*는 *Validator*가 제공한 모든 작업의 형식을 확인하여 잘못된 메시지를 *Elector*에 전달하지 않도록 합니다.

- 비상시, 예를 들어 *Elector* 컨트랙트가 업그레이드되어 인터페이스가 변경된 경우에도 *소유자*는 여전히 raw 메시지를 *SingleNominator*로 보내 *Elector*에서 스테이크를 회수할 수 있습니다.

- 극단적인 비상시, *소유자*는 *SingleNominator*의 코드를 설정하고 예상치 못한 상황에 대처하기 위해 현재 로직을 재정의할 수 있습니다.

이러한 공격 벡터 중 일부는 일반 노미네이터 풀 컨트랙트를 사용하여 완화할 수 없습니다. 왜냐하면 그렇게 하면 검증자를 운영하는 사람이 노미네이터로부터 자금을 훔칠 수 있게 되기 때문입니다. *SingleNominator*에서는 *소유자*와 *Validator*가 같은 당사자에 의해 소유되므로 이것이 문제가 되지 않습니다.

### 보안 감사

Certik에 의해 수행된 전체 보안 감사가 이 저장소에서 제공됩니다 - [Certik Audit](https://github.com/orbs-network/single-nominator/blob/main/certik-audit.pdf).

## 기존 대안들의 비교

혼자서 검증할 수 있는 충분한 스테이크를 가진 검증자라고 가정할 때, MyTonCtrl과 함께 사용할 수 있는 대안 설정은 다음과 같습니다:

---

### 1. 단순 핫 월렛

이는 MyTonCtrl이 자금을 보유한 동일한 [표준 월렛](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)에 연결된 가장 단순한 설정입니다. 이 월렛은 인터넷에 연결되어 있으므로 핫 월렛으로 간주됩니다.

![image](/img/nominator-pool/hot-wallet.png)

인터넷에 연결된 개인키를 공격자가 얻을 수 있으므로 안전하지 않습니다. 개인키가 있으면 공격자는 스테이킹 자금을 누구에게나 보낼 수 있습니다.

---

### 2. 제한된 월렛

이 설정은 표준 월렛을 *Elector*와 소유자의 주소와 같은 제한된 대상에만 출금 거래를 보낼 수 있는 [restricted-wallet](https://github.com/EmelyanenkoK/nomination-contract/blob/master/restricted-wallet/wallet.fc)로 대체합니다.

![image](/img/nominator-pool/restricted-wallet.png)

제한된 월렛은 관리되지 않으며(노미네이터-풀로 대체됨) 가스 소진 공격과 같은 해결되지 않은 공격 벡터가 있습니다. 동일한 월렛이 가스 수수료와 스테이크 원금을 동일한 잔액에 보유하므로, 개인키를 해킹한 공격자는 상당한 원금 손실을 야기하는 거래를 생성할 수 있습니다. 또한 seqno 충돌로 인해 인출을 시도할 때 공격자와 소유자 사이에 경쟁 조건이 있습니다.

---

### 3. 노미네이터 풀

[nominator-pool](https://github.com/ton-blockchain/nominator-pool)은 스테이크 소유자(노미네이터)와 인터넷에 연결된 검증자 사이의 명확한 분리를 도입한 최초의 것입니다. 이 설정은 최대 40명의 노미네이터가 동일한 검증자에 함께 스테이킹하는 것을 지원합니다.

![image](/img/nominator-pool/nominator-pool.png)

노미네이터 풀 컨트랙트는 40명의 동시 노미네이터를 지원하기 때문에 불필요하게 복잡합니다. 또한 컨트랙트는 노미네이터를 컨트랙트 배포자로부터 보호해야 합니다. 왜냐하면 이들은 별개의 엔티티이기 때문입니다. 이 설정은 괜찮지만 공격 표면의 크기로 인해 전체적으로 감사하기가 매우 어렵습니다. 이 솔루션은 주로 검증자가 혼자 검증할 수 있는 충분한 스테이크가 없거나 제3자 스테이크홀더와 수익을 공유하고 싶을 때 의미가 있습니다.

---

### 4. 단일 노미네이터

이는 이 저장소에서 구현된 설정입니다. 단일 노미네이터를 지원하고 이 노미네이터를 컨트랙트 배포자로부터 보호할 필요가 없는(동일한 엔티티이므로) 노미네이터 풀의 매우 단순화된 버전입니다.

![image](/img/nominator-pool/single-nominator-architecture.png)

검증을 위한 모든 스테이크를 보유한 단일 노미네이터가 있는 경우, 이것이 사용할 수 있는 가장 안전한 설정입니다. 단순성 외에도, 이 컨트랙트는 소유자에게 스테이크 회수 인터페이스를 깨뜨리는 *Elector* 업그레이드와 같은 극단적인 시나리오에서도 스테이크를 회수할 수 있는 여러 비상 안전장치를 제공합니다.

### 소유자 전용 메시지

노미네이터 소유자는 4가지 작업을 수행할 수 있습니다:

#### 1. `withdraw`

소유자의 월렛로 자금을 인출하는 데 사용됩니다. 자금을 인출하기 위해 소유자는 다음을 포함하는 본문이 있는 메시지를 보내야 합니다: opcode=0x1000 (32비트), query_id (64비트) 및 인출 금액(coin 변수로 저장). 노미네이터 컨트랙트는 BOUNCEABLE 플래그와 mode=64로 자금을 보냅니다. <br/><br/>
소유자가 **핫 월렛**을 사용하는 경우(권장하지 않음), [withdraw-deeplink.ts](https://github.com/orbs-network/single-nominator/blob/main/scripts/ts/withdraw-deeplink.ts)를 사용하여 tonkeeper 월렛에서 인출을 시작하기 위한 딥링크를 생성할 수 있습니다. <br/>
명령줄: `ts-node scripts/ts/withdraw-deeplink.ts single-nominator-addr withdraw-amount` 여기서:

- single-nominator-addr은 소유자가 인출하고자 하는 단일 노미네이터 주소입니다.
- withdraw-amount는 인출할 금액입니다. 노미네이터 컨트랙트는 컨트랙트에 1 TON을 남겨두므로 실제로 소유자 주소로 전송될 금액은 요청된 금액과 컨트랙트 잔액 - 1 중 작은 값입니다. <br/>
  소유자는 tonkeeper 월렛이 있는 휴대폰에서 딥링크를 실행해야 합니다. <br/>

소유자가 **콜드 월렛**을 사용하는 경우(권장), [withdraw.fif](https://github.com/orbs-network/single-nominator/blob/main/scripts/fift/withdraw.fif)를 사용하여 인출 opcode와 인출할 금액이 포함된 boc 본문을 생성할 수 있습니다. <br/>
명령줄: `fift -s scripts/fif/withdraw.fif withdraw-amount` 여기서 withdraw-amount는 노미네이터 컨트랙트에서 소유자의 월렛으로 인출할 금액입니다. 위에서 설명한 대로 노미네이터 컨트랙트는 컨트랙트에 최소 1 TON을 남겨둡니다. <br/>
이 스크립트는 소유자의 월렛에서 서명하고 보내야 하는 boc 본문(withdraw.boc이라는 이름)을 생성합니다. <br/>
블랙 컴퓨터에서 소유자는 다음을 실행해야 합니다:

- tx 생성 및 서명: `fift -s wallet-v3.fif my-wallet single_nominator_address sub_wallet_id seqno amount -B withdraw.boc` 여기서 my-wallet은 소유자의 pk 파일(확장자 없음)입니다. 수수료를 지불하기 위해 amount 1 TON이면 충분합니다(남은 금액은 소유자에게 반환됨). withdraw.boc은 위에서 생성된 boc입니다.
- 인터넷 접속이 가능한 컴퓨터에서 `lite-client -C global.config.json -c 'sendfile wallet-query.boc'`를 실행하여 이전 단계에서 생성된 boc 파일(wallet-query.boc)을 보냅니다.

#### 2. `change-validator`

검증자 주소를 변경하는 데 사용됩니다. 검증자는 NEW_STAKE와 RECOVER_STAKE만 elector에 보낼 수 있습니다. 검증자의 개인키가 도난당한 경우, 검증자 주소를 변경할 수 있습니다. 이 경우 소유자만이 자금을 인출할 수 있으므로 자금은 안전합니다.<br/>

소유자가 **핫 월렛**을 사용하는 경우(권장하지 않음), [change-validator-deeplink.ts](https://github.com/orbs-network/single-nominator/blob/main/scripts/ts/change-validator-deeplink.ts)를 사용하여 검증자 주소를 변경하기 위한 딥링크를 생성할 수 있습니다. <br/>
명령줄: `ts-node scripts/ts/change-validator-deeplink.ts single-nominator-addr new-validator-address` 여기서:

- single-nominator-addr은 단일 노미네이터 주소입니다.
- new-validator-address(기본값은 ZERO 주소)는 새로운 검증자의 주소입니다. 검증자를 즉시 비활성화하고 나중에 새로운 검증자를 설정하려면 검증자 주소를 ZERO 주소로 설정하는 것이 편리할 수 있습니다.
  소유자는 tonkeeper 월렛이 있는 휴대폰에서 딥링크를 실행해야 합니다. <br/>

소유자가 **콜드 월렛**을 사용하는 경우(권장), [change-validator.fif](https://github.com/orbs-network/single-nominator/blob/main/scripts/fift/change-validator.fif)를 사용하여 change-validator opcode와 새로운 검증자 주소가 포함된 boc 본문을 생성할 수 있습니다. <br/>
명령줄: `fift -s scripts/fif/change-validator.fif new-validator-address`
이 스크립트는 소유자의 월렛에서 서명하고 보내야 하는 boc 본문(change-validator.boc이라는 이름)을 생성합니다. <br/>
블랙 컴퓨터에서 소유자는 다음을 실행해야 합니다:

- tx 생성 및 서명: `fift -s wallet-v3.fif my-wallet single_nominator_address sub_wallet_id seqno amount -B change-validator.boc` 여기서 my-wallet은 소유자의 pk 파일(확장자 없음)입니다. 수수료를 지불하기 위해 amount 1 TON이면 충분합니다(남은 금액은 소유자에게 반환됨). change-validator.boc은 위에서 생성된 boc입니다.
- 인터넷 접속이 가능한 컴퓨터에서 `lite-client -C global.config.json -c 'sendfile wallet-query.boc'`를 실행하여 이전 단계에서 생성된 boc 파일(wallet-query.boc)을 보냅니다.

#### 3. `send-raw-msg`

이 opcode는 정상적인 상황에서는 사용될 것으로 예상되지 않습니다. <br/>
노미네이터 컨트랙트에서 **모든** 메시지를 보내는 데 사용할 수 있습니다(소유자의 월렛에서 서명하고 보내야 함). <br/>
예를 들어, elector 컨트랙트 주소가 예기치 않게 변경되었고 자금이 여전히 elector에 잠겨있는 경우 이 opcode를 사용할 수 있습니다. 이 경우 검증자의 RECOVER_STAKE가 작동하지 않으며 소유자는 특정 메시지를 구성해야 합니다. <br/>
메시지 본문에는 opcode=0x7702 (32비트), query_id (64비트), mode (8비트), raw 메시지로 전송될 cell msg에 대한 참조가 포함되어야 합니다. <br/>

#### 4. `upgrade`

이는 비상 opcode이며 아마도 절대 사용되지 않아야 합니다.<br/>
노미네이터 컨트랙트를 업그레이드하는 데 사용할 수 있습니다. <br/>
메시지 본문에는 opcode=0x9903 (32비트), query_id (64비트), 새로운 cell 코드에 대한 참조가 포함되어야 합니다. <br/>

## 참조

- [Single Nominator Pool contract](https://github.com/orbs-network/single-nominator)
- [How to use Single Nominator Pool](/v3/guidelines/smart-contracts/howto/single-nominator-pool)
