# 创建manifest.json

每个应用都需要有它的清单才能将元信息传递到钱包中。 清单是一个 JSON 文件，名称为“tonconnect-manifest.json”，格式如下：

```json
Mr.
    "url": "<app-url>", // 必填
    "name": "<app-name>", // 需要
    "iconUrl": "<app-icon-url>", // 需要
    "termsOfUseUrl": "<terms-of-use-url>", // 可选
    "privacyPolicyUrl": "<privacy-policy-url>" // 可选
}
```

## 示例

您可以在下面找到一个清单示例：

```json
{
    "url": "https://ton.vote",
    "name": "TON Vote",
    "iconUrl": "https://ton.vote/logo.png"
}
```

## A. 最佳做法

- 最佳做法是将清单放置在您的应用程序和仓库的根目录中，例如`https://myapp.com/tonconnect-manifest.json`。 它允许钱包更好地处理您的应用并改进连接到您的应用的 UX 。
- 请确保通过 URL 将`manifest.json` 文件提供给GET。

## 字段描述

| 字段                 | 要求  | 描述                                                                                                                                                                                   |
| ------------------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url`              | 必填  | 应用 URL。 将用作DApp标识符。 将用于打开 DAppafter 点击钱包中的图标。 建议通过 url 不要关闭 slash ，例如'https://mydapp.com' 而不是 'https://mydapp.com/'。 |
| `name`             | 必填  | 应用名称 可能是简单的，将不会被用作标识符。                                                                                                                                                               |
| `iconUrl`          | 必填  | URL到应用图标。 必须是PNG, ICO, ... 格式。 不支持 SVG 图标。 完美地将URL传递到 180x180px PNG 图标。                                                              |
| `termsOfUseUrl`    | 可选的 | 使用文档条款的 url 。 普通应用可选，但是放在守护者推荐应用列表中的应用所需。                                                                                                                                            |
| `privacyPolicyUrl` | 可选的 | URL 到隐私政策文档。 普通应用可选，但是放在守护者推荐应用列表中的应用所需。                                                                                                                                             |
