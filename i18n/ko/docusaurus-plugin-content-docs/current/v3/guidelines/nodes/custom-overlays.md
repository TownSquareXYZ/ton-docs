# 커스텀 오버레이

TON 노드들은 _오버레이_라고 불리는 서브넷을 형성하여 서로 통신합니다. 각 샤드의 공개 오버레이, 검증자들이 참여하는 일반 검증자 오버레이, 특정 검증자 세트를 위한 오버레이와 같은 몇 가지 공통 오버레이가 있습니다.

노드는 커스텀 오버레이에 참여하도록 구성될 수도 있습니다.
현재 이러한 오버레이는 두 가지 목적으로 사용될 수 있습니다:

- 외부 메시지 브로드캐스팅
- 블록 후보 브로드캐스팅

커스텀 오버레이 참여를 통해 공개 오버레이의 불확실성을 피하고 전송 신뢰성과 지연시간을 개선할 수 있습니다.

각 커스텀 오버레이는 외부 메시지와 블록을 보낼 수 있는 권한 등 사전 정의된 권한을 가진 참여자 목록이 엄격하게 결정됩니다. 오버레이의 설정은 모든 참여 노드에서 동일해야 합니다.

여러 노드를 제어하고 있다면, 모든 검증자가 블록 후보를 보낼 수 있고 모든 LS가 외부 메시지를 보낼 수 있는 커스텀 오버레이로 통합하는 것이 유익합니다. 이렇게 하면 LS가 더 빠르게 동기화되는 동시에 외부 메시지 전송률이 높아지고(일반적으로 전송이 더 안정적) 됩니다. 추가 오버레이는 추가 네트워크 트래픽을 발생시킨다는 점에 유의하세요.

## 기본 커스텀 오버레이

Mytonctrl은 https://ton-blockchain.github.io/fallback_custom_overlays.json 에서 사용할 수 있는 기본 커스텀 오버레이를 사용합니다. 이 오버레이는 대부분의 시간 동안 사용되지 않으며 공개 오버레이 연결에 문제가 있는 경우 비상용으로 사용됩니다.
기본 커스텀 오버레이 참여를 중지하려면 다음 명령을 실행하세요

```bash
MyTonCtrl> set useDefaultCustomOverlays false
MyTonCtrl> delete_custom_overlay default
```

## 커스텀 오버레이 생성

### ADNL 주소 수집

커스텀 오버레이에 검증자를 추가하려면 `validator-console -c getconfig`로 확인할 수 있는 `fullnode adnl id` 또는 mytonctrl의 status에서 찾을 수 있는 `validator adnl id`를 사용할 수 있습니다.
커스텀 오버레이에 라이트서버를 추가하려면 반드시 `fullnode adnl id`를 사용해야 합니다.

### 설정 파일 생성

다음 형식으로 설정 파일을 생성하세요:

```json
{
    "adnl_address_hex_1": {
        "msg_sender": true,
        "msg_sender_priority": 1
    },
    "adnl_address_hex_2": {
        "msg_sender": false
    },

    "adnl_address_hex_2": {
        "block_sender": true
    },
  ...
}
```

`msg_sender_priority`는 블록에 외부 메시지가 포함되는 순서를 결정합니다: 우선 순위가 높은 소스의 메시지가 먼저 처리됩니다. 공개 오버레이와 로컬 LS의 메시지는 우선 순위 0을 가집니다.

**주의: 설정에 나열된 모든 노드가 오버레이에 참여해야 합니다(즉, 정확히 이 설정으로 오버레이를 추가해야 함). 그렇지 않으면 연결이 좋지 않고 브로드캐스트가 실패할 것입니다**

`@validators`라는 특별한 단어를 사용하여 mytonctrl이 각 라운드마다 현재 모든 검증자를 추가하여 자동으로 생성하는 동적 커스텀 오버레이를 만들 수 있습니다.

### 커스텀 오버레이 추가

mytonctrl 명령을 사용하여 커스텀 오버레이를 추가하세요:

```bash
MyTonCtrl> add_custom_overlay <name> <path_to_config>
```

이름과 설정 파일이 모든 오버레이 멤버에서 **반드시** 동일해야 합니다. mytonctrl의 `list_custom_overlays` 명령을 사용하여 오버레이가 생성되었는지 확인하세요.

### 디버그

노드 상세 수준을 4로 설정하고 "CustomOverlay" 단어로 로그를 grep할 수 있습니다.

## 커스텀 오버레이 삭제

노드에서 커스텀 오버레이를 제거하려면 mytonctrl 명령 `delete_custom_overlay <name>`을 사용하세요.
오버레이가 동적인 경우(즉, 설정에 `@validators` 단어가 있는 경우) 1분 내에 삭제되고, 그렇지 않으면 즉시 제거됩니다.
노드가 커스텀 오버레이를 삭제했는지 확인하려면 mytonctrl의 `list_custom_overlays`와 validator-console의 `showcustomoverlays` 명령을 확인하세요.

## 로우 레벨

커스텀 오버레이 작업을 위한 validator-console 명령 목록:

- `addcustomoverlay <path_to_config>` - 로컬 노드에 커스텀 오버레이를 추가합니다. 이 설정은 mytonctrl용 설정과 다른 형식이어야 합니다:
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
- `delcustomoverlay <name>` - 노드에서 커스텀 오버레이를 삭제합니다.
- `showcustomoverlays` - 노드가 알고 있는 커스텀 오버레이 목록을 보여줍니다.


