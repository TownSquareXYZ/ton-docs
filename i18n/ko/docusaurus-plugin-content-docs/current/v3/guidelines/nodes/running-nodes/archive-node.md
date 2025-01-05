# 아카이브 노드

:::info
이 문서를 읽기 전에 [전체 노드](/v3/guidelines/nodes/running-nodes/full-node)에 대해 먼저 읽어보세요
:::

## 개요

아카이브 노드는 블록체인의 확장된 과거 데이터를 저장하는 전체 노드의 한 유형입니다. 블록체인 탐색기나 과거 데이터에 대한 접근이 필요한 유사한 애플리케이션을 만드는 경우, 인덱서로 아카이브 노드를 사용하는 것이 권장됩니다.

## OS 요구사항

다음과 같은 지원되는 운영 체제에서 mytonctrl을 설치할 것을 강력히 권장합니다:

- Ubuntu 20.04
- Ubuntu 22.04
- Debian 11

## 하드웨어 요구사항

- 16 코어 CPU
- 128GB ECC 메모리
- 9TB SSD *또는* 64k+ IOPS 프로비저닝된 스토리지
- 1 Gbit/s 네트워크 연결
- 최대 부하 시 월 16 TB 트래픽
- 공인 IP 주소(고정 IP 주소)

:::info 데이터 압축
압축되지 않은 데이터의 경우 9TB가 필요합니다. 6TB는 압축이 활성화된 ZFS 볼륨을 사용하는 경우입니다.
2024년 11월 기준으로 데이터 볼륨은 매월 약 0.5TB와 0.25TB씩 증가합니다.
:::

## 설치

### ZFS 설치 및 볼륨 준비

덤프는 plzip으로 압축된 ZFS 스냅샷 형태로 제공됩니다. 호스트에 zfs를 설치하고 덤프를 복원해야 합니다. 자세한 내용은 [Oracle 문서](https://docs.oracle.com/cd/E23824_01/html/821-1448/gavvx.html#scrolltoc)를 참조하세요.

일반적으로 _전용 SSD 드라이브_에 노드를 위한 별도의 ZFS 풀을 만드는 것이 좋습니다. 이를 통해 저장 공간을 쉽게 관리하고 노드를 백업할 수 있습니다.

1. [zfs](https://ubuntu.com/tutorials/setup-zfs-storage-pool#1-overview) 설치

```shell
sudo apt install zfsutils-linux
```

2. 전용 4TB `<disk>`에 `data`라는 이름으로 [풀 생성](https://ubuntu.com/tutorials/setup-zfs-storage-pool#3-creating-a-zfs-pool)

```shell
sudo zpool create data <disk>
```

3. 복원하기 전에 상위 ZFS 파일시스템에서 압축을 활성화할 것을 강력히 권장합니다. 이렇게 하면 [많은 공간](https://www.servethehome.com/the-case-for-using-zfs-compression/)을 절약할 수 있습니다. root 계정을 사용하여 `data` 볼륨의 압축을 활성화하려면:

```shell
sudo zfs set compression=lz4 data
```

### MyTonCtrl 설치

mytonctrl을 **설치**하고 **실행**하려면 [전체 노드 실행하기](/v3/guidelines/nodes/running-nodes/full-node)를 참조하세요.

### 아카이브 노드 실행

#### 노드 준비

1. 복원을 수행하기 전에 root 계정을 사용하여 validator를 중지해야 합니다:

```shell
sudo -s
systemctl stop validator.service
```

2. `ton-work` 설정 파일의 백업을 만듭니다(`/var/ton-work/db/config.json`, `/var/ton-work/keys`, `/var/ton-work/db/keyring`가 필요합니다).

```shell
mv /var/ton-work /var/ton-work.bak
```

#### 덤프 다운로드

1. 덤프 다운로드 접근 권한을 얻기 위해 [@TONBaseChatEn](https://t.me/TONBaseChatEn) 텔레그램 채팅에서 `user`와 `password` 자격 증명을 요청하세요.
2. ton.org 서버에서 **메인넷** 덤프를 다운로드하고 복원하는 예제 명령입니다:

```shell
wget --user <usr> --password <pwd> -c https://archival-dump.ton.org/dumps/latest.zfs.lz | pv | plzip -d -n <cores> | zfs recv data/ton-work
```

**테스트넷** 덤프를 설치하려면:

```shell
wget --user <usr> --password <pwd> -c https://archival-dump.ton.org/dumps/latest_testnet.zfs.lz | pv | plzip -d -n <cores> | zfs recv data/ton-work
```

덤프 크기는 약 __4TB__이므로 다운로드하고 복원하는데 며칠(최대 4일)이 걸릴 수 있습니다. 네트워크가 성장함에 따라 덤프 크기가 증가할 수 있습니다.

명령을 준비하고 실행하세요:

1. 필요한 경우 도구(`pv`, `plzip`) 설치
2. `<usr>`와 `<pwd>`를 자격 증명으로 교체
3. `plzip`에게 추출 속도를 높이기 위해 시스템이 허용하는 만큼의 코어를 사용하도록 지시(`-n`)

#### 덤프 마운트

1. zfs 마운트:

```shell
zfs set mountpoint=/var/ton-work data/ton-work && zfs mount data/ton-work
```

2. `/var/ton-work`에 백업에서 `db/config.json`, `keys`, `db/keyring` 복원

```shell
cp /var/ton-work.bak/db/config.json /var/ton-work/db/config.json
cp -r /var/ton-work.bak/keys /var/ton-work/keys
cp -r /var/ton-work.bak/db/keyring /var/ton-work/db/keyring
```

3. `/var/ton-work`와 `/var/ton-work/keys` 디렉토리의 권한이 올바르게 설정되었는지 확인:

- `/var/ton-work/db` 디렉토리의 소유자는 `validator` 사용자여야 합니다:

```shell
chown -R validator:validator /var/ton-work/db
```

- `/var/ton-work/keys` 디렉토리의 소유자는 `ubuntu` 사용자여야 합니다:

```shell
chown -R ubuntu:ubuntu /var/ton-work/keys
```

#### 설정 업데이트

아카이브 노드를 위한 노드 설정을 업데이트합니다.

1. `/etc/systemd/system/validator.service` 노드 설정 파일 열기

```shell
nano /etc/systemd/system/validator.service
```

2. `ExecStart` 줄에 노드의 스토리지 설정 추가:

```shell
--state-ttl 315360000 --archive-ttl 315360000 --block-ttl 315360000
```

:::info
노드를 시작하고 로그를 관찰할 때 인내심을 가지세요.
덤프는 DHT 캐시 없이 제공되므로, 노드가 다른 노드를 찾고 동기화하는 데 시간이 걸립니다.
스냅샷의 나이와 인터넷 연결 속도에 따라,
노드가 네트워크를 따라잡는 데 **몇 시간에서 며칠**이 걸릴 수 있습니다.
**최소 설정에서는 이 과정이 최대 5일까지 걸릴 수 있습니다.**
이는 정상적인 현상입니다.
:::

:::caution
노드 동기화 과정이 이미 5일이 지났지만 여전히 동기화되지 않은 경우,
[문제 해결 섹션](/v3/guidelines/nodes/nodes-troubleshooting#archive-node-is-out-of-sync-even-after-5-days-of-the-syncing-process)을 확인해야 합니다.
:::

#### 노드 시작

1. 다음 명령을 실행하여 validator 시작:

```shell
systemctl start validator.service
```

2. _로컬 사용자_로 `mytonctrl`을 열고 `status`를 사용하여 노드 상태를 확인합니다.

## 노드 유지관리

노드 데이터베이스는 주기적으로(주 1회 권장) 정리가 필요합니다. root로 다음 단계를 수행하세요:

1. validator 프로세스 중지(절대 건너뛰지 마세요!)

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

5. validator 프로세스 시작

```shell
systemctl start validator.service
```

## 문제 해결 및 백업

어떤 이유로든 작동하지 않거나 문제가 발생하면 ZFS 파일시스템에서 @archstate 스냅샷으로 [롤백](https://docs.oracle.com/cd/E23824_01/html/821-1448/gbciq.html#gbcxk)할 수 있습니다. 이는 덤프의 원래 상태입니다.

1. validator 프로세스 중지(**절대 건너뛰지 마세요!**)

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

노드가 잘 작동하면 저장 공간을 절약하기 위해 이 스냅샷을 제거할 수 있지만, validator 노드가 일부 경우에 데이터와 config.json을 손상시킬 수 있으므로 롤백을 위해 파일시스템을 정기적으로 스냅샷하는 것을 권장합니다. [zfsnap](https://www.zfsnap.org/docs.html)은 스냅샷 회전을 자동화하는 좋은 도구입니다.

:::tip 도움이 필요하신가요?
질문이 있거나 도움이 필요하신가요? 커뮤니티의 도움을 받으려면 [TON dev 채팅](https://t.me/tondev_eng)에서 질문하세요. MyTonCtrl 개발자들도 그곳에 있습니다.
:::

## 팁 & 트릭

### 아카이브 노드가 블록을 저장하지 않도록 강제하기

노드가 아카이브 블록을 저장하지 않도록 강제하려면 86400 값을 사용하세요. 자세한 내용은 [set_node_argument 섹션](/v3/documentation/infra/nodes/mytonctrl/mytonctrl-overview#set_node_argument)을 확인하세요.

```bash
installer set_node_argument --archive-ttl 86400
```

## 지원

[@mytonctrl_help](https://t.me/mytonctrl_help)에서 기술 지원을 받으세요.

## 참고 자료

- [TON 노드 유형](/v3/documentation/infra/nodes/node-types)
- [전체 노드 실행하기](/v3/guidelines/nodes/running-nodes/full-node)
