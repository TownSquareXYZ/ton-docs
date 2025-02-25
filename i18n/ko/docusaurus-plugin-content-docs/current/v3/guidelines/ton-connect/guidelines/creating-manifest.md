# manifest.json 생성하기

모든 앱은 지갑에 메타 정보를 전달하기 위한 manifest가 필요합니다. manifest는 `tonconnect-manifest.json`이라는 이름의 JSON 파일로 다음 형식을 따릅니다:

```json
{
    "url": "<app-url>",                        // required
    "name": "<app-name>",                      // required
    "iconUrl": "<app-icon-url>",               // required
    "termsOfUseUrl": "<terms-of-use-url>",     // optional
    "privacyPolicyUrl": "<privacy-policy-url>" // optional
}
```

## 예시

manifest 예시는 다음과 같습니다:

```json
{
    "url": "https://ton.vote",
    "name": "TON Vote",
    "iconUrl": "https://ton.vote/logo.png"
}
```

## 모범 사례

- manifest는 앱과 저장소의 루트에 위치시키는 것이 좋습니다(예: `https://myapp.com/tonconnect-manifest.json`). 이를 통해 지갑이 앱을 더 잘 처리하고 앱 관련 UX를 개선할 수 있습니다.
- `manifest.json` 파일이 URL을 통해 GET 요청으로 접근 가능한지 확인하세요

## 필드 설명

| 필드                 | 요구사항 | 설명                                                                                                                                                                                                                                                                                                         |
| ------------------ | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`              | 필수   | 앱 URL. DApp 식별자로 사용됩니다. 지갑에서 앱 아이콘 클릭 시 DApp을 열 때 사용됩니다. 마지막 슬래시를 제외한 URL 사용을 권장합니다(예: 'https://mydapp.com/'가 아닌 'https://mydapp.com'). |
| `name`             | 필수   | 앱 이름. 단순할 수 있으며 식별자로 사용되지 않습니다.                                                                                                                                                                                                                                            |
| `iconUrl`          | 필수   | 앱 아이콘 URL. PNG, ICO 등의 형식이어야 합니다. SVG 아이콘은 지원되지 않습니다. 180x180px PNG 아이콘 URL을 전달하는 것이 가장 좋습니다.                                                                                                                                              |
| `termsOfUseUrl`    | 선택   | 이용 약관 문서 URL. 일반 앱의 경우 선택사항이지만, Tonkeeper 추천 앱 목록에 포함될 앱의 경우 필수입니다.                                                                                                                                                                                                        |
| `privacyPolicyUrl` | 선택   | 개인정보 처리방침 문서 URL. 일반 앱의 경우 선택사항이지만, Tonkeeper 추천 앱 목록에 포함될 앱의 경우 필수입니다.                                                                                                                                                                                                    |
