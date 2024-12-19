# 유지관리 및 보안

## <a id="introduction"></a>소개

이 가이드는 TON Validator 노드의 유지관리와 보안에 대한 기본 정보를 제공합니다.

이 문서는 validator가 **[TON Foundation이 권장하는](/v3/guidelines/nodes/running-nodes/full-node)** 구성과 도구를 사용하여 설치되었다고 가정하지만, 일반적인 개념은 다른 시나리오에도 적용되며 시스템 관리자에게 유용할 수 있습니다.

## <a id="maintenance"></a>유지관리

### <a id="database-grooming"></a>데이터베이스 관리

TON Node는 `validator-engine`의 `--db` 플래그로 지정된 경로(일반적으로 `/var/ton-work/db`)에 데이터베이스를 유지합니다. 데이터베이스 크기를 줄이기 위해 저장된 데이터의 TTL(time-to-live)을 줄일 수 있습니다.

현재 TTL 값은 노드 서비스 파일(기본 경로는 `/etc/systemd/system/validator.service`)에서 찾을 수 있습니다. MyTonCtrl을 사용하는 경우 `installer status` 명령을 사용할 수 있습니다. 일부 값이 설정되지 않은 경우 기본값이 사용됩니다.

### archive-ttl

`archive-ttl`은 블록의 수명을 정의하는 매개변수입니다. 기본값은 604800초(7일)입니다. 데이터베이스 크기를 줄이기 위해 이 값을 줄일 수 있습니다.

```bash
MyTonCtrl> installer set_node_argument --archive-ttl <value>
```

MyTonCtrl을 사용하지 않는 경우 노드 서비스 파일을 편집할 수 있습니다.

### state-ttl

`state-ttl`은 블록 상태의 수명을 정의하는 매개변수입니다. 기본값은 86400초(24시간)입니다. 데이터베이스 크기를 줄이기 위해 이 값을 줄일 수 있지만, validator의 경우 기본값을 사용하는 것이 매우 권장됩니다(플래그를 설정하지 않음).
또한 이 값은 검증 기간 길이보다 커야 합니다([15번 설정 매개변수](https://docs.ton.org/v3/documentation/network/configs/blockchain-configs#param-15)에서 값을 찾을 수 있음).

```bash
MyTonCtrl> installer set_node_argument --state-ttl <value>
```

MyTonCtrl을 사용하지 않는 경우 노드 서비스 파일을 편집할 수 있습니다.

### <a id="backups"></a>백업

validator를 백업하는 가장 쉽고 효율적인 방법은 중요한 노드 구성 파일, 키 및 mytonctrl 설정을 복사하는 것입니다:

- 노드 구성 파일: `/var/ton-work/db/config.json`
- 노드 개인 키링: `/var/ton-work/db/keyring`
- 노드 공개 키: `/var/ton-work/keys`
- mytonctrl 구성 및 지갑: `$HOME/.local/share/myton*` ($HOME은 mytonctrl 설치를 시작한 사용자의 홈 디렉토리) **또는** root로 mytonctrl을 설치한 경우 `/usr/local/bin/mytoncore`

이 세트는 노드를 처음부터 복구하는데 필요한 모든 것입니다.

#### 스냅샷

ZFS와 같은 현대적인 파일 시스템은 스냅샷 기능을 제공하며, 대부분의 클라우드 제공업체도 고객이 나중에 사용할 수 있도록 전체 디스크가 보존되는 동안 기계의 스냅샷을 만들 수 있게 합니다.

두 방법 모두의 문제는 스냅샷을 수행하기 전에 노드를 중지해야 한다는 것입니다. 그렇지 않으면 예기치 않은 결과를 초래하는 손상된 데이터베이스가 생길 가능성이 높습니다. 많은 클라우드 제공업체는 스냅샷을 수행하기 전에 기계의 전원을 꺼야 합니다.

이러한 중지는 자주 수행해서는 안 됩니다. 일주일에 한 번 노드의 스냅샷을 만드는 경우 최악의 시나리오에서 복구 후 일주일 된 데이터베이스가 있는 노드를 갖게 되며, mytonctrl의 "덤프에서 설치" 기능(`install.sh` 스크립트 실행 시 추가된 -d 플래그)을 사용하여 새 설치를 수행하는 것보다 네트워크를 따라잡는 데 더 많은 시간이 걸릴 것입니다.

### <a id="disaster-recovery"></a>재해 복구

새 기계에서 노드 복구를 수행하려면:

#### mytonctrl / 노드 설치

가장 빠른 노드 초기화를 위해 설치 스크립트 실행에 `-d` 스위치를 추가하세요.

#### root 사용자로 전환

```sh
sudo -s
```

#### mytoncore 및 validator 프로세스 중지

```sh
systemctl stop validator
systemctl stop mytoncore
```

#### 백업된 노드 구성 파일 적용

- 노드 구성 파일: `/var/ton-work/db/config.json`
- 노드 개인 키링: `/var/ton-work/db/keyring`
- 노드 공개 키: `/var/ton-work/keys`

#### <a id="set-node-ip"></a> 노드 IP 주소 설정

새 노드의 IP 주소가 다른 경우 노드 구성 파일 `/var/ton-work/db/config.json`을 편집하고 `.addrs[0].ip` 리프를 새 IP 주소의 **10진수** 표현으로 설정해야 합니다. **[이](https://github.com/sonofmom/ton-tools/blob/master/node/ip2dec.py)** 파이썬 스크립트를 사용하여 IP를 10진수로 변환할 수 있습니다.

#### 적절한 데이터베이스 권한 확인

```sh
chown -R validator:validator /var/ton-work/db
```

#### 백업된 mytonctrl 구성 파일 적용

mytonctrl 설치를 시작한 사용자의 홈 디렉토리인 `$HOME/.local/share/myton*`을 백업된 내용으로 교체하고, 복사하는 모든 파일의 소유자가 해당 사용자인지 확인하세요.

#### mytoncore 및 validator 프로세스 시작

```sh
systemctl start validator
systemctl start mytoncore
```

## <a id="security"></a>보안

### <a id="host-security"></a>호스트 수준 보안

호스트 수준 보안은 이 문서의 범위를 벗어나는 큰 주제이지만, root 사용자로 mytonctrl을 설치하지 말고 권한 분리를 위해 서비스 계정을 사용하는 것을 권장합니다.

### <a id="network-security"></a>네트워크 수준 보안

TON Validator는 외부 위협으로부터 보호해야 하는 고가치 자산입니다. 첫 번째 단계 중 하나는 노드를 가능한 한 보이지 않게 만드는 것입니다. 이는 모든 네트워크 연결을 잠그는 것을 의미합니다. validator 노드에서는 노드 운영에 사용되는 UDP 포트만 인터넷에 노출되어야 합니다.

#### 도구

**[ufw](https://help.ubuntu.com/community/UFW)** 방화벽 인터페이스와 **[jq](https://github.com/stedolan/jq)** JSON 명령줄 프로세서를 사용할 것입니다.

#### 관리 네트워크

노드 운영자로서 기계에 대한 완전한 제어 권한과 접근 권한을 유지해야 합니다. 이를 위해서는 최소한 하나의 고정 IP 주소나 범위가 필요합니다.

또한 고정 IP가 있는 작은 "점프스테이션" VPS를 설정하여 집/사무실에 고정 IP가 없는 경우 잠긴 기계에 접근하거나 기본 IP 주소를 잃어버린 경우 보안 기계에 접근할 수 있는 대체 방법을 추가하는 것을 권장합니다.

#### ufw와 jq 설치

```sh
sudo apt install -y ufw jq
```

#### ufw 룰셋의 기본 잠금

```sh
sudo ufw default deny incoming; sudo ufw default allow outgoing
```

#### 자동 ICMP 에코 요청 수락 비활성화

```sh
sudo sed -i 's/-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/#-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/g' /etc/ufw/before.rules
```

#### 관리 네트워크에서 모든 접근 허용

```sh
sudo ufw insert 1 allow from <MANAGEMENT_NETWORK>
```

각 관리 네트워크/주소에 대해 위 명령을 반복하세요.

#### 노드/validator UDP 포트를 공개적으로 노출

```sh
sudo ufw allow proto udp from any to any port `sudo jq -r '.addrs[0].port' /var/ton-work/db/config.json`
```

#### 관리 네트워크 재확인

<mark>중요</mark>: 방화벽을 활성화하기 전에 올바른 관리 주소를 추가했는지 다시 확인하세요!

#### ufw 방화벽 활성화

```sh
sudo ufw enable
```

#### 상태 확인

방화벽 상태를 확인하려면 다음 명령을 사용하세요:

```sh
    sudo ufw status numbered
```

두 개의 관리 네트워크/주소가 있는 잠긴 노드의 출력 예시:

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

validator에서는 LiteServer 포트를 공개적으로 노출하면 안 됩니다.

#### UFW에 대한 자세한 정보

더 많은 ufw 마법을 알아보려면 Digital Ocean의 이 훌륭한 \*\*[ufw 튜토리얼](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)\*\*을 참조하세요.

### <a id="ip-switch"></a>IP 전환

노드가 공격을 받고 있다고 생각되면 IP 주소 전환을 고려해야 합니다. 전환을 달성하는 방법은 호스팅 제공업체에 따라 다릅니다. 두 번째 주소를 미리 주문하거나, **중지된** VM을 다른 인스턴스로 복제하거나, **[재해 복구](#disaster-recovery)** 프로세스를 수행하여 새 인스턴스를 설정할 수 있습니다.

어떤 경우든 노드 구성 파일에서 \*\*[새 IP 주소를 설정](/v3/guidelines/nodes/node-maintenance-and-security#-set-node-ip-address)\*\*했는지 확인하세요!
