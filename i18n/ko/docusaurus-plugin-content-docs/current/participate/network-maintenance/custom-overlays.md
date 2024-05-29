# 사용자 지정 오버레이

TON `v2024.04` 업데이트에서 사용자 지정 오버레이를 사용할 수 있는 기능이 도입되었습니다.\
현재는 외부 메시지 브로드캐스팅에만 사용할 수 있습니다. 주요 아이디어는
발신자 노드와 유효성 검사기를 사용하여 비공개 오버레이를 만드는 것입니다. 발신자 노드만 외부 메시지로 브로드캐스트를 만들 수 있으며, 이 메시지는 블록 콜레이터가
수신하여 블록에 들어갈 수 있습니다.

## 기본 사용자 지정 오버레이

Mytonctrl은 https://ton-blockchain.github.io/fallback_custom_overlays.json 에서 제공되는 기본 사용자 정의 오버레이를 사용합니다.
기본 사용자 지정 오버레이 참여를 중지하려면 다음 명령을 실행하세요.

```bash
MyTonCtrl> set useDefaultCustomOverlays false
MyTonCtrl> delete_custom_overlay default
```

## 사용자 지정 오버레이 만들기

### 광고 주소 수집

사용자 정의 오버레이에 유효성 검사기를 추가하려면 `validator-console -c getconfig`로 사용할 수 있는 `풀노드 adnl id`(
) 또는 mytonctrl의 상태에서 찾을 수 있는 `validator adnl id`를 사용하면 됩니다.
라이트서버를 사용자 정의 오버레이에 추가하려면 해당 라이트서버의 `풀노드 adnl id`를 사용해야 합니다.

### 구성 파일 만들기

형식에 맞는 구성 파일을 만듭니다:

```json
{
    "adnl_address_hex_1": {
        "msg_sender": true,
        "msg_sender_priority": 1
    },
    "adnl_address_hex_2": {
        "msg_sender": false
    },
  ...
}
```

msg_sender_priority\`는 외부 메시지를 블록에 포함할 순서를 결정합니다. 우선순위가 높은 소스에서 온 메시지를 먼저 처리합니다. 퍼블릭 오버레이 및 로컬 LS의 메시지는 우선 순위가 0입니다.

**구성에 나열된 모든 노드가 오버레이에 참여해야 하며(즉, 정확히 이 구성으로 오버레이를 추가해야 함), 그렇지 않으면 연결 상태가 좋지 않고 생방송이 실패합니다**.

동적 사용자 정의 오버레이를 만들려면 '@validators'라는 특수 단어를 사용하면 mytonctrl이 현재 모든 유효성 검사기를 추가할 때마다 자동으로
생성합니다.

### 사용자 지정 오버레이 추가

mytonctrl 명령을 사용하여 사용자 지정 오버레이를 추가합니다:

```bash
MyTonCtrl> add_custom_overlay <name> <path_to_config>
```

모든 오버레이 멤버에서 이름과 구성 파일이 동일해야 한다는 점에 유의하세요.
mytonctrl `list_custom_overlays` 명령을 사용하여 오버레이가 생성되었는지 확인합니다.

### Debug

노드 상세도 수준을 4로 설정하고 "CustomOverlay" 단어로 로그를 그립할 수 있습니다.

## 사용자 지정 오버레이 삭제

노드에서 사용자 정의 오버레이를 제거하려면 mytonctrl 명령 `delete_custom_overlay <name>`를 사용합니다.
오버레이가 동적인 경우(즉, 구성에 `@validators` 단어가 있는 경우) 1분 이내에 삭제되며, 그렇지 않으면 즉시 제거됩니다.
노드가 사용자 정의 오버레이를 삭제했는지 확인하려면 `list_custom_overlays` mytonctrl 및 `showcustomoverlays` validator-console 명령을 확인합니다.

## 낮은 수준

사용자 지정 오버레이와 함께 작동하는 유효성 검사기 콘솔 명령 목록입니다:

- addcustomoverlay \<path_to_config>\` - 로컬 노드에 사용자 정의 오버레이를 추가합니다. 이 구성은 mytonctrl용 구성이 아닌 다른 형식이어야 한다는 점에 유의하세요:
  ```json
  {
    "name": "OverlayName",
    "nodes": [
      {
        "adnl_id": "adnl_address_b64_1",
        "msg_sender": true,
        "msg_sender_priority": 1
      },
      {
        "adnl_id": "adnl_address_b64_2",
        "msg_sender": false
      }, ...
    ]
  }
  ```
- delcustomoverlay `<name>\` - 노드에서 사용자 지정 오버레이를 삭제합니다.
- '쇼커스텀 오버레이' - 노드가 알고 있는 커스텀 오버레이 목록을 표시합니다.
