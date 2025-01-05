# TON 사이트 접속 방법

이 글에서는 다양한 기기에서 TON 사이트를 방문하는 가장 일반적인 방법들을 살펴보겠습니다.

각 방법은 고유한 장점과 단점을 가지고 있으며, 여기에서 이를 분석해 보겠습니다.

가장 간단한 방법부터 시작해서 가장 고급 방법으로 마무리하겠습니다.

## 😄 간단한 방법

### ton.run 또는 tonp.io를 통한 접속

TON 사이트에 접속하는 가장 쉬운 방법은 [ton.run](https://ton.run)과 같은 사이트를 이용하는 것입니다. 기기에 아무것도 설치하거나 설정할 필요 없이 **ton.run** 또는 **tonp.io**를 열면 바로 TON 사이트를 탐색할 수 있습니다.

이 방법은 일상적인 TON 사이트 탐색이나 간단한 확인에는 적합하지만, 다음과 같은 단점 때문에 정기적인 사용에는 적합하지 않습니다:

- 인터넷 트래픽을 **ton.run**에 맡겨야 함
- 언제든 오프라인이 되거나 고장날 수 있음
- 인터넷 제공업체에 의해 차단될 수 있음

### TON Wallet과 MyTonWallet 확장 프로그램

조금 더 어렵지만 더 나은 방법은 TON 프록시에 연결해주는 브라우저 확장 프로그램을 사용하는 것입니다. 이를 통해 ton.run과 같은 중간 서비스 없이 TON 사이트를 탐색할 수 있습니다.

현재 TON 프록시는 [MyTonWallet](https://mytonwallet.io/) 확장 프로그램에서 사용 가능하며, [TON Wallet](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) 확장 프로그램에서도 곧 사용할 수 있게 될 예정입니다.

이 방법도 꽤 간단하지만, 작동을 위해서는 브라우저에 확장 프로그램을 설치해야 합니다. 대부분의 사용자에게 적합한 방법입니다.

## 🤓 고급 방법

### Tonutils-Proxy 사용하기

이것이 TON 사이트에 접속하는 가장 안전한 방법입니다.

1. [여기서](https://github.com/xssnick/Tonutils-Proxy#download-precompiled-version) 최신 버전을 다운로드하세요

2. 실행한 후 "Start Gateway"를 누르세요

3. 완료!

## 참고

- [C++ 구현 실행하기](/v3/guidelines/web3/ton-proxy-sites/running-your-own-ton-proxy)
