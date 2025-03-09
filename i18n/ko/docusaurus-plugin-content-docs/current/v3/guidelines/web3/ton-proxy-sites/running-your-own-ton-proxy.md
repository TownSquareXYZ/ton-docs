# TON 프록시 실행하기

이 문서는 TON 네트워크를 통해 접근하는 웹사이트인 TON Sites에 대한 기본적인 소개를 제공합니다. TON Sites는 다른 TON 서비스의 편리한 진입점으로 사용될 수 있습니다. 특히 TON Sites에서 다운로드한 HTML 페이지는 사용자의 기기에 TON Wallet이 설치되어 있는 경우 클릭으로 결제할 수 있는 `ton://...` URI 링크를 포함할 수 있습니다.

기술적 관점에서 TON Sites는 표준 웹사이트와 매우 유사하지만, 인터넷 대신 [TON 네트워크](/v3/concepts/dive-into-ton/ton-blockchain/ton-networking)(인터넷 내부의 오버레이 네트워크)를 통해 접근합니다. 구체적으로, IPv4나 IPv6 주소 대신 [ADNL](/v3/documentation/network/protocols/adnl/overview) 주소를 가지며, 일반적인 TCP/IP 대신 [RLDP](/v3/documentation/network/protocols/rldp) 프로토콜(ADNL 위에 구축된 상위 레벨 RPC 프로토콜)을 통해 HTTP 쿼리를 수신합니다. 모든 암호화는 ADNL이 처리하므로, 진입 프록시가 사용자의 기기에서 로컬로 호스팅되는 경우 HTTPS(TLS)를 사용할 필요가 없습니다.

기존 사이트에 접근하고 새로운 TON Sites를 만들기 위해서는 "일반" 인터넷과 TON 네트워크 사이의 특별한 게이트웨이가 필요합니다. 본질적으로 TON Sites는 클라이언트 기기에서 로컬로 실행되는 HTTP->RLDP 프록시의 도움으로 접근되며, 원격 웹 서버에서 실행되는 역방향 RLDP->HTTP 프록시를 통해 생성됩니다.

[TON Sites, WWW, Proxy에 대해 더 알아보기](https://blog.ton.org/ton-sites)

## 진입 프록시 실행하기

기존 TON Sites에 접근하기 위해서는 컴퓨터에서 RLDP-HTTP 프록시를 실행해야 합니다.

1. [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드하세요.

 또는 이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy)을 따라 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. TON [글로벌 설정](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)을 다운로드하세요.

3. **rldp-http-proxy** 실행

 ```bash
 rldp-http-proxy/rldp-http-proxy -p 8080 -c 3333 -C global.config.json
 ```

위 예시에서 `8080`은 localhost에서 들어오는 HTTP 쿼리를 수신할 TCP 포트이며, `3333`은 모든 아웃바운드 및 인바운드 RLDP와 ADNL 활동(TON 네트워크를 통한 TON Sites 연결)에 사용될 UDP 포트입니다. `global.config.json`은 TON 글로벌 설정 파일의 이름입니다.

모든 것을 올바르게 수행했다면, 진입 프록시는 종료되지 않고 터미널에서 계속 실행될 것입니다. 이제 TON Sites 접근에 사용할 수 있습니다. 더 이상 필요하지 않을 때는 `Ctrl-C`를 누르거나 터미널 창을 닫아 종료할 수 있습니다.

진입 프록시는 `localhost` 포트 `8080`에서 HTTP로 사용할 수 있습니다.

## 원격 컴퓨터에서 진입 프록시 실행하기

1. [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드하세요.

 또는 이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy)을 따라 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. TON [글로벌 설정](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)을 다운로드하세요.

3. [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 **generate-random-id**를 다운로드하세요.

 또는 이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#generate-random-id)을 따라 **generate-random-id**를 직접 컴파일할 수 있습니다.

4. 진입 프록시용 영구 ADNL 주소 생성하기

 ```bash
 mkdir keyring

 utils/generate-random-id -m adnlid
 ```

 다음과 같은 내용이 표시됩니다:

 ```
 45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
 ```

 이것은 16진수와 사용자 친화적 형식으로 된 새로 생성된 영구 ADNL 주소입니다. 해당하는 개인키는 현재 디렉토리의 `45061...2DB` 파일에 저장됩니다. 키를 keyring 디렉토리로 이동하세요.

 ```bash
 mv 45061C1* keyring/
 ```

5. **rldp-http-proxy** 실행

 ```
 rldp-http-proxy/rldp-http-proxy -p 8080 -a <your_public_ip>:3333 -C global.config.json -A <your_adnl_address>
 ```

 여기서 `<your_public_ip>`는 공개 IPv4 주소이고 `<your_adnl_address>`는 이전 단계에서 생성한 ADNL 주소입니다.

 예시:

 ```
 rldp-http-proxy/rldp-http-proxy -p 8080 -a 777.777.777.777:3333 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
 ```

 위 예시에서 `8080`은 localhost에서 들어오는 HTTP 쿼리를 수신할 TCP 포트이며, `3333`은 모든 아웃바운드 및 인바운드 RLDP와 ADNL 활동에 사용될 UDP 포트입니다. `global.config.json`은 TON 글로벌 설정 파일의 이름입니다.

모든 것을 올바르게 수행했다면, 프록시는 종료되지 않고 터미널에서 계속 실행될 것입니다. 이제 TON Sites 접근에 사용할 수 있습니다. 더 이상 필요하지 않을 때는 `Ctrl-C`를 누르거나 터미널 창을 닫아 종료할 수 있습니다. Unix 서비스로 실행하여 영구적으로 실행할 수 있습니다.

진입 프록시는 `<your_public_ip>` 포트 `8080`에서 HTTP로 사용할 수 있습니다.

## TON Sites 접근하기

[위](#running-an-entry-proxy-on-a-remote-computer)에서 설명한 대로 컴퓨터에서 RLDP-HTTP 프록시가 실행되고 `localhost:8080`에서 인바운드 TCP 연결을 수신한다고 가정해봅시다.

모든 것이 제대로 작동하는지 테스트하는 간단한 방법은 `curl`이나 `wget` 같은 프로그램을 사용하는 것입니다. 예를 들어,

```
curl -x 127.0.0.1:8080 http://just-for-test.ton
```

이는 `127.0.0.1:8080`의 프록시를 사용하여 (TON) 사이트 `just-for-test.ton`의 메인 페이지를 다운로드하려고 시도합니다. 프록시가 실행 중이라면 다음과 같은 내용이 표시됩니다:

```html

<html>
<head>
<title>TON Site</title>
</head>
<body>
<h1>TON Proxy Works!</h1>
</body>
</html>

```

가짜 도메인 `<adnl-addr>.adnl`을 사용하여 ADNL 주소로도 TON Sites에 접근할 수 있습니다.

```bash
curl -x 127.0.0.1:8080 http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/
```

현재 동일한 TON 웹 페이지를 가져옵니다.

또는 브라우저에서 `localhost:8080`을 HTTP 프록시로 설정할 수 있습니다. Firefox를 사용하는 경우, [설정] -> 일반 -> 네트워크 설정 -> 설정 -> 프록시 액세스 구성 -> 수동 프록시 구성으로 이동하여 "HTTP 프록시" 필드에 "127.0.0.1"을, "포트" 필드에 "8080"을 입력하세요.

브라우저에서 `localhost:8080`을 HTTP 프록시로 설정하면, `http://just-for-test.ton` 또는 `http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/`와 같은 필요한 URI를 브라우저의 주소 표시줄에 입력하고 일반 웹 사이트와 동일한 방식으로 TON Site와 상호작용할 수 있습니다.

## TON Site 실행하기

:::tip 튜토리얼 발견!
[TON Site 실행 방법](/v3/guidelines/web3/ton-proxy-sites/how-to-run-ton-site) 초보자 친화적 튜토리얼로 시작하시는 건 어떠세요?
:::

대부분의 사람들은 새로운 TON Sites를 만들기보다는 기존 TON Sites에 접근하기만 하면 됩니다. 하지만 새로 만들고 싶다면, Apache나 Nginx와 같은 일반적인 웹 서버 소프트웨어와 함께 서버에서 RLDP-HTTP 프록시를 실행해야 합니다.

일반적인 웹사이트 설정 방법을 알고 있고, 서버에 이미 구성했으며, TCP 포트 `<your-server-ip>:80`에서 들어오는 HTTP 연결을 수락하고, 웹 서버 구성에서 필요한 TON 네트워크 도메인 이름(예: `example.ton`)을 메인 도메인 이름이나 별칭으로 정의했다고 가정합니다.

1. [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드하세요.

 또는 이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy)을 따라 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. TON [글로벌 설정](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config)을 다운로드하세요.

3. [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 **generate-random-id**를 다운로드하세요.

 또는 이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#generate-random-id)을 따라 **generate-random-id**를 직접 컴파일할 수 있습니다.

4. 서버용 영구 ADNL 주소 생성하기

 ```bash
 mkdir keyring

 utils/generate-random-id -m adnlid
 ```

 다음과 같은 내용이 표시됩니다:

 ```bash
 45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
 ```

 이것은 새로 생성된 지속적인 ADNL 주소로, 16진수와 사용자 친화적인 형태로 제공됩니다. 해당하는 개인 키는 현재 디렉토리의 `45061...2DB` 파일에 저장되었습니다. 이를 keyring 디렉토리로 이동시키세요.

 ```bash
 mv 45061C1* keyring/
 ```

5. 웹서버가 `.ton`과 `.adnl` 도메인의 HTTP 요청을 수락하도록 확인하세요.

 예를 들어 nginx에서 `server_name example.com;` 설정을 사용하는 경우, `server_name _;` 또는 `server_name example.com example.ton vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl;`로 변경해야 합니다.

6. 역방향 모드로 프록시 실행

 ```bash
 rldp-http-proxy/rldp-http-proxy -a <your-server-ip>:3333 -L '*' -C global.config.json -A <your-adnl-address> -d -l <log-file>
 ```

 여기서 `<your_public_ip>`는 서버의 공개 IPv4 주소이고 `<your_adnl_address>`는 이전 단계에서 생성한 ADNL 주소입니다.

TON Site를 영구적으로 실행하려면 `-d`와 `-l <log-file>` 옵션을 사용해야 합니다.

예시:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -L '*' -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

모든 것이 제대로 작동한다면, RLDP-HTTP 프록시는 IPv4 주소 `<your-server-ip>`의 UDP 포트 3333(원하는 경우 다른 UDP 포트를 사용할 수 있음)에서 실행되는 RLDP/ADNL을 통해 TON 네트워크로부터 들어오는 HTTP 쿼리를 수신합니다(특히 방화벽을 사용하는 경우 `rldp-http-proxy`가 이 포트에서 UDP 패킷을 수신하고 보낼 수 있도록 허용하는 것을 잊지 마세요). 모든 호스트로 향하는 이러한 HTTP 쿼리(특정 호스트만 전달하려면 `-L '*'`를 `-L <your hostname>`으로 변경)를 `127.0.0.1`의 TCP 포트 `80`(일반 웹 서버)으로 전달합니다.

"TON Sites 접근하기" 섹션에서 설명한 대로 클라이언트 기기에서 실행 중인 브라우저를 사용하여 TON Site `http://<your-adnl-address>.adnl`(이 예시에서는 `http://vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl`)을 방문하여 TON Site가 실제로 공개적으로 사용 가능한지 확인할 수 있습니다.

원하는 경우 'example.ton'과 같은 TON DNS 도메인을 [등록](/v3/guidelines/web3/ton-proxy-sites/site-and-domain-management)하고, 이 도메인에 대한 `site` 레코드를 TON Site의 영구 ADNL 주소를 가리키도록 생성할 수 있습니다. 그러면 클라이언트 모드에서 실행되는 RLDP-HTTP 프록시가 http://example.ton을 ADNL 주소를 가리키는 것으로 해석하고 TON Site에 접근할 것입니다.

별도의 서버에서 역방향 프록시를 실행하고 웹서버를 원격 주소로 설정할 수도 있습니다. 이 경우 `-L '*'` 대신 `-R '*'@<YOUR_WEB_SERVER_HTTP_IP>:<YOUR_WEB_SERVER_HTTP_PORT>`를 사용하세요.

예시:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -R '*'@333.333.333.333:80 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

이 경우 일반 웹서버는 `http://333.333.333.333:80`에서 사용할 수 있어야 합니다(이 IP는 외부에 노출되지 않음).

### 권장 사항

익명성은 TON Proxy 2.0에서만 사용할 수 있으므로, 웹 서버의 IP 주소를 공개하지 않으려면 다음 두 가지 방법으로 할 수 있습니다:

- 위에서 설명한 대로 `-R` 플래그를 사용하여 별도의 서버에서 역방향 프록시를 실행합니다.

- 웹사이트 사본이 있는 중복 서버를 만들고 로컬에서 역방향 프록시를 실행합니다.

