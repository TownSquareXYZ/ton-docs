# Обслуживание и безопасность

## <a id="introduction"></a>Введение

В этом руководстве представлена ​​базовая информация об обслуживании и защите узлов валидатора TON.

В этом документе предполагается, что валидатор установлен с использованием конфигурации и инструментов **[рекомендованных TON Foundation](/v3/guidelines/nodes/running-nodes/full-node)**, н но общие концепции применимы и к другим сценариям и могут быть полезны для опытных системных администраторов.

## <a id="maintenance"></a>Техническое обслуживание

### <a id="database-grooming"></a>Уход за базой данных

Узел TON хранит свою базу данных в пределах пути, указанного флагом `--db validator-engine`, обычно `/var/ton-work/db`. Чтобы уменьшить размер базы данных, вы можете уменьшить TTL (время жизни) некоторых сохраненных данных.

Текущие значения TTL можно найти в файле службы узла (путь по умолчанию — `/etc/systemd/system/validator.service`). Если вы используете MyTonCtrl, вы можете использовать команду `installer status`. Если какие-либо из значений не установлены, то используются стандартные значения.

### archive-ttl

`archive-ttl` - это параметр, который определяет время жизни для блоков. Стандартное значение — 604800 секунд (7 дней). Вы можете уменьшить это значение для сжатия базы данных.

```bash
MyTonCtrl> installer set_node_argument --archive-ttl <value>
```

Если вы не используете MyTonCtrl, вы можете отредактировать файл службы узла.

### state-ttl

`state-ttl` - это параметр, который определяет время жизни состояний блоков. Значение по умолчанию — 86400 секунд (24 часа). Вы можете уменьшить это значение для сжатия базы данных, но для валидаторов крайне рекомендуется использовать стандартное значение (не устанавливайте флаг).
Также это значение должно быть больше продолжительности периода валидации (значение можно найти в [15-м параметре конфигурации](https://docs.ton.org/v3/documentation/network/configs/blockchain-configs#param-15)).

```bash
MyTonCtrl> installer set_node_argument --state-ttl <value>
```

Если вы не используете MyTonCtrl, вы можете отредактировать файл службы узла.

### <a id="backups"></a>Резервное копирование

Самый простой и эффективный способ сделать резервную копию валидатора — скопировать важные файлы конфигурации узла, ключи и настройки mytonctrl:

- Файл конфигурации узла: `/var/ton-work/db/config.json`
- Закрытый ключ узла: `/var/ton-work/db/keyring`
- Открытый ключ узла: `/var/ton-work/keys`
- Конфигурация и кошельки mytonctrl: `$HOME/.local/share/myton*`, где $HOME - домашний каталог пользователя, который начал установку mytonctrl **или** `/usr/local/bin/mytoncore`, если вы установили mytonctrl как root.

Этот набор — все, что вам нужно для восстановления вашего узла с нуля.

#### Снимки

Современные файловые системы, такие как ZFS, предлагают функцию снимков, большинство поставщиков облачных услуг также позволяют своим клиентам делать снимки своих машин, во время которых весь диск сохраняется для будущего использования.

Проблема с обоими методами заключается в том, что вы должны остановить узел перед выполнением снимка, невыполнение этого требования, скорее всего, приведет к повреждению базы данных с неожиданными последствиями. Многие поставщики облачных услуг также требуют, чтобы вы выключали машину перед выполнением снимка.

Такие остановки не следует выполнять часто, если вы делаете снимок своего узла раз в неделю, то в худшем случае после восстановления у вас будет узел с недельной базой данных, и вашему узлу потребуется больше времени, чтобы догнать сеть, чем для выполнения новой установки с использованием функции mytonctrl "install from dump" (флаг -d добавляется во время вызова скрипта install.sh).

### <a id="disaster-recovery"></a>Аварийное восстановление

Чтобы выполнить восстановление вашего узла на новой машине:

#### Установите mytonctrl / node

Для самого быстрого запуска узла добавьте ключ `-d` при вызове скрипта установки.

#### Переключитесь на пользователя root

```sh
sudo -s
```

#### Остановите процессы mytoncore и validator

```sh
systemctl stop validator
systemctl stop mytoncore
```

#### Примените резервные копии файлов конфигурации узла

- Файл конфигурации узла: `/var/ton-work/db/config.json`
- Закрытый ключ узла: `/var/ton-work/db/keyring`
- Открытый ключ узла: `/var/ton-work/keys`

#### <a id="set-node-ip"></a> Установите IP-адрес узла

Если у вашего нового узла другой IP-адрес, то вы должны отредактировать файл конфигурации узла `/var/ton-work/db/config.json` и установить `.addrs[0].ip` в **десятичное** значение нового IP-адреса. Вы можете использовать **[этот](https://github.com/sonofmom/ton-tools/blob/master/node/ip2dec.py)** скрипт Python для преобразования вашего IP в десятичное значение.

#### Убедитесь, что у вас правильные разрешения на использование базы данных

```sh
chown -R validator:validator /var/ton-work/db
```

#### Примените файлы конфигурации mytonctrl из резервной копии

Замените `$HOME/.local/share/myton*`, где $HOME - домашний каталог пользователя, который начал установку mytonctrl, на резервную копию содержимого, убедитесь, что пользователь является владельцем всех копируемых файлов.

#### Запустите процессы mytoncore и validator

```sh
systemctl start validator
systemctl start mytoncore
```

## <a id="security"></a>Безопасность

### <a id="host-security"></a>Безопасность на уровне хоста

Безопасность на уровне хоста — это огромная тема, которая выходит за рамки этого документа, однако мы рекомендуем вам никогда не устанавливать mytonctrl под пользователем root, используйте учетную запись службы для обеспечения разделения привилегий.

### <a id="network-security"></a>Безопасность на сетевом уровне

Валидаторы TON — это ценные активы, которые следует защищать от внешних угроз, один из первых шагов, которые вы должны предпринять, — сделать свой узел максимально невидимым, это означает блокировку всех сетевых подключений. На узле валидатора только UDP-порт, используемый для операций узла, должен быть открыт для Интернета.

#### Инструменты

Мы будем использовать интерфейс брандмауэра **[ufw](https://help.ubuntu.com/community/UFW)**, а также JSON процессор для командной строки **[jq](https://github.com/stedolan/jq)**.

#### Управление сетями

Как оператор узла, вам необходимо сохранить полный контроль и доступ к машине, для этого вам нужен как минимум один фиксированный IP-адрес или диапазон адресов.

Мы также советуем вам настроить небольшой VPS-сервер "jumpstation" с фиксированным IP-адресом, который вы сможете использовать для доступа к заблокированным машинам, если у вас нет фиксированного IP-адреса дома/в офисе, или для добавления альтернативного способа доступа к защищенным машинам в случае потери основного IP-адреса.

#### Установите ufw и jq1

```sh
sudo apt install -y ufw jq
```

#### Базовая настройка сетевого фильтра при помощи UFW

```sh
sudo ufw default deny incoming; sudo ufw default allow outgoing
```

#### Отключение автоматического приема ICMP-запросов

```sh
sudo sed -i 's/-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/#-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT/g' /etc/ufw/before.rules
```

#### Включите полный доступ из сетей управления

```sh
sudo ufw insert 1 allow from <MANAGEMENT_NETWORK>
```

повторите указанную выше команду для каждой сети управления/адреса.

#### Откройте порт UDP узла/валидатора для общего доступа

```sh
sudo ufw allow proto udp from any to any port `sudo jq -r '.addrs[0].port' /var/ton-work/db/config.json`
```

#### Перепроверьте сети управления

<mark>Важно</mark>: перед включением брандмауэра дважды проверьте, что вы добавили правильные адреса управления!

#### Включите брандмауэр ufw

```sh
sudo ufw enable
```

#### Проверьте состояние

Чтобы проверить состояние брандмауэра, используйте следующую команду:

```sh
    sudo ufw status numbered
```

Вот пример вывода заблокированного узла с двумя сетями управления/адресами:

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] Anywhere                   ALLOW IN    <MANAGEMENT_NETWORK_A>/28
[ 2] Anywhere                   ALLOW IN    <MANAGEMENT_NETWORK_B>/32
[ 3] <NODE_PORT>/udp            ALLOW IN    Anywhere
[ 4] <NODE_PORT>/udp (v6)       ALLOW IN    Anywhere (v6)
```

#### Откройте порт LiteServer

```sh
sudo ufw allow proto tcp from any to any port `sudo jq -r '.liteservers[0].port' /var/ton-work/db/config.json`
```

Обратите внимание, что порт LiteServer не должен быть открыт публично на валидаторе.

#### Дополнительная информация о UFW

См. это превосходное **[руководство по ufw](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)** от Digital Ocean для получения дополнительной информации о магии ufw.

### <a id="ip-switch"></a>Переключение IP-адреса

Если вы считаете, что ваш узел подвергся атаке, вам следует рассмотреть возможность смены IP-адреса. Способ переключения зависит от вашего хостинг-провайдера; вы можете предварительно заказать второй адрес, клонировать **остановленную** виртуальную машину в другой экземпляр или настроить новый экземпляр, выполнив процесс **[аварийного восстановления](#disaster-recovery)**.

В любом случае убедитесь, что вы **[установили свой новый IP-адрес](/v3/guidelines/nodes/node-maintenance-and-security#-set-node-ip-address)** в файле конфигурации узла!