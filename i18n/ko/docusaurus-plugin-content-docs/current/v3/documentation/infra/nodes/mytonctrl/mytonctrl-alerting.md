# MyTonCtrl 알림 봇

## 개요

MyTonCtrl 알림 봇은 텔레그램 봇을 통해 노드 상태 알림을 받을 수 있는 도구입니다.
MyTonCtrl 도구 세트의 일부이며 검증자와 라이트서버 모두에서 사용할 수 있습니다.

## 설정

MyTonCtrl 알림 봇을 설정하려면 다음 단계를 따르세요:

### 봇 준비

1. https://t.me/BotFather 에 가서 `/newbot` 명령어로 봇을 생성하세요. 이후 `BotToken`을 받게 됩니다.
2. 생성된 봇으로 가서 `Start` 버튼을 누르세요. 이렇게 하면 봇으로부터 메시지를 받을 수 있습니다.
3. 그룹(채팅)에서 봇의 메시지를 받고 싶다면, 봇을 그룹에 추가하고 필요한 권한을 부여하세요(그룹 관리자로 설정).
4. https://t.me/getmyid_bot 에 가서 `Start` 버튼을 누르세요. 당신의 `ChatId`를 알려줄 것입니다. 텔레그램 계정으로 직접 메시지를 받고 싶다면 이것을 사용하세요.
   그룹으로 메시지를 받고 싶다면 봇을 그룹에 추가하면 그룹의 `ChatId`를 알려줄 것입니다.

### 알림 봇 활성화

1. 다음 명령어로 `alert-bot` 활성화

   ```bash
   MyTonCtrl> enable_mode alert-bot
   ```

2. 다음 명령어 실행

   ```bash
   MyTonCtrl> set BotToken <BotToken>
   ```

3. 다음 명령어 실행

   ```bash
   MyTonCtrl> set ChatId <ChatId>
   ```

4. 다음 명령어로 봇의 메시지 전송 가능 여부 확인

   ```bash
   MyTonCtrl> test_alert
   ```

   텔레그램 계정이나 채팅에서 봇의 메시지를 받아야 합니다.

## 지원되는 알림

MyTonCtrl 알림 봇은 다음 알림을 지원합니다:

- 검증자 지갑 잔액 부족
- 노드 DB 사용량 80% 초과
- 노드 DB 사용량 95% 초과
- 검증자 라운드 효율성 저조
- 노드 동기화 안 됨
- 노드 실행 안 됨(서비스 중단)
- 노드가 ADNL 연결에 응답하지 않음
- 검증자가 지난 6시간 동안 블록을 생성하지 않음
- 검증자가 이전 검증 라운드에서 슬래시됨

## 알림 활성화/비활성화

알림을 활성화하거나 비활성화하려면 다음 명령어를 사용하세요:

- 알림 활성화: `enable_alert <alert-name>` 명령어 사용
- 알림 비활성화: `disable_alert <alert-name>` 명령어 사용
- 알림 상태 확인: `list_alerts` 명령어 사용
