# 유지 관리 및 보안

## <a id="introduction"></a>소개

이 가이드는 TON 검증자 노드의 유지 관리 및 보안에 대한 몇 가지 기본 정보를 제공합니다.

이 문서는 **[TON 재단에서 권장하는](/participate/run-nodes/full-node)** 구성 및 도구를 사용하여 유효성 검사기를 설치한다고 가정하지만 일반적인 개념은 다른 시나리오에도 적용되며 숙련된 시스템 관리자에게도 유용할 수 있습니다.

## <a id="maintenance"></a>유지 관리

### <a id="database-grooming"></a>데이터베이스 그루밍

TON 노드/검증기는 `--db` 플래그가 지정한 경로(보통 `/var/ton-work/db`)에 데이터베이스를 보관하며, 이 디렉토리는 노드에서 생성 및 관리하지만 일부 아티팩트를 제거하기 위해 한 달에 한 번 데이터베이스 그루밍/정리 작업을 수행하는 것을 권장합니다.

**중요**: 아래 설명된 단계를 수행하기 전에 유효성 검사기 프로세스를 **중단**해야 하며, 그렇게 하지 않으면 데이터베이스가 손상될 수 있습니다.

이 절차는 완료하는 데 약 5분 정도 소요되며 서비스 중단을 일으키지 않습니다.

#### 루트로 전환

```sh
sudo -s
```

#### 유효성 검사기 서비스 중지

```sh
systemctl stop validator
```

#### 유효성 검사기가 실행되고 있지 않은지 확인

```sh
systemctl status validator
```

#### 데이터베이스 정리 수행

```sh
find /var/ton-work/db -name 'LOG.old*' -exec rm {} +
```

#### 유효성 검사기 서비스 시작

```sh
systemctl start validator
```

프로세스 및 로그를 분석하여 유효성 검사기 프로세스가 실행 중인지 확인합니다. 유효성 검사기는 몇 분 내에 네트워크와 다시 동기화되어야 합니다.

### <a id="backups"></a>백업

유효성 검사기를 백업하는 가장 쉽고 효율적인 방법은 중요한 노드 구성 파일, 키 및 mytonctrl 설정을 복사하는 것입니다:

- 노드 구성 파일: `/var/ton-work/db/config.json`
- 노드 개인 키링: `/var/ton-work/db/keyring`
- 노드 공개키: `/var/ton-work/keys`
- mytonctrl 구성 및 지갑: '$HOME/.local/share/myton\*`여기서 $HOME 은 mytonctrl 설치를 시작한 사용자의 홈 디렉터리 **또는**`/usr/local/bin/mytoncore\`를 루트로 설치한 경우입니다.

이 세트는 노드를 처음부터 복구하는 데 필요한 모든 것입니다.

#### 스냅샷

ZFS와 같은 최신 파일 시스템은 스냅샷 기능을 제공하며, 대부분의 클라우드 제공업체는 고객이 나중에 사용할 수 있도록 전체 디스크를 보존하는 컴퓨터의 스냅샷을 만들 수 있도록 허용합니다.

두 방법의 문제점은 스냅샷을 수행하기 전에 노드를 중지해야 하며, 그렇게 하지 않으면 예기치 않은 결과로 데이터베이스가 손상될 가능성이 높다는 것입니다. 또한 많은 클라우드 제공업체는 스냅샷을 수행하기 전에 컴퓨터의 전원을 꺼야 합니다.

이러한 정지는 자주 수행해서는 안 되며, 일주일에 한 번씩 노드를 스냅샷하면 복구 후 최악의 경우 일주일 전 데이터베이스가 있는 노드를 갖게 되고 노드가 네트워크를 따라잡는 데 시간이 더 걸리고 mytonctrl "덤프에서 설치" 기능(-d 플래그가 `install.sh` 스크립트 호출 중에 추가됨)을 사용하여 새로 설치하는 데 시간이 더 걸릴 수 있습니다.

### <a id="disaster-recovery"></a>재해 복구

새 머신에서 노드 복구를 수행하려면 다음과 같이 하세요:

#### mytonctrl/노드 설치

가장 빠른 노드 초기화를 위해 설치 스크립트 호출에 `-d` 스위치를 추가합니다.

#### 루트 사용자로 전환

```sh
sudo -s
```

#### 마이톤코어 및 유효성 검사기 프로세스 중지

```sh
systemctl stop validator
systemctl stop mytoncore
```

#### 백업된 노드 구성 파일 적용

- 노드 구성 파일: `/var/ton-work/db/config.json`
- 노드 개인 키링: `/var/ton-work/db/keyring`
- 노드 공개키: `/var/ton-work/keys`

#### <a id="set-node-ip"></a> 노드 IP 주소 설정

새 노드의 IP 주소가 다른 경우 노드 구성 파일 `/var/ton-work/db/config.json`을 편집하고 리프 `.addrs[0].ip`를 새 IP 주소의 **decimal** 표현으로 설정해야 합니다. 파이썬 스크립트 \*\*[this](https://github.com/sonofmom/ton-tools/blob/master/node/ip2dec.py)\*\*를 사용하여 IP를 십진수로 변환할 수 있습니다.

#### 적절한 데이터베이스 권한 확인

```sh
chown -R validator:validator /var/ton-work/db
```

#### 백업된 mytonctrl 구성 파일 적용하기

$HOME/.local/share/myton\*\`에서 $HOME 은 백업된 콘텐츠로 mytonctrl 설치를 시작한 사용자의 홈 디렉터리이며, 해당 사용자가 복사하는 모든 파일의 소유자인지 확인합니다.

#### 마이톤코어 및 유효성 검사기 프로세스 시작

```sh
systemctl start validator
systemctl start mytoncore
```

## <a id="security"></a>보안

### <a id="host-security"></a>호스트 수준 보안

호스트 수준의 보안은 이 문서의 범위를 벗어나는 방대한 주제이지만, 루트 사용자로 mytonctrl을 설치하지 말고 서비스 계정을 사용하여 권한 분리를 보장하는 것이 좋습니다.

### <a id="network-security"></a>네트워크 수준 보안

TON 검증자는 외부 위협으로부터 보호해야 하는 고가의 자산이므로, 가장 먼저 취해야 할 조치 중 하나는 노드를 최대한 보이지 않게 만드는 것인데, 이는 모든 네트워크 연결을 잠그는 것을 의미합니다. 검증자 노드에서는 노드 작동에 사용되는 UDP 포트만 인터넷에 노출되어야 합니다.

#### 도구

ufw](https://help.ubuntu.com/community/UFW)\*\* 방화벽 인터페이스와 **[jq](https://github.com/stedolan/jq)** JSON 명령줄 프로세서를 사용할 것입니다.

#### 관리 네트워크

노드 운영자는 머신에 대한 완전한 제어 및 액세스 권한을 유지해야 하며, 이를 위해서는 적어도 하나의 고정 IP 주소 또는 범위가 필요합니다.

또한 집/사무실에 고정 IP가 없는 경우 잠긴 머신에 액세스하거나 기본 IP 주소를 잃어버린 경우 보안 머신에 액세스할 수 있는 대체 방법을 추가하기 위해 고정 IP 주소가 있는 작은 "점프스테이션" VPS를 설정하는 것이 좋습니다.

#### ufw 및 jq1 설치

```sh
sudo apt install -y ufw jq
```

#### ufw 규칙 집합의 기본 잠금

```sh
sudo ufw default deny incoming; sudo ufw default allow outgoing
```

#### 자동 ICMP 에코 요청 수락 사용 안 함

```sh
sudo sed -i 's/-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/#-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/g' /etc/ufw/before.rules
```

#### 관리 네트워크에서 모든 액세스 활성화

```sh
sudo ufw insert 1 allow from <MANAGEMENT_NETWORK>
```

각 관리 네트워크/주소에 대해 위의 명령을 반복합니다.

#### 노드/검증자 UDP 포트를 공개에 노출하기

```sh
sudo ufw allow proto udp from any to any port `sudo jq -r '.addrs[0].port' /var/ton-work/db/config.json`
```

#### 관리 네트워크 재확인

<mark>중요</mark>: 방화벽을 활성화하기 전에 올바른 관리 주소를 추가했는지 다시 확인하세요!

#### ufw 방화벽 사용

```sh
sudo ufw enable
```

#### 상태 확인

방화벽 상태를 확인하려면 다음 명령을 사용하세요:

```sh
    sudo ufw status numbered
```

다음은 두 개의 관리 네트워크/주소가 있는 잠긴 노드의 출력 예시입니다:

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] Anywhere                   ALLOW IN    <MANAGEMENT_NETWORK_A>/28
[ 2] Anywhere                   ALLOW IN    <MANAGEMENT_NETWORK_B>/32
[ 3] <NODE_PORT>/udp            ALLOW IN    Anywhere
[ 4] <NODE_PORT>/udp (v6)       ALLOW IN    Anywhere (v6)
```

#### LiteServer 포트 노출

```sh
sudo ufw allow proto tcp from any to any port `sudo jq -r '.liteservers[0].port' /var/ton-work/db/config.json`
```

LiteServer 포트는 유효성 검사기에 공개적으로 노출되어서는 안 됩니다.

#### UFW에 대한 자세한 정보

디지털 오션의 훌륭한 \*\*[ufw 튜토리얼](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)\*\*에서 더 많은 ufw 마법을 확인하세요.

### <a id="ip-switch"></a>IP 스위치

노드가 공격을 받고 있다고 생각되면 IP 주소 전환을 고려해야 합니다. 전환 방법은 호스팅 제공업체에 따라 다르며, 두 번째 주소를 사전 주문하거나 **중단된** VM을 다른 인스턴스로 복제하거나 **[재해 복구](#재해 복구)** 프로세스를 수행하여 새 인스턴스를 설정할 수 있습니다.

어떤 경우든 노드 설정 파일에서 \*\*[새 IP 주소 설정](#set-node-ip)\*\*을 하시기 바랍니다!
