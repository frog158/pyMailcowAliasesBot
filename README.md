# Бот для создания алиасов в [mailcow](https://github.com/mailcow/mailcow-dockerized)
## About
Я использую личный почтовый сервер на основе [mailcow](https://github.com/mailcow/mailcow-dockerized). Мне удобно при регистрации на сайтах указывать алиас вида site@my-domain.ru И мне надоело каждый раз ходить в настройки почтового сервера для создания алиасов. Этот бот получает название алиаса создает его. Для запуска необходимо
- Создать бота в телеграмме
- Сгенерировать API-ключ в настройках почтового сервера

## Установка
Создайте файл `.env`. В нем указываем токен бота, ключ API и URL сервера
```shell
SERVER_URL="https://mail.example.com"
X_API_KEY="key"
TG_BOT_TOKEN="bot token"
```
### docker
```shell
docker run --name mailcow-aliases --env-file .env -v ${PWD}:/data -d frog158/pymailcowaliasesbot
```
### docker compose
Скачайте `docker-compose.yml` и выполните
```shell
docker compose up -d 
```
## Управление пользователями
При первом запуске бот создат пустую sqlite базу. Для возможноси создания алиасов надо добвить пользователя. Для добавления нужно
- ID пользователя в телеге
- Имя пользователя 
- Имя домена в котором будут создаваться алиасы
- Адрес куда будет перенаправляться почта
### Создание 
```shell
docker exec -it mailcow-aliases add_user 123 Ivan example.com test@example.com
```
### Удаление
```shell
docker exec -it mailcow-aliases delete_user 123
```
### Получить список
```shell
docker exec -it mailcow-aliases get_all_users
```
## Использование
Все это делалось исходя из того, что у одного пользователя есть один домен. По этому для создания алиаса достаточно отправить название алиаса. Если алиась не удалось создать(он уже существует, существует такой ящик и прочие ошибки) бот пришлет сообщение об ошибке. 
