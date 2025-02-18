# TON Networking

Projekt TON wykorzystuje własne protokoły sieciowe peer-to-peer.

- **TON Blockchain wykorzystuje te protokoły** do propagacji nowych bloków, wysyłania i zbierania kandydatów do transakcji i tak dalej.

  Podczas gdy wymagania sieciowe projektów single-blockchain, takich jak Bitcoin czy Ethereum, można spełnić dość łatwo (zasadniczo trzeba zbudować
  sieć nakładkową peer-to-peer, a następnie propagować wszystkie nowe bloki i
  kandydatów do transakcji za pośrednictwem protokołu [gossip](https://en.wikipedia.org/wiki/Gossip_protocol)), podczas gdy projekty multi-blockchain, takie
  jak TON, są znacznie bardziej wymagające (np. trzeba być w stanie
  subskrybować aktualizacje tylko niektórych shardchainów, niekoniecznie wszystkich).

- \*\*Usługi ekosystemu TON (np. TON Proxy, TON Sites, TON Storage) działają w oparciu o te protokoły.

  Po wprowadzeniu bardziej wyrafinowanych protokołów sieciowych potrzebnych
  do obsługi TON Blockchain, okazuje się, że można je łatwo
  wykorzystać do celów niekoniecznie związanych z bezpośrednimi wymaganiami samego blockchaina
  , zapewniając w ten sposób większe możliwości i elastyczność tworzenia
  nowych usług w ekosystemie TON.
