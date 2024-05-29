# TON 사이트 실행 방법

## 👋 소개

[TON 사이트](https://blog.ton.org/ton-sites)는 설치를 제외하고는 일반 사이트와 거의 비슷하게 작동합니다. 사이트를 시작하려면 몇 가지 추가 작업이 필요합니다. 이 튜토리얼에서는 그 방법을 보여드리겠습니다.

## 🖥 러닝 톤 사이트

웹사이트에 톤 프록시를 사용하려면 [톤툴즈 리버스 프록시](https://github.com/tonutils/reverse-proxy)를 설치하세요.

### 모든 Linux에 설치

##### 다운로드

```bash
wget https://github.com/ton-utils/reverse-proxy/releases/download/v0.2.0/tonutils-reverse-proxy-linux-amd64
chmod 777 tonutils-reverse-proxy-linux-amd64
```

##### 실행

도메인 구성으로 실행하고 단계를 따릅니다:

```
./tonutils-reverse-proxy-linux-amd64 --domain your-domain.ton 
```

톤키퍼, 톤허브 또는 기타 지갑을 사용하여 단말기에서 QR 코드를 스캔하고 거래를 실행합니다. 도메인이 사이트에 연결됩니다.

###### 도메인 없이 실행

또는 .ton 또는 .t.me 도메인이 없는 경우 .adnl 도메인을 사용하여 단순 모드로 실행할 수 있습니다:

```
./tonutils-reverse-proxy-linux-amd64
```

##### 사용

이제 누구나 TON 사이트에 액세스할 수 있습니다! ADNL 주소 또는 도메인 사용.

프록시 패스 URL과 같은 일부 설정을 변경하려면 `config.json` 파일을 열고 프록시를 편집한 후 다시 시작하세요. 기본 프록시 패스 URL은 `http://127.0.0.1:80/`입니다.

프록시는 추가 헤더를 추가합니다:
`X-Adnl-Ip` - 클라이언트의 ip, `X-Adnl-Id` - 클라이언트의 adnl id.

### 다른 OS에 설치

./build.sh\`를 사용하여 소스에서 빌드하고 Linux의 경우 2단계와 같이 실행합니다. 빌드하려면 Go 환경이 필요합니다.

## 👀 추가 단계

### 🔍 사이트 가용성 확인

선택한 방법의 모든 단계를 완료한 후 TON 프록시가 시작되었을 것입니다. 모든 것이 성공적으로 완료되면 해당 단계에서 받은 ADNL 주소에서 사이트를 사용할 수 있습니다.

도메인 '.adnl'로 이 주소를 열면 사이트 이용 가능 여부를 확인할 수 있습니다. 또한 사이트가 열리려면 브라우저에서 [MyTonWallet](https://mytonwallet.io/) 확장 프로그램을 통해 TON 프록시가 실행 중이어야 합니다.

## 📌 참고 자료

- [톤 사이트, 톤 WWW 및 톤 프록시](https://blog.ton.org/ton-sites)
- [토누틸스 리버스 프록시](https://github.com/tonutils/reverse-proxy)
- 저자: [Andrew Burnosov](https://github.com/AndreyBurnosov) (TG: [@AndrewBurnosov](https://t.me/AndreyBurnosov)), [Daniil Sedov](https://gusarich.com) (TG: [@sedov](https://t.me/sedov)), [George Imedashvili](https://github.com/drforse)
