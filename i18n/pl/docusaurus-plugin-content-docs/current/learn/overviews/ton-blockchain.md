# Blockchain łańcuchów bloków

:::tip
Terminy "**smart contract**", "**account**" i "**actor**" są używane zamiennie w tym dokumencie w celu opisania podmiotu blockchain.
:::

## Pojedynczy aktor

Rozważmy jeden inteligentny kontrakt.

W TON jest to *rzecz* z właściwościami takimi jak `adres`, `kod`, `dane`, `bilans` i innymi. Innymi słowy, jest to obiekt, który posiada *storage* i *behavior*.
To zachowanie ma następujący wzór:

- coś się dzieje (najczęstszą sytuacją jest to, że umowa otrzymuje wiadomość)
- Kontrakt obsługuje to zdarzenie zgodnie z jego własnymi właściwościami, wykonując swój "kod" w wirtualnej maszynie TON.
- kontrakt modyfikuje swoje własne właściwości (`code`, `data` i inne)
- umowa opcjonalnie generuje wiadomości wychodzące
- Kontrakt przechodzi w tryb czuwania do momentu wystąpienia kolejnego zdarzenia

Kombinacja tych kroków nazywana jest **transakcją**. Ważne jest, aby zdarzenia były obsługiwane jedno po drugim, dlatego *transakcje* są ściśle uporządkowane i nie mogą się wzajemnie przerywać.

Ten wzorzec zachowania jest dobrze znany i nazywany "aktorem".

### Najniższy poziom: Łańcuch kont

Sekwencję *transakcji* `Tx1 -> Tx2 -> Tx3 -> ....` można nazwać **łańcuchem**. W rozważanym przypadku jest on nazywany **AccountChain**, aby podkreślić, że jest to *łańcuch* pojedynczego konta transakcji.

Teraz, ponieważ węzły przetwarzające transakcje muszą od czasu do czasu koordynować stan inteligentnego kontraktu (aby osiągnąć *konsensus* co do stanu), te *transakcje* są grupowane:
`[Tx1 -> Tx2] -> [Tx3 -> Tx4 -> Tx5] -> [] -> [Tx6]`.
Batching nie ingeruje w sekwencjonowanie, każda transakcja nadal ma tylko jeden "prev tx" i co najwyżej jeden "next tx", ale teraz ta sekwencja jest pocięta na **bloki**.

Wskazane jest również dołączenie kolejek wiadomości przychodzących i wychodzących do *blocks*. W takim przypadku *block* będzie zawierał pełny zestaw informacji, które określają i opisują, co stało się z inteligentnym kontraktem podczas tego bloku.

## Wiele łańcuchów kont: Shards

Rozważmy teraz wiele kont. Możemy uzyskać kilka *AccountChains* i przechowywać je razem, taki zestaw *AccountChains* nazywany jest **ShardChain**. W ten sam sposób możemy podzielić **ShardChain** na **ShardBlocks**, które są agregacją poszczególnych *AccountBlocks*.

### Dynamiczne dzielenie i łączenie łańcuchów ShardChains

Proszę zauważyć, że ponieważ *ShardChain* składa się z łatwo rozróżnialnych *AccountChains*, możemy go łatwo podzielić. W ten sposób, jeśli mamy 1 *ShardChain*, który opisuje zdarzenia, które mają miejsce z 1 milionem kont i jest zbyt wiele transakcji na sekundę, aby mogły być przetwarzane i przechowywane w jednym węźle, więc po prostu podzielimy (lub **split**) ten łańcuch na dwa mniejsze *ShardChains* z każdym łańcuchem odpowiadającym za pół miliona kont i każdym łańcuchem przetwarzanym na oddzielnym podzbiorze węzłów.

Analogicznie, jeśli niektóre odłamki stały się zbyt wolne, mogą zostać **połączone** w jeden większy odłamek.

Istnieją oczywiście dwa ograniczające przypadki: gdy shard zawiera tylko jedno konto (a zatem nie może być dalej dzielony) i gdy shard zawiera wszystkie konta.

Konta mogą wchodzić ze sobą w interakcje poprzez wysyłanie wiadomości. Istnieje specjalny mechanizm routingu, który przenosi wiadomości z kolejek wychodzących do odpowiednich kolejek przychodzących i zapewnia, że 1) wszystkie wiadomości zostaną dostarczone 2) wiadomości zostaną dostarczone kolejno (wiadomość wysłana wcześniej dotrze do celu wcześniej).

:::info UWAGA BOCZNA
Aby podział i łączenie były deterministyczne, agregacja AccountChains w shardy opiera się na bitowej reprezentacji adresów kont. Na przykład, adres wygląda jak `(prefiks shardu, adres)`. W ten sposób wszystkie konta w shardchainie będą miały dokładnie taki sam prefiks binarny (na przykład wszystkie adresy będą zaczynać się od `0b00101`).
:::

## Blockchain

Agregacja wszystkich odłamków, która zawiera wszystkie konta zachowujące się zgodnie z jednym zestawem reguł, nazywana jest **Blockchain**.

W TON może istnieć wiele zestawów reguł, a tym samym wiele łańcuchów bloków, które działają jednocześnie i mogą wchodzić ze sobą w interakcje poprzez wysyłanie wiadomości crosschain w taki sam sposób, w jaki konta jednego łańcucha mogą wchodzić ze sobą w interakcje.

### Workchain: Blockchain z własnymi zasadami

Jeśli chcą Państwo dostosować zasady grupy Shardchainów, można utworzyć **Workchain**. Dobrym przykładem jest stworzenie łańcucha roboczego, który działa w oparciu o EVM, aby uruchamiać na nim inteligentne kontrakty Solidity.

Teoretycznie każdy w społeczności może stworzyć własny łańcuch roboczy. W rzeczywistości jest to dość skomplikowane zadanie, aby go zbudować, a następnie zapłacić (kosztowną) cenę za jego utworzenie i otrzymać 2/3 głosów od walidatorów, aby zatwierdzić utworzenie Workchaina.

TON pozwala na utworzenie do `2^32` łańcuchów roboczych, każdy podzielony na do `2^60` shardów.

Obecnie w TON istnieją tylko 2 łańcuchy robocze: MasterChain i BaseChain.

BaseChain jest używany do codziennych transakcji między aktorami, ponieważ jest dość tani, podczas gdy MasterChain ma kluczową funkcję dla TON, więc omówmy, co robi!

### Masterchain: Blockchain of Blockchains

Istnieje konieczność synchronizacji routingu wiadomości i wykonywania transakcji. Innymi słowy, węzły w sieci potrzebują sposobu na ustalenie pewnego "punktu" w stanie multichain i osiągnięcie konsensusu co do tego stanu. W TON do tego celu wykorzystywany jest specjalny łańcuch o nazwie **MasterChain**. Bloki *masterchain* zawierają dodatkowe informacje (najnowsze skróty bloków) o wszystkich innych łańcuchach w systemie, dzięki czemu każdy obserwator jednoznacznie określa stan wszystkich systemów multichain w pojedynczym bloku masterchain.
