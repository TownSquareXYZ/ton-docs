# 사이트 & 도메인 관리

## 도메인 편집 방법

1. 컴퓨터에서 Google Chrome 브라우저를 엽니다.

2. [링크](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd)에서 Google Chrome TON 확장 프로그램을 설치합니다.

3. 확장 프로그램을 열고 "Import wallet"을 클릭한 후 도메인이 저장된 지갑을 가져옵니다.

> 복구 문구
>
> 복구 문구는 지갑 생성 시 기록한 24개의 단어로 구성됩니다.
>
> 복구 문구를 잃어버린 경우 TON Wallet을 통해 복구할 수 있습니다.
> Tonkeeper에서: 설정 > 지갑 보호 > 개인 키로 이동하세요.
>
> 24개의 단어를 기록하여 안전한 곳에 보관하세요. 비상시 복구 문구만으로 지갑 접근을 복구할 수 있습니다.
> 복구 문구를 엄격히 기밀로 유지하세요. 복구 문구에 접근 권한이 있는 사람은 자금에 대한 완전한 접근 권한을 갖게 됩니다.

4. https://dns.ton.org 에서 도메인을 열고 "Edit" 버튼을 클릭합니다.

## 도메인에 지갑 연결 방법

도메인에 지갑을 연결하면 사용자가 지갑 주소 대신 도메인을 수신자 주소로 입력하여 코인을 보낼 수 있습니다.

1. 위에서 설명한 대로 도메인을 편집용으로 엽니다.

2. "Wallet address" 필드에 지갑 주소를 복사하고 "Save"를 클릭합니다.

3. 확장 프로그램에서 트랜잭션 전송을 확인합니다.

## 도메인에 TON 사이트 연결 방법

1. 위에서 설명한 대로 도메인을 편집용으로 엽니다.

2. "Site" 필드에 TON 사이트의 ADNL 주소를 HEX 형식으로 복사하고 "Save"를 클릭합니다.

3. 확장 프로그램에서 트랜잭션 전송을 확인합니다.

## 서브도메인 설정 방법

1. 웹사이트나 서비스의 서브도메인을 관리하기 위한 스마트 컨트랙트를 네트워크에 생성합니다. 기존의 [manual-dns](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-manual-code.fc) 또는 [auto-dns](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/dns-auto-code.fc) 스마트 컨트랙트를 사용하거나, TON DNS 인터페이스를 구현하는 다른 스마트 컨트랙트를 사용할 수 있습니다.

2. 위에서 설명한 대로 도메인을 편집용으로 엽니다.

3. "Subdomains" 필드에 서브도메인의 스마트 컨트랙트 주소를 복사하고 "Save"를 클릭합니다.

4. 확장 프로그램에서 트랜잭션 전송을 확인합니다.


