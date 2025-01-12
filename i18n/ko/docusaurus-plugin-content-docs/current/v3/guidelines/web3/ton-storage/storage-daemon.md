# 스토리지 데몬

*스토리지 데몬은 TON 네트워크에서 파일을 다운로드하고 공유하는 데 사용되는 프로그램입니다. `storage-daemon-cli` 콘솔 프로그램은 실행 중인 스토리지 데몬을 관리하는 데 사용됩니다.*

스토리지 데몬의 현재 버전은 [Testnet](https://github.com/ton-blockchain/ton/tree/testnet) 브랜치에서 찾을 수 있습니다.

## 하드웨어 요구사항

- 최소 1GHz 및 2코어 CPU
- 최소 2 GB RAM
- 최소 2 GB SSD (토렌트를 위한 공간은 제외)
- 고정 IP를 가진 10 Mb/s 네트워크 대역폭

## 바이너리

Linux/Windows/MacOS용 `storage-daemon` 및 `storage-daemon-cli` 바이너리는 [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 다운로드할 수 있습니다.

## 소스에서 컴파일하기

이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#storage-daemon)을 사용하여 `storage-daemon` 및 `storage-damon-cli`를 소스에서 컴파일할 수 있습니다.

## 주요 개념

- *파일 가방* 또는 *Bag* - TON Storage를 통해 배포되는 파일 모음
- TON Storage의 네트워크 부분은 토렌트와 유사한 기술을 기반으로 하므로, *Torrent*, *Bag of files*, *Bag*이라는 용어를 서로 바꿔 사용할 수 있습니다. 그러나 몇 가지 차이점에 주목해야 합니다: TON Storage는 [RLDP](/v3/documentation/network/protocols/rldp) 프로토콜을 통해 [ADNL](/v3/documentation/network/protocols/adnl/overview)을 통해 데이터를 전송하고, 각 *Bag*은 자체 네트워크 오버레이를 통해 배포되며, 머클 구조는 효율적인 다운로드를 위한 대용량 청크와 효율적인 소유권 증명을 위한 작은 청크의 두 가지 버전으로 존재할 수 있으며, 피어를 찾기 위해 [TON DHT](/v3/documentation/network/protocols/dht/ton-dht) 네트워크가 사용됩니다.
- *파일 가방*은 *토렌트 정보*와 데이터 블록으로 구성됩니다.
- 데이터 블록은 *토렌트 헤더*로 시작합니다 - 파일 이름과 크기가 포함된 파일 목록이 있는 구조입니다. 데이터 블록에는 파일 자체가 이어집니다.
- 데이터 블록은 청크로 나뉘며(기본값 128 KB), 이러한 청크의 SHA256 해시에 대해 *머클 트리*(TVM 셀로 만들어짐)가 구축됩니다. 이를 통해 개별 청크의 *머클 증명*을 구축하고 검증할 수 있으며, 수정된 청크의 증명만 교환하여 효율적으로 *Bag*을 재생성할 수 있습니다.
- *토렌트 정보*에는 다음의 *머클 루트*가 포함됩니다
  - 청크 크기 (데이터 블록)
  - 청크 크기 목록
  - 해시 *머클 트리*
  - 설명 - 토렌트 생성자가 지정한 텍스트
- *토렌트 정보*는 TVM 셀로 직렬화됩니다. 이 셀의 해시를 *BagID*라고 하며, 이는 *Bag*을 고유하게 식별합니다.
- *Bag 메타*는 *토렌트 정보*와 *토렌트 헤더*를 포함하는 파일입니다.\* 이는 `.torrent` 파일의 아날로그입니다.

## 스토리지 데몬 및 storage-daemon-cli 시작하기

### storage-daemon을 시작하기 위한 예제 명령:

`storage-daemon -v 3 -C global.config.json -I <ip>:3333 -p 5555 -D storage-db`

- `-v` - 상세 수준 (INFO)
- `-C` - 글로벌 네트워크 설정 ([글로벌 설정 다운로드](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config))
- `-I` - adnl을 위한 IP 주소와 포트
- `-p` - 콘솔 인터페이스를 위한 TCP 포트
- `-D` - 스토리지 데몬 데이터베이스 디렉토리

### storage-daemon-cli 관리

다음과 같이 시작됩니다:

```
storage-daemon-cli -I 127.0.0.1:5555 -k storage-db/cli-keys/client -p storage-db/cli-keys/server.pub
```

- `-I` - 데몬의 IP 주소와 포트 (포트는 위의 `-p` 매개변수에 지정된 것과 동일)
- `-k`와 `-p` - 클라이언트의 개인 키와 서버의 공개 키 (`validator-engine-console`와 유사). 이 키들은 데몬의 첫 실행 시 생성되어 `<db>/cli-keys/`에 저장됩니다.

### 명령 목록

`storage-daemon-cli` 명령 목록은 `help` 명령으로 얻을 수 있습니다.

명령에는 위치 매개변수와 플래그가 있습니다. 공백이 있는 매개변수는 따옴표(`'` 또는 `"`)로 둘러싸야 하며, 공백은 이스케이프될 수 있습니다. 다른 이스케이프도 사용 가능합니다. 예:

```
create filename\ with\ spaces.txt -d "Description\nSecond line of \"description\"\nBackslash: \\"
```

`--` 플래그 뒤의 모든 매개변수는 위치 매개변수입니다. 대시로 시작하는 파일 이름을 지정하는 데 사용할 수 있습니다:

```
create -d "Description" -- -filename.txt
```

`storage-daemon-cli`는 실행할 명령을 전달하여 비대화형 모드로 실행할 수 있습니다:

```
storage-daemon-cli ... -c "add-by-meta m" -c "list --hashes"
```

## 파일 가방 추가하기

*파일 가방*을 다운로드하려면 `BagID`를 알거나 메타 파일이 있어야 합니다. 다운로드를 위해 *Bag*을 추가하는 데 다음 명령을 사용할 수 있습니다:

```
add-by-hash <hash> -d directory
add-by-meta <meta-file> -d directory
```

*Bag*은 지정된 디렉토리에 다운로드됩니다. 생략하면 스토리지 데몬 디렉토리에 저장됩니다.

:::info
해시는 16진수 형식으로 지정됩니다(길이 - 64자).
:::

메타 파일로 *Bag*을 추가할 때는 *Bag*에 대한 정보(크기, 설명, 파일 목록)를 즉시 사용할 수 있습니다. 해시로 추가할 때는 이 정보가 로드될 때까지 기다려야 합니다.

## 추가된 Bag 관리하기

- `list` 명령은 *Bag* 목록을 출력합니다.
- `list --hashes`는 전체 해시가 포함된 목록을 출력합니다.

이후의 모든 명령에서 `<BagID>`는 해시(16진수) 또는 세션 내 *Bag*의 순서 번호(list 명령으로 볼 수 있는 번호)입니다. *Bag*의 순서 번호는 storage-daemon-cli 재시작 사이에 저장되지 않으며 비대화형 모드에서는 사용할 수 없습니다.

### 메소드

- `get <BagID>` - *Bag*에 대한 자세한 정보를 출력합니다: 설명, 크기, 다운로드 속도, 파일 목록.
- `get-peers <BagID>` - 피어 목록을 출력합니다.
- `download-pause <BagID>`, `download-resume <BagID>` - 다운로드를 일시 중지하거나 재개합니다.
- `upload-pause <BagID>`, `upload-resume <BagID>` - 업로드를 일시 중지하거나 재개합니다.
- `remove <BagID>` - *Bag*을 제거합니다. `remove --remove-files`는 *Bag*의 모든 파일도 삭제합니다. *Bag*이 내부 스토리지 데몬 디렉토리에 저장된 경우 파일이 어떤 경우에도 삭제됩니다.

## 부분 다운로드, 우선순위

:::info
*Bag*을 추가할 때 다운로드할 파일을 지정할 수 있습니다:
:::

```
add-by-hash <hash> -d dir --partial file1 file2 file3
add-by-meta <meta-file> -d dir --partial file1 file2 file3
```

### 우선순위

*파일 가방*의 각 파일에는 0에서 255 사이의 우선순위 번호가 있습니다. 우선순위 0은 파일이 다운로드되지 않음을 의미합니다. `--partial` 플래그는 지정된 파일의 우선순위를 1로, 나머지는 0으로 설정합니다.

이미 추가된 *Bag*의 우선순위는 다음 명령으로 변경할 수 있습니다:

- `priority-all <BagID> <priority>` - 모든 파일에 대해.
- `priority-idx <BagID> <idx> <priority>` - 번호로 하나의 파일에 대해 (get 명령으로 확인).
- `priority-name <BagID> <name> <priority>` - 이름으로 하나의 파일에 대해.
  파일 목록이 다운로드되기 전에도 우선순위를 설정할 수 있습니다.

## 파일 가방 만들기

*Bag*을 만들고 배포를 시작하려면 `create` 명령을 사용합니다:

```
create <path>
```

`<path>`는 단일 파일이나 디렉토리를 가리킬 수 있습니다. *Bag*을 만들 때 설명을 지정할 수 있습니다:

```
create <path> -d "Bag of Files description"
```

*Bag*이 생성되면 콘솔에 자세한 정보가 표시되며(*Bag*을 식별하는 `BagID`인 해시 포함), 데몬이 토렌트 배포를 시작합니다. `create`의 추가 옵션:

- `--no-upload` - 데몬이 피어에게 파일을 배포하지 않습니다. 업로드는 `upload-resume`을 사용하여 시작할 수 있습니다.
- `--copy` - 파일이 스토리지 데몬의 내부 디렉토리에 복사됩니다.

다른 사용자가 *Bag*을 다운로드하려면 해시만 알면 됩니다. 토렌트 메타 파일도 저장할 수 있습니다:

```
get-meta <BagID> <meta-file>
```
