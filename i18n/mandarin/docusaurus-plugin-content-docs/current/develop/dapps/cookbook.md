从 '@theme/Tabs'导入标签页;
从 '@theme/TabItem' 导入标签页;

# TON Cookbook

在产品开发过程中，往往会出现与关于TON的不同合同相互作用的各种问题。

创建此文档是为了收集所有开发者的最佳做法，并与所有人分享。

## 标准操作

<!-- TODO: zoom on click (lightbox?) -->

<img src="/img/interaction-schemes/ecosystem.svg" alt="Full ecosystem scheme"></img>

## 与合同地址合作

### 如何转换(用户友好的 <-> 下拉)，组装并从字符串中提取地址？

TON 地址独特识别了区块链中的合约，表示其工作链和原始状态哈希。 [两种常见格式](/learn/overviews/address#raw-and user-friendly-user-address)被使用：**raw** (工作链和 HEX编码的散列，用":" 字符分隔)和**方便用户** (使用某些标志编码的基64)。

```
用户友好：EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gqPrHF
Raw: 0:ca6e321ccce9ecedf0a8ca2492ec8592494a5fb5ce0387dff96ef6af982a3e
```

要从SDK中的字符串获取地址对象，您可以使用以下代码：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address } from "@ton/core";


const address1 = Address.parse('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');
const address2 = Address.parse('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e');

// toStrings arguments: urlSafe, bounceable, testOnly
// defaults values: true, true, false

console.log(address1.toString()); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address1.toRawString()); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

console.log(address2.toString()); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address2.toRawString()); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require('tonweb');

const address1 = new TonWeb.utils.Address('EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gPrHF');
const address2 = new TonWeb.utils. ddress('0:ca6e321c7cce9ecedf0a8ca2492ec8592494a5fb5ce0387dff96ef6af982a3e');

// toString 参数：用户友好、isUrlSafe、isBounceable、只有

console.log(address1)。 oString(true，true)); // EQDKbjIcfM6ezt8KjKJLshZJJSqX7XA4ff-W72r5gPrHF
console.log(address1.toString(isUserlift= false)); // 0:ca6e321ccce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

console.log(address1.toString(true)); // EQDKbjIcfM6ezt8KJJJLshZJJJSqX7XOA4ff-W72r5gPrHF

```


<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"github.com/xssnick/tonutils-go/address"
)

// Here, we will need to manually implement the handling of raw addresses since they are not supported by the library.

func main() {
	address1 := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF")
	address2 := mustParseRawAddr("0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e", true, false)

	fmt.Println(address1.String()) // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
	fmt.Println(printRawAddr(address1)) // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

	fmt.Println(address2.String()) // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
	fmt.Println(printRawAddr(address2)) // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
}

func mustParseRawAddr(s string, bounceable bool, testnet bool) *address.Address {
	addr, err := parseRawAddr(s, bounceable, testnet)
	if err != nil {
		panic(err)
	}
	return addr
}

func parseRawAddr(s string, bounceable bool, testnet bool) (*address.Address, error) {
	var (
		workchain int32
		data      []byte
	)
	_, err := fmt.Sscanf(s, "%d:%x", &workchain, &data)
	if err != nil {
		return nil, err
	}
	if len(data) != 32 {
		return nil, fmt.Errorf("address len must be 32 bytes")
	}

	var flags byte = 0b00010001
	if !bounceable {
		setBit(&flags, 6)
	}
	if testnet {
		setBit(&flags, 7)
	}

	return address.NewAddress(flags, byte(workchain), data), nil
}

func printRawAddr(addr *address.Address) string {
	return fmt.Sprintf("%v:%x", addr.Workchain, addr.Data())
}

func setBit(n *byte, pos uint) {
	*n |= 1 << pos
}
```


<TabItem value="py" label="Python">

```py
从 pytoniq_core 导入地址

address1 = Address('EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gqPrHF')
address2 = Address('0:ca6e321ccce9ecedf0a8ca2492ec8592494a5fb5ce0387dff96ef6af982a3e')

# to_strargess() : is_user_friendly, is_url_bounceable, is_test_only

print(address1)。 o_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True)) # EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gPrHF
print(address1)。 o_str(is_user_friendly=False)) # 0:ca6e321cccce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

print(address2.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True)) # EQDKbjIcfM6ezt8KjJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address2.to_str(is_user_friendly=False)) # 0:ca6e321ccc
```




### 用户友好的地址中有什么标志？

定义了两个标志：**bounceable**/**non-bounce** 和 **testnet**/**any-net**。 They can be easily detected by looking at the first letter of the address, because it stands for first 6 bits in address encoding, and flags are located there according to [TEP-2](https://github.com/ton-blockchain/TEPs/blob/master/text/0002-address.md#smart-contract-addresses):

|                          地址开始                         |           二进制表单           | 可充值 | 仅测试网 |
| :---------------------------------------------------: | :-----------------------: | :-: | :--: |
|  我... | 000100.01 |  是的 |   否  |
| 我们... | 010100.01 |  否  |   否  |
|  k... | 100100.01 |  是的 |  是的  |
|  0... | 110100.01 |  否  |  是的  |

:::tip
只有Testnet的标志在区块链中根本没有代表。 只有当作为传送目的地址使用时，不可退信标志才会有所改变：在这种情况下，发出的消息[不允许退信](/develop/smart-contracts/guidelines/non-bouncable-messages)； blockchain中的地址，也不包含此标识。
:::

另外，在一些库中，您可能会注意到一个名为“urlSafe”的序列化参数。 问题是，基64 格式不安全 URL ，这意味着一些字符 (即： `+` 和 `/`)在链接中传送地址时可能引起问题。 当`urlSafe = true`时，所有`+`符号被替换为`-`，所有`/`符号被替换为`_`。 您可以使用以下代码获取这些地址格式：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address } from "@ton/core";

const address = Address.parse('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');

// toStrings arguments: urlSafe, bounceable, testOnly
// defaults values: true, true, false

console.log(address.toString()); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHFэ
console.log(address.toString({urlSafe: false})) // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff+W72r5gqPrHF
console.log(address.toString({bounceable: false})) // UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
console.log(address.toString({testOnly: true})) // kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
console.log(address.toString({bounceable: false, testOnly: true})) // 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require('tonweb');

const address = new TonWeb.utils.Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');

// toString arguments: isUserFriendly, isUrlSafe, isBounceable, isTestOnly

console.log(address.toString(true, true, true, false)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address.toString(true, false, true, false)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff+W72r5gqPrHF
console.log(address.toString(true, true, false, false)); // UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
console.log(address.toString(true, true, true, true)); // kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
console.log(address.toString(true, true, false, true)); // 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
```


<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"github.com/xssnick/tonutils-go/address"
)

func main() {
	address := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF")

	fmt.Println(address.String()) // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
	address.SetBounce(false)
	fmt.Println(address.String()) // UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
	address.SetBounce(true)
	address.SetTestnetOnly(true) // kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
	fmt.Println(address.String())
	address.SetBounce(false) // 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
	fmt.Println(address.String())
}
```


<TabItem value="py" label="Python">

```py
从 pytoniq_core 导入地址

= Address('EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gqPrHF')

# to_str() 参数：is_user_friendly, is_url_safet, is_bounceable, is_test_only

print(address)。 o_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=False)) # EQDKbjIcfM6ezt8KjKJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(addresss.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=False, is_test_only=False)) # EQDKbjIcfMezt8KjJJLshZJJJSqX7X4ff+W72r5gqPrHF
print( o_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True, is_test_only=False)) # UQDKbjIcfM6ezt8KjKJLshZJJJSqX7XOA4ff-W72r5gqPuwA
print(addresss.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=True) # kQDKbjIcfMezt8KjKJLshZJJSX7X4ff-W72r5gqPgpP
print(
```




## TON生态系统中的标准钱包

### 如何传输TON？ 如何发送文本消息到其他钱包？

<img src="/img/interaction-schemes/wallets.svg" alt="Wallet operations scheme"></img>

大多数SDK提供了从您的钱包发送消息的如下过程：

- 您创建了正确版本的钱包包装程序(在您的程序中对象) (在大多数情况下，v3r2)； 另见[钱包版本](/participate/wallets/contracts))，使用密钥和工作链(通常为0，代表 [basechain](/learn/overviews/ton-blockchain#workchain-blockchain-你自己的规则))。
- 您还创建了blockchain 包装器或“客户端”——您选择的任意路线为 API 或liteservers的对象。
- 然后，你_open_在区块链包装器中签约。 这意味着合同对象不再抽象，代表TON主机或测试网上的实际帐户。
- 在此之后，您可以发送您想要的消息。 您还可以根据[高级手册](/develop/smart-contracts/tutorials/wallet#sending-multiple-messages-同时发送)中描述的每次请求发送最多4条消息)。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
从 "@ton/ton"导入 { TonClient, WalletContractV4, internal } ；从"@ton/crypto"导入 { mnemonicNew, mnemonicToPrivateKey } ；

const client = new TonClient(* *
  endpoint: 'https://testnet)。 oncenter.com/api/v2/jsonRPC',
});

// 将mnemonics 转换为私钥
let mnemonics = “word1 word2 ”。 .".split(" ");
let keyPair = 等待mnemonicToPrivateKey(mnemonics);

// 创建钱包合同
let workchain = 0; // 通常你需要一个工作链0
let 钱包 = WalletContractV4。 reate({ workchain, publicKey: keyPair.publicKey });
let contract = client.open(wallet);

// 创建一个transfer
let seqno: number = 等待合同。 etSeqno();
before contract.sendTransfer(Permanent
  seqno,
  secretKey: keyPair). ecretKey,
  messages: [internal(ford
    value: '1',
    to 'EQCD39VS5jcptHL8vMjEXrzGaRcVYto7HUn4bpAOg8xqB2N',
    正文：“示例传输机构”，
  }]
})；
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

```kotlin
// Setup liteClient
val context: CoroutineContext = Dispatchers.Default
val json = Json { ignoreUnknownKeys = true }
val config = json.decodeFromString<LiteClientConfigGlobal>(
    URI("https://ton.org/global-config.json").toURL().readText()
)
val liteClient = LiteClient(context, config)

val WALLET_MNEMONIC = "word1 word2 ...".split(" ")

val pk = PrivateKeyEd25519(Mnemonic.toSeed(WALLET_MNEMONIC))
val walletAddress = WalletV3R2Contract.address(pk, 0)
println(walletAddress.toString(userFriendly = true, bounceable = false))

val wallet = WalletV3R2Contract(liteClient, walletAddress)
runBlocking {
    wallet.transfer(pk, WalletTransfer {
        destination = AddrStd("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")
        bounceable = true
        coins = Coins(100000000) // 1 ton in nanotons
        messageData = org.ton.contract.wallet.MessageData.raw(
            body = buildCell {
                storeUInt(0, 32)
                storeBytes("Comment".toByteArray())
            }
        )
        sendMode = 0
    })
}
```

</TabItem>

<TabItem value="py" label="Python">

```py
从 pytoniq 导入 LiteBalancer, WalletV4R2
导入 asyncio

mnemonics = ["你的", "mnemonics", "here"]

async def main(:
    provider = LiteBalancer. rom_mainnet_config(1)
    正在等待 provider.start_up()

    钱包= 正在等待 WalletV4R2。 rom_mnemonic(provider=provider, mnemonics=mnemonics)

    transfer = Power
        "destination ADDRESS HERE", # 请记住可退还的标志
        "amount": int(10**9 * 0). (5)，# 发送的金额， 在 nanoTON
        "body": "示例传输机构", # 可能包含单元格； 请参阅下面的示例
    }

    等待钱包。 ransfer(**transfer)
	等待client.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

### 撰写评论：长字符串以吸附格式

有些时候需要存储长字符串(或其他大信息)，而单元格可以保持**最大1023 位**。 在这种情况下，我们可以使用吸血鬼细胞。 吸附单元格是指与另一单元格相关联的单元格，而另一单元格则包含对另一单元格的参照，等等。

<Tabs groupId="code-examples">
<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require("tonweb");

function writeStringTail(str, cell) {
    const bytes = Math.floor(cell.bits.getFreeBits() / 8); // 1 symbol = 8 bits
    if(bytes < str.length) { // if we can't write all string
        cell.bits.writeString(str.substring(0, bytes)); // write part of string
        const newCell = writeStringTail(str.substring(bytes), new TonWeb.boc.Cell()); // create new cell
        cell.refs.push(newCell); // add new cell to current cell's refs
    } else {
        cell.bits.writeString(str); // write all string
    }

    return cell;
}

function readStringTail(slice) {
    const str = new TextDecoder('ascii').decode(slice.array); // decode uint8array to string
    if (cell.refs.length > 0) {
        return str + readStringTail(cell.refs[0].beginParse()); // read next cell
    } else {
        return str;
    }
}

let cell = new TonWeb.boc.Cell();
const str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In euismod, ligula vel lobortis hendrerit, lectus sem efficitur enim, vel efficitur nibh dui a elit. Quisque augue nisi, vulputate vitae mauris sit amet, iaculis lobortis nisi. Aenean molestie ultrices massa eu fermentum. Cras rhoncus ipsum mauris, et egestas nibh interdum in. Maecenas ante ipsum, sodales eget suscipit at, placerat ut turpis. Nunc ac finibus dui. Donec sit amet leo id augue tempus aliquet. Vestibulum eu aliquam ex, sit amet suscipit odio. Vestibulum et arcu dui.";
cell = writeStringTail(str, cell);
const text = readStringTail(cell.beginParse());
console.log(text);
```




许多SDK已经具备了解析和储存长串的功能。 在另一些情况下，你可以使用循环来处理这种单元格，或者可能优化它(技巧称为“尾呼叫”)。

别忘了评论消息有 32 0 位(一个可以说，它的代码是 0)！

## TEP-74 (Jettons Standard)

<img src="/img/interaction-schemes/jettons.svg" alt="Jetton operations scheme"></img>

### 如何计算用户的 Jetton 钱包地址 (离链) ？

为了计算用户的珠宝钱包地址，我们需要与用户地址实际调用杰顿主合同的"get_wallet_address"get-method。 对于这项任务，我们可以轻松地使用JettonMaster 的 getWalletAddress 方法或我们自己的电话主合同。

:::info
`@ton/ton`中的`JettonMaster`'缺少很多功能，但是幸运的是，\*这个功能已经存在。
:::

<Tabs groupId="code-examples">
<TabItem value="user-jetton-wallet-method-js" label="@ton/ton">

```js
const { Address, beginCell } = require("@ton/core")
const { TonClient, JettonMaster } = require("@ton/ton")

const client = new TonClient(哇，
    endpoint: 'https://toncenter. om/api/v2/jsonRPC'，
})；

const jettonMasterAddress = Address.parse('。 .') // 例如EQBlqsm144Dq6SjbPI4jZvA1hqTIP3CvHovbIfW_t-SCALE
const userAddress = Address.parse('...')

const jettonMaster = client.open(JettonMaster.create(jettonMasterAddress))
console.log(等待jettonMaster.getWalletAddress(userAddress))
```

</TabItem>

<TabItem value="user-jetton-wallet-get-method-js" label="Manually call get-method">

```js
const { Address, beginCell } = require("@ton/core")
const { TonClient } = require("@ton/ton")

async function getUserWalletAddress(userAddress, jettonMasterAddress) {
    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    });
    const userAddressCell = beginCell().storeAddress(userAddress).endCell()
    const response = await client.runMethod(jettonMasterAddress, "get_wallet_address", [
        {type: "slice", cell: userAddressCell}
    ])
    return response.stack.readAddress()
}
const jettonMasterAddress = Address.parse('...') // for example EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE
const userAddress = Address.parse('...')

getUserWalletAddress(userAddress, jettonMasterAddress)
    .then((jettonWalletAddress) => {console.log(jettonWalletAddress)})
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

```kotlin
// Setup liteClient
val context: CoroutineContext = Dispatchers.Default
val json = Json { ignoreUnknownKeys = true }
val config = json.decodeFromString<LiteClientConfigGlobal>(
    URI("https://ton.org/global-config.json").toURL().readText()
)
val liteClient = LiteClient(context, config)

val USER_ADDR = AddrStd("Wallet address")
val JETTON_MASTER = AddrStd("Jetton Master contract address") // for example EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE

// we need to send regular wallet address as a slice
val userAddressSlice = CellBuilder.beginCell()
    .storeUInt(4, 3)
    .storeInt(USER_ADDR.workchainId, 8)
    .storeBits(USER_ADDR.address)
    .endCell()
    .beginParse()

val response = runBlocking {
    liteClient.runSmcMethod(
        LiteServerAccountId(JETTON_MASTER.workchainId, JETTON_MASTER.address),
        "get_wallet_address",
        VmStackValue.of(userAddressSlice)
    )
}

val stack = response.toMutableVmStack()
val jettonWalletAddress = stack.popSlice().loadTlb(MsgAddressInt) as AddrStd
println("Calculated Jetton wallet:")
println(jettonWalletAddress.toString(userFriendly = true))

```

</TabItem>

<TabItem value="py" label="Python">

```py
from pytoniq import LiteBalancer, begin_cell
import asyncio

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    JETTON_MASTER_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    USER_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"


    result_stack = await provider.run_get_method(address=JETTON_MASTER_ADDRESS, method="get_wallet_address",
                                                   stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()])
    jetton_wallet = result_stack[0].load_address()
    print(f"Jetton wallet address for {USER_ADDRESS}: {jetton_wallet.to_str(1, 1, 1)}")
	await provider.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

### 如何计算用户的杰顿钱包地址(离线)？

调用GET方法获取钱包地址可能需要很多时间和资源。 如果我们事先知道Jetton Wallet 代码及其存储结构，我们可以获得钱包地址，不需要任何网络请求。

您可以使用 Tonviewer 获取代码。 我们以`jUSDT`为例，Jeton Master 地址是 `EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtbSTQgGoXwiuA`。 如果我们[转到这个地址](https://tonviewer.com/EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA?section=method)打开方法标签，我们可以看到那里已经有一个 `get_jetton_data` 方法。 通过调用它，我们可以使用Jeton Wallet 代码获得该单元格的十六进制表单：

```
b5ee9c7201021301000385000114ff00f4a413f4bcf2c80b0102016202030202cb0405001ba0f605da89a1f401f481f481a9a30201ce06070201580a0b02f70831c02497c138007434c0c05c6c2544d7c0fc07783e903e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7c076cf16cc8d0d0d09208403e29fa96ea68c1b088d978c4408fc06b809208405e351466ea6cc1b08978c840910c03c06f80dd6cda0841657c1ef2ea7c09c6c3cb4b01408eebcb8b1807c073817c160080900113e910c30003cb85360005c804ff833206e953080b1f833de206ef2d29ad0d30731d3ffd3fff404d307d430d0fa00fa00fa00fa00fa00fa00300008840ff2f00201580c0d020148111201f70174cfc0407e803e90087c007b51343e803e903e903534544da8548b31c17cb8b04ab0bffcb8b0950d109c150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c032481c007e401d3232c084b281f2fff274013e903d010c7e800835d270803cb8b13220060072c15401f3c59c3e809dc072dae00e02f33b51343e803e903e90353442b4cfc0407e80145468017e903e9014d771c1551cdbdc150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c0325c007e401d3232c084b281f2fff2741403f1c147ac7cb8b0c33e801472a84a6d8206685401e8062849a49b1578c34975c2c070c00870802c200f1000aa13ccc88210178d4519580a02cb1fcb3f5007fa0222cf165006cf1625fa025003cf16c95005cc2391729171e25007a813a008aa005004a017a014bcf2e2c501c98040fb004300c85004fa0258cf1601cf16ccc9ed5400725269a018a1c882107362d09c2902cb1fcb3f5007fa025004cf165007cf16c9c8801001cb0527cf165004fa027101cb6a13ccc971fb0050421300748e23c8801001cb055006cf165005fa027001cb6a8210d53276db580502cb1fcb3fc972fb00925b33e24003c85004fa0258cf1601cf16ccc9ed5400eb3b51343e803e903e9035344174cfc0407e800870803cb8b0be903d01007434e7f440745458a8549631c17cb8b049b0bffcb8b0b220841ef765f7960100b2c7f2cfc07e8088f3c58073c584f2e7f27220060072c148f3c59c3e809c4072dab33260103ec01004f214013e809633c58073c5b3327b55200087200835c87b51343e803e903e9035344134c7c06103c8608405e351466e80a0841ef765f7ae84ac7cbd34cfc04c3e800c04e81408f214013e809633c58073c5b3327b5520
```

现在，我们可以手动计算钱包地址：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton/ton)">

```js
import { Address, Cell, beginCell, storeStateInit } from '@ton/core';

const JETTON_WALLET_CODE = Cell.fromBoc(Buffer.from('b5ee9c7201021301000385000114ff00f4a413f4bcf2c80b0102016202030202cb0405001ba0f605da89a1f401f481f481a9a30201ce06070201580a0b02f70831c02497c138007434c0c05c6c2544d7c0fc07783e903e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7c076cf16cc8d0d0d09208403e29fa96ea68c1b088d978c4408fc06b809208405e351466ea6cc1b08978c840910c03c06f80dd6cda0841657c1ef2ea7c09c6c3cb4b01408eebcb8b1807c073817c160080900113e910c30003cb85360005c804ff833206e953080b1f833de206ef2d29ad0d30731d3ffd3fff404d307d430d0fa00fa00fa00fa00fa00fa00300008840ff2f00201580c0d020148111201f70174cfc0407e803e90087c007b51343e803e903e903534544da8548b31c17cb8b04ab0bffcb8b0950d109c150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c032481c007e401d3232c084b281f2fff274013e903d010c7e800835d270803cb8b13220060072c15401f3c59c3e809dc072dae00e02f33b51343e803e903e90353442b4cfc0407e80145468017e903e9014d771c1551cdbdc150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c0325c007e401d3232c084b281f2fff2741403f1c147ac7cb8b0c33e801472a84a6d8206685401e8062849a49b1578c34975c2c070c00870802c200f1000aa13ccc88210178d4519580a02cb1fcb3f5007fa0222cf165006cf1625fa025003cf16c95005cc2391729171e25007a813a008aa005004a017a014bcf2e2c501c98040fb004300c85004fa0258cf1601cf16ccc9ed5400725269a018a1c882107362d09c2902cb1fcb3f5007fa025004cf165007cf16c9c8801001cb0527cf165004fa027101cb6a13ccc971fb0050421300748e23c8801001cb055006cf165005fa027001cb6a8210d53276db580502cb1fcb3fc972fb00925b33e24003c85004fa0258cf1601cf16ccc9ed5400eb3b51343e803e903e9035344174cfc0407e800870803cb8b0be903d01007434e7f440745458a8549631c17cb8b049b0bffcb8b0b220841ef765f7960100b2c7f2cfc07e8088f3c58073c584f2e7f27220060072c148f3c59c3e809c4072dab33260103ec01004f214013e809633c58073c5b3327b55200087200835c87b51343e803e903e9035344134c7c06103c8608405e351466e80a0841ef765f7ae84ac7cbd34cfc04c3e800c04e81408f214013e809633c58073c5b3327b5520', 'hex'))[0];
const JETTON_MASTER_ADDRESS = Address.parse('EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA');
const USER_ADDRESS = Address.parse('UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA');

const jettonWalletStateInit = beginCell().store(storeStateInit({
    code: JETTON_WALLET_CODE,
    data: beginCell()
        .storeCoins(0)
        .storeAddress(USER_ADDRESS)
        .storeAddress(JETTON_MASTER_ADDRESS)
        .storeRef(JETTON_WALLET_CODE)
        .endCell()
}))
.endCell();
const userJettonWalletAddress = new Address(0, jettonWalletStateInit.hash());

console.log('User Jetton Wallet address:', userJettonWalletAddress.toString());
```




大多数主要代币没有不同的存储结构，因为它们使用 [标准执行 TEP-74 标准](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc)。 例外情况是中央集权施塔布林的新的[Jetton-with-governance contracts](https://github.com/ton-blockchain/stablecoin-contract)。 其中的差别是[在保险库中存在一个钱包状态字段和没有代码单元格](https://github.com/ton-blockchain/stablecoin-contract/blob/7a22416d4de61336616960473af391713e100d7b/contracts/jetton-utils.fc#L3-L12)。

### 如何构造带有评论的珠宝传输消息？

为了理解如何构造一个令牌传输消息，我们使用 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md#1-transfer)，它描述了令牌标准。

:::warning
When displayed, token doesn't usually show count of indivisible units user has; rather, amount is divided by `10 ^ decimals`. This value is commonly set to `9`, and this allows us to use `toNano` function. If decimals were different, we would **need to multiply by a different value** (for instance, if decimals are 6, then we would end up transferring thousand times the amount we wanted).

当然，人们总是可以在不可分割的单位中进行计算。
:::

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
Import Windows Address, begcell, internal, storage MessageRelaxed, toNano } from "@ton/core";

async function main() por
    const jettonWalletAddress = Address。 arse('放置你的jetton钱包地址');
    const destinationAddress = 地址。 arse('放置目标钱包地址');

    const forwardPayload = beginCell()
        . toreUint(0, 32) // 0 opcode 表示我们有一个评论
        。 toreStringTail('Hello, TON!')
        ndCell();

    const messageBody = beginCell()
        . toreUint(0x0f8a7ea5, 32)// jeton transfer
        toreUint(0, 64) // 查询 id
        。 toreCoins (toNano(5))) /jeton amount * 10^9
        toreAddress(目的地地址)
        toreAddress(目的地地址) // 响应目标
        toreBit(0) // 没有自定义payload
        .storeCoins(toNano('0) ")) // 转发金额 - 如果>0, 将发送通知消息
        。 toreBit(1) // 我们存储转发有效载荷作为参考
        toreRef(forwardPayload)
        ndCell();

    const internalMessage = internal(请注意，
        to jettonWalletAddress,
        值：toNano('0). '),
        boun: true
        正文：消息正文
    })；
    const internalMessageCell = beginCell()
        tore(storeMessageRelaxed(internalMessage))
        .endCell();
}

main().finally(() => console.log("Exiting..."));
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require("tonweb");
const {mnemonicToKeyPair} = require("tonweb-mnemonic");

async function main() {
    const tonweb = new TonWeb(new TonWeb.HttpProvider(
        'https://toncenter.com/api/v2/jsonRPC', {
            apiKey: 'put your api key'
        })
    );
    const destinationAddress = new TonWeb.Address('put destination wallet address');

    const forwardPayload = new TonWeb.boc.Cell();
    forwardPayload.bits.writeUint(0, 32); // 0 opcode means we have a comment
    forwardPayload.bits.writeString('Hello, TON!');

    /*
        Tonweb has a built-in class for interacting with jettons, which has
        a method for creating a transfer. However, it has disadvantages, so
        we manually create the message body. Additionally, this way we have a
        better understanding of what is stored and how it functions.
     */

    const jettonTransferBody = new TonWeb.boc.Cell();
    jettonTransferBody.bits.writeUint(0xf8a7ea5, 32); // opcode for jetton transfer
    jettonTransferBody.bits.writeUint(0, 64); // query id
    jettonTransferBody.bits.writeCoins(new TonWeb.utils.BN('5')); // jetton amount, amount * 10^9
    jettonTransferBody.bits.writeAddress(destinationAddress);
    jettonTransferBody.bits.writeAddress(destinationAddress); // response destination
    jettonTransferBody.bits.writeBit(false); // no custom payload
    jettonTransferBody.bits.writeCoins(TonWeb.utils.toNano('0.02')); // forward amount
    jettonTransferBody.bits.writeBit(true); // we store forwardPayload as a reference
    jettonTransferBody.refs.push(forwardPayload);

    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const jettonWallet = new TonWeb.token.ft.JettonWallet(tonweb.provider, {
        address: 'put your jetton wallet address'
    });

    // available wallet types: simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // workchain
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: jettonWallet.address,
        amount: tonweb.utils.toNano('0.1'),
        seqno: await wallet.methods.seqno().call(),
        payload: jettonTransferBody,
        sendMode: 3
    }).send(); // create transfer and send it
}

main().finally(() => console.log("Exiting..."));
```

</TabItem>

<TabItem value="py" label="Python">

```py
from pytoniq import LiteBalancer, WalletV4R2, begin_cell
import asyncio

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
    USER_ADDRESS = wallet.address
    JETTON_MASTER_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    DESTINATION_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"

    USER_JETTON_WALLET = (await provider.run_get_method(address=JETTON_MASTER_ADDRESS,
                                                        method="get_wallet_address",
                                                        stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()]))[0].load_address()
    forward_payload = (begin_cell()
                      .store_uint(0, 32) # TextComment op-code
                      .store_snake_string("Comment")
                      .end_cell())
    transfer_cell = (begin_cell()
                    .store_uint(0xf8a7ea5, 32)          # Jetton Transfer op-code
                    .store_uint(0, 64)                  # query_id
                    .store_coins(1 * 10**9)             # Jetton amount to transfer in nanojetton
                    .store_address(DESTINATION_ADDRESS) # Destination address
                    .store_address(USER_ADDRESS)        # Response address
                    .store_bit(0)                       # Custom payload is None
                    .store_coins(1)                     # Ton forward amount in nanoton
                    .store_bit(1)                       # Store forward_payload as a reference
                    .store_ref(forward_payload)         # Forward payload
                    .end_cell())

    await wallet.transfer(destination=USER_JETTON_WALLET, amount=int(0.05*1e9), body=transfer_cell)
	await provider.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

如果`forward_amount`为非零，则向目的地合同发送关于jetton接收的通知。 可以在本节顶部的计划中看到。 如果“response_destination”地址不是空的，则剩下的toncoins (它们被称为“过剩”) 会被发送到该地址。

:::tip
资源管理器支持jetton通知中的评论以及常见的TON传输。 它们的格式是32个零位数，然后是文本，最好是UTF-8。
:::

:::tip
需要认真考虑传出信息背后的费用和数额。 例如，如果您使用 0.2 TON“呼叫”转账，您将无法转发0.1 TON 并在多余的退货信息中接收0.1 TON
:::

## TEP-62 (NFT Standard)

<img src="/img/interaction-schemes/nft.svg" alt="NFT ecosystem scheme"></img>

NFT 收藏非常不同。 实际上，TON上的 NFT 合同可以定义为“具有适当get-methods 并返回有效的元数据的合同”。 传输操作已经标准化，并相当类似于[jetton's one](/develop/dapps/cookbook#how to construct-a-message-for-a-jetton-transfer-----comment)， 这样我们就不会潜入它，而是看到你可能会遇到的大多数收藏提供的额外功能！

:::warning
提醒：下面有关NFT的所有方法都不受TEP-62的约束。 在尝试之前，请检查您的 NFT 或集合是否会以预期方式处理这些消息。 钱包应用程序模拟在这种情况下可能证明是有用的。
:::

### 如何使用 NFT 批量部署？

智能收藏合同允许在一次交易中部署250个NFT。 然而，必须考虑到，由于计算费用的限额是1吨，这一上限实际上是100-130。 为了做到这一点，我们需要在字典中存储有关新的 NFT 的信息。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, Cell, Dictionary, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";
import { TonClient } from "@ton/ton";

async function main() {
    const collectionAddress = Address.parse('put your collection address');
   	const nftMinStorage = '0.05';
    const client = new TonClient({
        endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC' // for Testnet
    });
    const ownersAddress = [
        Address.parse('EQBbQljOpEM4Z6Hvv8Dbothp9xp2yM-TFYVr01bSqDQskHbx'),
        Address.parse('EQAUTbQiM522Y_XJ_T98QPhPhTmb4nV--VSPiha8kC6kRfPO'),
        Address.parse('EQDWTH7VxFyk_34J1CM6wwEcjVeqRQceNwzPwGr30SsK43yo')
    ];
    const nftsMeta = [
        '0/meta.json',
        '1/meta.json',
        '2/meta.json'
    ];

    const getMethodResult = await client.runMethod(collectionAddress, 'get_collection_data');
    let nextItemIndex = getMethodResult.stack.readNumber();
```




首先，让我们假定储存费的最低TON金额是 `0.05'。 这意味着在部署了NFT后，收集的智能合约将把这么多的TON送到它的平衡点。 接下来，我们与新的 NFT 所有者和他们的内容一起获得数组。 然后，我们将使用 GET 方法 `get_collection_data` 获取`next item_index\` 。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
	let counter = 0;
    const nftDict = Dictionary.empty<number, Cell>();
    for (let index = 0; index < 3; index++) {
        const metaCell = beginCell()
            .storeStringTail(nftsMeta[index])
            .endCell();
        const nftContent = beginCell()
            .storeAddress(ownersAddress[index])
            .storeRef(metaCell)
            .endCell();
        nftDict.set(nextItemIndex, nftContent);
        nextItemIndex++;
        counter++;
    }

	/*
		We need to write our custom serialization and deserialization
		functions to store data correctly in the dictionary since the
		built-in functions in the library are not suitable for our case.
	*/
    const messageBody = beginCell()
        .storeUint(2, 32)
        .storeUint(0, 64)
        .storeDict(nftDict, Dictionary.Keys.Uint(64), {
            serialize: (src, builder) => {
                builder.storeCoins(toNano(nftMinStorage));
                builder.storeRef(src);
            },
            parse: (src) => {
                return beginCell()
                    .storeCoins(src.loadCoins())
                    .storeRef(src.loadRef())
                    .endCell();
            }
        })
        .endCell();

    const totalValue = String(
        (counter * parseFloat(nftMinStorage) + 0.015 * counter).toFixed(6)
    );

    const internalMessage = internal({
        to: collectionAddress,
        value: totalValue,
        bounce: true,
        body: messageBody
    });
}

main().finally(() => console.log("Exiting..."));
```




其次，我们需要正确计算交易总成本。 `0.015`的值是通过测试获得的，但每次都可能不同。 这主要取决于NFT的内容，因为内容规模的增加导致了更高的**预付费** (交货费)。

### 如何改变收藏智能合同的所有者？

更改收藏的所有者非常简单。 要做到这一点，您需要指定 **opcode = 3**，任意查询_id，以及新所有者的地址：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import cord Address, begCell, internal, storage MessageRelaxed, toNano } from "@ton/core";

async function main() pow
    const collectionAddress = Address。 arse('放置您的收藏地址');
    const newownnerAddress = 地址。 arse('放置新所有者钱包地址');

    const messageBody = beginCell()
        . toreUint(3, 32) // 更改所有者的opcode
        。 toreUint(0, 64) // 查询 id
        toreAddress(新所有者地址)
        ndCell();

    const internalMessage = internal(Windows
        to collectionAddress,
        值：toNano('0). 5',
        bounce: true
        正文：消息正文
    })；
    const internalMessageCell = beginCell()
        tore(storeMessageRelaxed(内部Message))
        .endCell();
}

main().finally(() => console.log("Exiting..."));
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require("tonweb");
const {mnemonicToKeyPair} = require("tonweb-mnemonic");

async function main() {
    const tonweb = new TonWeb(new TonWeb.HttpProvider(
        'https://toncenter.com/api/v2/jsonRPC', {
            apiKey: 'put your api key'
        })
    );
    const collectionAddress  = new TonWeb.Address('put your collection address');
    const newOwnerAddress = new TonWeb.Address('put new owner wallet address');

    const messageBody  = new TonWeb.boc.Cell();
    messageBody.bits.writeUint(3, 32); // opcode for changing owner
    messageBody.bits.writeUint(0, 64); // query id
    messageBody.bits.writeAddress(newOwnerAddress);

    // available wallet types: simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // workchain
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: collectionAddress,
        amount: tonweb.utils.toNano('0.05'),
        seqno: await wallet.methods.seqno().call(),
        payload: messageBody,
        sendMode: 3
    }).send(); // create transfer and send it
}

main().finally(() => console.log("Exiting..."));
```




### 如何更改集合智能合约中的内容？

为了改变智能合约集合的内容，我们需要了解它是如何存储的。 收藏将所有内容存储在一个单元中，其中有两个单元：**收藏内容** 和 **NFT 通用内容** 。 第一个单元格包含收集的元数据，第二个单元格包含NFT元数据的基本URL。

集合的元数据通常以类似于`0.json`的格式存储，并继续递增，而此文件之前的地址保持不变。 这个地址应该存储在 NFT 的常见内容。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import cord Address, begCell, internal, storage MessageRelaxed, toNano } from "@ton/core";

async function main() pow
    const collectionAddress = Address。 arse('放置您的收藏地址');
    const newCollectionMeta = '放置url fol 收藏元';
    const newNftCommonMeta = “放置nft meta的共同url for nft mete”；
    const 特许权使用费地址 = 地址。 arse('放电费地址');

    const collectionMetacell = beginCell()
        toreUint(1, 8) // 我们有离链元数据
        toreStringTail(newCollectionMeta)
        ndCell();
    const nftCommonMetacell = beginCell()
        . toreUint(1, 8) // 我们有离链元数据
        toreStringTail(newNftCommonMeta)
        ndCell();

    const contentcell = beginCell()
        toreRef(collectionMetaCell)
        .storeRef(nftCommonMetaCell)
        ndCell();

    const entitycell = beginCell()
        . toreUint(5, 16) //factor
        toreUint(100, 16), // base
        . toreAddress(特许使用费地址) // 此地址将收到每笔销售的5%
        ndCell();

    const messageBody = beginCell()
        toreUint(4, 32)// 更改内容的opcode
        。 toreUint(0, 64) // 查询 id
        .storeRef(contentCell)
        toreRef(特许使用费单元)
        ndCell();

    const internalMessage = internal(请注意，
        to collectionAddress,
        值：toNano('0). 5',
        boun: true
        正文：信息正文
    })；

    const internalMessageCell = beginCell()
        tore(storeMessageRelaxed(internalMessage))
        .endCell();
}

main().finally(() => console.log("Exiting...");
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require("tonweb");
const {mnemonicToKeyPair} = require("tonweb-mnemonic");

async function main() {
    const tonweb = new TonWeb(new TonWeb.HttpProvider(
        'https://testnet.toncenter.com/api/v2/jsonRPC', {
            apiKey: 'put your api key'
        })
    );
    const collectionAddress  = new TonWeb.Address('put your collection address');
    const newCollectionMeta = 'put url fol collection meta';
    const newNftCommonMeta = 'put common url for nft meta';
    const royaltyAddress = new TonWeb.Address('put royalty address');

    const collectionMetaCell = new TonWeb.boc.Cell();
    collectionMetaCell.bits.writeUint(1, 8); // we have offchain metadata
    collectionMetaCell.bits.writeString(newCollectionMeta);
    const nftCommonMetaCell = new TonWeb.boc.Cell();
    nftCommonMetaCell.bits.writeUint(1, 8); // we have offchain metadata
    nftCommonMetaCell.bits.writeString(newNftCommonMeta);

    const contentCell = new TonWeb.boc.Cell();
    contentCell.refs.push(collectionMetaCell);
    contentCell.refs.push(nftCommonMetaCell);

    const royaltyCell = new TonWeb.boc.Cell();
    royaltyCell.bits.writeUint(5, 16); // factor
    royaltyCell.bits.writeUint(100, 16); // base
    royaltyCell.bits.writeAddress(royaltyAddress); // this address will receive 5% of each sale

    const messageBody = new TonWeb.boc.Cell();
    messageBody.bits.writeUint(4, 32);
    messageBody.bits.writeUint(0, 64);
    messageBody.refs.push(contentCell);
    messageBody.refs.push(royaltyCell);

    // available wallet types: simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // workchain
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: collectionAddress,
        amount: tonweb.utils.toNano('0.05'),
        seqno: await wallet.methods.seqno().call(),
        payload: messageBody,
        sendMode: 3
    }).send(); // create transfer and send it
}

main().finally(() => console.log("Exiting..."));
```




此外，我们需要在我们的信息中包括特许权使用费信息，因为它们也使用这种代码来改变。 重要的是要注意，不需要在所有地方指定新的值。 例如，如果只需要更改NFT的共同内容，那么所有其他值都可以像以前一样指定。

## 第三方当事方：分散化交易

### 如何发送交换消息到DEX (DeDust)？

DEXs使用不同的协议进行工作。 在这个示例中，我们将与 **DeDust**交互。

- [DeDust 文档](https://docs.edust.io/)。

DeDust有两个交换路径：jeton <-> jetton或 TON <-> jetton。 每个机构都有不同的计划。 要互换，您需要将jettons (或toncoin) 发送到指定的 **vault** 并提供一个特殊的有效载荷。 以下是将珠宝换成珠宝或珠宝换成玉米的计划：

```tlb
swap#e3a0d482 _:SwapStepswap_params:^SwapParams = ForwardPayload;
              step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next :(可能是^ SwapStep) = SwapStepParams;
              swap_params#_ 截止日期:Timestamp receivent_addr:MsgAddressInt referal_addr:MsgAddress
                    complet_payload:(可能是^Cell) reject_payload:(也许是^Cell) = SwapParams;
```

此方案显示了你jettons传输消息的`forward_payload`中的内容(`transfer#0f8a7ea5`)。

和调味宝石互换模式：

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStepswap_params:^SwapParams = InMsgBody;
              步数#_ 池_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next :(可能是^ SwapStep) = SwapStepParams;
              swap_params#_ 截止日期:Timestamp receivent_addr:MsgAddressInt referal_addr:MsgAddress
                    complet_payload:(可能是^Cell) reject_payload:(也许是^Cell) = SwapParams;
```

这是转账主体转账到音调币**保险库**的方案。

首先，您需要知道您要交换的首饰或音币**vault**地址**vault**。 这可以使用 `get_vault_address` 获取合同方法[**Factory**](https://docs.dedust.io/reference/factory) 来完成。 作为一个参数，您需要根据方案传递切片：

```tlb
native$0000 = Asset; // for ton
jetton$0001 workchain_id:int8 address:uint256 = Asset; // for jetton
```

对于交易所本身，我们需要**池** 地址 - 从获取方法 `get_pool_address` 中获得。 作为论据——根据上面的办法，资产分割。 作为回应，两种方法都会返回请求的 **保险库** / **池** 地址的分割。

这足以构建信息。

<Tabs groupId="code-examples">

 <TabItem value="js-ton" label="JS (@ton)">
DEXs使用不同的协议进行工作。 我们需要熟悉关键的概念和一些重要的组成部分，并且还需要了解参与正确进行互换进程的TL-B方案。 在这个教程中，我们处理的是Dedust，它是一个完全在TON中实现的著名DEX。
在DeDust, 我们有一个抽象的资产概念，其中包括任何可交换的资产类型。 对资产类型的抽象简化了交换过程，因为资产类型不重要。 在这种做法中，还将更容易地涵盖额外货币甚至其他链条的资产。

以下是DeDust为资产概念引入的TL-B方案。

```tlb
本土$000 = 资产；// 吨

jetton$0001 workchain_id:int8 address:uint256 = 资产； / 对于任何jetton,address referred to jeton master address

// Upcoming, 尚未实现。
extran_currency$0010 currency_id:int32 = 资产；
```

其次，DeDust引入了三个组件：Vault、Pool和Factory。 这些组成部分是合同或一组合同，负责部分互换过程。 工厂可以寻找其他组件地址(如保险库和池)
并建造其他部件。
保险库负责接收传输消息，持有资产，并且只是通知相应的库“用户A想要交换100X到Y”。

而另一方面，资源库， 负责根据通知其他负责资产Y的保险库的预定义公式计算交换金额， 并告诉它向用户支付一个计算的金额。
交换数额的计算是根据一个数学公式，这意味着我们迄今有两个不同的池，一个称为Volatile。 根据常用的“常产量”公式运作：x \* y = k， 另一种称作稳定交换——对几乎同等价值的资产进行优化（e）。 。USDT / USDC, TON / stTON)。 它使用的公式：x3 \* y + y3 \* x = k。
所以对于每次交换，我们都需要相应的保险库，它只需要实现一个针对不同的资产类型的特定的 API。 DeDust 有三个版本的 Vault, Native Vault - 处理本机硬币 (Toncoin). Jetton Vault - 管理珠宝和货币外币保险库(升起) - 专为TON外币服务。

DeDust 提供了一个特殊的 SDk 来处理合同、组件和API，它是用打字写成的。
足够的理论，让我们建立我们的环境与TON交换一台珠宝。

```bash
npm install --save @ton/core @ton/ton @ton/crypt

```

我们还需要引入DeDust SDK。

```bash
npm install --save @dedust/sdk
```

现在我们需要初始化一些对象。

```typescript
import { Factory, MAINNET_FACTORY_ADDR } from "@dedust/sdk";
import { Address, TonClient4 } from "@ton/ton";

const tonClient = new TonClient4({
  endpoint: "https://mainnet-v4.tonhubapi.com",
});
const factory = tonClient.open(Factory.createFromAddress(MAINNET_FACTORY_ADDR));
//The Factory contract  is used to  locate other contracts.
```

交换过程有一些步骤，例如： 若要与Jetton交换一些TON，我们首先需要找到相应的密码库和 Pool
然后确保部署他们。 对于我们的TON和SCALE，代码如下所示：

```typescript
import { Asset, VaultNative } from "@dedust/sdk";

//Native vault is for TON
const tonVault = tonClient.open(await factory.getNativeVault());
//We use the factory to find our native coin (Toncoin) Vault.
```

下一步是在这里找到相应的资源库(TON和SCALE)

```typescript
import { PoolType } from "@dedust/sdk";

const SCALE_ADDRESS = Address.parse(
  "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE",
);
// master address of SCALE jetton
const TON = Asset.native();
const SCALE = Asset.jetton(SCALE_ADDRESS);

const pool = tonClient.open(
  await factory.getPool(PoolType.VOLATILE, [TON, SCALE]),
);
```

现在我们应当确保这些合同的存在，因为向不活动的合同提供资金可能造成无法挽回的损失。

```typescript
import { ReadinessStatus } from "@dedust/sdk";

// Check if the pool exists:
if ((await pool.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error("Pool (TON, SCALE) does not exist.");
}

// Check if the vault exits:
if ((await tonVault.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error("Vault (TON) does not exist.");
}
```

在此之后，我们可以发送传输信息的数量为 TON

```typescript
import { toNano } from "@ton/core";
import { mnemonicToPrivateKey } from "@ton/crypto";

  if (!process.env.MNEMONIC) {
    throw new Error("Environment variable MNEMONIC is required.");
  }

  const mnemonic = process.env.MNEMONIC.split(" ");

  const keys = await mnemonicToPrivateKey(mnemonic);
  const wallet = tonClient.open(
    WalletContractV3R2.create({
      workchain: 0,
      publicKey: keys.publicKey,
    }),
  );

const sender = wallet.sender(keys.secretKey);

const amountIn = toNano("5"); // 5 TON

await tonVault.sendSwap(sender, {
  poolAddress: pool.address,
  amount: amountIn,
  gasAmount: toNano("0.25"),
});
```

若要与 Y交换令牌X, 这个过程是相同的，例如，我们向保险库X 发送一个数量的 X 令牌。 私密库X
接收我们的资产，持有它并通知池(X, Y) 此地址要求进行一个交换，现在基于
计算的池会通知另一个密码库， 这里的 私密库 Y 发布等效的 Y 向请求交换的用户发布。

资产之间的差异仅仅是关于诸如jettons的转让方法。 我们使用传输消息将它们传送到保险库，并附加一个特定的 forward_payload。 但对于本机硬币，我们向保险库发送了一个交换信息，附加相应数量的TON。

这是TON和jetton的模式：

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStepswap_params:^SwapParams = InMsgBody;
```

所以每个金库和相应的库都是为特定的交换所设计的，并且有一个专门针对特殊资产的特殊API。

它正在与喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式转机。 与珠宝互换珠宝的过程是一样的， 唯一的区别是我们应该提供TL-B方案中描述的有效载荷。

```TL-B
swap#e3a0d482 _:SwapStepswap_params:^SwapParams = ForwardPayload;
```

```typescript
/found Vault
const scaleVault = Client.open(等待工厂.getJettonVault(SCALE_ADDRESS));
```

```typescript
//find jetton address
import { JettonRoot, JettonWallet } from '@dedust/sdk';

const scaleRoot = tonClient.open(JettonRoot.createFromAddress(SCALE_ADDRESS));
const scaleWallet = tonClient.open(await scaleRoot.getWallet(sender.address);

// Transfer jettons to the Vault (SCALE) with corresponding payload

const amountIn = toNano('50'); // 50 SCALE

await scaleWallet.sendTransfer(sender, toNano("0.3"), {
  amount: amountIn,
  destination: scaleVault.address,
  responseAddress: sender.address, // return gas to user
  forwardAmount: toNano("0.25"),
  forwardPayload: VaultJetton.createSwapPayload({ poolAddress }),
});
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

构建资产分割：

```kotlin
val assetASlice = buildcellent ow.
    storUInt(1,4)
    storeint(JETTON_MASTER_A.workchainId, 8)
    storbits(JETTON_MASTER_A.adds)
}.beginparse()
```

运行获取方式：

```kotlin
val responsePool = runBlocking Pow.
    liteClient.runSmcMethod(
        LiteServerAccountId(DEDUST_FACTORY). orkchainId, DEDUST_FACTORY.address),
        "get_pool_address",
        VmStackValue f(0)，
        VmStackValue.of(assetASlice)，
        VmStackValue。 f(cetBSlice)
    (
}
stack = responsePool。 oMutableVmStack()
val point 地址 = stack.popSlice().loadTlb(MsgAddressint) 为 AddrStd
```

构建和传输消息：

```kotlin
runBlocking {
    wallet.transfer(pk, WalletTransfer {
        destination = JETTON_WALLET_A // yours existing jetton wallet
        bounceable = true
        coins = Coins(300000000) // 0.3 ton in nanotons
        messageData = MessageData.raw(
            body = buildCell {
                storeUInt(0xf8a7ea5, 32) // op Transfer
                storeUInt(0, 64) // query_id
                storeTlb(Coins, Coins(100000000)) // amount of jettons
                storeSlice(addrToSlice(jettonAVaultAddress)) // destination address
                storeSlice(addrToSlice(walletAddress))  // response address
                storeUInt(0, 1)  // custom payload
                storeTlb(Coins, Coins(250000000)) // forward_ton_amount // 0.25 ton in nanotons
                storeUInt(1, 1)
                // forward_payload
                storeRef {
                    storeUInt(0xe3a0d482, 32) // op swap
                    storeSlice(addrToSlice(poolAddress)) // pool_addr
                    storeUInt(0, 1) // kind
                    storeTlb(Coins, Coins(0)) // limit
                    storeUInt(0, 1) // next (for multihop)
                    storeRef {
                        storeUInt(System.currentTimeMillis() / 1000 + 60 * 5, 32) // deadline
                        storeSlice(addrToSlice(walletAddress)) // recipient address
                        storeSlice(buildCell { storeUInt(0, 2) }.beginParse()) // referral (null address)
                        storeUInt(0, 1)
                        storeUInt(0, 1)
                        endCell()
                    }
                }
            }
        )
        sendMode = 3
    })
}
```

</TabItem>

<TabItem value="py" label="Python">

这个示例显示了如何将Toncoins转换给犹太人。

```py
from pytoniq import Address, begin_cell, LiteBalancer, WalletV4R2
import time
import asyncio

DEDUST_FACTORY = "EQBfBWT7X2BHg9tXAxzhz2aKiNTU1tpt5NsiK0uSDW_YAJ67"
DEDUST_NATIVE_VAULT = "EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_"

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    JETTON_MASTER = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")  # jetton address swap to
    TON_AMOUNT = 10**9  # 1 ton - swap amount
    GAS_AMOUNT = 10**9 // 4  # 0.25 ton for gas

    pool_type = 0 # Volatile pool type

    asset_native = (begin_cell()
                   .store_uint(0, 4) # Asset type is native
                   .end_cell().begin_parse())
    asset_jetton = (begin_cell()
                   .store_uint(1, 4) # Asset type is jetton
                   .store_uint(JETTON_MASTER.wc, 8)
                   .store_bytes(JETTON_MASTER.hash_part)
                   .end_cell().begin_parse())

    stack = await provider.run_get_method(
        address=DEDUST_FACTORY, method="get_pool_address",
        stack=[pool_type, asset_native, asset_jetton]
    )
    pool_address = stack[0].load_address()
    
    swap_params = (begin_cell()
                  .store_uint(int(time.time() + 60 * 5), 32) # Deadline
                  .store_address(wallet.address) # Recipient address
                  .store_address(None) # Referall address
                  .store_maybe_ref(None) # Fulfill payload
                  .store_maybe_ref(None) # Reject payload
                  .end_cell())
    swap_body = (begin_cell()
                .store_uint(0xea06185d, 32) # Swap op-code
                .store_uint(0, 64) # Query id
                .store_coins(int(1*1e9)) # Swap amount
                .store_address(pool_address)
                .store_uint(0, 1) # Swap kind
                .store_coins(0) # Swap limit
                .store_maybe_ref(None) # Next step for multi-hop swaps
                .store_ref(swap_params)
                .end_cell())

    await wallet.transfer(destination=DEDUST_NATIVE_VAULT,
                          amount=TON_AMOUNT + GAS_AMOUNT, # swap amount + gas
                          body=swap_body)
    
    await provider.close_all()

asyncio.run(main())

```




## 接收信息处理的基础

### 如何解析账户交易(转账、犹太人、NFTs)？

帐户上的交易列表可以通过 `getTransactions` API 方法获取。 它返回一个 `Transaction` 对象的数组，其中每个项目都有很多属性。 然而，最常用的领域是：

- 启动此交易的消息发送者、正文和价值
- 交易哈希和逻辑时间(LT)

_Sender_ 和 _Body_ 字段可用来确定消息类型(常规传输、jetton传输、nft 传输等)。

下面是一个示例，说明您如何在任意区块链账户中获取5个最新交易。 根据类型解析它们并在循环中打印。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, TonClient, beginCell, fromNano } from '@ton/ton';

async function main() {
    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: '1b312c91c3b691255130350a49ac5a0742454725f910756aff94dfe44858388e',
    });

    const myAddress = Address.parse('EQBKgXCNLPexWhs2L79kiARR1phGH1LwXxRbNsCFF9doc2lN'); // address that you want to fetch transactions from

    const transactions = await client.getTransactions(myAddress, {
        limit: 5,
    });

    for (const tx of transactions) {
        const inMsg = tx.inMessage;

        if (inMsg?.info.type == 'internal') {
            // we only process internal messages here because they are used the most
            // for external messages some of the fields are empty, but the main structure is similar
            const sender = inMsg?.info.src;
            const value = inMsg?.info.value.coins;

            const originalBody = inMsg?.body.beginParse();
            let body = originalBody.clone();
            if (body.remainingBits < 32) {
                // if body doesn't have opcode: it's a simple message without comment
                console.log(`Simple transfer from ${sender} with value ${fromNano(value)} TON`);
            } else {
                const op = body.loadUint(32);
                if (op == 0) {
                    // if opcode is 0: it's a simple message with comment
                    const comment = body.loadStringTail();
                    console.log(
                        `Simple transfer from ${sender} with value ${fromNano(value)} TON and comment: "${comment}"`
                    );
                } else if (op == 0x7362d09c) {
                    // if opcode is 0x7362d09c: it's a Jetton transfer notification

                    body.skip(64); // skip query_id
                    const jettonAmount = body.loadCoins();
                    const jettonSender = body.loadAddressAny();
                    const originalForwardPayload = body.loadBit() ? body.loadRef().beginParse() : body;
                    let forwardPayload = originalForwardPayload.clone();

                    // IMPORTANT: we have to verify the source of this message because it can be faked
                    const runStack = (await client.runMethod(sender, 'get_wallet_data')).stack;
                    runStack.skip(2);
                    const jettonMaster = runStack.readAddress();
                    const jettonWallet = (
                        await client.runMethod(jettonMaster, 'get_wallet_address', [
                            { type: 'slice', cell: beginCell().storeAddress(myAddress).endCell() },
                        ])
                    ).stack.readAddress();
                    if (!jettonWallet.equals(sender)) {
                        // if sender is not our real JettonWallet: this message was faked
                        console.log(`FAKE Jetton transfer`);
                        continue;
                    }

                    if (forwardPayload.remainingBits < 32) {
                        // if forward payload doesn't have opcode: it's a simple Jetton transfer
                        console.log(`Jetton transfer from ${jettonSender} with value ${fromNano(jettonAmount)} Jetton`);
                    } else {
                        const forwardOp = forwardPayload.loadUint(32);
                        if (forwardOp == 0) {
                            // if forward payload opcode is 0: it's a simple Jetton transfer with comment
                            const comment = forwardPayload.loadStringTail();
                            console.log(
                                `Jetton transfer from ${jettonSender} with value ${fromNano(
                                    jettonAmount
                                )} Jetton and comment: "${comment}"`
                            );
                        } else {
                            // if forward payload opcode is something else: it's some message with arbitrary structure
                            // you may parse it manually if you know other opcodes or just print it as hex
                            console.log(
                                `Jetton transfer with unknown payload structure from ${jettonSender} with value ${fromNano(
                                    jettonAmount
                                )} Jetton and payload: ${originalForwardPayload}`
                            );
                        }

                        console.log(`Jetton Master: ${jettonMaster}`);
                    }
                } else if (op == 0x05138d91) {
                    // if opcode is 0x05138d91: it's a NFT transfer notification

                    body.skip(64); // skip query_id
                    const prevOwner = body.loadAddress();
                    const originalForwardPayload = body.loadBit() ? body.loadRef().beginParse() : body;
                    let forwardPayload = originalForwardPayload.clone();

                    // IMPORTANT: we have to verify the source of this message because it can be faked
                    const runStack = (await client.runMethod(sender, 'get_nft_data')).stack;
                    runStack.skip(1);
                    const index = runStack.readBigNumber();
                    const collection = runStack.readAddress();
                    const itemAddress = (
                        await client.runMethod(collection, 'get_nft_address_by_index', [{ type: 'int', value: index }])
                    ).stack.readAddress();

                    if (!itemAddress.equals(sender)) {
                        console.log(`FAKE NFT Transfer`);
                        continue;
                    }

                    if (forwardPayload.remainingBits < 32) {
                        // if forward payload doesn't have opcode: it's a simple NFT transfer
                        console.log(`NFT transfer from ${prevOwner}`);
                    } else {
                        const forwardOp = forwardPayload.loadUint(32);
                        if (forwardOp == 0) {
                            // if forward payload opcode is 0: it's a simple NFT transfer with comment
                            const comment = forwardPayload.loadStringTail();
                            console.log(`NFT transfer from ${prevOwner} with comment: "${comment}"`);
                        } else {
                            // if forward payload opcode is something else: it's some message with arbitrary structure
                            // you may parse it manually if you know other opcodes or just print it as hex
                            console.log(
                                `NFT transfer with unknown payload structure from ${prevOwner} and payload: ${originalForwardPayload}`
                            );
                        }
                    }

                    console.log(`NFT Item: ${itemAddress}`);
                    console.log(`NFT Collection: ${collection}`);
                } else {
                    // if opcode is something else: it's some message with arbitrary structure
                    // you may parse it manually if you know other opcodes or just print it as hex
                    console.log(
                        `Message with unknown structure from ${sender} with value ${fromNano(
                            value
                        )} TON and body: ${originalBody}`
                    );
                }
            }
        }
        console.log(`Transaction Hash: ${tx.hash().toString('hex')}`);
        console.log(`Transaction LT: ${tx.lt}`);
        console.log();
    }
}

main().finally(() => console.log('Exiting...'));
```

</TabItem>

<TabItem value="py" label="Python">

```py
from pytoniq import LiteBalancer, begin_cell
import asyncio

async def parse_transactions(transactions):
    for transaction in transactions:
        if not transaction.in_msg.is_internal:
            continue
        if transaction.in_msg.info.dest.to_str(1, 1, 1) != MY_WALLET_ADDRESS:
            continue

        sender = transaction.in_msg.info.src.to_str(1, 1, 1)
        value = transaction.in_msg.info.value_coins
        if value != 0:
            value = value / 1e9
        
        if len(transaction.in_msg.body.bits) < 32:
            print(f"TON transfer from {sender} with value {value} TON")
        else:
            body_slice = transaction.in_msg.body.begin_parse()
            op_code = body_slice.load_uint(32)
            
            # TextComment
            if op_code == 0:
                print(f"TON transfer from {sender} with value {value} TON and comment: {body_slice.load_snake_string()}")
            
            # Jetton Transfer Notification
            elif op_code == 0x7362d09c:
                body_slice.load_bits(64) # skip query_id
                jetton_amount = body_slice.load_coins() / 1e9
                jetton_sender = body_slice.load_address().to_str(1, 1, 1)
                if body_slice.load_bit():
                    forward_payload = body_slice.load_ref().begin_parse()
                else:
                    forward_payload = body_slice
                
                jetton_master = (await provider.run_get_method(address=sender, method="get_wallet_data", stack=[]))[2].load_address()
                jetton_wallet = (await provider.run_get_method(address=jetton_master, method="get_wallet_address",
                                                               stack=[
                                                                        begin_cell().store_address(MY_WALLET_ADDRESS).end_cell().begin_parse()
                                                                     ]))[0].load_address().to_str(1, 1, 1)

                if jetton_wallet != sender:
                    print("FAKE Jetton Transfer")
                    continue
                
                if len(forward_payload.bits) < 32:
                    print(f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton")
                else:
                    forward_payload_op_code = forward_payload.load_uint(32)
                    if forward_payload_op_code == 0:
                        print(f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and comment: {forward_payload.load_snake_string()}")
                    else:
                        print(f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and unknown payload: {forward_payload} ")
            
            # NFT Transfer Notification
            elif op_code == 0x05138d91:
                body_slice.load_bits(64) # skip query_id
                prev_owner = body_slice.load_address().to_str(1, 1, 1)
                if body_slice.load_bit():
                    forward_payload = body_slice.load_ref().begin_parse()
                else:
                    forward_payload = body_slice

                stack = await provider.run_get_method(address=sender, method="get_nft_data", stack=[])
                index = stack[1]
                collection = stack[2].load_address()
                item_address = (await provider.run_get_method(address=collection, method="get_nft_address_by_index",
                                                              stack=[index]))[0].load_address().to_str(1, 1, 1)

                if item_address != sender:
                    print("FAKE NFT Transfer")
                    continue

                if len(forward_payload.bits) < 32:
                    print(f"NFT transfer from {prev_owner}")
                else:
                    forward_payload_op_code = forward_payload.load_uint(32)
                    if forward_payload_op_code == 0:
                        print(f"NFT transfer from {prev_owner} with comment: {forward_payload.load_snake_string()}")
                    else:
                        print(f"NFT transfer from {prev_owner} with unknown payload: {forward_payload}")

                print(f"NFT Item: {item_address}")
                print(f"NFT Collection: {collection}")
        print(f"Transaction hash: {transaction.cell.hash.hex()}")
        print(f"Transaction lt: {transaction.lt}")

MY_WALLET_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"
provider = LiteBalancer.from_mainnet_config(1)

async def main():
    await provider.start_up()
    transactions = await provider.get_transactions(address=MY_WALLET_ADDRESS, count=5)
    await parse_transactions(transactions)
    await provider.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

请注意，这个示例只包括传入信息的最简单的情况，即只需要在单个账户中获取交易信息就够了。 如果您想更深入地处理更复杂的交易链和消息，您应该把`tx.outMessages`字段放入一个帐户。 它包含智能合约在这笔交易结果中发送的输出消息列表。 要更好地理解整个逻辑，您可以阅读这些文章：

- [消息概述](/develop/smart-contracts/guidelines/message-delivery-guarante)
- [内部信息](/develop/smart-contracts/guidelines/internal-messages)

在[付款处理](/develop/dapps/asset-processing)文章中更深入地探讨这个主题。

### 如何找到特定的 TON 连接结果的交易？

TON Connect 2 只返回发送到blockchain的单元格 未生成交易哈希值(因为该交易可能无法通过，如果外部消息丢失或超时)。 不过，BOC提供了让我们能够在我们的帐户历史中搜索这个准确信息。

:::tip
您可以使用索引器使搜索变得更容易。 提供的实现是连接到 RPC 的 `TonClient` 。
:::

准备`retry`函数用于监听区块链的尝试：

```typescript

export async function retry<T>(fn: () => Promise<T>, options: { retries: number, delay: number }): Promise<T> {
  let lastError: Error | undefined;
  for (let i = 0; i < options.retries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (e instanceof Error) {
        lastError = e;
      }
      await new Promise(resolve => setTimeout(resolve, options.delay));
    }
  }
  throw lastError;
}

```

创建监听器函数，在某些帐户上使用特定的传入外部消息进行特定交易，等于正文中的消息：

<Tabs>
<TabItem value="ts" label="@ton/ton">

```typescript

import {Cell, Address, beginCell, storeMessage, TonClient} from "@ton/ton";

const res = tonConnectUI.send(msg); // exBoc in the result of sending message
const exBoc = res.boc;
const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'INSERT YOUR API-KEY', // https://t.me/tonapibot
    });

export async function getTxByBOC(exBoc: string): Promise<string> {

    const myAddress = Address.parse('INSERT TON WALLET ADDRESS'); // Address to fetch transactions from

    return retry(async () => {
        const transactions = await client.getTransactions(myAddress, {
            limit: 5,
        });
        for (const tx of transactions) {
            const inMsg = tx.inMessage;
            if (inMsg?.info.type === 'external-in') {

                const inBOC = inMsg?.body;
                if (typeof inBOC === 'undefined') {

                    reject(new Error('Invalid external'));
                    continue;
                }
                const extHash = Cell.fromBase64(exBoc).hash().toString('hex')
                const inHash = beginCell().store(storeMessage(inMsg)).endCell().hash().toString('hex')

                console.log(' hash BOC', extHash);
                console.log('inMsg hash', inHash);
                console.log('checking the tx', tx, tx.hash().toString('hex'));


                // Assuming `inBOC.hash()` is synchronous and returns a hash object with a `toString` method
                if (extHash === inHash) {
                    console.log('Tx match');
                    const txHash = tx.hash().toString('hex');
                    console.log(`Transaction Hash: ${txHash}`);
                    console.log(`Transaction LT: ${tx.lt}`);
                    return (txHash);
                }
            }
        }
        throw new Error('Transaction not found');
    }, {retries: 30, delay: 1000});
}

 txRes = getTxByBOC(exBOC);
 console.log(txRes);
  

```

</TabItem>

</Tabs>
