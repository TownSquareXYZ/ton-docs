import Feedback from '@site/src/components/Feedback';

# 外部消息

外部消息是`从外部发送`到 TON 区块链中的智能合约，以使它们执行特定操作。

例如，钱包智能合约期望接收包含钱包所有者签名的订单的外部消息（例如，从钱包智能合约发送的内部消息）。当这样的外部消息被钱包智能合约接收时，它首先检查签名，然后接受消息（通过运行 TVM 原语 `ACCEPT`），然后执行所需的任何操作。

## Replay protection

:::caution
Stay vigilant and check replay protection in contracts for external-in messages.
:::

Notice that all external messages must be protected against replay attacks. The validators normally remove an external message from the pool of suggested external messages (received from the network); however, in some situations another validator could process the same external message twice (thus creating a second transaction for the same external message, leading to the duplication of the original action). Even worse, a `malicious actor could extract` the external message from the block containing the processing transaction and re-send it later. This could force a wallet smart contract to repeat a payment.

The simplest way to protect smart contracts from replay attacks related to external messages is to store a 32-bit counter `cur-seqno` in the persistent data of the smart contract, and to expect a `req-seqno` value in (the signed part of) any inbound external messages. Then an external message is accepted only if both the signature is valid and `req-seqno` equals `cur-seqno`. After successful processing, the `cur-seqno` value in the persistent data is increased by one, so the same external message will never be accepted again.

And one could also include an `expire-at` field in the external message, and accept an external message only if the current Unix time is less than the value of this field. This approach can be used in conjunction with `seqno`; alternatively, the receiving smart contract could store the set of (the hashes of) all recent (not expired) accepted external messages in its persistent data, and reject a new external message if it is a duplicate of one of the stored messages. Some garbage collection of expired messages in this set should also be performed to avoid bloating the persistent data.

:::note\
In general, an external message begins with a 256-bit signature (if needed), a 32-bit `req-seqno` (if needed), a 32-bit `expire-at` (if needed), and possibly a 32-bit `op` and other required parameters depending on `op`. The layout of external messages does not need to be as standardized as that of internal messages because external messages are not used for interaction between different smart contracts (written by different developers and managed by different owners).\
:::

<Feedback />

