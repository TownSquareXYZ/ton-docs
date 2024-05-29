# 매니페스트.json 만들기

모든 앱은 지갑에 메타 정보를 전달하기 위해 매니페스트가 있어야 합니다. 매니페스트는 다음 형식의 'tonconnect-manifest.json'이라는 JSON 파일입니다:

```json
{
    "url": "<app-url>",                        // required
    "name": "<app-name>",                      // required
    "iconUrl": "<app-icon-url>",               // required
    "termsOfUseUrl": "<terms-of-use-url>",     // optional
    "privacyPolicyUrl": "<privacy-policy-url>" // optional
}
```

## 예

아래에서 매니페스트의 예를 확인할 수 있습니다:

```json
{
    "url": "https://ton.vote",
    "name": "TON Vote",
    "iconUrl": "https://ton.vote/logo.png"
}
```

## 모범 사례

- 매니페스트를 앱과 저장소의 루트(예: `https://myapp.com/tonconnect-manifest.json`)에 배치하는 것이 가장 좋습니다. 이를 통해 지갑이 앱을 더 잘 처리하고 앱과 연결된 UX를 개선할 수 있습니다.
- manifest.json\` 파일을 URL로 GET할 수 있는지 확인합니다.

## 필드 설명

| 필드               | 요구 사항 | 설명                                                                                                                                                                                                                                                                   |
| ---------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | 필수    | 앱 URL. 디앱 식별자로 사용됩니다. 지갑에서 아이콘을 클릭한 후 디앱을 여는 데 사용됩니다. 'https://mydapp.com/' 대신 'https://mydapp.com'와 같이 닫는 슬래시 없이 URL을 전달하는 것이 좋습니다. |
| 이름\`             | 필수    | 앱 이름. 단순할 수 있으며 식별자로 사용되지 않습니다.                                                                                                                                                                                                      |
| `iconUrl`        | 필수    | 앱 아이콘의 URL입니다. PNG, ICO, ... 형식이어야 합니다. SVG 아이콘은 지원되지 않습니다. 180x180px PNG 아이콘에 URL을 완벽하게 전달하세요.                                                      |
| `termsOfUseUrl`  | 선택 사항 | URL을 이용약관 문서로 이동합니다. 일반 앱의 경우 선택 사항이지만 Tonkeeper 추천 앱 목록에 있는 앱의 경우 필수입니다.                                                                                                                                                            |
| `개인정보 보호 정책 URL` | 선택 사항 | URL을 개인정보처리방침 문서로 이동합니다. 일반 앱의 경우 선택 사항이지만 Tonkeeper 추천 앱 목록에 있는 앱의 경우 필수입니다.                                                                                                                                                        |
