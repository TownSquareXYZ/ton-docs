# Docker에서 MyTonCtrl 실행하기

## 하드웨어 요구사항:

- 16 코어 CPU
- 128GB RAM
- 1TB NVME SSD 또는 64k+ IOPS 프로비저닝된 스토리지
- 1 Gbit/s 네트워크 연결
- 공인 IP 주소(고정 IP)
- 최대 부하시 월 16TB 트래픽

***권장하지 않음!*** ***테스트 목적으로만 사용!***

**IGNORE_MINIMAL_REQS=true** 변수로 CPU/RAM 요구사항 검증을 끌 수 있습니다.

## 소프트웨어 요구사항:

- docker-ce
- docker-ce-cli
- containerd.io
- docker-buildx-plugin
- docker-compose-plugin

  *공식 [Docker](https://docs.docker.com/engine/install/) 설치 가이드 참조*

## 테스트된 운영체제:

- Ubuntu 20.04
- Ubuntu 22.04
- Ubuntu 24.04
- Debian 11
- Debian 12

## 공식 도커 이미지로 MyTonCtrl v2 실행:

- 이미지를 받고 MyTonCtrl이 있는 노드 실행

````bash
docker run -d --name ton-node -v <YOUR_LOCAL_FOLDER>:/var/ton-work -it ghcr.io/ton-blockchain/ton-docker-ctrl:latest


## Install and start MyTonCtrl from sources:

1. Clone the last version of the repository
```bash
git clone https://github.com/ton-blockchain/ton-docker-ctrl.git
````

2. 디렉토리로 이동

```bash
cd ./ton-docker-ctrl
```

3. .env 파일에 필요한 값 지정

```bash
vi .env
```

4. 도커 이미지 조립 시작. 이 단계에서는 fift, validator-engine, lite-client 등의 최신 버전 컴파일과 MyTonCtrl 설치 및 초기 설정이 포함됩니다.

```bash
docker compose build ton-node
```

5. MyTonCtrl 시작

```bash
docker compose up -d
```

## 비Docker 전체노드 또는 validator를 도커화된 MyTonCtrl v2로 마이그레이션

TON 바이너리와 소스의 경로, TON 작업 디렉토리 경로, 그리고 가장 중요한 MyTonCtrl 설정과 지갑의 경로를 지정하세요.

```bash
docker run -d --name ton-node --restart always \
-v <EXISTING_TON_WORK_FOLDER>:/var/ton-work \
-v /usr/bin/ton:/usr/bin/ton \
-v /usr/src/ton:/usr/src/ton \
-v /home/<USER>/.local/share:/usr/local/bin \
ghcr.io/ton-blockchain/ton-docker-ctrl:latest
```

## 변수 설정:

.env 파일에 지정된 변수들

- **GLOBAL_CONFIG_URL** - TON 블록체인의 네트워크 설정(기본값: [Testnet](https://ton.org/testnet-global.config.json))
- **MYTONCTRL_VERSION** - MyTonCtrl이 조립된 Git 브랜치
- **TELEMETRY** - 텔레메트리 활성화/비활성화
- **MODE** - 지정된 모드로 MyTonCtrl 설정(validator 또는 liteserver)
- **IGNORE_MINIMAL_REQS** - 하드웨어 요구사항 무시

## 변수 설정:

1. 컨테이너 중지

```bash
docker compose stop
```

2. 컨테이너 삭제

```bash
docker compose down
```

3. 데이터와 함께 컨테이너 삭제

```bash
docker compose down --volumes
```

## MyTonCtrl 연결:

```bash
docker compose exec -it ton-node bash -c "mytonctrl"
```

연결되면 `status` 명령으로 상태를 확인할 수 있습니다

```bash
MyTonCtrl> status
```

![](https://raw.githubusercontent.com/ton-blockchain/mytonctrl/master/screens/mytonctrl-status.png)

`help` 명령으로 사용 가능한 명령어 목록 확인

```bash
MyTonCtrl> help
```

## MyTonCtrl 로그 확인:

```bash
docker compose logs
```

## MyTonCtrl 및 TON 업데이트:

TON validator와 MyTonCtrl의 최신 버전을 받으려면 docker-compose.yml이 있는 디렉토리로 이동하여 조립해야 합니다

```bash
cd ./ton-docker-ctrl
docker compose build ton-node
```

완료되면 Docker Compose를 다시 시작

```bash
docker compose up -d
```

MyTonCtrl에 연결하면 자동으로 업데이트를 확인합니다. 업데이트가 감지되면 "*MyTonCtrl 업데이트 가능. `update` 명령으로 업데이트하세요.*" 메시지가 표시됩니다.

업데이트는 필요한 브랜치를 지정하여 update 명령으로 수행

```bash
MyTonCtrl> update mytonctrl2
```

## 데이터 저장 경로 변경:

기본적으로 TON과 Mytoncore 작업은 \*\*/var/lib/docker/volumes/\*\*에 저장됩니다

docker-compose.yml 파일의 **volumes** 섹션에서 원하는 경로를 지정하여 변경할 수 있습니다
