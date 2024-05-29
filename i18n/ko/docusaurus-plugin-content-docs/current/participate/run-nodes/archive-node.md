# 아카이브 노드 실행

## 개요

:::caution 시스템 관리자 필요
노드를 실행하려면 Linux/Ubuntu 시스템 관리에 대한 기본 지식이 필요합니다.
:::

아카이브 노드는 블록체인의 확장된 기록 데이터를 저장하는 [풀 노드](/참여/실행 노드/풀 노드)의 한 유형입니다. 기록 데이터에 액세스해야 하는 블록체인 탐색기 또는 유사한 애플리케이션을 만드는 경우, 아카이브 노드를 인덱서로 사용하는 것이 좋습니다.

## 전제 조건

지원되는 운영 체제를 사용하여 mytonctrl을 설치할 것을 적극 권장합니다:

- 우분투 20.04
- 우분투 22.04
- Debian 11

sudo 권한이 있는 루트 사용자가 아닌 사용자](/참여/실행 노드/전체 노드#전제 조건-1)로 mytonctrl을 설치 및 실행하세요.

## 하드웨어 요구 사항

- 16 x 코어 CPU
- 128GB ECC 메모리
- 4TB SSD *또는* 프로비저닝된 32+k IOPS 스토리지
- 1Gbit/s 네트워크 연결
- 최대 부하 시 월 16TB/월 트래픽
- 공인 IP 주소(고정 IP 주소)

__Note__4TB는 압축이 활성화된 상태에서 zfs 볼륨을 사용한다고 가정합니다.

## 설치

일반적으로 아카이브 노드를 실행하려면 다음 단계가 필요합니다:

1. ZFS 설치 및 볼륨 준비
2. MyTonCtrl 설치
3. 서버에서 전체 노드를 실행하고 유효성 검사기 프로세스를 중지합니다.
4. https://archival-dump.ton.org 에서 덤프 데이터 다운로드 및 복원
5. 아카이브 노드에 대한 DB 사양 구성으로 전체 노드 실행

### ZFS 설치 및 볼륨 준비

덤프는 plzip을 사용하여 압축된 ZFS 스냅샷의 형태로 제공되며, 호스트에 zfs를 설치하고 덤프를 복원해야 합니다. 자세한 내용은 [Oracle 문서](https://docs.oracle.com/cd/E23824_01/html/821-1448/gavvx.html#scrolltoc)를 참조하세요.

일반적으로 _전용 SSD 드라이브_에 노드를 위한 별도의 ZFS 풀을 생성하는 것이 좋은데, 이렇게 하면 저장 공간을 쉽게 관리하고 노드를 백업할 수 있습니다.

1. zfs](https://ubuntu.com/tutorials/setup-zfs-storage-pool#1-overview) 설치

```shell
sudo apt install zfsutils-linux
```

2. 전용 4TB `<disk>`에 [풀 생성](https://ubuntu.com/tutorials/setup-zfs-storage-pool#3-creating-a-zfs-pool)을 하고 이름을 '데이터'로 지정합니다.

```shell
sudo zpool create data <disk>
```

3. 복원하기 전에 상위 ZFS 파일 시스템에서 압축을 활성화하는 것이 좋습니다. 이렇게 하면 [많은 공간]을 절약할 수 있습니다(https://www.servethehome.com/the-case-for-using-zfs-compression/). '데이터' 볼륨에 압축을 사용하려면 루트 계정을 사용하여 입력합니다:

```shell
sudo zfs set compression=lz4 data
```

### MyTonCtrl 설치

실행 중인 전체 노드](/participate/run-nodes/full-node)를 사용하여 mytonctrl을 설치하세요.

### 아카이브 노드 실행

#### 노드 준비

1. 복원을 수행하기 전에 루트 계정을 사용하여 유효성 검사기를 중지해야 합니다:

```shell
sudo -s
systemctl stop validator.service
```

2. ton-work` 구성 파일을 백업합니다(`/var/ton-work/db/config.json`, `/var/ton-work/keys`, `/var/ton-work/db/keyring\`이 필요합니다).

```shell
mv /var/ton-work /var/ton-work.bak
```

#### 덤프 다운로드

1. 사용자`및`비밀번호\` 자격 증명을 요청하여 [@TONBaseChatEn](https://t.me/TONBaseChatEn) 텔레그램 채팅에서 덤프 다운로드에 대한 액세스 권한을 얻으세요.
2. 다음은 ton.org 서버에서 덤프를 다운로드하고 복원하는 명령어 예시입니다:

```shell
wget --user <usr> --password <pwd> -c https://archival-dump.ton.org/dumps/latest.zfs.lz | pv | plzip -d -n <cores> | zfs recv data/ton-work
```

덤프의 크기는 __~1.5TB__이므로 다운로드하고 복원하는 데 다소 시간이 걸립니다.

명령을 준비하고 실행합니다:

1. 필요한 경우 도구 설치(`pv`, `plzip`)
2. `<usr>`및`<pwd>\`를 자격 증명으로 바꿉니다.
3. 추출 속도를 높이기 위해 컴퓨터가 허용하는 만큼의 코어를 사용하도록 `plzip`에게 지시합니다(`-n`).

#### 덤프 마운트

1. zfs를 마운트합니다:

```shell
zfs set mountpoint=/var/ton-work data/ton-work && zfs mount data/ton-work
```

2. 백업에서 `db/config.json`, `keys` 및 `db/keyring`을 `/var/ton-work`로 복원합니다.

```shell
cp /var/ton-work.bak/db/config.json /var/ton-work/db/config.json
cp -r /var/ton-work.bak/keys /var/ton-work/keys
cp -r /var/ton-work.bak/db/keyring /var/ton-work/db/keyring
```

3. 변/톤작업`및`/변/톤작업/키\` 디렉터리에 대한 권한이 올바르게 승격되었는지 확인하세요:

- var/ton-work/db`디렉터리의 소유자는`validator\` 사용자여야 합니다:

```shell
chown -R validator:validator /var/ton-work/db
```

- var/ton-work/keys`디렉터리의 소유자는`ubuntu\` 사용자이어야 합니다:

```shell
chown -R ubuntu:ubuntu /var/ton-work/keys
```

#### 구성 업데이트

아카이브 노드에 대한 노드 구성을 업데이트합니다.

1. 노드 구성 파일 `/etc/systemd/system/validator.service`를 엽니다.

```shell
nano /etc/systemd/system/validator.service
```

2. 실행 시작\` 줄에 노드에 대한 스토리지 설정을 추가합니다:

```shell
--state-ttl 315360000 --archive-ttl 315360000 --block-ttl 315360000
```

:::info
노드를 시작하고 로그를 관찰하는 동안 조금만 기다려주세요. 덤프는 DHT 캐시 없이 제공되므로 노드가 다른 노드를 찾아서 동기화하는 데 시간이 걸립니다. 스냅샷의 오래된 버전에 따라 노드가 네트워크를 따라잡는 데 몇 시간에서 며칠이 걸릴 수 있습니다. 이는 정상적인 현상입니다.
:::

#### 노드 시작

1. 명령을 실행하여 유효성 검사기를 시작합니다:

```shell
systemctl start validator.service
```

2. 로컬 사용자_에서 `mytonctrl`을 열고 `status`를 사용하여 노드 상태를 확인합니다.

## 노드 유지 관리

노드 데이터베이스를 수시로 정리해야 하며(일주일에 한 번 권장), 정리하려면 루트 권한으로 다음 단계를 수행하세요:

1. 유효성 검사기 프로세스 중지 (절대 건너뛰지 마세요!)

```shell
sudo -s
systemctl stop validator.service
```

2. 오래된 로그 제거

```shell
find /var/ton-work -name 'LOG.old*' -exec rm {} +
```

4. 임시 파일 제거

```shell
rm -r /var/ton-work/db/files/packages/temp.archive.*
```

5. 유효성 검사기 프로세스 시작

```shell
systemctl start validator.service
```

## 문제 해결 및 백업

어떤 이유로 작동하지 않거나 중단되는 경우 언제든지 ZFS 파일 시스템의 @archstate 스냅샷으로 [롤백](https://docs.oracle.com/cd/E23824_01/html/821-1448/gbciq.html#gbcxk)하면 덤프의 원래 상태가 됩니다.

1. 유효성 검사기 프로세스 중지 (절대 건너뛰지 마세요!)

```shell
sudo -s
systemctl stop validator.service
```

2. 스냅샷 이름 확인

```shell
zfs list -t snapshot
```

3. 스냅샷으로 롤백

```shell
zfs rollback data/ton-work@dumpstate
```

노드가 잘 작동한다면 이 스냅샷을 제거하여 저장 공간을 절약할 수 있지만, 경우에 따라 유효성 검사기 노드가 config.json뿐만 아니라 데이터를 손상시키는 것으로 알려져 있으므로 롤백 목적으로 파일 시스템을 정기적으로 스냅샷하는 것이 좋습니다. [zfsnap](https://www.zfsnap.org/docs.html)은 스냅샷 로테이션을 자동화할 수 있는 좋은 도구입니다.

:::tip 도움이 필요하신가요?
질문이 있거나 도움이 필요하신가요? TON 개발자 채팅](https://t.me/tondev_eng)에서 질문하여 커뮤니티의 도움을 받으세요. MyTonCtrl 개발자들도 그곳에 모여 있습니다.
:::

## 참고 항목

- [TON 노드 유형](/참여/노드/노드 유형)
- [전체 노드 실행](/참여/런-노드/풀-노드)
