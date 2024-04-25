# 非弹回消息

export const Highlight = ({children, color}) => (
\<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#fff',
padding: '0.2rem',
}}>
{children} </span>
);

几乎所有在智能合约之间发送的内部消息都应该是可弹回的，即应该设置它们的“bounce”位。然后，如果目标智能合约不存在，或者在处理此消息时抛出未处理的异常，消息将被“bounced”，携带原始值的剩余部分（减去所有消息传输和gas费用）。弹回消息的主体将包含32位的`0xffffffff`，紧接着是原始消息的256位，但是“bounce”标志位被清除，“bounced”标志位被设置。因此，所有智能合约都应检查所有入站消息的“bounced”标志，并且要么默默接受它们（通过立即以exit code 0终止），要么执行一些特殊处理来检测哪个出站查询失败了。弹回消息主体中包含的查询永远不应执行。 Then, if the destination smart contract does not exist, or if it throws an unhandled exception while processing this message, the message will be "bounced" back carrying the remainder of the original value (minus all message transfer and gas fees). The body of the bounced message will contain 32 bit `0xffffffff` followed by 256 bit from original message, but with the "bounce" flag cleared and the "bounced" flag set. Therefore, all smart contracts should check the "bounced" flag of all inbound messages and either silently accept them (by immediately terminating with a zero exit code) or perform some special processing to detect which outbound query has failed. The query contained in the body of a bounced message should never be executed.

:::info
弹回消息主体中包含的查询<Highlight color="#186E8A">永远不应执行</Highlight>。
:::

On some occasions, `non-bounceable internal messages` must be used. For instance, new accounts cannot be created without at least one non-bounceable internal message being sent to them. Unless this message contains a `StateInit` with the code and data of the new smart contract, it does not make sense to have a non-empty body in a non-bounceable internal message.

:::tip
不允许最终用户（例如，钱包的用户）发送包含大量价值（例如，超过五个Toncoin）的不可弹回消息是一个好主意，或者如果他们这样做了就警告他们。更好的做法是先发送少量金额，接着初始化新的智能合约，然后再发送更大的金额。 It is a `better idea` to send a small amount first, then initialize the new smart contract, and then send a larger amount.
:::
