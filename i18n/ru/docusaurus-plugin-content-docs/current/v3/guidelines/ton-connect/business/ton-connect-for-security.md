# TON Connect для обеспечения безопасности

TON Connect обеспечивает пользователям полный контроль над данными, которыми они делятся, что исключает утечку данных при передаче между приложением и кошельком. Для усиления этой системы кошельки и приложения используют надежные криптографические системы аутентификации, которые работают совместно.

## Безопасность пользовательских данных и средств

- В TON Connect данные пользователей шифруются от конца до конца при передаче в кошельки через мосты. Это позволяет приложениям и кошелькам использовать сторонние серверы-мосты, которые снижают вероятность кражи и манипуляции данными, значительно повышая их целостность и безопасность.
- В TON Connect предусмотрены параметры безопасности, позволяющие напрямую аутентифицировать данные пользователей с адресом их кошелька. Это позволяет пользователям использовать несколько кошельков и выбирать, какой из них будет использоваться в конкретном приложении.
- Протокол TON Connect позволяет передавать персональные данные (например, контактные данные, информацию о KYC и т.д.) при условии, что пользователь явно подтверждает передачу таких данных.

Конкретные детали и примеры кода, связанные с TON Connect и его ориентированным на безопасность дизайном, можно найти на [TON Connect GitHub] (https://github.com/ton-connect/).