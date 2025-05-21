# 노드를 위한 보안 가이드라인

블록체인이나 분산 시스템과 같은 탈중앙화 네트워크에서 노드의 보안을 확보하는 것은 데이터의 무결성, 기밀성, 가용성을 유지하는데 매우 중요합니다. 노드 보안 가이드라인은 네트워크 통신부터 하드웨어 및 소프트웨어 구성까지 다양한 계층을 다뤄야 합니다. 다음은 노드를 위한 보안 가이드라인입니다:

### 1. 서버는 TON 노드 실행용으로만 사용

- 서버를 다른 작업에 사용하는 것은 잠재적인 보안 위험을 초래합니다

### 2. 정기적인 업데이트 및 패치

- 시스템이 항상 최신 보안 패치로 업데이트되어 있는지 확인하세요.
- apt(Debian/Ubuntu용) 또는 yum/dnf(CentOS/Fedora용)와 같은 패키지 관리 도구를 사용하여 정기적으로 업데이트하세요:

```bash
sudo apt update && sudo apt upgrade -y
```

- 무인 업그레이드를 활성화하여 보안 업데이트를 자동화하는 것을 고려하세요.

### 3. 강력한 SSH 구성 사용

- Root 로그인 비활성화: SSH를 통한 root 접근을 방지하세요. /etc/ssh/sshd_config 파일을 편집하세요:

```bash
PermitRootLogin no
```

- SSH 키 사용: 비밀번호 인증을 피하고 대신 SSH 키를 사용하세요.

```bash
PasswordAuthentication no
```

- 기본 SSH 포트 변경: SSH를 비표준 포트로 이동하면 자동화된 무차별 대입 공격을 줄일 수 있습니다. 예:

```bash
Port 2222
```

- SSH 접근 제한: 방화벽 규칙을 사용하여 신뢰할 수 있는 IP에서만 SSH를 허용하세요

### 4. 방화벽 구현

- 필요한 서비스만 허용하도록 방화벽을 구성하세요. 일반적인 도구로는 ufw(Uncomplicated Firewall) 또는 iptables가 있습니다:

```bash
sudo ufw allow 22/tcp   # Allow SSH
sudo ufw allow 80/tcp   # Allow HTTP
sudo ufw allow 443/tcp  # Allow HTTPS
sudo ufw enable         # Enable firewall
```

### 5. 로그 모니터링

- 의심스러운 활동을 식별하기 위해 시스템 로그를 정기적으로 모니터링하세요:
   - */var/log/auth.log* (인증 시도용)
   - */var/log/syslog* 또는 */var/log/messages*
- 중앙 집중식 로깅 고려

### 6. 사용자 권한 제한

- 신뢰할 수 있는 사용자에게만 root 또는 sudo 권한을 제공하세요. sudo 명령을 주의해서 사용하고 접근을 최소화하기 위해 _/etc/sudoers_를 감사하세요.
- 정기적으로 사용자 계정을 검토하고 불필요하거나 비활성 사용자를 제거하세요.

### 7. SELinux 또는 AppArmor 구성

- **SELinux**(RHEL/CentOS용)와 **AppArmor**(Ubuntu/Debian용)는 프로그램이 특정 시스템 리소스에 접근하는 것을 제한함으로써 추가적인 보안 계층을 제공하는 필수 접근 제어를 제공합니다.

### 8. 보안 도구 설치

- Lynis와 같은 도구를 사용하여 정기적인 보안 감사를 수행하고 잠재적인 취약점을 식별하세요:

```bash
sudo apt install lynis
sudo lynis audit system
```

### 9. 불필요한 서비스 비활성화

- 공격 표면을 최소화하기 위해 사용하지 않는 서비스를 비활성화하거나 제거하세요. 예를 들어, FTP나 메일 서비스가 필요하지 않다면 다음과 같이 비활성화하세요:

```bash
sudo systemctl disable service_name
```

### 10. 침입 탐지 및 방지 시스템(IDS/IPS) 사용

- Fail2ban과 같은 도구를 설치하여 로그인 시도 실패가 너무 많은 IP 주소를 차단하세요:

```bash
sudo apt install fail2ban
```

- AIDE(Advanced Intrusion Detection Environment)를 사용하여 파일 무결성을 모니터링하고 무단 변경을 탐지하세요.
