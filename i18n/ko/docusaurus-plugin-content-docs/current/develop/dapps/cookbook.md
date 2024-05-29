'@theme/Tabs'에서 Tabs 가져오기;
'@theme/TabItem'에서 TabItem 가져오기;

# TON 요리책

제품을 개발하는 동안 TON의 여러 계약과의 상호 작용과 관련하여 다양한 질문이 자주 발생합니다.

이 문서는 모든 개발자의 모범 사례를 수집하여 모든 개발자와 공유하기 위해 작성되었습니다.

## 표준 작업

<!-- TODO: zoom on click (lightbox?) -->

<img src="/img/interaction-schemes/ecosystem.svg" alt="Full ecosystem scheme"></img>

## 계약 주소로 작업하기

### 문자열에서 주소를 변환(사용자 친화적인 <-> raw)하고, 조합하고, 추출하는 방법은 무엇인가요?

TON 주소는 블록체인에서 컨트랙트를 고유하게 식별하며, 워크체인과 원래 상태 해시를 나타냅니다. [두 가지 일반적인 형식](/학습/개요/주소#raw-and-user-friendly-addresses)이 사용됩니다: **raw**(워크체인과 ":" 문자로 구분된 HEX 인코딩 해시)와 **사용자 친화적**(특정 플래그가 포함된 base64 인코딩).

```
User-friendly: EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
Raw: 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```

SDK의 문자열에서 주소 객체를 가져오려면 다음 코드를 사용할 수 있습니다:

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

</TabItem>
<TabItem value="js-tonweb" label="JS (tonweb)">

```js
const TonWeb = require('tonweb');

const address1 = new TonWeb.utils.Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF');
const address2 = new TonWeb.utils.Address('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e');

// toString arguments: isUserFriendly, isUrlSafe, isBounceable, isTestOnly

console.log(address1.toString(true, true, true)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address1.toString(isUserFriendly = false)); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

console.log(address1.toString(true, true, true)); // EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
console.log(address2.toString(isUserFriendly = false)); // 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```

</TabItem>
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

</TabItem>
<TabItem value="py" label="Python">

```py
from pytoniq_core import Address

address1 = Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF')
address2 = Address('0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e')

# to_str() arguments: is_user_friendly, is_url_safe, is_bounceable, is_test_only

print(address1.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address1.to_str(is_user_friendly=False))  # 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e

print(address2.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address2.to_str(is_user_friendly=False))  # 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```

</TabItem>
</Tabs>

### 사용자 친화적인 주소에는 어떤 플래그가 있나요?

두 개의 플래그가 정의되어 있습니다: **bounceable**/**non-bounceable** and **testnet**/**any-net**. 주소 인코딩에서 첫 6비트를 의미하므로 주소의 첫 글자를 보면 쉽게 알 수 있으며, 플래그는 [TEP-2](https://github.com/ton-blockchain/TEPs/blob/master/text/0002-address.md#smart-contract-addresses)에 따라 해당 위치에 있습니다:

|                         주소 시작                        |           이진 형식           | 바운스 가능 | 테스트넷 전용 |
| :--------------------------------------------------: | :-----------------------: | :----: | :-----: |
| E... | 000100.01 |   yes  |   아니요   |
| U... | 010100.01 |   아니요  |   아니요   |
| k... | 100100.01 |   yes  |   yes   |
| 0... | 110100.01 |   아니요  |   yes   |

:::tip
테스트넷 전용 플래그는 블록체인에서 전혀 표현되지 않습니다. 반송 불가 플래그는 전송 대상 주소로 사용될 때만 차이를 만듭니다: 이 경우 전송된 메시지에 대해 [반송을 허용하지 않음](/개발/스마트컨트랙트/가이드라인/반송 불가 메시지)이지만, 블록체인 주소에는 이 플래그가 포함되어 있지 않습니다.
:::

또한 일부 라이브러리에서는 `urlSafe`라는 직렬화 매개변수를 발견할 수 있습니다. 문제는 base64 형식이 URL 안전하지 않기 때문에 링크에서 주소를 전송할 때 일부 문자(예: `+` 및 `/`)가 문제를 일으킬 수 있다는 것입니다. urlSafe = true`인 경우 모든 `+`기호는`-`로 대체되고 모든 `/`기호는`_\`로 대체됩니다. 다음 코드를 사용하여 이러한 주소 형식을 얻을 수 있습니다:

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

</TabItem>
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

</TabItem>
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

</TabItem>
<TabItem value="py" label="Python">

```py
from pytoniq_core import Address

address = Address('EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF')

# to_str() arguments: is_user_friendly, is_url_safe, is_bounceable, is_test_only

print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=False))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=False, is_test_only=False))  # EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff+W72r5gqPrHF
print(address.to_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True, is_test_only=False))  # UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
print(address.to_str(is_user_friendly=True, is_bounceable=True, is_url_safe=True, is_test_only=True))  # kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
print(address.to_str(is_user_friendly=True, is_bounceable=False, is_url_safe=True, is_test_only=True))  # 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
```

</TabItem>
</Tabs>

### TON 주소의 유효성을 어떻게 확인하나요?

<Tabs groupId="address-examples">

<TabItem value="Tonweb" label="JS (Tonweb)">

```js

const TonWeb = require("tonweb")

TonWeb.utils.Address.isValid('...')
```

</TabItem>
<TabItem value="GO" label="tonutils-go">

```python
package main

import (
    "fmt"
    "github.com/xssnick/tonutils-go/address"
)

if _, err := address.ParseAddr("EQCD39VS5j...HUn4bpAOg8xqB2N"); err != nil {
 return errors.New("invalid address")
}
```

</TabItem>
<TabItem value="Java" label="ton4j">

```javascript
  /* Maven
  <dependency>
    <groupId>io.github.neodix42</groupId>
    <artifactId>address</artifactId>
    <version>0.3.2</version>
  </dependency>
  */

  try {
  Address.of("...");
  } catch (Exception e) {
  // not valid address
  }
```

</TabItem>
<TabItem value="Kotlin" label="ton-kotlin">

```javascript
try {
    AddrStd("...")
} catch(e: IllegalArgumentException) {
   // not valid address
}
```

</TabItem>
</Tabs>

## TON 생태계의 표준 지갑

### TON을 전송하는 방법은 무엇인가요? 다른 지갑으로 문자 메시지를 보내는 방법은 무엇인가요?

<img src="/img/interaction-schemes/wallets.svg" alt="Wallet operations scheme"></img>

대부분의 SDK는 지갑에서 메시지를 전송하기 위해 다음과 같은 프로세스를 제공합니다:

- 비밀 키와 워크체인(보통 0, [베이스체인](/학습/개요/톤블록체인#워크체인-블록체인-자신의-규칙)을 사용하여 올바른 버전(대부분의 경우 v3r2, [지갑 버전](/참여/월렛/계약) 참조)의 지갑 래퍼(프로그램 내 객체)를 생성합니다.)
- 또한 API 또는 라이트서버 중 원하는 서버로 요청을 라우팅하는 블록체인 래퍼 또는 '클라이언트' 객체를 생성합니다.
- 그런 다음 블록체인 랩퍼에서 컨트랙트를 *개방*합니다. 즉, 컨트랙트 객체는 더 이상 추상적이지 않으며 TON 메인넷이나 테스트넷에서 실제 계정을 나타냅니다.
- 그 후 원하는 메시지를 작성하여 전송할 수 있습니다. 고급 매뉴얼](/개발/스마트컨트랙트/자습서/지갑#다중 메시지 동시 전송)에 설명된 대로 요청당 최대 4개의 메시지를 동시에 보낼 수도 있습니다.

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { TonClient, WalletContractV4, internal } from "@ton/ton";
import { mnemonicNew, mnemonicToPrivateKey } from "@ton/crypto";

const client = new TonClient({
  endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC',
});

// Convert mnemonics to private key
let mnemonics = "word1 word2 ...".split(" ");
let keyPair = await mnemonicToPrivateKey(mnemonics);

// Create wallet contract
let workchain = 0; // Usually you need a workchain 0
let wallet = WalletContractV4.create({ workchain, publicKey: keyPair.publicKey });
let contract = client.open(wallet);

// Create a transfer
let seqno: number = await contract.getSeqno();
await contract.sendTransfer({
  seqno,
  secretKey: keyPair.secretKey,
  messages: [internal({
    value: '1',
    to: 'EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N',
    body: 'Example transfer body',
  })]
});
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
from pytoniq import LiteBalancer, WalletV4R2
import asyncio

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    transfer = {
        "destination": "DESTINATION ADDRESS HERE",    # please remember about bounceable flags
        "amount":      int(10**9 * 0.05),             # amount sent, in nanoTON
        "body":        "Example transfer body",       # may contain a cell; see next examples
    }

    await wallet.transfer(**transfer)
	await client.close_all()

asyncio.run(main())
```

</TabItem>

</Tabs>

### 댓글 작성하기: 스네이크 형식의 긴 문자열

셀은 **최대 1023비트**를 저장할 수 있지만 긴 문자열(또는 기타 대용량 정보)을 저장해야 할 때가 있습니다. 이 경우 스네이크 셀을 사용할 수 있습니다. 스네이크 셀은 다른 셀에 대한 참조를 포함하고, 그 참조는 다시 다른 셀에 대한 참조를 포함하는 셀입니다.

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

</TabItem>
</Tabs>

많은 SDK에는 이미 긴 문자열을 구문 분석하고 저장하는 함수가 있습니다. 다른 경우에는 재귀를 사용하여 이러한 셀로 작업하거나 최적화("테일 콜"이라고 알려진 트릭)할 수도 있습니다.

댓글 메시지에는 32개의 0비트가 있다는 것을 잊지 마세요(연산자 코드가 0이라고 할 수도 있습니다)!

## TEP-74(제톤 표준)

<img src="/img/interaction-schemes/jettons.svg" alt="Jetton operations scheme"></img>

### 사용자의 제톤 지갑 주소(오프체인)를 계산하는 방법은 무엇인가요?

사용자의 젯튼 지갑 주소를 계산하려면 실제로 사용자 주소로 젯튼 마스터 컨트랙트의 "get_wallet_address" get-method를 호출해야 합니다. 이 작업은 젯튼마스터의 getWalletAddress 메서드를 사용하거나 마스터 컨트랙트를 직접 호출하여 쉽게 수행할 수 있습니다.

:::info
'@톤/톤'의 'JettonMaster'는 기능이 많이 부족하지만 다행히도 *이 기능*이 있습니다.
:::

<Tabs groupId="code-examples">
<TabItem value="user-jetton-wallet-method-js" label="@ton/ton">

```js
const { Address, beginCell } = require("@ton/core")
const { TonClient, JettonMaster } = require("@ton/ton")

const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
});

const jettonMasterAddress = Address.parse('...') // for example EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE
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

### 사용자의 제톤 지갑 주소(오프라인)는 어떻게 계산하나요?

지갑 주소를 가져오기 위해 매번 GET 메서드를 호출하면 많은 시간과 리소스가 소요될 수 있습니다. Jetton 지갑 코드와 저장 구조를 미리 알고 있다면 네트워크 요청 없이 지갑 주소를 가져올 수 있습니다.

톤뷰어를 사용하여 코드를 받을 수 있습니다. jUSDT`를 예로 들어보면, 제톤 마스터 주소는 `EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA`입니다. 이 주소(https://tonviewer.com/EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA?section=method)로 이동하여 메소드 탭을 열면 이미 `get_jetton_data\` 메소드가 있는 것을 확인할 수 있습니다. 이 메서드를 호출하면 제톤 지갑 코드가 포함된 16진수 형태의 셀을 얻을 수 있습니다:

```
b5ee9c7201021301000385000114ff00f4a413f4bcf2c80b0102016202030202cb0405001ba0f605da89a1f401f481f481a9a30201ce06070201580a0b02f70831c02497c138007434c0c05c6c2544d7c0fc07783e903e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7c076cf16cc8d0d0d09208403e29fa96ea68c1b088d978c4408fc06b809208405e351466ea6cc1b08978c840910c03c06f80dd6cda0841657c1ef2ea7c09c6c3cb4b01408eebcb8b1807c073817c160080900113e910c30003cb85360005c804ff833206e953080b1f833de206ef2d29ad0d30731d3ffd3fff404d307d430d0fa00fa00fa00fa00fa00fa00300008840ff2f00201580c0d020148111201f70174cfc0407e803e90087c007b51343e803e903e903534544da8548b31c17cb8b04ab0bffcb8b0950d109c150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c032481c007e401d3232c084b281f2fff274013e903d010c7e800835d270803cb8b13220060072c15401f3c59c3e809dc072dae00e02f33b51343e803e903e90353442b4cfc0407e80145468017e903e9014d771c1551cdbdc150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c0325c007e401d3232c084b281f2fff2741403f1c147ac7cb8b0c33e801472a84a6d8206685401e8062849a49b1578c34975c2c070c00870802c200f1000aa13ccc88210178d4519580a02cb1fcb3f5007fa0222cf165006cf1625fa025003cf16c95005cc2391729171e25007a813a008aa005004a017a014bcf2e2c501c98040fb004300c85004fa0258cf1601cf16ccc9ed5400725269a018a1c882107362d09c2902cb1fcb3f5007fa025004cf165007cf16c9c8801001cb0527cf165004fa027101cb6a13ccc971fb0050421300748e23c8801001cb055006cf165005fa027001cb6a8210d53276db580502cb1fcb3fc972fb00925b33e24003c85004fa0258cf1601cf16ccc9ed5400eb3b51343e803e903e9035344174cfc0407e800870803cb8b0be903d01007434e7f440745458a8549631c17cb8b049b0bffcb8b0b220841ef765f7960100b2c7f2cfc07e8088f3c58073c584f2e7f27220060072c148f3c59c3e809c4072dab33260103ec01004f214013e809633c58073c5b3327b55200087200835c87b51343e803e903e9035344134c7c06103c8608405e351466e80a0841ef765f7ae84ac7cbd34cfc04c3e800c04e81408f214013e809633c58073c5b3327b5520
```

이제 Jetton 지갑 코드, Jetton 마스터 주소, 볼트 구조를 알았으니 지갑 주소를 수동으로 계산할 수 있습니다:

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

</TabItem>

<TabItem value="Python" label="Python">

```python

from pytoniq_core import Address, Cell, begin_cell

def calculate_jetton_address(
    owner_address: Address, jetton_master_address: Address, jetton_wallet_code: str
):
    # Recreate from jetton-utils.fc calculate_jetton_wallet_address()
    # https://tonscan.org/jetton/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs#source

    data_cell = (
        begin_cell()
        .store_uint(0, 4)
        .store_coins(0)
        .store_address(owner_address)
        .store_address(jetton_master_address)
        .end_cell()
    )

    code_cell = Cell.one_from_boc(jetton_wallet_code)

    state_init = (
        begin_cell()
        .store_uint(0, 2)
        .store_maybe_ref(code_cell)
        .store_maybe_ref(data_cell)
        .store_uint(0, 1)
        .end_cell()
    )
    state_init_hex = state_init.hash.hex()
    jetton_address = Address(f'0:{state_init_hex}')

    return jetton_address

```

전체 예제 [여기](/static/example-code-snippets/pythoniq/jetton-offline-address-calc-wrapper.py)를 읽어보세요.

</TabItem>
</Tabs>

대부분의 주요 토큰은 [TEP-74 표준의 표준 구현](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc)을 사용하기 때문에 다른 저장 구조를 가지고 있지 않습니다. 중앙화된 스테이블코인을 위한 새로운 [제튼 위드 거버넌스 컨트랙트](https://github.com/ton-blockchain/stablecoin-contract)는 예외입니다. 이 둘의 차이점은 [지갑 상태 필드의 존재와 금고에 코드 셀이 없다는 것](https://github.com/ton-blockchain/stablecoin-contract/blob/7a22416d4de61336616960473af391713e100d7b/contracts/jetton-utils.fc#L3-L12)입니다.

### 댓글이 포함된 제톤 전송 메시지를 작성하는 방법은 무엇인가요?

토큰 전송을 위한 메시지를 구성하는 방법을 이해하기 위해 토큰 표준을 설명하는 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md#1-transfer)를 사용합니다.

:::warning
When displayed, token doesn't usually show count of indivisible units user has; rather, amount is divided by `10 ^ decimals`. This value is commonly set to `9`, and this allows us to use `toNano` function. If decimals were different, we would **need to multiply by a different value** (for instance, if decimals are 6, then we would end up transferring thousand times the amount we wanted).

물론 항상 분할 단위로 계산할 수 있습니다.
:::

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";

async function main() {
    const jettonWalletAddress = Address.parse('put your jetton wallet address');
    const destinationAddress = Address.parse('put destination wallet address');

    const forwardPayload = beginCell()
        .storeUint(0, 32) // 0 opcode means we have a comment
        .storeStringTail('Hello, TON!')
        .endCell();

    const messageBody = beginCell()
        .storeUint(0x0f8a7ea5, 32) // opcode for jetton transfer
        .storeUint(0, 64) // query id
        .storeCoins(toNano(5)) // jetton amount, amount * 10^9
        .storeAddress(destinationAddress)
        .storeAddress(destinationAddress) // response destination
        .storeBit(0) // no custom payload
        .storeCoins(toNano('0.02')) // forward amount - if >0, will send notification message
        .storeBit(1) // we store forwardPayload as a reference
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

</TabItem>
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

전달_금액`이 0이 아닌 경우, 이 섹션 상단의 구성표에서 볼 수 있듯이 제톤 수신에 관한 알림이 대상 컨트랙트로 전송됩니다. 응답_대상` 주소가 0이 아닌 경우, 남은 톤코인("초과분"이라고 함)이 해당 주소로 전송됩니다.

:::tip
익스플로러는 일반적인 TON 전송뿐만 아니라 젯톤 알림에서도 댓글을 지원합니다. 형식은 32개의 0비트와 텍스트(가급적 UTF-8)입니다.
:::

:::tip
제톤 송금은 발신 메시지에 대한 수수료와 금액에 대해 신중하게 고려해야 합니다. 예를 들어, 0.2톤으로 '통화' 송금하는 경우 0.1톤을 전달하고 0.1톤의 초과 답장 메시지를 받을 수 없습니다.
:::

## TEP-62(NFT 표준)

<img src="/img/interaction-schemes/nft.svg" alt="NFT ecosystem scheme"></img>

NFT 컬렉션은 매우 다릅니다. 실제로 TON의 NFT 컨트랙트는 "적절한 가져오는 방법을 가지고 있고 유효한 메타데이터를 반환하는 컨트랙트"로 정의할 수 있습니다. 전송 작업은 표준화되어 있고 [jetton의 것]과 매우 유사하므로(/develop/dapps/cookbook#how-to-construct-a-message-for-a-jetton-transfer-with-a-comment) 자세히 살펴보지는 않고 여러분이 만날 수 있는 대부분의 컬렉션에서 제공하는 추가 기능을 살펴보기로 하겠습니다!

:::warning
참고: 아래 NFT에 대한 모든 방법은 TEP-62에 구속되지 않습니다. 시도하기 전에 NFT 또는 컬렉션이 해당 메시지를 예상한 방식으로 처리하는지 확인하시기 바랍니다. 이 경우 지갑 앱 에뮬레이션이 유용할 수 있습니다.
:::

### NFT 일괄 배포는 어떻게 사용하나요?

수집을 위한 스마트 콘트랙트를 사용하면 단일 트랜잭션에 최대 250개의 NFT를 배포할 수 있습니다. 그러나 실제로는 1톤의 계산 수수료 제한으로 인해 최대 100-130개의 NFT를 배포할 수 있다는 점을 고려해야 합니다. 이를 위해서는 새로운 NFT에 대한 정보를 사전에 저장해야 합니다.

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

</TabItem>
</Tabs>

우선, 보관 수수료의 최소 TON이 '0.05'라고 가정해 봅시다. 즉, NFT를 배포한 후 컬렉션의 스마트 콘트랙트는 이만큼의 TON을 잔고로 전송합니다. 다음으로, 새로운 NFT의 소유자와 해당 콘텐츠의 배열을 얻습니다. 그 후, GET 메서드 `get_collection_data`를 사용하여 `next_item_index`를 가져옵니다.

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

</TabItem>
</Tabs>

다음으로 총 트랜잭션 비용을 정확하게 계산해야 합니다. 테스트를 통해 '0.015'라는 값을 얻었지만 각 경우에 따라 달라질 수 있습니다. 이는 주로 콘텐츠 크기가 증가하면 **전달 수수료**(전달 수수료)가 높아지기 때문에 NFT의 콘텐츠에 따라 달라집니다.

### 컬렉션의 스마트 컨트랙트 소유자를 변경하려면 어떻게 해야 하나요?

컬렉션의 소유자를 변경하는 방법은 매우 간단합니다. 이렇게 하려면 **opcode = 3**, 임의의 쿼리 아이디, 새 소유자의 주소를 지정해야 합니다:

<Tabs groupId="code-examples">
<TabItem value="js-ton" label="JS (@ton)">

```js
import { Address, beginCell, internal, storeMessageRelaxed, toNano } from "@ton/core";

async function main() {
    const collectionAddress = Address.parse('put your collection address');
    const newOwnerAddress = Address.parse('put new owner wallet address');

    const messageBody = beginCell()
        .storeUint(3, 32) // opcode for changing owner
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

</TabItem>
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

</TabItem>
</Tabs>

### 컬렉션의 스마트 컨트랙트에서 콘텐츠를 변경하려면 어떻게 해야 하나요?

스마트 콘트랙트 컬렉션의 콘텐츠를 변경하려면 컬렉션이 어떻게 저장되는지 이해해야 합니다. 컬렉션은 모든 콘텐츠를 하나의 셀에 저장하며, 그 안에는 두 개의 셀이 있습니다: **컬렉션 콘텐츠**와 **NFT 공통 콘텐츠**입니다. 첫 번째 셀에는 컬렉션의 메타데이터가 들어 있고, 두 번째 셀에는 NFT 메타데이터의 기본 URL이 들어 있습니다.

종종 컬렉션의 메타데이터는 '0.json'과 유사한 형식으로 저장되고 계속 증가하는 반면, 이 파일 앞의 주소는 동일하게 유지됩니다. NFT 공통 콘텐츠에 저장되어야 하는 주소는 바로 이 주소입니다.

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
        .storeUint(1, 8) // we have offchain metadata
        .storeStringTail(newCollectionMeta)
        .endCell();
    const nftCommonMetaCell = beginCell()
        .storeUint(1, 8) // we have offchain metadata
        .storeStringTail(newNftCommonMeta)
        .endCell();

    const contentCell = beginCell()
        .storeRef(collectionMetaCell)
        .storeRef(nftCommonMetaCell)
        .endCell();

    const royaltyCell = beginCell()
        .storeUint(5, 16) // factor
        .storeUint(100, 16) // base
        .storeAddress(royaltyAddress) // this address will receive 5% of each sale
        .endCell();

    const messageBody = beginCell()
        .storeUint(4, 32) // opcode for changing content
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

</TabItem>
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

</TabItem>
</Tabs>

또한 로열티 정보도 이 옵코드를 사용하여 변경되므로 메시지에 로열티 정보를 포함해야 합니다. 중요한 점은 모든 곳에 새로운 값을 지정할 필요는 없다는 것입니다. 예를 들어 NFT 공통 콘텐츠만 변경해야 하는 경우 다른 모든 값은 이전과 동일하게 지정할 수 있습니다.

## 타사: 탈중앙화 거래소(DEX)

### DEX(디더스트)에 스왑 메시지를 보내는 방법은 무엇인가요?

DEX는 작업에 서로 다른 프로토콜을 사용합니다. 이 예시에서는 **DeDust**와 상호 작용합니다.

- [디더스트 문서](https://docs.dedust.io/).

디더스트에는 jetton <-> jetton 또는 TON <-> jetton의 두 가지 교환 경로가 있습니다. 각각 다른 체계를 가지고 있습니다. 교환하려면 특정 **볼트**로 제톤(또는 톤코인)을 전송하고 특별한 페이로드를 제공해야 합니다. 다음은 제톤을 제톤으로 또는 제톤을 톤코인으로 교환하는 방식입니다:

```tlb
swap#e3a0d482 _:SwapStep swap_params:^SwapParams = ForwardPayload;
              step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;
              swap_params#_ deadline:Timestamp recipient_addr:MsgAddressInt referral_addr:MsgAddress
                    fulfill_payload:(Maybe ^Cell) reject_payload:(Maybe ^Cell) = SwapParams;
```

이 체계는 제톤 전송 메시지(`전송#0f8a7ea5`)의 `전송_페이로드`에 포함되어야 할 내용을 보여줍니다.

그리고 톤코인에서 제트턴으로 스왑하는 계획도 있습니다:

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
              step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
              step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;
              swap_params#_ deadline:Timestamp recipient_addr:MsgAddressInt referral_addr:MsgAddress
                    fulfill_payload:(Maybe ^Cell) reject_payload:(Maybe ^Cell) = SwapParams;
```

이것은 톤코인 **볼트**로 전송하는 본체에 대한 계획입니다.

먼저 스왑할 제톤의 **볼트** 주소 또는 톤코인 **볼트** 주소를 알아야 합니다. 이는 컨트랙트 [**Factory**](https://docs.dedust.io/reference/factory)의 `get_vault_address` get 메서드를 사용하여 수행할 수 있습니다. 인자로 계획에 따라 슬라이스를 전달해야 합니다:

```tlb
native$0000 = Asset; // for ton
jetton$0001 workchain_id:int8 address:uint256 = Asset; // for jetton
```

또한 거래소 자체의 경우, get 메서드 `get_pool_address`에서 얻은 **pool** 주소가 필요합니다. 인자로는 위의 체계에 따른 자산 슬라이스가 필요합니다. 이에 대한 응답으로 두 메서드 모두 요청된 **볼트** / **풀** 주소의 슬라이스를 반환합니다.

이 정도면 메시지를 작성하기에 충분합니다.

<Tabs groupId="code-examples">

 <TabItem value="js-ton" label="JS (@ton)">
탈중앙 거래소는 작업에 다양한 프로토콜을 사용하므로 주요 개념과 몇 가지 중요한 구성 요소를 숙지하고 스왑 프로세스를 올바르게 수행하는 데 관련된 TL-B 스키마에 대해서도 알아야 합니다. 이 튜토리얼에서는 TON으로만 구현된 유명한 DEX 중 하나인 디더스트에 대해 다룹니다.
디더스트에는 스왑 가능한 모든 자산 유형을 포함하는 추상적인 자산 개념이 있습니다. 자산 유형에 대한 추상화는 자산 유형이 중요하지 않기 때문에 스왑 프로세스를 단순화하며, 이 접근 방식에서는 추가 통화나 다른 체인의 자산도 쉽게 다룰 수 있습니다.

다음은 디더스트가 자산 개념에 도입한 TL-B 스키마입니다.

```tlb
native$0000 = Asset; // for ton

jetton$0001 workchain_id:int8 address:uint256 = Asset; // for any jetton,address refer to jetton master address

// Upcoming, not implemented yet.
extra_currency$0010 currency_id:int32 = Asset;
```

다음으로 디더스트는 볼트, 풀, 팩토리의 세 가지 구성 요소를 소개했습니다. 이러한 구성 요소는 컨트랙트 또는 컨트랙트 그룹으로, 스왑 프로세스의 일부를 담당합니다. 팩토리는 볼트, 풀과 같은 다른 컴포넌트 주소(
)를 찾고 다른 컴포넌트를 구축하는 역할을 합니다.
볼트는 전송 메시지를 수신하고, 자산을 보관하며, 해당 풀에 "사용자 A가 X 100개를 Y로 스왑하고 싶다"고 알리는 역할을 담당합니다.

반면, 풀은 자산 Y를 담당하는 다른 볼트에 미리 정의된 공식에 따라 스왑 금액을 계산하고, 계산된 금액을 사용자에게 지급하도록 지시하는 역할을 담당합니다.
스왑 금액 계산은 수학 공식을 기반으로 하며, 지금까지는 일반적으로 사용되는 "상수 제품" 공식을 기반으로 작동하는 변동성 풀과 변동성이라는 두 가지 풀이 있습니다: x \* y = k, 그리고 다른 하나는 거의 동일한 가치의 자산(예: USDT/USDC, TON/stTON)에 최적화된 스테이블 스왑으로 알려져 있습니다. 공식을 사용합니다:
따라서 모든 스왑에 대해 해당 볼트가 필요하며, 특정 자산 유형과 상호작용할 수 있도록 맞춤화된 특정 API를 구현하기만 하면 됩니다. 디더스트에는 세 가지 볼트 구현이 있습니다. 네이티브 볼트 - 네이티브 코인(톤코인)을 처리합니다. 제톤 볼트 - 제톤을 관리하고, 추가 통화 볼트(출시 예정) - TON 추가 통화용으로 설계되었습니다.

디더스트는 컨트랙트, 컴포넌트, API와 함께 작동하는 특별한 SDk를 제공하며, 이는 타입스크립트로 작성되었습니다.
이론은 충분하니 이제 하나의 제튼을 TON으로 교체하도록 환경을 설정해 보겠습니다.

```bash
npm install --save @ton/core @ton/ton @ton/crypto

```

디더스트 SDK도 가져와야 합니다.

```bash
npm install --save @dedust/sdk
```

이제 몇 가지 객체를 초기화해야 합니다.

```typescript
import { Factory, MAINNET_FACTORY_ADDR } from "@dedust/sdk";
import { Address, TonClient4 } from "@ton/ton";

const tonClient = new TonClient4({
  endpoint: "https://mainnet-v4.tonhubapi.com",
});
const factory = tonClient.open(Factory.createFromAddress(MAINNET_FACTORY_ADDR));
//The Factory contract  is used to  locate other contracts.
```

스왑 프로세스에는 몇 가지 단계가 있습니다. 예를 들어, 일부 TON을 Jetton으로 스왑하려면 먼저 해당 Vault와 Pool
을 찾은 다음 배포되었는지 확인해야 합니다. 톤과 스케일 예시의 경우 코드는 다음과 같습니다:

```typescript
import { Asset, VaultNative } from "@dedust/sdk";

//Native vault is for TON
const tonVault = tonClient.open(await factory.getNativeVault());
//We use the factory to find our native coin (Toncoin) Vault.
```

다음 단계는 여기에서 해당 풀을 찾는 것입니다(톤 및 규모).

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

비활성화된 계약에 자금을 송금하면 복구할 수 없는 손실이 발생할 수 있으므로 이제 이러한 계약이 존재하는지 확인해야 합니다.

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

그 후, TON의 양으로 전송 메시지를 보낼 수 있습니다.

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

토큰 X를 Y와 교환하는 과정은 동일합니다. 예를 들어, X 토큰을 X 볼트에 보내고, X 볼트
가 자산을 받아 보유하고, 풀에 이 주소가 스왑을 요청했음을 알리고, 이제 풀은
계산에 따라 다른 볼트에 알리고, 여기서 볼트 Y는 스왑을 요청한 사용자에게 동등한 양의 Y를 릴리스합니다.

자산 간의 차이점은 전송 방법에 관한 것인데, 예를 들어 제톤의 경우 전송 메시지를 사용하여 볼트에 전송하고 특정 포워드 페이로드를 첨부하지만 네이티브 코인의 경우 해당 금액의 TON을 첨부하여 스왑 메시지를 볼트에 전송합니다.

이것이 톤과 제튼의 스키마입니다:

```tlb
swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
```

따라서 모든 볼트와 해당 풀은 특정 스왑을 위해 설계되었으며 특수 자산에 맞춘 특수 API가 있습니다.

이것은 톤을 제톤 SCALE로 바꾸는 것입니다. 제톤을 제톤으로 교체하는 프로세스는 동일하며, 유일한 차이점은 TL-B 스키마에 설명된 페이로드를 제공해야 한다는 점입니다.

```TL-B
swap#e3a0d482 _:SwapStep swap_params:^SwapParams = ForwardPayload;
```

```typescript
//find Vault
const scaleVault = tonClient.open(await factory.getJettonVault(SCALE_ADDRESS));
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

에셋 슬라이스를 빌드합니다:

```kotlin
val assetASlice = buildCell {
    storeUInt(1,4)
    storeInt(JETTON_MASTER_A.workchainId, 8)
    storeBits(JETTON_MASTER_A.address)
}.beginParse()
```

get 메서드를 실행합니다:

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

메시지를 작성하고 전송합니다:

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

이 예시는 톤코인을 제톤으로 교환하는 방법을 보여줍니다.

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

</TabItem>
</Tabs>

## 수신 메시지 처리의 기본 사항

### 계정의 거래(이체, 제트온, NFT)를 분석하는 방법은 무엇인가요?

계정의 트랜잭션 목록은 `겟트랜잭션` API 메서드를 통해 가져올 수 있습니다. 이 메서드는 각 항목에 많은 속성이 있는 `Transaction` 객체 배열을 반환합니다. 그러나 가장 일반적으로 사용되는 필드는 다음과 같습니다:

- 이 트랜잭션을 시작한 메시지의 발신자, 본문 및 값
- 트랜잭션의 해시 및 논리적 시간(LT)

발신자_ 및 *본인* 필드를 사용하여 메시지 유형(일반 송금, 제톤 송금, nft 송금 등)을 결정할 수 있습니다.

다음은 모든 블록체인 계정에서 가장 최근 거래 5개를 가져와 유형에 따라 구문 분석하고 반복해서 출력하는 방법에 대한 예제입니다.

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

이 예는 단일 계정에서 트랜잭션을 가져오는 것으로 충분한 수신 메시지가 있는 가장 간단한 경우에만 적용됩니다. 더 깊이 들어가서 더 복잡한 트랜잭션과 메시지 체인을 처리하려면 `tx.outMessages` 필드를 계정으로 가져와야 합니다. 여기에는 이 트랜잭션의 결과에서 스마트 컨트랙트가 보낸 출력 메시지 목록이 포함됩니다. 전체 로직을 더 잘 이해하려면 다음 문서를 읽어보시기 바랍니다:

- [메시지 개요](/개발/스마트-계약/가이드라인/메시지-배달-보증)
- [내부 메시지](/개발/스마트-계약/가이드라인/내부 메시지)

이 주제는 [결제 처리](/개발/앱/자산 처리) 문서에서 더 자세히 살펴볼 수 있습니다.

### 특정 톤 커넥트 결과에 대한 트랜잭션을 찾는 방법은 무엇인가요?

톤 커넥트 2는 블록체인으로 전송된 셀만 반환하며, 생성된 트랜잭션 해시는 반환하지 않습니다(외부 메시지가 손실되거나 시간 초과된 경우 해당 트랜잭션이 이루어지지 않을 수 있기 때문입니다). 하지만 BOC가 제공되면 계정 기록에서 해당 메시지를 정확하게 검색할 수 있습니다.

:::tip
인덱서를 사용하면 검색을 더 쉽게 할 수 있습니다. 제공된 구현은 RPC에 연결된 '톤클라이언트'를 위한 것입니다.
:::

블록체인 수신 시도에 대한 '재시도' 기능을 준비합니다:

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

특정 계정에서 특정 외부 메시지가 수신되는 경우, boc의 본문 메시지와 동일한 특정 트랜잭션을 주장하는 리스너 함수를 생성합니다:

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
