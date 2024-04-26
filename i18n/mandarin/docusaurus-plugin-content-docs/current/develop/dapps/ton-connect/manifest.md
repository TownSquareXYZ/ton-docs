# 创建 manifest.json

Every app needs to have its manifest to pass meta information to the wallet. 每个应用都需要有它的 manifest 文件，用以向钱包传递元信息。Manifest 是一个名为 `tonconnect-manifest.json` 的 JSON 文件，遵循以下格式：

```json
{
    "url": "<app-url>",                        // 必填
    "name": "<app-name>",                      // 必填
    "iconUrl": "<app-icon-url>",               // 必填
    "termsOfUseUrl": "<terms-of-use-url>",     // 可选
    "privacyPolicyUrl": "<privacy-policy-url>" // 可选
}
```

## 示例

您可以在下面找到一个 manifest 的示例：

```json
{
    "url": "https://ton.vote",
    "name": "TON Vote",
    "iconUrl": "https://ton.vote/logo.png"
}
```

## 最佳实践

- 最佳实践是将 manifest 放置在您应用和库的根目录，例如 `https://myapp.com/tonconnect-manifest.json`。这样可以让钱包更好地处理您的应用，并提升与您应用相关的用户体验。 It allows the wallet to handle your app better and improve the UX connected to your app.
- 确保 `manifest.json` 文件通过其 URL 可以被 GET 访问。

## 字段描述

| 字段                 | 要求 | 描述                                                                                                                                                                                                                                                                                                                                           |
| ------------------ | -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`              | 必填 | app URL. Will be used as the DAppidentifier. Will be used to open the DAppafter click to its icon in the wallet. 应用 URL。将被用作 DApp 标识符。点击钱包中的图标后，将用来打开 DApp。推荐传递不带关闭斜杠的 url，例如 'https://mydapp.com' 而非 'https://mydapp.com/'。 |
| `name`             | 必填 | app name. 应用名称。可以简单，不会被用作标识符。                                                                                                                                                                                                                                                                                                |
| `iconUrl`          | 必填 | Url to the app icon. Must be PNG, ICO, ... format. SVG icons are not supported. 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。                                                                                           |
| `termsOfUseUrl`    | 可选 | url to the Terms Of Use document. Optional for usual apps, but required for the apps which is placed in the Tonkeeper recommended apps list.                                                                                                                                                                 |
| `privacyPolicyUrl` | 可选 | url to the Privacy Policy document. Optional for usual apps, but required for the apps which is placed in the Tonkeeper recommended apps list.                                                                                                                                                               |
