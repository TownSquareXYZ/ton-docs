# 자체 TON 프록시 실행

이 문서의 목적은 TON 네트워크를 통해 액세스하는 웹사이트인 TON 사이트에 대한 간략한 소개를 제공하는 것입니다. TON 사이트는 다른 TON 서비스를 위한 편리한 진입점으로 사용될 수 있습니다. 특히, TON 사이트에서 다운로드한 HTML 페이지에는 `ton://...` URI에 대한 링크가 포함될 수 있으며, 사용자의 기기에 TON 월렛이 설치되어 있는 경우 사용자가 해당 링크를 클릭하여 결제를 수행할 수 있습니다.

기술적인 관점에서 보면 TON 사이트는 일반 웹사이트와 매우 유사하지만, 인터넷이 아닌 인터넷 내부의 오버레이 네트워크인 [TON 네트워크](/learn/네트워킹/오버뷰)를 통해 액세스됩니다. 보다 구체적으로, 일반적인 IPv4 또는 IPv6 주소 대신 [ADNL](/learn/네트워킹/adnl) 주소를 사용하며, 일반적인 TCP/IP 대신 [RLDP](/learn/네트워킹/rldp) 프로토콜(TON 네트워크의 기본 프로토콜인 ADNL에 기반한 상위 수준의 RPC 프로토콜)을 통해 HTTP 쿼리를 수락합니다. 모든 암호화는 ADNL에서 처리되므로 엔트리 프록시가 사용자 디바이스에서 로컬로 호스팅되는 경우 HTTPS(즉, TLS)를 사용할 필요가 없습니다.

기존 사이트에 액세스하고 새로운 TON을 생성하기 위해서는 "일반" 인터넷과 TON 네트워크 사이에 특별한 게이트웨이가 필요합니다. 기본적으로 TON 사이트는 클라이언트 컴퓨터에서 로컬로 실행되는 HTTP->RLDP 프록시의 도움으로 액세스되며, 원격 웹 서버에서 실행되는 역방향 RLDP->HTTP 프록시를 통해 생성됩니다.

[TON 사이트, WWW 및 프록시에 대해 자세히 알아보기](https://blog.ton.org/ton-sites)

## 항목 프록시 실행

기존 TON 사이트에 액세스하려면 컴퓨터에서 RLDP-HTTP 프록시를 실행해야 합니다.

1. TON 자동 빌드](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드합니다.

   또는 다음 [지침](/개발/방법/컴파일#rldp-http-proxy)에 따라 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. [다운로드](/개발/하우투/컴파일#다운로드-글로벌-config) TON 글로벌 설정.

3. rldp-http-proxy\*\*를 실행합니다.

   ```bash
   rldp-http-proxy/rldp-http-proxy -p 8080 -c 3333 -C global.config.json
   ```

위의 예에서 `8080`은 수신 HTTP 쿼리에 대해 localhost에서 수신 대기할 TCP 포트이고, `3333`은 모든 아웃바운드 및 인바운드 RLDP 및 ADNL 활동(즉, TON 네트워크를 통해 TON 사이트에 연결할 때)에 사용되는 UDP 포트입니다. global.config.json\`은 TON 글로벌 구성의 파일명입니다.

모든 작업을 올바르게 완료했다면 입력 프록시는 종료되지 않고 터미널에서 계속 실행됩니다. 이제 TON 사이트에 액세스하는 데 사용할 수 있습니다. 더 이상 필요하지 않은 경우 `Ctrl-C`를 누르거나 터미널 창을 닫아 종료할 수 있습니다.

입력 프록시는 `localhost` 포트 `8080`에서 HTTP로 사용할 수 있습니다.

## 원격 컴퓨터에서 항목 프록시 실행

1. TON 자동 빌드](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드합니다.

   또는 다음 [지침](/개발/방법/컴파일#rldp-http-proxy)에 따라 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. [다운로드](/개발/하우투/컴파일#다운로드-글로벌-config) TON 글로벌 설정.

3. TON 자동 빌드](https://github.com/ton-blockchain/ton/releases/latest)에서 **generate-random-id**를 다운로드합니다.

   또는 다음 [지침](/개발/방법/컴파일#생성-랜덤-ID)에 따라 **생성-랜덤-ID**를 직접 컴파일할 수 있습니다.

4. 엔트리 프록시를 위한 영구 ANDL 주소 생성하기

   ```bash
   mkdir keyring

   utils/generate-random-id -m adnlid
   ```

   다음과 같은 내용이 표시됩니다.

   ```
   45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   새로 생성된 16진수 형식의 사용자 친화적인 영구 ADNL 주소입니다. 해당 개인 키는 현재 디렉터리의 `45061...2DB` 파일에 저장됩니다. 키를 키링 디렉터리로 이동

   ```bash
   mv 45061C1* keyring/
   ```

5. rldp-http-proxy\*\*를 실행합니다.

   ```
   rldp-http-proxy/rldp-http-proxy -p 8080 -a <your_public_ip>:3333 -C global.config.json -A <your_adnl_address>
   ```

   여기서 `<your_public_ip>`는 공용 IPv4 주소이고 `<your_adnl_address>`는 이전 단계에서 생성한 ADNL 주소입니다.

   예시:

   ```
   rldp-http-proxy/rldp-http-proxy -p 8080 -a 777.777.777.777:3333 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   위의 예에서 `8080`은 수신 HTTP 쿼리에 대해 localhost에서 수신 대기할 TCP 포트이고, `3333`은 모든 아웃바운드 및 인바운드 RLDP 및 ADNL 활동(즉, TON 네트워크를 통해 TON 사이트에 연결할 때)에 사용되는 UDP 포트입니다. global.config.json\`은 TON 글로벌 구성의 파일명입니다.

모든 작업을 올바르게 완료했다면 프록시는 종료되지 않고 터미널에서 계속 실행됩니다. 이제 TON 사이트에 액세스하는 데 사용할 수 있습니다. 더 이상 필요하지 않은 경우 `Ctrl-C`를 누르거나 터미널 창을 닫아 종료할 수 있습니다. 유닉스 서비스로 실행하여 영구적으로 실행할 수 있습니다.

입력 프록시는 `<your_public_ip>` 포트 `8080`에서 HTTP로 사용할 수 있습니다.

## TON 사이트 액세스

이제 [위](#running-entry-proxy)에서 설명한 대로 컴퓨터에서 실행 중인 RLDP-HTTP 프록시 인스턴스가 있고 인바운드 TCP 연결을 위해 '로컬 호스트:8080'에서 수신 대기 중이라고 가정해 보겠습니다.

모든 것이 제대로 작동하는지 간단한 테스트는 `curl` 또는 `wget`과 같은 프로그램을 사용하여 수행할 수 있습니다. 예를 들어

```
curl -x 127.0.0.1:8080 http://just-for-test.ton
```

127.0.0.1:8080`에서 프록시를 사용하여 (TON) 사이트 `just-for-test.ton\`의 메인 페이지를 다운로드하려고 시도합니다. 프록시가 실행 중이면 다음과 같은 내용이 표시됩니다.

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

또한 가짜 도메인 `<adnl-addr>.adnl`을 사용하여 ADNL 주소를 통해 TON 사이트에 액세스할 수도 있습니다.

```bash
curl -x 127.0.0.1:8080 http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/
```

는 현재 동일한 TON 웹 페이지를 가져옵니다.

또는 브라우저에서 `localhost:8080`을 HTTP 프록시로 설정할 수 있습니다. 예를 들어 Firefox를 사용하는 경우 [설정] -> 일반 -> 네트워크 설정 -> 설정 -> 프록시 액세스 구성 -> 수동 프록시 구성으로 이동하여 "HTTP 프록시" 필드에 "127.0.0.1"을, "포트" 필드에 "8080"을 입력합니다.

브라우저에서 사용할 HTTP 프록시로 `localhost:8080`을 설정한 후에는 브라우저 탐색창에 `http://just-for-test.ton` 또는 `http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/`과 같은 필수 URI를 입력하기만 하면 일반 웹 사이트와 동일한 방식으로 TON 사이트와 상호 작용할 수 있습니다.

## TON 사이트 실행

:::tip 튜토리얼을 찾았습니다!
초보자를 위한 튜토리얼 [톤 사이트 실행 방법](/개발/앱/튜토리얼/how-to-run-ton-site)부터 시작하세요.
:::

대부분의 사람들은 새 사이트를 만들지 않고 기존 TON 사이트에 액세스하기만 하면 됩니다. 하지만 새 사이트를 만들려면 서버에서 Apache 또는 Nginx와 같은 일반적인 웹 서버 소프트웨어와 함께 RLDP-HTTP 프록시를 실행해야 합니다.

일반 웹사이트를 설정하는 방법을 이미 알고 있고, 서버에 이미 웹사이트를 구성했으며, TCP 포트 `<your-server-ip>:80`에서 들어오는 HTTP 연결을 수락하고 있고, 웹 서버 구성에서 웹사이트의 기본 도메인 이름 또는 별칭으로 필요한 TON 네트워크 도메인 이름(예: `example.ton`)을 정의했다고 가정해 보겠습니다.

1. TON 자동 빌드](https://github.com/ton-blockchain/ton/releases/latest)에서 **rldp-http-proxy**를 다운로드합니다.

   또는 다음 [지침](/개발/방법/컴파일#rldp-http-proxy)을 통해 **rldp-http-proxy**를 직접 컴파일할 수 있습니다.

2. [다운로드](/개발/하우투/컴파일#다운로드-글로벌-config) TON 글로벌 설정.

3. TON 자동 빌드](https://github.com/ton-blockchain/ton/releases/latest)에서 **generate-random-id**를 다운로드합니다.

   또는 다음 [지침](/개발/방법/컴파일#생성-랜덤-ID)에 따라 **생성-랜덤-ID**를 직접 컴파일할 수 있습니다.

4. 서버의 영구 ANDL 주소 생성하기

   ```bash
   mkdir keyring

   utils/generate-random-id -m adnlid
   ```

   다음과 같은 내용이 표시됩니다.

   ```bash
   45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   새로 생성된 16진수 형식의 사용자 친화적인 영구 ADNL 주소입니다. 해당 개인 키는 현재 디렉터리의 `45061...2DB` 파일에 저장됩니다. 키링 디렉터리로 이동합니다.

   ```bash
   mv 45061C1* keyring/
   ```

5. 웹서버가 '.ton' 및 '.adnl' 도메인을 가진 HTTP 요청을 허용하는지 확인하세요.

   예를 들어 `서버_이름 예제닷컴;` 구성으로 nginx를 사용하는 경우 `서버_이름 _;` 또는 `서버_이름 예제닷컴 예제.ton vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl;`로 변경해야 합니다.

6. 역방향 모드에서 프록시 실행

   ```bash
   rldp-http-proxy/rldp-http-proxy -a <your-server-ip>:3333 -L '*' -C global.config.json -A <your-adnl-address> -d -l <log-file>
   ```

   여기서 `<your_public_ip>`는 서버 공인 IPv4 주소이고 `<your_adnl_address>`는 이전 단계에서 생성한 ADNL 주소입니다.

TON 사이트를 영구적으로 실행하려면 `-d` 및 `-l <log-file>` 옵션을 사용해야 합니다.

예시:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -L '*' -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

모든 것이 정상적으로 작동하면 RLDP-HTTP 프록시는 IPv4 주소 `<your-server-ip>`의 UDP 포트 3333(물론 원하는 경우 다른 UDP 포트를 사용할 수 있음)에서 실행되는 RLDP/ADNL을 통해 TON 네트워크에서 들어오는 HTTP 쿼리를 받아들입니다(특히 방화벽을 사용하는 경우), 이 포트에서 UDP 패킷을 수신하고 보낼 수 있도록 `rldp-http-proxy`를 허용하는 것을 잊지 마세요), 모든 호스트(특정 호스트만 전달하려면 `-L '*'`를 `-L <your hostname>`로 변경)로 주소가 지정된 HTTP 쿼리를 `80`의 TCP 포트 `127`로 전달합니다.0.0.1\`(즉, 일반 웹 서버로)로 전달합니다.

클라이언트 컴퓨터에서 실행 중인 브라우저에서 "TON 사이트 액세스하기" 섹션에 설명된 대로 TON 사이트 `http://<your-adnl-address>.adnl`(이 예에서는 `http://vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl`)을 방문하여 TON 사이트가 실제로 공개되어 있는지 확인할 수 있습니다.

원하는 경우, 'example.ton'과 같은 TON DNS 도메인을 [등록](/participate/web3/site-management)하고 이 도메인에 대한 `site` 레코드가 TON 사이트의 영구 ADNL 주소를 가리키도록 만들 수 있습니다. 그러면 클라이언트 모드에서 실행되는 RLDP-HTTP 프록시는 http://example.ton 을 ADNL 주소를 가리키는 것으로 확인하여 TON 사이트에 액세스합니다.

별도의 서버에서 역방향 프록시를 실행하고 웹서버를 원격 주소로 설정할 수도 있습니다. 이 경우 `-L '*'` 대신 `-R '*'@<YOUR_WEB_SERVER_HTTP_IP>:<YOUR_WEB_SERVER_HTTP_PORT>`를 사용합니다.

예시:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -R '*'@333.333.333.333:80 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

이 경우 일반 웹서버는 http://333.333.333.333:80(이 IP는 외부에 노출되지 않음)에서 사용할 수 있어야 합니다.

### 권장 사항

익명성은 TON 프록시 2.0에서만 사용할 수 있으므로 웹 서버의 IP 주소를 공개하고 싶지 않은 경우 두 가지 방법으로 익명성을 설정할 수 있습니다:

- 위에서 설명한 대로 `-R` 플래그를 사용하여 별도의 서버에서 리버스 프록시를 실행합니다.

- 웹사이트 사본으로 복제 서버를 만들고 로컬에서 역방향 프록시를 실행합니다.
