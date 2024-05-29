# TON에서 간단한 ZK 프로젝트 빌드하기

## 👋 소개

**영지식**(ZK) 증명은 한 당사자(증명자)가 다른 당사자(검증자)에게 진술 자체의 유효성 이외의 정보를 공개하지 않고도 진술이 참임을 증명할 수 있는 기본적인 암호화 기본 요소입니다. 영지식 증명은 개인정보를 보호하는 시스템을 구축하기 위한 강력한 도구로 익명 결제, 익명 메시징 시스템, 신뢰 없는 브리지 등 다양한 애플리케이션에서 사용되어 왔습니다.

:::tip TVM 업그레이드 2023.07
2023년 6월 이전에는 TON에서 암호화 증명을 검증할 수 없었습니다. 페어링 알고리즘 뒤에 복잡한 연산이 존재하기 때문에, 증명 검증을 수행하기 위해 TVM 옵코드를 추가하여 TVM의 기능을 향상시켜야 했습니다. 이 기능은 [2023년 6월 업데이트](https://docs.ton.org/learn/tvm-instructions/tvm-upgrade#bls12-381)에서 추가되었으며, 이 글을 쓰는 시점에서는 테스트넷에서만 사용할 수 있습니다.
:::

## 🦄 이 튜토리얼에서는 다음 내용을 다룹니다.

1. 영지식 암호화, 특히 zk-SNARK(영지식 간결한 비대화형 지식 인수)의 기본 사항
2. 신뢰할 수 있는 설정 의식 시작하기(타우의 힘 사용)
3. 간단한 ZK 회로 작성 및 컴파일하기(Circom 언어 사용)
4. 샘플 ZK 증명 검증을 위한 FunC 컨트랙트 생성, 배포 및 테스트하기

## 색상 중심의 예시를 통해 ZK 증명에 대해 설명하기

영 지식에 대해 자세히 알아보기 전에 간단한 문제부터 시작해 보겠습니다. 색맹인 사람에게 서로 다른 색을 구별할 수 있다는 것을 증명하고 싶다고 가정해 보겠습니다. 이 문제를 해결하기 위해 대화형 솔루션을 사용하겠습니다. 색맹인(검증자)이 하나는 빨간색 🟥이고 하나는 파란색 🟦인 두 개의 동일한 종이를 발견했다고 가정합니다.

검증자가 여러분(증명자)에게 종이 조각 중 하나를 보여주며 색을 기억해달라고 요청합니다. 그런 다음 검증자가 특정 종이를 등 뒤로 들고 동일하게 유지하거나 변경한 후 색이 변했는지 여부를 묻습니다. 차이를 구분할 수 있다면 색을 볼 수 있습니다(또는 50%의 확률로 정답을 맞출 수 있으므로 운이 좋았습니다).

이제 검증자가 이 프로세스를 10번 완료하고 매번 차이를 구분할 수 있다면 검증자는 올바른 색상을 사용하고 있다고 99.90234% (1 - (1/2)^10) 확신합니다. 따라서 검증자가 이 프로세스를 30회 완료하면 검증자는 99.99999990686774%(1 - (1/2)^30)의 확신을 갖게 됩니다.

하지만 이는 대화형 솔루션이기 때문에 특정 데이터를 증명하기 위해 사용자에게 30개의 트랜잭션을 보내도록 요청하는 디앱은 효율적이지 않습니다. 따라서 비대화형 솔루션이 필요하며, 이것이 바로 Zk-SNARK와 Zk-STARK가 등장하는 이유입니다.

이 튜토리얼에서는 Zk-SNARKs만 다루겠습니다. 그러나 Zk-STARK의 작동 방식에 대한 자세한 내용은 [StarkWare 웹사이트](https://starkware.co/stark/)에서 확인할 수 있으며, [Panther Protocol 블로그 게시물](https://blog.pantherprotocol.io/zk-snarks-vs-zk-starks-differences-in-zero-knowledge-technologies/)에서 Zk-SNARK와 Zk-STARK의 차이점을 비교하는 정보를 확인할 수 있습니다\*\*.

### 🎯 Zk-SNARK: 영지식 간결한 비대화형 지식 논증

Zk-SNARK는 비대화형 증명 시스템으로, 증명자는 하나의 증명만 제출하면 어떤 진술이 참임을 검증자에게 증명할 수 있습니다. 그리고 검증자는 매우 짧은 시간 내에 증명을 검증할 수 있습니다. 일반적으로 Zk-SNARK를 다루는 작업은 세 가지 주요 단계로 구성됩니다:

- 다자간 계산(MPC)](https://en.wikipedia.org/wiki/Secure_multi-party_computation) 프로토콜을 사용하여 증명 및 검증 키를 생성하는 신뢰할 수 있는 설정을 수행합니다(TAU의 힘 사용).
- 증명자 키, 공개 입력 및 비밀 입력(증인)을 사용하여 증명 생성하기
- 증명 확인

개발 환경을 설정하고 코딩을 시작해 보겠습니다!

## ⚙ 개발 환경 설정

다음 단계를 수행하여 프로세스를 시작하겠습니다:

1. 블루프린트](https://github.com/ton-org/blueprint)를 사용하여 다음 명령을 실행하여 "simple-zk"라는 새 프로젝트를 생성한 후, 계약 이름(예: ZkSimple)을 입력한 다음 첫 번째 옵션(빈 계약 사용)을 선택합니다.

```bash
npm create ton@latest simple-zk
```

2. 다음으로 FunC 컨트랙트를 지원하도록 조정된 [snarkjs repo](https://github.com/kroist/snarkjs)를 복제합니다.

```bash
git clone https://github.com/kroist/snarkjs.git
cd snarkjs
npm ci
cd ../simple-zk
```

3. 그런 다음 ZkSNARK에 필요한 필수 라이브러리를 설치합니다.

```bash
npm add --save-dev snarkjs ffjavascript
npm i -g circom
```

4. 다음으로 package.json에 아래 섹션을 추가하겠습니다(사용할 일부 옵코드는 아직 메인넷 릴리스에서 사용할 수 없습니다).

```json
"overrides": {
    "@ton-community/func-js-bin": "0.4.5-tvmbeta.1",
    "@ton-community/func-js": "0.6.3-tvmbeta.1"
}
```

5. 또한 [최신 TVM 업데이트](https://t.me/thetontech/56)를 사용할 수 있도록 @ton-community/sandbox의 버전을 변경해야 합니다.

```bash
npm i --save-dev @ton-community/sandbox@0.12.0-tvmbeta.1
```

잘됐네요! 이제 TON에서 첫 번째 ZK 프로젝트를 작성할 준비가 되었습니다!

현재 ZK 프로젝트를 구성하는 두 개의 주요 폴더가 있습니다:

- simple-zk\` 폴더: 회로와 컨트랙트 및 테스트를 작성할 수 있는 블루프린트 템플릿이 들어 있습니다.
- snarkjs\` 폴더: 2단계에서 복제한 snarkjs 리포지토리가 들어 있습니다.

## 서컴 회로

먼저 'simple-zk/circuits' 폴더를 생성한 다음 그 안에 파일을 만들고 다음 코드를 추가해 보겠습니다:

```circom
template Multiplier() {
   signal private input a;
   signal private input b;
   //private input means that this input is not public and will not be revealed in the proof

   signal output c;

   c <== a*b;
 }

component main = Multiplier();
```

위에 간단한 승수 회로를 추가했습니다. 이 회로를 사용하면 해당 숫자(a와 b) 자체를 밝히지 않고도 함께 곱하면 특정 숫자(c)가 되는 두 개의 숫자를 알고 있다는 것을 증명할 수 있습니다.

circom 언어에 대한 자세한 내용은 [이 웹사이트](https://docs.circom.io/)를 참조하세요.

다음으로 빌드 파일을 위한 폴더를 만들고 'simple-zk' 폴더에 있는 상태에서 다음을 수행하여 데이터를 해당 폴더로 이동합니다:

```bash
mkdir -p ./build/circuits
cd ./build/circuits
```

### 💪 TAU의 힘으로 신뢰할 수 있는 설정 만들기

이제 신뢰할 수 있는 설정을 구축할 차례입니다. 이 과정을 수행하기 위해 [타우의 힘](https://a16zcrypto.com/posts/article/on-chain-trusted-setup-ceremony/) 방법을 사용하겠습니다(완료하는 데 몇 분 정도 걸립니다). 시작해 보겠습니다:

```bash
echo 'prepare phase1'
node ../../../snarkjs/build/cli.cjs powersoftau new bls12-381 14 pot14_0000.ptau -v
echo 'contribute phase1 first'
node ../../../snarkjs/build/cli.cjs powersoftau contribute pot14_0000.ptau pot14_0001.ptau --name="First contribution" -v -e="some random text"
echo 'contribute phase1 second'
node ../../../snarkjs/build/cli.cjs powersoftau contribute pot14_0001.ptau pot14_0002.ptau --name="Second contribution" -v -e="some random text"
echo 'apply a random beacon'
node ../../../snarkjs/build/cli.cjs powersoftau beacon pot14_0002.ptau pot14_beacon.ptau 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f 10 -n="Final Beacon"
echo 'prepare phase2'
node ../../../snarkjs/build/cli.cjs powersoftau prepare phase2 pot14_beacon.ptau pot14_final.ptau -v
echo 'Verify the final ptau'
node ../../../snarkjs/build/cli.cjs powersoftau verify pot14_final.ptau
```

위의 프로세스가 완료되면 build/circuits 폴더에 pot14_final.ptau 파일이 생성되며, 이 파일은 향후 관련 회로를 작성하는 데 사용할 수 있습니다.

:::caution 제약 조건 크기
더 많은 제약 조건이 있는 더 복잡한 회로를 작성하는 경우 더 큰 매개 변수를 사용하여 PTAU 설정을 생성해야 합니다.
:::

불필요한 파일을 제거할 수 있습니다:

```bash
rm pot14_0000.ptau pot14_0001.ptau pot14_0002.ptau pot14_beacon.ptau
```

### 📜 회로 편집

이제 `build/circuits` 폴더에서 다음 명령을 실행하여 회로를 컴파일해 보겠습니다:

```bash
circom ../../circuits/test.circom --r1cs circuit.r1cs --wasm circuit.wasm --prime bls12381 --sym circuit.sym
```

이제 `build/circuits/circuit.sym`, `build/circuits/circuit.r1cs` 및 `build/circuits/circuit.wasm` 파일에 회로가 컴파일되었습니다.

:::info ALTBN-128 및 BLS12-381 커브
altbn-128 및 bls12-381 타원 커브는 현재 snarkjs에서 지원됩니다. altbn-128](https://eips.ethereum.org/EIPS/eip-197) 커브는 이더리움에서만 지원됩니다. 그러나 TON에서는 bls12-381 커브만 지원됩니다.
:::

다음 명령을 입력하여 회로의 제약 조건 크기를 확인해 보겠습니다:

```bash
node ../../../snarkjs/build/cli.cjs r1cs info circuit.r1cs 
```

따라서 올바른 결과가 나와야 합니다:

```bash
[INFO]  snarkJS: Curve: bls12-381
[INFO]  snarkJS: # of Wires: 4
[INFO]  snarkJS: # of Constraints: 1
[INFO]  snarkJS: # of Private Inputs: 2
[INFO]  snarkJS: # of Public Inputs: 0
[INFO]  snarkJS: # of Labels: 4
[INFO]  snarkJS: # of Outputs: 1
```

이제 다음을 실행하여 참조 zkey를 생성할 수 있습니다:

```bash
node ../../../snarkjs/build/cli.cjs zkey new circuit.r1cs pot14_final.ptau circuit_0000.zkey
```

그런 다음 아래 기여를 zkey에 추가합니다:

```bash
echo "some random text" | node ../../../snarkjs/build/cli.cjs zkey contribute circuit_0000.zkey circuit_0001.zkey --name="1st Contributor Name" -v
```

다음으로 최종 zkey를 내보내 보겠습니다:

```bash
echo "another random text" | node ../../../snarkjs/build/cli.cjs zkey contribute circuit_0001.zkey circuit_final.zkey
```

이제 `build/circuits/circuit_final.zkey` 파일에 최종 zkey가 있습니다. 그런 다음 다음을 입력하여 zkey를 확인합니다:

```bash
node ../../../snarkjs/build/cli.cjs zkey verify circuit.r1cs pot14_final.ptau circuit_final.zkey
```

마지막으로 인증 키를 생성할 차례입니다:

```bash
node ../../../snarkjs/build/cli.cjs zkey export verificationkey circuit_final.zkey verification_key.json
```

그런 다음 불필요한 파일을 제거합니다:

```bash
rm circuit_0000.zkey circuit_0001.zkey
```

위의 과정을 수행하면 다음과 같이 `build/circuits` 폴더가 표시되어야 합니다:

```
build
└── circuits
        ├── circuit_final.zkey
        ├── circuit.r1cs
        ├── circuit.sym
        ├── circuit.wasm
        ├── pot14_final.ptau
        └── verification_key.json

```

### ✅ 검증자 계약 내보내기

이 섹션의 마지막 단계는 ZK 프로젝트에서 사용할 FunC 검증자 컨트랙트를 생성하는 것입니다.

```bash
node ../../../snarkjs/build/cli.cjs zkey export funcverifier circuit_final.zkey ../../contracts/verifier.fc
```

그러면 `verifier.fc` 파일이 `contracts` 폴더에 생성됩니다.

## 🚢 검증자 컨트랙트 배포

계약/검증자.fc\` 파일을 차근차근 살펴보겠습니다. 이 파일에는 ZK-SNARK의 마법이 담겨 있기 때문입니다:

```func
const slice IC0 = "b514a6870a13f33f07bc314cdad5d426c61c50b453316c241852089aada4a73a658d36124c4df0088f2cd8838731b971"s;
const slice IC1 = "8f9fdde28ca907af4acff24f772448a1fa906b1b51ba34f1086c97cd2c3ac7b5e0e143e4161258576d2a996c533d6078"s;

const slice vk_gamma_2 = "93e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8"s;
const slice vk_delta_2 = "97b0fdbc9553a62a79970134577d1b86f7da8937dd9f4d3d5ad33844eafb47096c99ee36d2eab4d58a1f5b8cc46faa3907e3f7b12cf45449278832eb4d902eed1d5f446e5df9f03e3ce70b6aea1d2497fd12ed91bd1d5b443821223dca2d19c7"s;
const slice vk_alpha_1 = "a3fa7b5f78f70fbd1874ffc2104f55e658211db8a938445b4a07bdedd966ec60090400413d81f0b6e7e9afac958abfea"s;
const slice vk_beta_2 = "b17e1924160eff0f027c872bc13ad3b60b2f5076585c8bce3e5ea86e3e46e9507f40c4600401bf5e88c7d6cceb05e8800712029d2eff22cbf071a5eadf166f266df75ad032648e8e421550f9e9b6c497b890a1609a349fbef9e61802fa7d9af5"s;
```

위는 검증자 컨트랙트가 증명 검증을 구현하기 위해 사용해야 하는 상수입니다. 이러한 파라미터는 `build/circuits/verification_key.json` 파일에서 찾을 수 있습니다.

```func
slice bls_g1_add(slice x, slice y) asm "BLS_G1_ADD";
slice bls_g1_neg(slice x) asm "BLS_G1_NEG";
slice bls_g1_multiexp(
        slice x1, int y1,
        int n
) asm "BLS_G1_MULTIEXP";
int bls_pairing(slice x1, slice y1, slice x2, slice y2, slice x3, slice y3, slice x4, slice y4, int n) asm "BLS_PAIRING";
```

위의 라인은 TON 블록체인에서 페어링 확인을 수행할 수 있는 새로운 [TVM 옵코드](https://docs.ton.org/learn/tvm-instructions/tvm-upgrade-2023-07#bls12-381)(BLS12-381)입니다.

로드_데이터 및 저장_데이터 함수는 단순히 증명 검증 결과를 로드하고 저장하는 데 사용됩니다(테스트 목적으로만 사용).

```func
() load_data() impure {

    var ds = get_data().begin_parse();

    ctx_res = ds~load_uint(32);

    ds.end_parse();
}

() save_data() impure {
    set_data(
            begin_cell()
                    .store_uint(ctx_res, 32)
                    .end_cell()
    );
}
```

다음으로 컨트랙트에 전송된 증명 데이터를 로드하는 데 사용되는 몇 가지 간단한 활용 함수가 있습니다:

```func
(slice, slice) load_p1(slice body) impure {
    ...
}

(slice, slice) load_p2(slice body) impure {
    ...
}

(slice, int) load_newint(slice body) impure {
    ...
}
```

마지막 부분은 계약에 전송된 증명의 유효성을 확인하는 데 필요한 groth16Verify 기능입니다.

```func
() groth16Verify(
        slice pi_a,
        slice pi_b,
        slice pi_c,

        int pubInput0

) impure {

    slice cpub = bls_g1_multiexp(

            IC1, pubInput0,

            1
    );


    cpub = bls_g1_add(cpub, IC0);
    slice pi_a_neg = bls_g1_neg(pi_a);
    int a = bls_pairing(
            cpub, vk_gamma_2,
            pi_a_neg, pi_b,
            pi_c, vk_delta_2,
            vk_alpha_1, vk_beta_2,
            4);
    ;; ctx_res = a;
    if (a == 0) {
        ctx_res = 0;
    } else {
        ctx_res = 1;
    }
    save_data();
}
```

이제 `wrappers` 폴더에 있는 두 파일을 편집해야 합니다. 가장 먼저 주목해야 할 파일은 `ZkSimple.compile.ts` 파일입니다(1단계에서 컨트랙트의 다른 이름을 설정한 경우, 이름이 달라집니다). 컴파일해야 하는 컨트랙트 목록에 `verifier.fc` 파일을 넣겠습니다.

```ts
import { CompilerConfig } from '@ton-community/blueprint';

export const compile: CompilerConfig = {
  lang: 'func',
  targets: ['contracts/verifier.fc'], // <-- here we put the path to our contract
};
```

주의가 필요한 다른 파일은 `ZkSimple.ts`입니다. 먼저 `Opcodes` 열거형에 `verify`의 옵코드를 추가해야 합니다:

```ts
export const Opcodes = {
  verify: 0x3b3cca17,
};
```

다음으로, `ZkSimple` 클래스에 `sendVerify` 함수를 추가해야 합니다. 이 함수는 컨트랙트에 증명을 전송하고 테스트하는 데 사용되며 다음과 같이 표시됩니다:

```ts
async sendVerify(
  provider: ContractProvider,
  via: Sender,
  opts: {
  pi_a: Buffer;
  pi_b: Buffer;
  pi_c: Buffer;
  pubInputs: bigint[];
  value: bigint;
  queryID?: number;
}
) {
  await provider.internal(via, {
    value: opts.value,
    sendMode: SendMode.PAY_GAS_SEPARATELY,
    body: beginCell()
      .storeUint(Opcodes.verify, 32)
      .storeUint(opts.queryID ?? 0, 64)
      .storeRef(
        beginCell()
          .storeBuffer(opts.pi_a)
          .storeRef(
            beginCell()
              .storeBuffer(opts.pi_b)
              .storeRef(
                beginCell()
                  .storeBuffer(opts.pi_c)
                  .storeRef(
                    this.cellFromInputList(opts.pubInputs)
                  )
              )
          )
      )
      .endCell(),
  });
}
```

다음으로 `ZkSimple` 클래스에 `cellFromInputList` 함수를 추가하겠습니다. 이 함수는 컨트랙트로 전송될 공개 입력에서 셀을 생성하는 데 사용됩니다.

```ts
 cellFromInputList(list: bigint[]) : Cell {
  var builder = beginCell();
  builder.storeUint(list[0], 256);
  if (list.length > 1) {
    builder.storeRef(
      this.cellFromInputList(list.slice(1))
    );
  }
  return builder.endCell()
}
```

마지막으로 `ZkSimple` 클래스에 추가할 함수는 `getRes` 함수입니다. 이 함수는 증명 검증 결과를 받는 데 사용됩니다.

```ts
 async getRes(provider: ContractProvider) {
  const result = await provider.get('get_res', []);
  return result.stack.readNumber();
}
```

이제 컨트랙트를 배포하는 데 필요한 필수 테스트를 실행할 수 있습니다. 이를 위해서는 컨트랙트가 배포 테스트를 성공적으로 통과할 수 있어야 합니다. 이 명령은 `simple-zk` 폴더의 루트에서 실행합니다:

```bash
npx blueprint test
```

## 🧑‍💻 검증자를 위한 테스트 작성

tests`폴더에서`ZkSimple.spec.ts`파일을 열고`verify\` 함수에 대한 테스트를 작성해 보겠습니다. 테스트는 다음과 같이 진행됩니다:

```ts
describe('ZkSimple', () => {
  let code: Cell;

  beforeAll(async () => {
    code = await compile('ZkSimple');
  });

  let blockchain: Blockchain;
  let zkSimple: SandboxContract<ZkSimple>;

  beforeEach(async () => {
    // deploy contract
  });

  it('should deploy', async () => {
    // the check is done inside beforeEach
    // blockchain and zkSimple are ready to use
  });

  it('should verify', async () => {
    // todo write the test
  });
});
```

먼저 테스트에 사용할 여러 패키지를 가져와야 합니다:

```ts
import * as snarkjs from "snarkjs";
import path from "path";
import {buildBls12381, utils} from "ffjavascript";
const {unstringifyBigInts} = utils;
```

- 테스트를 실행하면 'snarkjs' 및 ffjavascript 모듈에 대한 선언 파일이 없기 때문에 TypeScript 오류가 발생합니다. 이 문제는 'simple-zk' 폴더의 루트에 있는 `tsconfig.json` 파일을 편집하여 해결할 수 있습니다. 해당 파일에서 ***strict*** 옵션을 ***false***로 변경해야 합니다.
-

또한 계약에 전송할 증명을 생성하는 데 사용할 `circuit.wasm` 및 `circuit_final.zkey` 파일을 가져와야 합니다.

```ts
const wasmPath = path.join(__dirname, "../build/circuits", "circuit.wasm");
const zkeyPath = path.join(__dirname, "../build/circuits", "circuit_final.zkey");
```

'확인해야 함' 테스트를 작성해 보겠습니다. 먼저 증명을 생성해야 합니다.

```ts
it('should verify', async () => {
  // proof generation
  let input = {
    "a": "123",
    "b": "456",
  }
  let {proof, publicSignals} = await snarkjs.groth16.fullProve(input, wasmPath, zkeyPath);
  let curve = await buildBls12381();
  let proofProc = unstringifyBigInts(proof);
  var pi_aS = g1Compressed(curve, proofProc.pi_a);
  var pi_bS = g2Compressed(curve, proofProc.pi_b);
  var pi_cS = g1Compressed(curve, proofProc.pi_c);
  var pi_a = Buffer.from(pi_aS, "hex");
  var pi_b = Buffer.from(pi_bS, "hex");
  var pi_c = Buffer.from(pi_cS, "hex");
  
  // todo send the proof to the contract
});
```

다음 단계를 수행하려면 `g1Compressed`, `g2Compressed`, `toHexString` 함수를 정의해야 합니다. 이 함수는 암호화 증명을 컨트랙트가 기대하는 형식으로 변환하는 데 사용됩니다.

```ts
function g1Compressed(curve, p1Raw) {
  let p1 = curve.G1.fromObject(p1Raw);

  let buff = new Uint8Array(48);
  curve.G1.toRprCompressed(buff, 0, p1);
  // convert from ffjavascript to blst format
  if (buff[0] & 0x80) {
    buff[0] |= 32;
  }
  buff[0] |= 0x80;
  return toHexString(buff);
}

function g2Compressed(curve, p2Raw) {
  let p2 = curve.G2.fromObject(p2Raw);

  let buff = new Uint8Array(96);
  curve.G2.toRprCompressed(buff, 0, p2);
  // convert from ffjavascript to blst format
  if (buff[0] & 0x80) {
    buff[0] |= 32;
  }
  buff[0] |= 0x80;
  return toHexString(buff);
}

function toHexString(byteArray) {
  return Array.from(byteArray, function (byte: any) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join("");
}
```

이제 컨트랙트에 암호화 증명을 보낼 수 있습니다. 이를 위해 sendVerify 함수를 사용하겠습니다. sendVerify` 함수는 5개의 파라미터를 기대합니다: pi_a`, `pi_b`, `pi_c`, `pubInputs`, `value`입니다.

```ts
it('should verify', async () => {
  // proof generation
  
  
  // send the proof to the contract
  const verifier = await blockchain.treasury('verifier');
  const verifyResult = await zkSimple.sendVerify(verifier.getSender(), {
    pi_a: pi_a,
    pi_b: pi_b,
    pi_c: pi_c,
    pubInputs: publicSignals,
    value: toNano('0.15'), // 0.15 TON for fee
  });
  expect(verifyResult.transactions).toHaveTransaction({
    from: verifier.address,
    to: zkSimple.address,
    success: true,
  });

  const res = await zkSimple.getRes();

  expect(res).not.toEqual(0); // check proof result

  return;
  
});
```

TON 블록체인에서 첫 번째 증명을 검증할 준비가 되셨나요? 이 과정을 시작하기 위해 다음을 입력하여 블루프린트 테스트를 실행해 보겠습니다:

```bash
npx blueprint test
```

결과는 다음과 같아야 합니다:

```bash
 PASS  tests/ZkSimple.spec.ts
  ZkSimple
    ✓ should deploy (857 ms)
    ✓ should verify (1613 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
Snapshots:   0 total
Time:        4.335 s, estimated 5 s
Ran all test suites.
```

이 튜토리얼의 코드가 포함된 리포지토리를 확인하려면 [여기](https://github.com/SaberDoTcodeR/zk-ton-doc)에 있는 다음 링크를 클릭하세요.

## 🏁 결론

이 튜토리얼에서는 다음 기술을 배웠습니다:

- 영지식, 특히 ZK-SNARK의 복잡성
- Circom 순환 작성 및 컴파일하기
- 회로에 대한 검증 키를 생성하는 데 사용되는 MPC 및 TAU의 힘에 대한 친숙도가 높아졌습니다.
- 회로에 대한 FunC 검증기를 내보내기 위해 Snarkjs 라이브러리에 익숙해졌습니다.
- 검증기 배포 및 테스트 작성을 위한 블루프린트에 익숙해졌습니다.

참고: 위의 예시에서는 간단한 ZK 사용 사례를 구축하는 방법을 설명했습니다. 하지만 다양한 산업 분야에서 구현할 수 있는 매우 복잡한 ZK 중심 사용 사례는 매우 다양합니다. 그 중 일부는 다음과 같습니다:

- 비공개 투표 시스템 🗳
- 개인 복권 시스템 🎰
- 비공개 경매 시스템 🤝
- 비공개 거래💸(톤코인 또는 제톤의 경우)

이 튜토리얼에서 궁금한 점이 있거나 오류가 발생하면 언제든지 작성자에게 편지를 보내주세요: [@saber_coder](https://t.me/saber_coder)

## 📌 참고 자료

- [TVM 2023년 6월 업그레이드](https://docs.ton.org/learn/tvm-instructions/tvm-upgrade)
- [SnarkJs](https://github.com/iden3/snarkjs)
- [SnarkJs FunC 포크](https://github.com/kroist/snarkjs)
- [샘플 ZK on TON](https://github.com/SaberDoTcodeR/ton-zk-verifier)
- [청사진](https://github.com/ton-org/blueprint)

## 📖 참고 항목

- [TON 트러스트리스 브리지 EVM 계약](https://github.com/ton-blockchain/ton-trustless-bridge-evm-contracts)
- [톤 네트워크: 톤의 개인정보 보호 프로토콜](http://github.com/saberdotcoder/tonnel-network)
- [TVM 챌린지](https://blog.ton.org/tvm-challenge-is-here-with-over-54-000-in-rewards)

## 📬 저자 소개

- 텔레그램](https://t.me/saber_coder) 또는 [깃허브](https://github.com/saberdotcoder) 또는 [링크드인](https://www.linkedin.com/in/szafarpoor/)에서 세이버를 만나보세요.
