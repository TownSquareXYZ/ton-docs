# POW Givers

:::warning 已弃用
这种资料可能已经过时，不再有用。 请随时省略它。
:::

该案文的目的是说明如何与工作证明提供者智能合同交互以获取Toncoin。 我们假定熟悉TON Blockchain Lite 客户端，正如`Getting Started`所解释的那样， 并有编纂“Lite 客户端”和其他软件所需的程序。 为了获得运行验证器所需的更多Tonco币，我们还假定熟悉了 `Full Node` 和 `Validator` 两个页面。 您还需要一个足够强大的专用服务器来运行一个完整节点，以便获得更多的 Toncoin。 获取少量Tonco币不需要专用服务器，可能需要几分钟的时间在家电脑上完成。

> 请注意，目前由于采矿者人数众多，任何采矿活动都需要大量资源。

## 1. 提供工作证明的智能合同

为了防止少数恶意方收集所有Tonco， 一种特殊类型的“工作证明礼物”智能合同已经部署在网络的主链中。 这些智能联系地址是：

小型赠送器(每几分钟发送10到100吨)：

- kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN
- kf8SYc83pm5JkGt0p3TQRkuiM58O9Cr3waUtR9OFq716lN-
- kf-FV4QTxLl-7Ct3E6MqOtMt-RGXMxi27g4I645lw6MTWraV
- kf_NSzfDJI1A3rOM0GQm7xsoUXHTgmdhN5-OrGD8uwL2JMvQ
- kf8gf1PQy4u2kURl-Gz4LbS29eaN4sVdrVQkPO-JL80VhOe6
- kf8kO6K6Qh6YM4ddjRYYlvVAK7IgyW8Zet-4ZvNrVsmQ4EOF
- kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8
- kf91o4NNTryJ-Cw3sDGt9OTiafmETdVFUMvylQdFPoOxIsLm
- kf9iWhwk9GwAXjtwKG-vN7rmXT3hLIT23RBY6KhVaynRrIK7
- kf8JfFUEJhhpRW80_jqD7zzQteH6EBHOzxiOhygRhBdt4z2N

大型赠送器(至少每天一次送10,000吨硬币)：

- kf8guqdIbY6kpMykR8WFeVGbZcP2iuBagXfnQuq0rGrxgE04
- kf9CxReRyaGj0vpSH0gRZkOAitm_yDHvgiMGtmvG-ZTirrMC
- kf-WXA4CX4lqyVlN4qItlQSWPFIy00NvO2BAydgC4CTeIUme
- kf8yF4oXfIj7BZgkqXM6VsmDEgCqWVSKECO1pC0LXWl399Vx
- kf9nNY69S3_heBBSUtpHRhIzjjqY0ChugeqbWcQGtGj-gQxO
- kf_wUXx-l1Ehw0kfQRgFtWKO07B6WhSqcUQZNyh4Jmj8R4zL
- kf_6keW5RniwNQYeq3DNWGcohKOwI85p-V2MsPk4v23tyO3I
- kf_NSPpF4ZQ7mrPylwk-8XQQ1qFD5evLnx5_oZVNywzOjSfh
- kf-uNWj4JmTJefr7IfjBSYQhFbd3JqtQ6cxuNIsJqDQ8SiEA
- kf8mO4l6ZB_eaMn1OqjLRrrkiBcSt7kYTvJC_dzJLdpEDKxn

> 请注意，目前所有大型巨头都已经枯竭。

前十个智能合约使一个愿意获得少量Tonco币的用户能够获得一些不需要太多的计算功率(通常情况下)。 家用计算机上的工作时间应足以算出)。 其余的智能合约是为了获取更大数量的Tonco币来运行网络验证器； 典型的情况是，一个能够运行验证器的专用服务器上的一天工作应该足以获得必要的金额。

> 请注意，由于大量矿工，目前需要大量资源来开采小型矿石。

您应该随机选择其中一个"工作证明"智能合同"(根据您的目的从这两个列表中的一个)并通过类似于采矿的程序从这个智能合同中获取Tonco币。 本质上， 您必须在选定的“工作证明”智能合同中提交包含工作证明和钱包地址的外部消息。 然后向您发送必要的金额。

## 2. 采矿过程

为了创建一个包含“工作证明”的外部消息， 您应该运行一个特殊的采矿实用程序，它是从 GitHub 仓库的 TON 源编译的。 此工具位于与构建目录相关的文件`./crypto/pow-miner` 中，可以通过在构建目录中输入“制作粉末-矿物”进行编译。

然而，在运行 `pow-miner` 之前，你需要知道所选的“工作证明”智能合同的`种子`和`复杂性`的实际值。 这可以通过这个智能合约的 get-methodology `get_pow_params` 来完成。 例如，如果你使用提供者智能合同，`kf-kkdY_B7p-77TLn2hUhM6QidWrrrsl8FYWCIvBMpZKprBtN` 你可以简单地输入：

```
> runmethode kf-kdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN get_pow_params
```

在 Lite 客户端控制台中获取输出类似：

```...
    参数： [ 101616 ] 
    结果： [ 229760179690128740373110445116482216837 5391989333430795893340301740392613472742888450811449622072208432 100000000256] 
    远程结果(不受信任): [ 229760179012874037311045116482216837 1989333430795894030174039403926134728484848811449622072084332100000000000256]
```

“结果:”行中的头两个大数字是这个智能合约的`种子`和`复杂性`。 在这个例子中，种子是`229760179690128740373110445116482216837`，复杂性是`53919893334301279589334030174039261347274288845081144962207220420498432`。

接下来，你可以使用 \`粉末矿物' 工具如下：

```
$ crypto/pow-miner -vv -w<num-threads> -t<timeout-in-sec> <your-wallet-address> <seed> <complexity> <iterations> <pow-giver-address> <boc-filename>
```

这里：

- <num-threads>是你想要用于采矿的 CPU 核心数量。
- <timeout-in-sec>是矿工在承认失败之前运行的最大秒数。
- <your-wallet-address>是你钱包的地址(可能尚未初始化)。 t 要么在masterchain 上，要么在工作链上 (注意您需要一个masterchain 钱包来控制验证器)。
- <seed>和<complexity>是通过运行 get-method `get-pow-params` 获得的最新值。
- <pow-giver-address>是所选的提供工作证明者智能合同的地址。
- <boc-filename>是输出文件的文件名，在成功的情况下，将保存带有工作证明的外部信息。

例如，如果你的钱包地址是 `kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7`，你可以运行：

```
$ crypto/pow-miner -vv -w7 -t100 kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN mined.boc
```

该程序将运行一段时间(在这种情况下最多会运行100秒)，要么成功终止(零退出代码)，要么将所需的工作证明保存到文件“已输入”。 如果找不到工作证据，则使用非零退出代码终止。

在失败的情况下，您会看到一些东西：

```
   [ 预期成功需要哈希值: 2147483648 ]
   [计算哈希值: 1192230912 ]
```

该程序将以非零退出码终止。 然后你必须再次获得`种子`和`复杂性`(因为它们同时可能因处理较成功的采矿者提出的请求而有所改变)，并用新的参数重新运行`粉末-矿物`， 一再重复这一进程，直至成功。

在成功的情况下，你会看到以下几点：

```
   [预期成功所需哈希: 2147483648]
   4D696E65005EFE49705690D2AACC203003DBE333046683B693B698EF945FF250723C0F73297A2A1A41E2F1A1F533B3B3B3BC4F5664D6C743C5C74B3342F3A7314364B3D0DA698E6C80C1EA4ACDA33755876668680BAE9BE8A4D6385A1F3B3BC4F5664F664D6C743C574B3342F3A7314364B3D0DA698E6C80C1EA4
   oc`
   [ 计算的哈希值：1122036095]
```

然后您可以使用Lite客户端发送来自文件“已经输入”的外部消息。 oc\`到提供工作证明的智能合同(而且你必须尽快这样做)：

```
> sendfile mined.boc
... 外部消息状态是 1
```

您可以等待几秒钟并检查您钱包的状态：

:::info
请在此进一步说明，代码、评论和/或文件可能含有“gram”、“nangram”等参数、方法和定义。 这是由Telegram开发的原始TON代码的遗产。 Gram cryptocurrencity从未发过加密。 TON的货币是Tonco币，TON测试网的货币是Toncoin。
:::

```
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:1)
      bits:(var_uint len:1 value:111)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722498
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720869000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:100000000000))
      other:(extra_currencies
        dict:hme_empty))
    state:account_uninit))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F12025BC2F7F2341000001C169E9DCD0945D21DBA0004_}
last transaction lt = 7720869000001 hash = 83C15CDED025970FEF7521206E82D2396B462AADB962C7E1F4283D88A0FAB7D4
account balance is 100000000000ng
```

如果没有人在你面前提交了这个`种子`和`复杂性`的有效工作证据，提供工作证明者将接受你的工作证明。 并且这将反映在你的钱包余额中 (10或20秒可能会在发出外部消息后才会发生这种情况; 在检查你钱包的余额以刷新Lite客户端状态之前，必须多次尝试并输入 "last" 。 在取得成功的情况下， 您将会看到余额已经增加(甚至你的钱包是在未初始化状态下创建的，如果以前不存在的话)。 在失败的情况下，你必须获得新的`种子`和`复杂性`，并从一开始就重复开采过程。

如果你幸运，你钱包的余额已增加。 如果钱包尚未初始化，你可能想要初始化它(在`Stepby-Step`中可以找到更多关于钱包创建的信息)：

```
> sendfile new-wallet-query.boc
... external message status is 1
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:1147)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722691
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720945000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:99995640998))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
            ))
        library:hme_empty))))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1206811EC2F7F23A1800001C16B0BC790945D20D1929934_}
 x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
last transaction lt = 7720945000001 hash = 73353151859661AB0202EA5D92FF409747F201D10F1E52BD0CBB93E1201676BF
account balance is 99995640998ng
```

现在你是 100 Toncoin 的愉快的拥有者。 恭喜！

## 3. 在发生故障时实现采矿过程的自动化

如果您长时间未能获得您的 Toncoin 出现这种情况可能是因为太多其他用户同时从同一个工作证明给人的智能合同中挖掘。 也许你应该从上面给出的名单中选择另一个提供工作的人智能合同。 或者，， 您可以写一个简单的脚本，一次又一次地以正确的参数运行"粉末矿物"，直到成功(通过检查"粉末矿物"的退出代码检测到)，并使用带参数"-c"sendfile来调用Lite客户端。 oc'' 在找到后立即发送外部消息。
