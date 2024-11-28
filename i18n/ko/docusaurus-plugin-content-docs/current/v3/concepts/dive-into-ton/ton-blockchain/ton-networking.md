# TON 네트워킹

TON 프로젝트는 자체적인 피어-투-피어 네트워크 프로토콜을 사용합니다.

- **TON 블록체인은 이러한 프로토콜을** 새로운 블록을 전파하고, 트랜잭션 후보를 전송하고 수집하는 등의 작업에 사용합니다.

  비트코인이나 이더리움과 같은 단일 블록체인 프로젝트의 네트워킹 요구사항은 꽤 쉽게 충족될 수 있지만(본질적으로 피어-투-피어 오버레이 네트워크를 구성하고 [가십](https://en.wikipedia.org/wiki/Gossip_protocol) 프로토콜을 통해 모든 새로운 블록과 트랜잭션 후보를 전파하면 됨), TON과 같은 멀티 블록체인 프로젝트는 훨씬 더 까다롭습니다(예를 들어, 모든 샤드체인이 아닌 일부 샤드체인의 업데이트만 구독할 수 있어야 함).

- **TON 생태계 서비스(예: TON 프록시, TON 사이트, TON 스토리지)는 이러한 프로토콜 위에서 실행됩니다.**

  TON 블록체인을 지원하는 데 필요한 더 정교한 네트워크 프로토콜이 구축되면, 이들이 블록체인 자체의 즉각적인 요구사항과 반드시 관련되지 않은 목적으로도 쉽게 사용될 수 있음이 밝혀졌습니다. 이는 TON 생태계에서 새로운 서비스를 만드는 데 더 많은 가능성과 유연성을 제공합니다.

## 참고

- [ADNL 프로토콜](/v3/documentation/network/protocols/adnl/overview)
- [오버레이 서브네트워크](/v3/documentation/network/protocols/overlay)
- [RLDP 프로토콜](/v3/documentation/network/protocols/rldp)
- [TON DHT 서비스](/v3/documentation/network/protocols/dht/ton-dht)
