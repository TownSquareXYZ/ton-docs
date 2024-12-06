# TON 사이트 실행 방법

## 👋 소개

[TON 사이트](https://blog.ton.org/ton-sites)는 설치 과정을 제외하면 일반 사이트와 거의 동일하게 작동합니다. 실행을 위해 몇 가지 추가 작업이 필요합니다. 이 튜토리얼에서 방법을 설명하겠습니다.

## 🖥 TON 사이트 실행하기

웹사이트에 TON 프록시를 사용하기 위해 [Tonutils Reverse Proxy](https://github.com/tonutils/reverse-proxy)를 설치하세요.

### Linux 설치 방법

##### 다운로드

```bash
wget https://github.com/ton-utils/reverse-proxy/releases/latest/download/tonutils-reverse-proxy-linux-amd64
chmod +x tonutils-reverse-proxy-linux-amd64
```

##### 실행

도메인 설정으로 실행하고 단계를 따르세요:

```
./tonutils-reverse-proxy-linux-amd64 --domain your-domain.ton 
```

터미널의 QR 코드를 Tonkeeper, Tonhub 또는 다른 지갑으로 스캔하고 트랜잭션을 실행하세요. 도메인이 사이트에 연결됩니다.

###### 도메인 없이 실행

.ton 또는 .t.me 도메인이 없다면 .adnl 도메인으로 간단 모드에서 실행할 수 있습니다:

```
./tonutils-reverse-proxy-linux-amd64
```

##### 사용

이제 누구나 ADNL 주소나 도메인으로 TON 사이트에 접근할 수 있습니다.

프록시 패스 URL 등의 설정을 변경하려면 `config.json` 파일을 열어 수정하고 프록시를 재시작하세요. 기본 프록시 패스 url은 `http://127.0.0.1:80/`입니다.

프록시는 다음 헤더를 추가합니다:
`X-Adnl-Ip` - 클라이언트의 IP, `X-Adnl-Id` - 클라이언트의 ADNL ID

### 다른 OS 설치 방법

소스에서 빌드하고 리눅스의 2단계처럼 실행하세요. 빌드에는 Go 환경이 필요합니다.

```bash
git clone https://github.com/tonutils/reverse-proxy.git
cd reverse-proxy
make build
```

다른 운영체제용으로 빌드하려면 `make all` 실행

## 👀 다음 단계

### 🔍 사이트 가용성 확인

선택한 방법의 모든 단계를 완료하면 TON 프록시가 시작됩니다. 성공적이라면 해당 단계에서 받은 ADNL 주소로 사이트가 접근 가능합니다.

이 주소에 `.adnl`을 붙여 사이트 가용성을 확인할 수 있습니다. [MyTonWallet](https://mytonwallet.io/) 확장 프로그램 등을 통해 브라우저에서 TON 프록시가 실행 중이어야 사이트가 열립니다.

## 📌 참고 자료

- [TON Sites, TON WWW 및 TON Proxy](https://blog.ton.org/ton-sites)
- [Tonutils Reverse Proxy](https://github.com/tonutils/reverse-proxy)
- 제작자: [Andrew Burnosov](https://github.com/AndreyBurnosov) (TG: [@AndrewBurnosov](https://t.me/AndrewBurnosov)), [Daniil Sedov](https://gusarich.com) (TG: [@sedov](https://t.me/sedov)), [George Imedashvili](https://github.com/drforse)

## 참고

- [C++ 구현 실행하기](/v3/guidelines/web3/ton-proxy-sites/running-your-own-ton-proxy)
