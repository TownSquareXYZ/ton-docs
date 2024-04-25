import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TON 开发手册

在产品开发过程中，关于如何与不同的合约进行交互，常常会出现各种问题。

此文档旨在收集所有开发者的最佳实践，并与大家分享。

## Standard operations

<!-- TODO: zoom on click (lightbox?) -->

<img src="/img/interaction-schemes/ecosystem.svg" alt="Full ecosystem scheme"></img>

## Working with contracts' addresses

### 如何转换（用户友好型 <-> 原始格式）、组装和从字符串提取地址？

TON address uniquely identifies contract in blockchain, indicating its workchain and original state hash. [Two common formats](/learn/overviews/addresses#raw-and-user-friendly-addresses) are used: **raw** (workchain and HEX-encoded hash separated with ":" character) and **user-friendly** (base64-encoded with certain flags).

```
用户友好型: EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
原始格式: 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```

要从字符串中获取地址，可以使用以下代码：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address } from "@ton/core";


const address1 = Address.parse('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');
const address2 = Address.parse('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e');

// toStrings 参数：urlSafe, bounceable, testOnly
// 默认值：true, true, false

console.log(address1.toString()); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address1.toRawString()); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

console.log(address2.toString()); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address2.toRawString()); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```


<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require('tonweb');

const address1 = new TonWeb.utils.Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');
const address2 = new TonWeb.utils.Address('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e');

// toString 参数：isUserFriendly, isUrlSafe, isBounceable, isTestOnly

console.log(address1.toString(true, true, true)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address1.toString(isUserFriendly = false)); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

console.log(address1.toString(true, true, true)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address2.toString(isUserFriendly = false)); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```


<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"github.com/xssnick/tonutils-go/address"
)

// 在这里，我们需要手动实现对原始地址的处理，因为库不支持。

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
		return nil, fmt.Errorf("地址长度必须为 32 字节")
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
from pytoniq_core import Address

address1 = Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF')
address2 = Address('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e')

# to_str() 参数：is_user_friendly, is_url_safe, is_bounceable, is_test_only

print(address1.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address1.to_str(is_user_friendly=False))  # 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

print(address2.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address2.to_str(is_user_friendly=False))  # 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```




### What flags are there in user-friendly addresses?

Two flags are defined: **bounceable**/**non-bounceable** and **testnet**/**any-net**. They can be easily detected by looking at the first letter of the address, because it stands for first 6 bits in address encoding, and flags are located there according to [TEP-2](https://github.com/ton-blockchain/TEPs/blob/master/text/0002-address.md#smart-contract-addresses):

| Address beginning |   二进制形式  | 可弹回 | 测试网络 |
| :---------------: | :------: | :-: | :--: |
|         E         | 00010001 |  是  |   否  |
|         U         | 01010001 |  否  |   否  |
|         k         | 10010001 |  是  |   是  |
|         0         | 11010001 |  否  |   是  |

:::tip
Testnet-only flag doesn't have representation in blockchain at all. Non-bounceable flag makes difference only when used as destination address for a transfer: in this case, it [disallows bounce](/develop/smart-contracts/guidelines/non-bouncable-messages) for a message sent; address in blockchain, again, does not contain this flag.
:::

Also, in some libraries, you may notice a serialization parameter called `urlSafe`. 用户友好型地址采用 base64 编码，而原始格式地址采用 hex 编码。在原始格式中，地址所在的工作链单独写在“:”字符之前，字符的大小写不重要。 此外，在某些库中，你可能会注意到一个称为“url safe”的字段。事实是，base64 格式不是 url 安全的，这意味着在链接中传输这个地址时可能会出现问题。当 urlSafe = true 时，所有的 `+` 符号被替换为 `-`，所有的 `/` 符号被替换为 `_`。您可以使用以下代码获得这些地址格式： 在 TON 上，根据服务的不同，地址可以以两种格式出现：`用户友好型` 和 `原始格式`。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address } from "@ton/core";

const address = Address.parse('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');

// toStrings 参数：urlSafe, bounceable, testOnly
// 默认值：true, true, false

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

// toString 参数：isUserFriendly, isUrlSafe, isBounceable, isTestOnly

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
from pytoniq_core import Address

address = Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF')

# to_str() 参数：is_user_friendly, is_url_safe, is_bounceable, is_test_only

print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=False))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=False, is_test_only=False))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff+W72r5gqPrHF
print(address.to_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True, is_test_only=False))  # UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=True))  # kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
print(address.to_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True, is_test_only=True))  # 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
```




## Standard wallets in TON ecosystem

### 如何发送标准 TON 转账消息？ How to send a text message to other wallet?

<img src="/img/interaction-schemes/wallets.svg" alt="Wallet operations scheme"></img>

Most SDKs provide the following process for sending messages from your wallet:

- You create wallet wrapper (object in your program) of a correct version (in most cases, v3r2; see also [wallet versions](/participate/wallets/contracts)), using secret key and workchain (usually 0, which stands for [basechain](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules)).
- You also create blockchain wrapper, or "client" - object that will route requests to API or liteservers, whichever you choose.
- Then, you _open_ contract in the blockchain wrapper. This means contract object is no longer abstract and represents actual account in either TON mainnet or testnet.
- After that, you can form messages you want and send them. You can also send up to 4 messages per request, as described in an [advanced manual](/develop/smart-contracts/tutorials/wallet#sending-multiple-messages-simultaneously).

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { TonClient, WalletContractV4, internal } from "@ton/ton";
import { mnemonicNew, mnemonicToPrivateKey } from "@ton/crypto";

const client = new TonClient({
  endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC',
});

// 将助记词转换成私钥
let mnemonics = "word1 word2 ...".split(" ");
let keyPair = await mnemonicToPrivateKey(mnemonics);

// 创建钱包合约
let workchain = 0; // 通常你需要一个workchain 0
let wallet = WalletContractV4.create({ workchain, publicKey: keyPair.publicKey });
let contract = client.open(wallet);

// 创建转账
let seqno: number = await contract.getSeqno();
await contract.sendTransfer({
  seqno,
  secretKey: keyPair.secretKey,
  messages: [internal({
    value: '1',
    to: 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
    body: '转账示例内容',
  })]
});
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

```kotlin
// 设置liteClient
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
        coins = Coins(100000000) // 1 ton 的 nanotons
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
from pytoniq import LiteBalancer, WalletV4R2
import asyncio

mnemonics = ["你的", "助记词", "在这里"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
    DESTINATION_ADDRESS = "目的地址在这里"


    await wallet.transfer(destination=DESTINATION_ADDRESS, amount=int(0.05*1e9), body="转账示例内容")
	await client.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

### Writing comments: long strings in snake format

有时候，在cell最多可以包含 **1023位** 的情况下，需要存储长字符串（或其他大型信息）。这种情况下，我们可以使用 蛇形cells。蛇形cells 是包含对另一个cell的引用的cell，而该cell又包含对另一个cell的引用，依此类推。 In this case, we can use snake cells. Snake cells are cells that contain a reference to another cell, which, in turn, contains a reference to another cell, and so on.

<Tabs groupId="code-examples">
<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require("tonweb");

function writeStringTail(str, cell) {
    const bytes = Math.floor(cell.bits.getFreeBits() / 8); // 1字符 = 8位
    if(bytes < str.length) { // 如果我们不能写下所有字符串
        cell.bits.writeString(str.substring(0, bytes)); // 写入字符串的一部分
        const newCell = writeStringTail(str.substring(bytes), new TonWeb.boc.Cell()); // 创建新cell
        cell.refs.push(newCell); // 将新cell添加到当前cell的引用中
    } else {
        cell.bits.writeString(str); // 写下所有字符串
    }

    return cell;
}

function readStringTail(cell) {
    const slice = cell.beginParse(); // 将cell转换为切片
    if(cell.refs.length > 0) {
        const str = new TextDecoder('ascii').decode(slice.array); // 解码 uint8array 为字符串
        return str + readStringTail(cell.refs[0]); // 读取下一个cell
    } else {
        return new TextDecoder('ascii').decode(slice.array);
    }
}

let cell = new TonWeb.boc.Cell();
const str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In euismod, ligula vel lobortis hendrerit, lectus sem efficitur enim, vel efficitur nibh dui a elit. Quisque augue nisi, vulputate vitae mauris sit amet, iaculis lobortis nisi. Aenean molestie ultrices massa eu fermentum. Cras rhoncus ipsum mauris, et egestas nibh interdum in. Maecenas ante ipsum, sodales eget suscipit at, placerat ut turpis. Nunc ac finibus dui. Donec sit amet leo id augue tempus aliquet. Vestibulum eu aliquam ex, sit amet suscipit odio. Vestibulum et arcu dui.";
cell = writeStringTail(str, cell);
const text = readStringTail(cell);
console.log(text);
```




Many SDKs already have functions responsible for parsing and storing long strings. In others, you can work with such cells using recursion, or possibly optimize it out (trick known as "tail calls").

Don't forget that comment message has 32 zero bits (one may say, that its opcode is 0)!

## TEP-74 (Jettons Standard)

<img src="/img/interaction-schemes/jettons.svg" alt="Jetton operations scheme"></img>

### 如何计算用户的 Jetton 钱包地址？

为了计算用户的Jetton钱包地址，我们需要调用jetton主合约的"get_wallet_address" get方法，并实际传入用户地址。对于这项任务，我们可以轻松使用JettonMaster的getWalletAddress方法或者自行调用主合约。 要发送标准TON转账消息，首先需要打开您的钱包合约，之后获取您的钱包序列号（seqno）。只有完成这些步骤之后，您才能发送您的TON转账。请注意，如果您使用的是非V4版本的钱包，您需要将WalletContractV4重命名为WalletContract{您的钱包版本}，例如，WalletContractV3R2。

:::info
`JettonMaster` in `@ton/ton` lacks much functionality but has _this one_ present, fortunately.
:::

<Tabs groupId="code-examples">
<TabItem value="user-jetton-wallet-method-js" label="@ton/ton">

```js
const { Address, beginCell } = require("@ton/core")
const { TonClient, JettonMaster } = require("@ton/ton")

const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
});

const jettonMasterAddress = Address.parse('...') // 例如 EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE
const userAddress = Address.parse('...')

const jettonMaster = client.open(JettonMaster.create(jettonMasterAddress))
console.log(await jettonMaster.getWalletAddress(userAddress))
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

    const response = await client.runMethod(jettonMasterAddress, "get_wallet_address", [{type: "slice", cell: userAddressCell}])
    return response.stack.readAddress()
}
const jettonMasterAddress = Address.parse('...') // 例如 EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE
const userAddress = Address.parse('...')

getUserWalletAddress(userAddress, jettonMasterAddress)
    .then((userJettonWalletAddress) => {
        console.log(userJettonWalletAddress)
    }
)
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

```kotlin
// 设置liteClient
val context: CoroutineContext = Dispatchers.Default
val json = Json { ignoreUnknownKeys = true }
val config = json.decodeFromString<LiteClientConfigGlobal>(
    URI("https://ton.org/global-config.json").toURL().readText()
)
val liteClient = LiteClient(context, config)

val USER_ADDR = AddrStd("钱包地址")
val JETTON_MASTER = AddrStd("Jetton主合约地址") // 例如 EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE

// 我们需要以切片形式发送常规钱包地址
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
println("计算的Jetton钱包:")
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
    print(f"用户{USER_ADDRESS}的Jetton钱包地址: {jetton_wallet.to_str(1, 1, 1)}")
	await provider.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

### How to calculate user's Jetton wallet address (offline)?

Calling the GET method every time to get the wallet address can take a lot of time and resources. If we know the Jetton Wallet code and its storage structure in advance, we can get the wallet address without any network requests.

You can get the code using Tonviewer. Let's take `jUSDT` as an example, the Jetton Master address is `EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA`. If we [go to this address](https://tonviewer.com/EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA?section=method) and open the Methods tab, we can see that there is already a `get_jetton_data` method there. By calling it, we can get the hex form of the cell with the Jetton Wallet code:

```
b5ee9c7201021301000385000114ff00f4a413f4bcf2c80b0102016202030202cb0405001ba0f605da89a1f401f481f481a9a30201ce06070201580a0b02f70831c02497c138007434c0c05c6c2544d7c0fc07783e903e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7c076cf16cc8d0d0d09208403e29fa96ea68c1b088d978c4408fc06b809208405e351466ea6cc1b08978c840910c03c06f80dd6cda0841657c1ef2ea7c09c6c3cb4b01408eebcb8b1807c073817c160080900113e910c30003cb85360005c804ff833206e953080b1f833de206ef2d29ad0d30731d3ffd3fff404d307d430d0fa00fa00fa00fa00fa00fa00300008840ff2f00201580c0d020148111201f70174cfc0407e803e90087c007b51343e803e903e903534544da8548b31c17cb8b04ab0bffcb8b0950d109c150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c032481c007e401d3232c084b281f2fff274013e903d010c7e800835d270803cb8b13220060072c15401f3c59c3e809dc072dae00e02f33b51343e803e903e90353442b4cfc0407e80145468017e903e9014d771c1551cdbdc150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c0325c007e401d3232c084b281f2fff2741403f1c147ac7cb8b0c33e801472a84a6d8206685401e8062849a49b1578c34975c2c070c00870802c200f1000aa13ccc88210178d4519580a02cb1fcb3f5007fa0222cf165006cf1625fa025003cf16c95005cc2391729171e25007a813a008aa005004a017a014bcf2e2c501c98040fb004300c85004fa0258cf1601cf16ccc9ed5400725269a018a1c882107362d09c2902cb1fcb3f5007fa025004cf165007cf16c9c8801001cb0527cf165004fa027101cb6a13ccc971fb0050421300748e23c8801001cb055006cf165005fa027001cb6a8210d53276db580502cb1fcb3fc972fb00925b33e24003c85004fa0258cf1601cf16ccc9ed5400eb3b51343e803e903e9035344174cfc0407e800870803cb8b0be903d01007434e7f440745458a8549631c17cb8b049b0bffcb8b0b220841ef765f7960100b2c7f2cfc07e8088f3c58073c584f2e7f27220060072c148f3c59c3e809c4072dab33260103ec01004f214013e809633c58073c5b3327b55200087200835c87b51343e803e903e9035344134c7c06103c8608405e351466e80a0841ef765f7ae84ac7cbd34cfc04c3e800c04e81408f214013e809633c58073c5b3327b5520
```

Now, knowing the Jetton Wallet code, the Jetton Master address and the vault structure, we can manually calculate the wallet address:

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




Most major tokens do not have a different storage structure because they use [a standard implementation of the TEP-74 standard](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc). The exception is the new [Jetton-with-governance contracts](https://github.com/ton-blockchain/stablecoin-contract) for centralized stablecoins. In these, the difference is [the presence of a wallet status field and the absence of a code cell in the vault](https://github.com/ton-blockchain/stablecoin-contract/blob/7a22416d4de61336616960473af391713e100d7b/contracts/jetton-utils.fc#L3-L12).

### 如何构建带有评论的 jetton 转账消息？

为了理解如何构建 token 转账消息，我们使用 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md#1-transfer)，该标准描述了 token 标准。需要注意的是，每个 token 可以有自己的 `decimals`，默认值为 `9`。因此，在下面的示例中，我们将数量乘以 10^9。如果小数位数不同，您**需要乘以不同的值**。

:::warning
When displayed, token doesn't usually show count of indivisible units user has; rather, amount is divided by `10 ^ decimals`. This value is commonly set to `9`, and this allows us to use `toNano` function. If decimals were different, we would **need to multiply by a different value** (for instance, if decimals are 6, then we would end up transferring thousand times the amount we wanted).

Of course, one can always do calculation in indivisible units.
:::

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";

async function main() {
    const jettonWalletAddress = Address.parse('put your jetton wallet address');
    const destinationAddress = Address.parse('put destination wallet address');

    const forwardPayload = beginCell()
        .storeUint(0, 32) // 0 opcode 意味着我们有一个评论
        .storeStringTail('Hello, TON!')
        .endCell();

    const messageBody = beginCell()
        .storeUint(0x0f8a7ea5, 32) // jetton 转账的 opcode
        .storeUint(0, 64) // query id
        .storeCoins(toNano(5)) // jetton 数量，数量 * 10^9
        .storeAddress(destinationAddress)
        .storeAddress(destinationAddress) // 响应目的地
        .storeBit(0) // 无自定义有效负载
        .storeCoins(toNano('0.02')) // 转发金额
        .storeBit(1) // 我们将 forwardPayload 作为引用存储
        .storeRef(forwardPayload)
        .endCell();

    const internalMessage = internal({
        to: jettonWalletAddress,
        value: toNano('0.1'),
        bounce: true,
        body: messageBody
    });
    const internalMessageCell = beginCell()
        .store(storeMessageRelaxed(internalMessage))
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
    forwardPayload.bits.writeUint(0, 32); // 0 opcode 意味着我们有一个评论
    forwardPayload.bits.writeString('Hello, TON!');

    /*
        Tonweb 有一个内置的用于与 jettons 互动的类(class)，它有一个创建转账的方法。
        然而，它有缺点，所以我们手动创建消息体。此外，这种方式让我们更好地理解了
        存储的内容和它的功能是什么。
     */

    const jettonTransferBody = new TonWeb.boc.Cell();
    jettonTransferBody.bits.writeUint(0xf8a7ea5, 32); // jetton 转账的 opcode
    jettonTransferBody.bits.writeUint(0, 64); // query id
    jettonTransferBody.bits.writeCoins(new TonWeb.utils.BN('5')); // jetton 数量，数量 * 10^9
    jettonTransferBody.bits.writeAddress(destinationAddress);
    jettonTransferBody.bits.writeAddress(destinationAddress); // 响应目的地
    jettonTransferBody.bits.writeBit(false); // 无自定义有效载荷
    jettonTransferBody.bits.writeCoins(TonWeb.utils.toNano('0.02')); // 转发金额
    jettonTransferBody.bits.writeBit(true); // 我们将 forwardPayload 作为引用存储
    jettonTransferBody.refs.push(forwardPayload);

    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const jettonWallet = new TonWeb.token.ft.JettonWallet(tonweb.provider, {
        address: 'put your jetton wallet address'
    });

    // 可用钱包类型：simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // 工作链
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: jettonWallet.address,
        amount: tonweb.utils.toNano('0.1'),
        seqno: await wallet.methods.seqno().call(),
        payload: jettonTransferBody,
        sendMode: 3
    }).send(); // 创建转账并发送
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
                                                        stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()]))[0]
    forward_payload = (begin_cell()
                      .store_uint(0, 32) # 文本评论 op-code
                      .store_snake_string("Comment")
                      .end_cell())
    transfer_cell = (begin_cell()
                    .store_uint(0xf8a7ea5, 32)          # Jetton 转账 op-code
                    .store_uint(0, 64)                  # query_id
                    .store_coins(1)                     # 要转账的 Jetton 数量，以 nanojetton 计
                    .store_address(DESTINATION_ADDRESS) # 目标地址
                    .store_address(USER_ADDRESS)        # 响应地址
                    .store_bit(0)                       # 自定义有效负载为空
                    .store_coins(1)                     # TON 转发金额，以 nanoton 计
                    .store_bit(1)                       # 将 forward_payload 作为引用存储
                    .store_ref(forward_payload)         # 转发有效负载
                    .end_cell())

    await wallet.transfer(destination=USER_JETTON_WALLET, amount=int(0.05*1e9), body=transfer_cell)
	await client.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

If `forward_amount` is nonzero, a notification regarding jetton reception is sent to destination contract, as can be seen in the scheme in the top of this section. If `response_destination` address is not null, toncoins left (they're called "excesses") are sent to that address.

:::tip
Explorers support comments in jetton notifications as well as in common TON transfers. Their format is 32 zero bits and then text, preferably UTF-8.
:::

:::tip
Jetton transfers need careful consideration for fees and amounts behind outgoing messages. For instance, if you "call" transfer with 0.2 TON, you won't be able to forward 0.1 TON and receive 0.1 TON in excess return message.
:::

## TEP-62 (NFT Standard)

<img src="/img/interaction-schemes/nft.svg" alt="NFT ecosystem scheme"></img>

NFT collections are very different. Actually, NFT contract on TON can be defined as "contract that has appropriate get-method and returns valid metadata". Transfer operation is standartized and quite analogous to [jetton's one](/develop/dapps/cookbook#how-to-construct-a-message-for-a-jetton-transfer-with-a-comment), so we will not dive into it and rather see additional capabilities provided by most collections you may meet!

:::warning
Reminder: all methods about NFT below are not bound by TEP-62 to work. Before trying them, please check if your NFT or collection will process those messages in an expected way. Wallet app emulation may prove useful in this case.
:::

### 如何使用 NFT 批量部署?

集合的智能合约允许在单个交易中部署多达250个NFT。但是，实际上，由于1ton的计算费用限制，这个最大数量在100到130个NFT之间。为此，我们需要在字典中存储有关新NFT的信息。 However, it's essential to consider that, in practice, this maximum is around 100-130 NFTs due to the computation fee limit of 1 ton. To achieve this, we need to store information about the new NFTs in a dictionary.

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, Cell, Dictionary, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";
import { TonClient } from "@ton/ton";

async function main() {
    const collectionAddress = Address.parse('put your collection address');
   	const nftMinStorage = '0.05';
    const client = new TonClient({
        endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC' // 对于Testnet
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




To begin with, let's assume that the minimum amount of TON for the storage fee is `0.05`. This means that after deploying an NFT, the smart contract of the collection will send this much TON to its balance. Next, we obtain arrays with the owners of the new NFTs and their content. Afterward, we get the `next_item_index` using the GET method `get_collection_data`.

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
		我们需要编写自定义的序列化和反序列化
		函数来正确地在字典中存储数据，因为库中的
		内置函数不适合我们的案例。
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
    const internalMessageCell = beginCell()
        .store(storeMessageRelaxed(internalMessage))
        .endCell();
}

main().finally(() => console.log("Exiting..."));
```




Next, we need to correctly calculate the total transaction cost. The value of `0.015` was obtained through testing, but it can vary for each case. This mainly depends on the content of the NFT, as an increase in content size results in a higher **forward fee** (the fee for delivery).

### 如何更改集合的智能合约所有者？

Changing the owner of a collection is very simple. 更改集合的所有者非常简单。要做到这一点，你需要指定 **opcode = 3**，任何 query_id，以及新所有者的地址：

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";

async function main() {
    const collectionAddress = Address.parse('put your collection address');
    const newOwnerAddress = Address.parse('put new owner wallet address');

    const messageBody = beginCell()
        .storeUint(3, 32) // 改变所有者的opcode
        .storeUint(0, 64) // query id
        .storeAddress(newOwnerAddress)
        .endCell();

    const internalMessage = internal({
        to: collectionAddress,
        value: toNano('0.05'),
        bounce: true,
        body: messageBody
    });
    const internalMessageCell = beginCell()
        .store(storeMessageRelaxed(internalMessage))
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
    messageBody.bits.writeUint(3, 32); // 改变所有者的opcode
    messageBody.bits.writeUint(0, 64); // query id
    messageBody.bits.writeAddress(newOwnerAddress);

    // 可选的钱包类型有: simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // 工作链
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: collectionAddress,
        amount: tonweb.utils.toNano('0.05'),
        seqno: await wallet.methods.seqno().call(),
        payload: messageBody,
        sendMode: 3
    }).send(); // 创建并发送转账
}

main().finally(() => console.log("Exiting..."));
```




### 如何更改集合智能合约中的内容？

要更改智能合约集合的内容，我们需要了解它是如何存储的。集合将所有内容存储在一个单一的cell中，其中包含两个cell：**集合内容** 和 **NFT 通用内容**。第一个cell包含集合的元数据，而第二个cell包含NFT元数据的基本URL。 The collection stores all the content in a single cell, inside of which there are two cells: **collection content** and **NFT common content**. The first cell contains the collection's metadata, while the second one contains the base URL for the NFT metadata.

通常，集合的元数据存储格式类似于 `0.json` 并且继续递增，而这个文件之前的地址保持不变。正是这个地址应该存储在NFT通用内容中。 It is this address that should be stored in the NFT common content.

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";

async function main() {
    const collectionAddress = Address.parse('put your collection address');
    const newCollectionMeta = 'put url fol collection meta';
    const newNftCommonMeta = 'put common url for nft meta';
    const royaltyAddress = Address.parse('put royalty address');

    const collectionMetaCell = beginCell()
        .storeUint(1, 8) // 我们拥有链下元数据
        .storeStringTail(newCollectionMeta)
        .endCell();
    const nftCommonMetaCell = beginCell()
        .storeUint(1, 8) // 我们拥有链下元数据
        .storeStringTail(newNftCommonMeta)
        .endCell();

    const contentCell = beginCell()
        .storeRef(collectionMetaCell)
        .storeRef(nftCommonMetaCell)
        .endCell();

    const royaltyCell = beginCell()
        .storeUint(5, 16) // factor
        .storeUint(100, 16) // base
        .storeAddress(royaltyAddress) // 该地址将接收每次销售金额的5%
        .endCell();

    const messageBody = beginCell()
        .storeUint(4, 32) // 更改内容的 opcode
        .storeUint(0, 64) // query id
        .storeRef(contentCell)
        .storeRef(royaltyCell)
        .endCell();

    const internalMessage = internal({
        to: collectionAddress,
        value: toNano('0.05'),
        bounce: true,
        body: messageBody
    });

    const internalMessageCell = beginCell()
        .store(storeMessageRelaxed(internalMessage))
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
        'https://testnet.toncenter.com/api/v2/jsonRPC', {
            apiKey: 'put your api key'
        })
    );
    const collectionAddress  = new TonWeb.Address('put your collection address');
    const newCollectionMeta = 'put url fol collection meta';
    const newNftCommonMeta = 'put common url for nft meta';
    const royaltyAddress = new TonWeb.Address('put royalty address');

    const collectionMetaCell = new TonWeb.boc.Cell();
    collectionMetaCell.bits.writeUint(1, 8); // 我们拥有链下元数据
    collectionMetaCell.bits.writeString(newCollectionMeta);
    const nftCommonMetaCell = new TonWeb.boc.Cell();
    nftCommonMetaCell.bits.writeUint(1, 8); // 我们拥有链下元数据
    nftCommonMetaCell.bits.writeString(newNftCommonMeta);

    const contentCell = new TonWeb.boc.Cell();
    contentCell.refs.push(collectionMetaCell);
    contentCell.refs.push(nftCommonMetaCell);

    const royaltyCell = new TonWeb.boc.Cell();
    royaltyCell.bits.writeUint(5, 16); // factor
    royaltyCell.bits.writeUint(100, 16); // base
    royaltyCell.bits.writeAddress(royaltyAddress); // 该地址将接收每次销售金额的5%

    const messageBody = new TonWeb.boc.Cell();
    messageBody.bits.writeUint(4, 32);
    messageBody.bits.writeUint(0, 64);
    messageBody.refs.push(contentCell);
    messageBody.refs.push(royaltyCell);

    // 可选的钱包类型有: simpleR1, simpleR2, simpleR3,
    // v2R1, v2R2, v3R1, v3R2, v4R1, v4R2
    const keyPair = await mnemonicToKeyPair('put your mnemonic'.split(' '));
    const wallet = new tonweb.wallet.all['v4R2'](tonweb.provider, {
        publicKey: keyPair.publicKey,
        wc: 0 // 工作链
    });

    await wallet.methods.transfer({
        secretKey: keyPair.secretKey,
        toAddress: collectionAddress,
        amount: tonweb.utils.toNano('0.05'),
        seqno: await wallet.methods.seqno().call(),
        payload: messageBody,
        sendMode: 3
    }).send(); // 创建并发送转账
}

main().finally(() => console.log("Exiting..."));
```




Additionally, we need to include royalty information in our message, as they also change using this opcode. It's important to note that it's not necessary to specify new values everywhere. If, for example, only the NFT common content needs to be changed, then all other values can be specified as they were before.

## Third-party: Decentralized Exchanges (DEX)

### 如何向 DEX(DeDust)发送交换(swap)信息？

DEXs use different protocols for their work. In this example we will interact with **DeDust**.

- [DeDust文档](https://docs.dedust.io/)。

DEX使用不同的协议来进行交易。在这个例子中，我们将与**DeDust**交互。 Each has a different scheme. 接下来，我们需要正确计算总交易费用。通过测试得知`0.015`值，但每个案例可能会有所不同。主要取决于NFT的内容，内容的增加导致更高的**转发费**（交付费）。 DeDust有两种交换路径：jetton <-> jetton 或 toncoin <-> jetton。每种都有不同的方案。要进行交换，您需要将jettons（或toncoin）发送到特定的**vault**并提供特殊的有效负载。以下是将jetton交换为jetton或jetton交换为toncoin的方案：

```tlb
swap#e3a0d482 _:SwapStep swap_params:^SwapParams = ForwardPayload;
              step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;
              swap_params#_ deadline:Timestamp recipient_addr:MsgAddressInt referral_addr:MsgAddress
                    fulfill_payload:(Maybe ^Cell) reject_payload:(Maybe ^Cell) = SwapParams;
```

此方案显示了您的jettons转账消息（`transfer#0f8a7ea5`）的`forward_payload`中应包含的内容。

以及toncoin到jetton交换的方案：

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
              step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;
              swap_params#_ deadline:Timestamp recipient_addr:MsgAddressInt referral_addr:MsgAddress
                    fulfill_payload:(Maybe ^Cell) reject_payload:(Maybe ^Cell) = SwapParams;
```

这是向toncoin **vault**转账的方案。

首先，您需要知道您要交换的jettons的**vault**地址或toncoin **vault**地址。可以通过合约[**Factory**](https://docs.dedust.io/reference/factory)的`get_vault_address`方法来完成。您需要按照下面的方案传递一个切片： This can be done using the `get_vault_address` get method of the contract [**Factory**](https://docs.dedust.io/reference/factory). As an argument you need to pass a slice according to the scheme:

```tlb
native$0000 = Asset; // 用于ton
jetton$0001 workchain_id:int8 address:uint256 = Asset; // 用于jetton
```

此外，对于交换本身，我们需要**pool**地址 - 可以通过get方法`get_pool_address`获得。至于参数 - 根据上述方案的资产切片。作为响应，这两个方法都将返回所请求的**vault** / **pool**地址的切片。 As arguments - asset slices according to the scheme above. In response, both methods will return a slice of the address of the requested **vault** / **pool**.

这足以构建消息。

<Tabs groupId="code-examples">

 <TabItem value="js-ton" label="JS (@ton)">
DEXs use different protocols for their work, we need to familiarize ourselves with key concepts and some vital components and also know the TL-B schema involved in doing our swap process correctly. In this tutorial, we deal with DeDust, one of the famous DEX implemented entirely in TON.
In DeDust, we have an abstract Asset concept that includes any swappable asset types. Abstraction over asset types simplifies the swap process because the type of asset does not matter, and extra currency or even assets from other chains in this approach will be covered with ease.

以下是DeDust为Asset概念引入的TL-B模式。

```tlb
native$0000 = Asset; // 用于ton

jetton$0001 workchain_id:int8 address:uint256 = Asset; // 用于任何jetton，地址指的是jetton主地址

// 即将推出，尚未实现。
extra_currency$0010 currency_id:int32 = Asset;
```

Next, DeDust introduced three components, Vault, Pool, and Factory. These components are contracts or groups of contracts and are responsible for parts of the swap process. The factory acts as finding other component addresses (like vault, and pool)
and also building other components.
接下来，DeDust引入了三个组件，Vault，Pool和Factory。这些组件是合约或合约组，并且负责j交换过程的部分。Factory充当寻找其他组件地址（如vault和pool）的角色，并且还构建其他组件。
Vault负责接收转账消息，持有资产，只是通知相应的Pool，"用户A想要将100 X换成Y"。

Pool, on the other hand, is responsible for calculating the swap amount based on the predefined formula informing other Vault that are responsible for asset Y, and telling it to pay a calculated amount to the user.
另一方面，Pool负责根据预定义公式计算交换金额，通知负责资产Y的其他Vault，并告诉它支付给用户计算出的金额。
交换金额的计算基于数学公式，这意味着到目前为止我们有两种不同的pool，一种被称为Volatile，它基于常用的“恒定产品”公式运作：x \* y = k，另一种被称为Stable-Swap - 为近等值资产（例如USDT / USDC，TON / stTON）优化。它使用公式：x3 \* y + y3 \* x = k。
所以对于每次交换，我们需要相应的Vault，它只需要实现一个为与特定资产类型交互而定制的特定API。DeDust有三种Vault的实现，Native Vault - 处理原生代币（Toncoin）。Jetton Vault - 管理jettons和Extra-Currency Vault（即将推出）- 为TON额外代币设计。 It uses the formula: x3 \* y + y3 \* x = k.
另外，我们需要在消息中包含版权信息，因为使用这个 opcode 时，它们也会改变。需要注意的是，不是一定要在所有地方指定新值。例如，如果只需要更改NFT通用内容，则所有其他值可以按照之前的指定。 DeDust has three implementations of Vault, Native Vault - Handles the native coin (Toncoin). Jetton Vault - Manages jettons and Extra-Currency Vault (upcoming) - Designed for TON extra-currencies.

DeDust提供了一个特殊的SDk来处理合约、组件和API，它是用typescript编写的。
足够的理论，让我们设置环境以交换一个jetton和TON。
Enough theory, let's set up our environment to swap one jetton with TON.

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
//Factory合约用于定位其他合约。
```

交换过程有一些步骤，例如，要用Jetton交换一些TON，我们首先需要找到相应的Vault和Pool
然后确保它们已部署。对于我们的示例TON和SCALE，代码如下： For our example TON and SCALE, the code is as follows :

```typescript
import { Asset, VaultNative } from "@dedust/sdk";

//Native vault是用于TON的
const tonVault = tonClient.open(await factory.getNativeVault());
//我们使用factory来找到我们的原生代币（Toncoin）Vault。
```

下一步是找到相应的Pool，这里是（TON和SCALE）

```typescript
import { PoolType } from "@dedust/sdk";

const SCALE_ADDRESS = Address.parse(
  "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE",
);
// SCALE jetton的主地址
const TON = Asset.native();
const SCALE = Asset.jetton(SCALE_ADDRESS);

const pool = tonClient.open(
  await factory.getPool(PoolType.VOLATILE, [TON, SCALE]),
);
```

现在我们应该确保这些合约存在，因为向一个未激活的合约发送资金可能导致无法找回的损失。

```typescript
import { ReadinessStatus } from "@dedust/sdk";

// 检查pool是否存在：
if ((await pool.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error("Pool (TON, SCALE) 不存在。");
}

// 检查vault是否存在：
if ((await tonVault.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error("Vault (TON) 不存在。");
}
```

之后，我们可以发送带有TON数量的转账消息

```typescript
import { toNano } from "@ton/core";
import { mnemonicToPrivateKey } from "@ton/crypto";

  if (!process.env.MNEMONIC) {
    throw new Error("需要环境变量MNEMONIC。");
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

要用Y交换Token X，流程相同，例如，我们向Vault X发送X token的数量，Vault X接收我们的资产，持有它，并通知（X，Y）pool这个地址请求交换，然后Pool根据计算通知另一个Vault，这里Vault Y向请求交换的用户释放等价的Y。

资产之间的差异只是关于转账方法的问题，例如，对于jettons，我们使用转账消息将它们转入Vault，并附加特定的forward_payload，但对于原生代币，我们发送交换消息到Vault，附加相应数量的TON。

这是TON和jetton的模式：

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
```

因此，每个vault和相应的Pool都针对特定的交换设计，并具有为特定资产量身定做的特殊API。

This was swapping TON with jetton SCALE. 这是使用jetton SCALE交换TON的过程。jetton与jetton交换的过程是相同的，唯一的区别是我们应提供TL-B模式中描述的有效负载。

```TL-B
swap#e3a0d482 _:SwapStep swap_params:^SwapParams = ForwardPayload;
```

```typescript
//寻找Vault
const scaleVault = tonClient.open(await factory.getJettonVault(SCALE_ADDRESS));
```

```typescript
//寻找jetton地址
import { JettonRoot, JettonWallet } from '@dedust/sdk';

const scaleRoot = tonClient.open(JettonRoot.createFromAddress(SCALE_ADDRESS));
const scaleWallet = tonClient.open(await scaleRoot.getWallet(sender.address);

// 将jettons转移到Vault（SCALE）并附上相应的有效负载

const amountIn = toNano('50'); // 50 SCALE

await scaleWallet.sendTransfer(sender, toNano("0.3"), {
  amount: amountIn,
  destination: scaleVault.address,
  responseAddress: sender.address, // 将gas返回给用户
  forwardAmount: toNano("0.25"),
  forwardPayload: VaultJetton.createSwapPayload({ poolAddress }),
});
```

</TabItem>

<TabItem value="ton-kotlin" label="ton-kotlin">

构建资源片段：

```kotlin
val assetASlice = buildCell {
    storeUInt(1,4)
    storeInt(JETTON_MASTER_A.workchainId, 8)
    storeBits(JETTON_MASTER_A.address)
}.beginParse()
```

执行获取方法：

```kotlin
val responsePool = runBlocking {
    liteClient.runSmcMethod(
        LiteServerAccountId(DEDUST_FACTORY.workchainId, DEDUST_FACTORY.address),
        "get_pool_address",
        VmStackValue.of(0),
        VmStackValue.of(assetASlice),
        VmStackValue.of(assetBSlice)
    )
}
stack = responsePool.toMutableVmStack()
val poolAddress = stack.popSlice().loadTlb(MsgAddressInt) as AddrStd
```

构建并传输消息：

```kotlin
runBlocking {
    wallet.transfer(pk, WalletTransfer {
        destination = JETTON_WALLET_A // 你现有的jettons钱包
        bounceable = true
        coins = Coins(300000000) // 0.3 ton 的 nanotons
        messageData = MessageData.raw(
            body = buildCell {
                storeUInt(0xf8a7ea5, 32) // op 转账
                storeUInt(0, 64) // 查询_id
                storeTlb(Coins, Coins(100000000)) // jettons的数量
                storeSlice(addrToSlice(jettonAVaultAddress)) // 目的地地址
                storeSlice(addrToSlice(walletAddress))  // 响应地址
                storeUInt(0, 1)  // 自定义载荷
                storeTlb(Coins, Coins(250000000)) // forward_ton_amount // 0.25 ton 的 nanotons
                storeUInt(1, 1)
                // 前送载荷
                storeRef {
                    storeUInt(0xe3a0d482, 32) // op 交换
                    storeSlice(addrToSlice(poolAddress)) // pool_addr
                    storeUInt(0, 1) // 类型
                    storeTlb(Coins, Coins(0)) // 限制
                    storeUInt(0, 1) // next (用于multihop)
                    storeRef {
                        storeUInt(System.currentTimeMillis() / 1000 + 60 * 5, 32) // 截止日期
                        storeSlice(addrToSlice(walletAddress)) // 收件人地址
                        storeSlice(buildCell { storeUInt(0, 2) }.beginParse()) // 转发人（空地址）
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

此示例展示如何将Ton币兑换为Jetton。

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

    JETTON_MASTER = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")  # 想要兑换的jettons地址
    TON_AMOUNT = 10**9  # 1 ton - 兑换数量
    GAS_AMOUNT = 10**9 // 4  # 0.25 ton作为gas
    
    pool_type = 0 # Volatile pool类型

    asset_native = (begin_cell()
                   .store_uint(0, 4) # 资产类型是原生代币
                   .end_cell().begin_parse())
    asset_jetton = (begin_cell()
                   .store_uint(1, 4) # 资产类型是jettons
                   .store_uint(JETTON_MASTER.wc, 8)
                   .store_bytes(JETTON_MASTER.hash_part)
                   .end_cell().begin_parse())

    stack = await provider.run_get_method(
        address=DEDUST_FACTORY, method="get_pool_address",
        stack=[pool_type, asset_native, asset_jetton]
    )
    pool_address = stack[0].load_address()
    
    swap_params = (begin_cell()
                  .store_uint(int(time.time() + 60 * 5), 32) # 截止时间
                  .store_address(wallet.address) # 收件人地址
                  .store_address(None) # 转发人地址
                  .store_maybe_ref(None) # 完成载荷
                  .store_maybe_ref(None) # 拒绝载荷
                  .end_cell())
    swap_body = (begin_cell()
                .store_uint(0xea06185d, 32) # 交换操作码
                .store_uint(0, 64) # 查询id
                .store_coins(int(1*1e9)) # 交换数量
                .store_address(pool_address)
                .store_uint(0, 1) # 交换类型
                .store_coins(0) # 交换限制
                .store_maybe_ref(None) # 下一步，multi-hop的交换
                .store_ref(swap_params)
                .end_cell())

    await wallet.transfer(destination=DEDUST_NATIVE_VAULT,
                          amount=TON_AMOUNT + GAS_AMOUNT, # 交换数量+gas
                          body=swap_body)
    
    await provider.close_all()

asyncio.run(main())

```




## Basics of incoming message processing

### 如何解析账户的交易记录（转账、Jettons、NFTs）？

通过 `getTransactions` API方法可以获取到一个账户上的交易记录列表。它返回一个`Transaction`对象的数组，其中每个项都有很多属性。然而，最常用的字段有： It returns an array of `Transaction` objects, with each item having lots of attributes. However, the fields that are the most commonly used are:

- 初始化这笔交易的消息的Sender, Body和Value
- 交易的哈希和逻辑时间（LT）

_Sender_ 和 _Body_ 字段可用于确定消息的类型（常规转账、jetton转账、nft转账等等）。

以下是一个例子，展示了如何获取任何区块链账户上最近的5笔交易，根据类型解析它们，并在循环中打印出来。

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, TonClient, beginCell, fromNano } from '@ton/ton';

async function main() {
    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: '1b312c91c3b691255130350a49ac5a0742454725f910756aff94dfe44858388e',
    });

    const myAddress = Address.parse('EQBKgXCNLPexWhs2L79kiARR1phGH1LwXxRbNsCFF9doc2lN'); // 你想要从中获取交易记录的地址

    const transactions = await client.getTransactions(myAddress, {
        limit: 5,
    });

    for (const tx of transactions) {
        const inMsg = tx.inMessage;

        if (inMsg?.info.type == 'internal') {
            // 我们在这里只处理内部消息，因为它们最常用
            // 对于外部消息，一些字段是空的，但主要结构是相似的
            const sender = inMsg?.info.src;
            const value = inMsg?.info.value.coins;

            const originalBody = inMsg?.body.beginParse();
            let body = originalBody.clone();
            if (body.remainingBits < 32) {
                // 如果正文没有操作码：这是一条没有评论的简单消息
                console.log(`Simple transfer from ${sender} with value ${fromNano(value)} TON`);
            } else {
                const op = body.loadUint(32);
                if (op == 0) {
                    // 如果操作码是0：这是一条有评论的简单消息
                    const comment = body.loadStringTail();
                    console.log(
                        `Simple transfer from ${sender} with value ${fromNano(value)} TON and comment: "${comment}"`
                    );
                } else if (op == 0x7362d09c) {
                    // 如果操作码是0x7362d09c：这是一个Jetton转账通知

                    body.skip(64); // 跳过query_id
                    const jettonAmount = body.loadCoins();
                    const jettonSender = body.loadAddressAny();
                    const originalForwardPayload = body.loadBit() ? body.loadRef().beginParse() : body;
                    let forwardPayload = originalForwardPayload.clone();

                    // 重要：我们必须验证这条消息的来源，因为它可能被伪造
                    const runStack = (await client.runMethod(sender, 'get_wallet_data')).stack;
                    runStack.skip(2);
                    const jettonMaster = runStack.readAddress();
                    const jettonWallet = (
                        await client.runMethod(jettonMaster, 'get_wallet_address', [
                            { type: 'slice', cell: beginCell().storeAddress(myAddress).endCell() },
                        ])
                    ).stack.readAddress();
                    if (!jettonWallet.equals(sender)) {
                        // 如果发送者不是我们真正的JettonWallet：这条消息被伪造了
                        console.log(`FAKE Jetton transfer`);
                        continue;
                    }

                    if (forwardPayload.remainingBits < 32) {
                        // 如果forward payload没有操作码：这是一个简单的Jetton转账
                        console.log(`Jetton transfer from ${jettonSender} with value ${fromNano(jettonAmount)} Jetton`);
                    } else {
                        const forwardOp = forwardPayload.loadUint(32);
                        if (forwardOp == 0) {
                            // 如果forward payload的操作码是0：这是一次带有评论的简单Jetton转账
                            const comment = forwardPayload.loadStringTail();
                            console.log(
                                `Jetton transfer from ${jettonSender} with value ${fromNano(
                                    jettonAmount
                                )} Jetton and comment: "${comment}"`
                            );
                        } else {
                            // 如果forward payload的操作码是其他：这是一条具有任意结构的消息
                            // 如果你知道其他操作码，你可以手动解析它，或者直接以十六进制形式打印
                            console.log(
                                `Jetton transfer with unknown payload structure from ${jettonSender} with value ${fromNano(
                                    jettonAmount
                                )} Jetton and payload: ${originalForwardPayload}`
                            );
                        }

                        console.log(`Jetton Master: ${jettonMaster}`);
                    }
                } else if (op == 0x05138d91) {
                    // 如果操作码是0x05138d91：这是一个NFT转账通知

                    body.skip(64); // 跳过query_id
                    const prevOwner = body.loadAddress();
                    const originalForwardPayload = body.loadBit() ? body.loadRef().beginParse() : body;
                    let forwardPayload = originalForwardPayload.clone();

                    // 重要：我们必须验证这条消息的来源，因为它可能被伪造
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
                        // 如果forward payload没有操作码：这是一个简单的NFT转账
                        console.log(`NFT transfer from ${prevOwner}`);
                    } else {
                        const forwardOp = forwardPayload.loadUint(32);
                        if (forwardOp == 0) {
                            // 如果forward payload的操作码是0：这是一次带有评论的简单NFT转账
                            const comment = forwardPayload.loadStringTail();
                            console.log(`NFT transfer from ${prevOwner} with comment: "${comment}"`);
                        } else {
                            // 如果forward payload的操作码是其他：这是一条具有任意结构的消息
                            // 如果你知道其他操作码，你可以手动解析它，或者直接以十六进制形式打印
                            console.log(
                                `NFT transfer with unknown payload structure from ${prevOwner} and payload: ${originalForwardPayload}`
                            );
                        }
                    }

                    console.log(`NFT Item: ${itemAddress}`);
                    console.log(`NFT Collection: ${collection}`);
                } else {
                    // 如果操作码是其他的：这是一条具有任意结构的消息
                    // 如果你知道其他操作码，你可以手动解析它，或者直接以十六进制形式打印
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
            
            # NFT 转移通知
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

Note that this example covers only the simplest case with incoming messages, where it is enough to fetch the transactions on a single account. If you want to go deeper and handle more complex chains of transactions and messages, you should take `tx.outMessages` field into an account. It contains the list of the output messages sent by smart-contract in the result of this transaction. To understand the whole logic better, you can read these articles:

- [消息概览](/develop/smart-contracts/guidelines/message-delivery-guarantees)
- [内部消息](/develop/smart-contracts/guidelines/internal-messages)

This topic is explored in more depth in [Payments Processing](/develop/dapps/asset-processing) article.

### How to find transaction for a certain TON Connect result?

TON Connect 2 returns only cell which was sent to blockchain, not generated transaction hash (since that transaction may not come to pass, if external message gets lost or timeouts). Provided BOC, though, allows us to search for that exact message in our account history.

:::tip
You can use an indexer to make the search easier. The provided implementation is for `TonClient` connected to a RPC.
:::

Prepare `retry` function for attempts on listening blockchain:

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

Create listener function which will assert specific transaction on certain account with specific incoming external message, equal to body message in boc:

<Tabs>
<TabItem value="ts" label="@ton/ton">

```typescript
地址有三种格式：**可弹回的（bounceable）**、**不可弹回的（non-bounceable）**和**测试网络的（testnet）**。可以通过查看地址的第一个字母来轻松理解，因为它是第一个字节（8位）包含的标志根据 [TEP-2](https://github.com/ton-blockchain/TEPs/blob/master/text/0002-address.md#smart-contract-addresses)：
```

</TabItem>

</Tabs>
