import Feedback from '@site/src/components/Feedback';

# TON Connect for security

TON Connect 确保用户对他们分享的数据有明确的控制权，这意味着在应用程序和钱包传输期间数据不会泄露。为了加强这一设计，钱包和应用采用了强大的加密身份验证系统，这些系统相互协作。

## 用户数据和资金的安全性

- On TON Connect, user data is end-to-end encrypted when transmitted to wallets via bridges. This allows apps and wallets to employ third-party bridge servers that decrease the possibility of data theft and manipulation, dramatically increasing data integrity and safety.
- Through TON Connect, security parameters are implemented to allow users' data to be directly authenticated with their wallet address. This will enable users to use multiple wallets and choose which one is used within a particular app.
- The TON Connect protocol allows for sharing personal data items (such as contact details and KYC info, etc.), meaning the user explicitly confirms sharing such data.

Specific details and related code examples about TON Connect and its underlying security-focused design can be found via [TON Connect GitHub](https://github.com/ton-connect/).

<Feedback />

