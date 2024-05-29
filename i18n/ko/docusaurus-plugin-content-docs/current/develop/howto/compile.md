# 소스에서 컴파일

여기에서 미리 빌드된 바이너리를 다운로드할 수 있습니다(/개발/스마트계약/환경/설치#1-download).

그래도 소스를 직접 컴파일하려면 아래 지침을 따르세요.

:::caution
This is a simplified quick build guide.

가정용이 아닌 프로덕션용으로 빌드하는 경우 [자동 빌드 스크립트](https://github.com/ton-blockchain/ton/tree/master/.github/workflows)를 사용하는 것이 좋습니다.
:::

## 공통

이 소프트웨어는 대부분의 Linux 시스템에서 컴파일되고 제대로 작동할 것입니다. macOS와 Windows에서도 작동합니다.

1. GitHub 리포지토리(https://github.com/ton-blockchain/ton/)에서 최신 버전의 TON 블록체인 소스를 다운로드하세요:

```bash
git clone --recurse-submodules https://github.com/ton-blockchain/ton.git
```

2. 최신 버전을 설치합니다:

   - `만들다`
   - cmake\` 버전 3.0.2 이상
   - g++`또는`clang\`(또는 운영 체제에 적합한 다른 C++14 호환 컴파일러)을 사용하세요.
   - OpenSSL(C 헤더 파일 포함) 버전 1.1.1 이상
   - 빌드-에센셜`, `zlib1g-dev`, `gperf`, `libreadline-dev`, `ccache`, `libmicrohttpd-dev`, `pkg-config`, `libsodium-dev`, `libsecp256k1-dev\`

   우분투에서:

```bash
apt update
sudo apt install build-essential cmake clang openssl libssl-dev zlib1g-dev gperf libreadline-dev ccache libmicrohttpd-dev pkg-config libsodium-dev libsecp256k1-dev
```

3. 소스 트리를 `~/ton` 디렉토리로 가져왔고, 여기서 `~`는 홈 디렉토리이며, 빈 디렉토리 `~/ton-build`를 생성했다고 가정해 보겠습니다:

```bash
mkdir ton-build
```

그런 다음 Linux 또는 MacOS 터미널에서 다음을 실행합니다:

```bash
cd ton-build
export CC=clang
export CXX=clang++
cmake -DCMAKE_BUILD_TYPE=Release ../ton && cmake --build . -j$(nproc)
```

:::warning
On MacOS Intel before next step we need maybe install `openssl@3` with `brew` or just link the lib:

```zsh
brew install openssl@3 ninja libmicrohttpd pkg-config
```

그런 다음 `/usr/local/opt`를 검사해야 합니다:

```zsh
ls /usr/local/opt
```

openssl@3\` 라이브러리를 찾아 로컬 변수를 내보냅니다:

```zsh
export OPENSSL_ROOT_DIR=/usr/local/opt/openssl@3
```

:::

:::tip
메모리가 부족한 컴퓨터(예: 1Gb)에서 컴파일하는 경우, [스왑 파티션 생성](/개발/방법/컴파일-스왑)을 잊지 마세요.
:::

## 글로벌 구성 다운로드

라이트 클라이언트와 같은 도구의 경우 글로벌 네트워크 구성을 다운로드해야 합니다.

메인넷의 경우 https://ton-blockchain.github.io/global.config.json 에서 최신 구성 파일을 다운로드하세요:

```bash
wget https://ton-blockchain.github.io/global.config.json
```

또는 테스트넷의 경우 https://ton-blockchain.github.io/testnet-global.config.json 에서 확인하세요:

```bash
wget https://ton-blockchain.github.io/testnet-global.config.json
```

## 라이트 클라이언트

라이트 클라이언트를 빌드하려면 [공통 부분](/개발/방법/컴파일#공통), [설정 다운로드](/개발/방법/컴파일#다운로드-global-config)를 수행한 다음 수행합니다:

```bash
cmake --build . --target lite-client
```

구성으로 Lite 클라이언트를 실행합니다:

```bash
./lite-client/lite-client -C global.config.json
```

모든 것이 성공적으로 설치되면 라이트 클라이언트는 특수 서버(톤 블록체인 네트워크의 전체 노드)에 연결하고 몇 가지 쿼리를 서버로 전송합니다.
클라이언트에 추가 인수로 쓰기 가능한 "데이터베이스" 디렉토리를 지정하면 최신 마스터체인 블록에 해당하는 블록과 상태를 다운로드하여 저장합니다:

```bash
./lite-client/lite-client -C global.config.json -D ~/ton-db-dir
```

Lite 클라이언트에 `help`를 입력하면 기본 도움말 정보를 얻을 수 있습니다. 종료하려면 `quit`을 입력하거나 `Ctrl-C`를 누르세요.

## FunC

소스 코드에서 FunC 컴파일러를 빌드하려면 위에서 설명한 [공통 부분](/개발/하우투/컴파일#공통)을 수행한 다음, [공통]을 수행합니다:

```bash
cmake --build . --target func
```

FunC 스마트 컨트랙트를 컴파일합니다:

```bash
func -o output.fif -SPA source0.fc source1.fc ...
```

## Fift

소스 코드에서 Fift 컴파일러를 빌드하려면 위에서 설명한 [공통 부분](/개발/하우투/컴파일#공통)을 수행한 다음, [공통]을 수행합니다:

```bash
cmake --build . --target fift
```

Fift 스크립트를 실행하려면

```bash
fift -s script.fif script_param0 script_param1 ..
```

## Tonlib-cli

톤라이브-cli를 빌드하려면 [공통 부분](/개발/하우투/컴파일#common), [설정 다운로드](/개발/하우투/컴파일#다운로드-global-config)를 수행한 다음 실행합니다:

```bash
cmake --build . --target tonlib-cli
```

config를 사용하여 tonlib-cli를 실행합니다:

```bash
./tonlib/tonlib-cli -C global.config.json
```

톤라이브-cli에 `help`를 입력하면 기본 도움말 정보를 얻을 수 있습니다. 종료하려면 `quit`을 입력하거나 `Ctrl-C`를 누릅니다.

## RLDP-HTTP-프록시

rldp-http-proxy를 빌드하려면 [공통 부분](/개발/방법/컴파일#공통), [설정 다운로드](/개발/방법/컴파일#다운로드-global-config)를 수행한 다음 수행합니다:

```bash
cmake --build . --target rldp-http-proxy
```

프록시 바이너리는 다음과 같이 위치합니다:

```bash
rldp-http-proxy/rldp-http-proxy
```

## 생성-랜덤-ID

generate-random-id를 빌드하려면 [공통 부분](/개발/방법/컴파일#공통)을 실행한 다음 다음을 수행합니다:

```bash
cmake --build . --target generate-random-id
```

바이너리는 다음과 같이 위치합니다:

```bash
utils/generate-random-id
```

## 스토리지 데몬

스토리지-대몬과 스토리지-대몬-cli를 빌드하려면 [공통 부분](/개발/방법/컴파일#공통)을 실행한 다음 다음을 수행합니다:

```bash
cmake --build . --target storage-daemon storage-daemon-cli
```

바이너리는 다음 위치에 있습니다:

```bash
storage/storage-daemon/
```

# 이전 TON 버전 컴파일

TON 출시: https://github.com/ton-blockchain/ton/tags

```bash
git clone https://github.com/ton-blockchain/ton.git
cd ton
# git checkout <TAG> for example checkout func-0.2.0
git checkout func-0.2.0
git submodule update --init --recursive 
cd ..
mkdir ton-build
cd ton-build
cmake ../ton
# build func 0.2.0
cmake --build . --target func
```

## Apple M1에서 이전 버전을 컴파일합니다:

TON은 2022년 6월 11일부터 Apple M1을 지원합니다([애플 M1 지원 추가(#401)](https://github.com/ton-blockchain/ton/commit/c00302ced4bc4bf1ee0efd672e7c91e457652430) 커밋).

Apple M1에서 이전 TON 개정판을 컴파일하려면:

1. RocksDb 서브모듈을 6.27.3으로 업데이트하세요.
   ```bash
   cd ton/third-party/rocksdb/
   git checkout fcf3d75f3f022a6a55ff1222d6b06f8518d38c7c
   ```

2. 루트 `CMakeLists.txt`를 https://github.com/ton-blockchain/ton/blob/c00302ced4bc4bf1ee0efd672e7c91e457652430/CMakeLists.txt 으로 바꿉니다.
