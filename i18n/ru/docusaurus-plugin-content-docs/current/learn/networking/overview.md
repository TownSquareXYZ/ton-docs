# TON Networking

Проект TON использует собственные протоколы одноранговой сети.

- Блокчейн **TON использует эти протоколы** для распространения новых блоков, отправки и сбора кандидатов на транзакцию и так далее.

  В то время как сетевые требования одноблокчейновых проектов, таких как Bitcoin или Ethereum, могут быть удовлетворены довольно легко (по сути, необходимо построить
  одноранговую оверлейную сеть и затем распространять все новые блоки и
  кандидатов на транзакции с помощью протокола [gossip](https://en.wikipedia.org/wiki/Gossip_protocol)), многоблокчейновые проекты, такие как
  TON, гораздо более требовательны (например, необходимо иметь возможность
  подписаться на обновления только некоторых шардчейнов, не обязательно всех).

- Сервисы экосистемы **TON (например, TON Proxy, TON Sites, TON Storage) работают на этих протоколах.**.

  Как только более сложные сетевые протоколы, необходимые
  для поддержки блокчейна TON, будут созданы, окажется, что их можно легко
  использовать для целей, не обязательно связанных с непосредственными потребностями самого
  блокчейна, что дает больше возможностей и гибкости для создания
  новых услуг в экосистеме TON.