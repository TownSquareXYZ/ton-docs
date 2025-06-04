import Feedback from '@site/src/components/Feedback';

# TON Connect for security

TON Connectは、ユーザーが共有するデータを明確に管理できるようにします。つまり、アプリとウォレットの転送中にデータが漏れる可能性はありません。この設計を強化するため、ウォレットとアプリは強力な暗号認証システムを採用し、連携しています。

## ユーザーデータと資金のセキュリティ

- On TON Connect, user data is end-to-end encrypted when transmitted to wallets via bridges. This allows apps and wallets to employ third-party bridge servers that decrease the possibility of data theft and manipulation, dramatically increasing data integrity and safety.
- Through TON Connect, security parameters are implemented to allow users' data to be directly authenticated with their wallet address. This will enable users to use multiple wallets and choose which one is used within a particular app.
- The TON Connect protocol allows for sharing personal data items (such as contact details and KYC info, etc.), meaning the user explicitly confirms sharing such data.

Specific details and related code examples about TON Connect and its underlying security-focused design can be found via [TON Connect GitHub](https://github.com/ton-connect/).

<Feedback />

