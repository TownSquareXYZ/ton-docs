# TON Networking

Проект TON використовує власні пірингові мережеві протоколи.

- **Блокчейн використовує ці протоколи** для розповсюдження нових блоків, надсилання та отримання кандидатів на транзакції тощо.

  У той час як мережеві вимоги одноблочних проектів, таких як Bitcoin або Ethereum, можна задовольнити досить легко (потрібно лише побудувати
  однорангову оверлейну мережу, а потім поширювати всі нові блоки і
  кандидатів на транзакції за допомогою протоколу [gossip](https://en.wikipedia.org/wiki/Gossip_protocol)), багатоблочні проекти, такі
  як TON, набагато вимогливіші (наприклад, потрібно мати можливість
  підписатися на оновлення лише деяких шардчейнів, а не обов'язково на всі).

- **Екосистемні послуги TON (наприклад, TON Proxy, TON Sites, TON Storage) працюють на основі цих протоколів.**.

  Як тільки більш складні мережеві протоколи, необхідні
  для підтримки блокчейну TON, будуть створені, виявиться, що їх можна легко
  використовувати для цілей, не обов'язково пов'язаних з безпосередніми потребами самого
  блокчейну, таким чином надаючи більше можливостей і гнучкості для створення
  нових послуг в екосистемі TON.