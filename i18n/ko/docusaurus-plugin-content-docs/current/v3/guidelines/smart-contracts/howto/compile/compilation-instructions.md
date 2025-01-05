# 소스에서 컴파일하기

[여기](/v3/documentation/archive/precompiled-binaries#1-download)에서 미리 빌드된 바이너리를 다운로드할 수 있습니다.

여전히 직접 소스를 컴파일하고 싶다면, 아래 지침을 따르세요.

:::caution
This is a simplified quick build guide.

가정용이 아닌 프로덕션용으로 빌드하는 경우, [자동 빌드 스크립트](https://github.com/ton-blockchain/ton/tree/master/.github/workflows)를 사용하는 것이 좋습니다.
:::

## 공통

이 소프트웨어는 대부분의 Linux 시스템에서 컴파일되고 제대로 작동할 것입니다. macOS와 Windows에서도 작동해야 합니다.

1. GitHub 저장소 https://github.com/ton-blockchain/ton/에서 사용 가능한 최신 버전의 TON 블록체인 소스를 다운로드하세요:

```bash
git clone --recurse-submodules https://github.com/ton-blockchain/ton.git
```

2. 다음의 최신 버전을 설치하세요:
   - `make`
   - `cmake` 버전 3.0.2 이상
   - `g++` 또는 `clang` (또는 운영 체제에 적합한 다른 C++14 호환 컴파일러)
   - OpenSSL(C 헤더 파일 포함) 버전 1.1.1 이상
   - `build-essential`, `zlib1g-dev`, `gperf`, `libreadline-dev`, `ccache`, `libmicrohttpd-dev`, `pkg-config`, `libsodium-dev`, `libsecp256k1-dev`, `liblz4-dev`

### Ubuntu에서

```bash
apt update
sudo apt install build-essential cmake clang openssl libssl-dev zlib1g-dev gperf libreadline-dev ccache libmicrohttpd-dev pkg-config libsodium-dev libsecp256k1-dev liblz4-dev
```

3. 소스 트리를 홈 디렉토리 `~`의 `~/ton` 디렉토리로 가져왔고, 빈 디렉토리 `~/ton-build`를 만들었다고 가정합니다:

```bash
mkdir ton-build
```

그런 다음 Linux나 MacOS 터미널에서 다음을 실행하세요:

```bash
cd ton-build
export CC=clang
export CXX=clang++
cmake -DCMAKE_BUILD_TYPE=Release ../ton && cmake --build . -j$(nproc)
```

### MacOS에서

필요한 시스템 패키지를 설치하여 시스템 준비

```zsh
brew install ninja libsodium libmicrohttpd pkg-config automake libtool autoconf gnutls
brew install llvm@16
```

새로 설치된 clang 사용

```zsh
  export CC=/opt/homebrew/opt/llvm@16/bin/clang
  export CXX=/opt/homebrew/opt/llvm@16/bin/clang++
```

secp256k1 컴파일

```zsh
  git clone https://github.com/bitcoin-core/secp256k1.git
  cd secp256k1
  secp256k1Path=`pwd`
  git checkout v0.3.2
  ./autogen.sh
  ./configure --enable-module-recovery --enable-static --disable-tests --disable-benchmark
  make -j12
```

그리고 lz4:

```zsh
  git clone https://github.com/lz4/lz4
  cd lz4
  lz4Path=`pwd`
  git checkout v1.9.4
  make -j12
```

그리고 OpenSSL 3.0 다시 링크

```zsh
brew unlink openssl@1.1
brew install openssl@3
brew unlink openssl@3 &&  brew link --overwrite openssl@3
```

이제 TON을 컴파일할 수 있습니다

```zsh
cmake -GNinja -DCMAKE_BUILD_TYPE=Release .. \
-DCMAKE_CXX_FLAGS="-stdlib=libc++" \
-DSECP256K1_FOUND=1 \
-DSECP256K1_INCLUDE_DIR=$secp256k1Path/include \
-DSECP256K1_LIBRARY=$secp256k1Path/.libs/libsecp256k1.a \
-DLZ4_FOUND=1 \
-DLZ4_LIBRARIES=$lz4Path/lib/liblz4.a \
-DLZ4_INCLUDE_DIRS=$lz4Path/lib
```

:::

:::tip
메모리가 적은 컴퓨터(예: 1GB)에서 컴파일하는 경우, [스왑 파티션 생성](/v3/guidelines/smart-contracts/howto/compile/instructions-low-memory)을 잊지 마세요.
:::

## 전역 설정 다운로드

라이트 클라이언트와 같은 도구의 경우 전역 네트워크 설정을 다운로드해야 합니다.

메인넷의 경우 https://ton-blockchain.github.io/global.config.json 에서 최신 구성 파일을 다운로드하세요:

```bash
wget https://ton-blockchain.github.io/global.config.json
```

또는 테스트넷의 경우 https://ton-blockchain.github.io/testnet-global.config.json에서:

```bash
wget https://ton-blockchain.github.io/testnet-global.config.json
```

## 라이트 클라이언트

라이트 클라이언트를 빌드하려면, [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행하고, [설정을 다운로드](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)한 다음:

```bash
cmake --build . --target lite-client
```

설정으로 라이트 클라이언트 실행:

```bash
./lite-client/lite-client -C global.config.json
```

모든 것이 성공적으로 설치되면, 라이트 클라이언트는 특별 서버(TON 블록체인 네트워크용 전체 노드)에 연결하여 서버에 일부 쿼리를 보낼 것입니다.
클라이언트에 추가 인수로 쓰기 가능한 "데이터베이스" 디렉토리를 지정하면, 최신 마스터체인 블록에 해당하는 블록과 상태를 다운로드하여 저장합니다:

```bash
./lite-client/lite-client -C global.config.json -D ~/ton-db-dir
```

기본 도움말은 라이트 클라이언트에 `help`를 입력하여 얻을 수 있습니다. 종료하려면 `quit`를 입력하거나 `Ctrl-C`를 누르세요.

## FunC

소스 코드에서 FunC 컴파일러를 빌드하려면 위에서 설명한 [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행한 다음:

```bash
cmake --build . --target func
```

Fift 스크립트를 실행하려면:

```bash
./crypto/func -o output.fif -SPA source0.fc source1.fc ...
```

## Fift

소스 코드에서 Fift 컴파일러를 빌드하려면 위에서 설명한 [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행한 다음:

```bash
cmake --build . --target fift
```

Fift 스크립트를 실행하려면:

```bash
./crypto/fift -s script.fif script_param0 script_param1 ..
```

## Tonlib-cli

tonlib-cli를 빌드하려면, [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행하고, [설정을 다운로드](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)한 다음:

```bash
cmake --build . --target tonlib-cli
```

설정으로 tonlib-cli 실행:

```bash
./tonlib/tonlib-cli -C global.config.json
```

기본 도움말은 tonlib-cli에 `help`를 입력하여 얻을 수 있습니다. 종료하려면 `quit`를 입력하거나 `Ctrl-C`를 누르세요.

## RLDP-HTTP-Proxy

rldp-http-proxy를 빌드하려면, [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행하고, [설정을 다운로드](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)한 다음:

```bash
cmake --build . --target rldp-http-proxy
```

프록시 바이너리는 다음 위치에 있습니다:

```bash
./rldp-http-proxy/rldp-http-proxy
```

## generate-random-id

generate-random-id를 빌드하려면, [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행한 다음:

```bash
cmake --build . --target generate-random-id
```

바이너리는 다음 위치에 있습니다:

```bash
./utils/generate-random-id
```

## storage-daemon

storage-daemon과 storage-daemon-cli를 빌드하려면, [공통 부분](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#common)을 수행한 다음:

```bash
cmake --build . --target storage-daemon storage-daemon-cli
```

바이너리는 다음 위치에 있습니다:

```bash
./storage/storage-daemon/
```

# 이전 TON 버전 컴파일

TON 릴리스: https://github.com/ton-blockchain/ton/tags

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

## Apple M1에서 이전 버전 컴파일:

TON은 2022년 6월 11일부터 Apple M1을 지원합니다([Add apple m1 support (#401)](https://github.com/ton-blockchain/ton/commit/c00302ced4bc4bf1ee0efd672e7c91e457652430) 커밋).

Apple M1에서 이전 TON 개정판을 컴파일하려면:

1. RocksDb 서브모듈을 6.27.3으로 업데이트
   ```bash
   cd ton/third-party/rocksdb/
   git checkout fcf3d75f3f022a6a55ff1222d6b06f8518d38c7c
   ```

2. 루트 `CMakeLists.txt`를 https://github.com/ton-blockchain/ton/blob/c00302ced4bc4bf1ee0efd672e7c91e457652430/CMakeLists.txt로 교체
