1. Функциональные требования

Система должна поддерживать следующие функции:

заказ такси пользователем;
начало и конец работы водителя;
подбор ближайшего водителя для поездки;
подтверждение или отклонение заказа водителем;
наблюдение за поездкой в реальном времени;
просмотр истории поездок.

Основные участники системы:

Passenger — пассажир;
Driver — водитель;
Order — заказ;
Trip — поездка;
Vehicle — автомобиль;
Location — координаты;
Payment — платёж.
2. Нефункциональные требования

Исходные данные:

Параметр	Значение
Количество пассажиров	100 млн
Количество водителей	5 млн
Поездок на пассажира	1 в день
Поездок на водителя	20 в день
Средняя длительность поездки	30 минут
Response time	до 1 минуты
Availability	95–99%
3. Расчёт нагрузки
3.1 Количество поездок

Каждый пассажир совершает 1 поездку в день:

100 000 000 пассажиров × 1 поездка/день = 100 000 000 поездок/день

Проверим по водителям:

5 000 000 водителей × 20 поездок/день = 100 000 000 поездок/день

Баланс сходится.

Итого система должна обрабатывать:

100 млн поездок в день
3.2 RPS создания заказов

В сутках:

24 × 60 × 60 = 86 400 секунд

Средняя нагрузка на создание заказов:

100 000 000 / 86 400 ≈ 1 157 заказов/сек

С учётом утренних и вечерних пиков берём коэффициент 3–5.

Пиковая нагрузка ≈ 5 000–10 000 заказов/сек
3.3 Одновременные активные поездки

Средняя длительность поездки — 30 минут, то есть 0.5 часа.

100 000 000 поездок/день × 0.5 часа / 24 часа
≈ 2 083 333 активных поездки

В среднем одновременно активно:

~2 млн поездок

В пике:

~5–6 млн активных поездок
3.4 Онлайн-водители

Каждый водитель выполняет 20 поездок в день.

20 поездок × 30 минут = 600 минут = 10 часов

Если водитель находится онлайн около 10 часов в день:

5 000 000 × 10 / 24 ≈ 2 083 333 онлайн-водителя

В пике может быть:

3–5 млн онлайн-водителей
3.5 Обновления геолокации

Пусть водитель отправляет координаты раз в 5 секунд.

Для 3 млн онлайн-водителей:

3 000 000 / 5 = 600 000 location updates/sec

Для 5 млн онлайн-водителей:

5 000 000 / 5 = 1 000 000 location updates/sec

Итого Location Service должен выдерживать:

до 1 млн обновлений координат в секунду

Это самая тяжёлая часть системы.

4. Основные сущности
4.1 User

Пользователь-пассажир.

Поля:

id: String
name: String
phone: String
paymentMethod: String
rating: Float

Методы:

createOrder(pickup, dropoff)
cancelOrder(orderId)
getTripHistory()

Связи:

User 1 -> 0..* Order

Один пользователь может создать много заказов.

4.2 Driver

Водитель.

Поля:

id: String
userId: String
vehicleId: String
status: DriverStatus
currentLocation: Location
rating: Float

Методы:

startShift()
endShift()
acceptOrder(orderId)
rejectOrder(orderId)
updateLocation(location)

Связи:

Driver 1 -> 1 Vehicle
Driver 1 -> 0..* Order
Driver 1 -> 0..* Trip
Driver 1 -> 1 Location
4.3 Vehicle

Автомобиль.

Поля:

id: String
driverId: String
licensePlate: String
model: String
color: String
tariffClass: String

Связи:

Vehicle 1 -> 1 Driver
4.4 Order

Заказ такси.

Поля:

id: String
passengerId: String
driverId: String?
pickupLocation: Location
dropoffLocation: Location
status: OrderStatus
price: Float
createdAt: DateTime
updatedAt: DateTime

Методы:

calculateFare()
assignDriver(driverId)
cancel()
expire()

Статусы заказа:

CREATED
SEARCHING_DRIVER
OFFERED_TO_DRIVER
ACCEPTED
CANCELLED
EXPIRED

Связи:

Order 1 -> 1 User
Order 0..1 -> 1 Driver
Order 1 -> 2 Location
Order 0..1 -> 1 Trip
4.5 Trip

Поездка.

Поля:

id: String
orderId: String
passengerId: String
driverId: String
status: TripStatus
startedAt: DateTime
finishedAt: DateTime?
route: List<Location>
price: Float

Методы:

start()
finish()
updateRoute(location)

Статусы поездки:

DRIVER_ARRIVING
IN_PROGRESS
COMPLETED
CANCELLED

Связи:

Trip 1 -> 1 Order
Trip 1 -> 1 User
Trip 1 -> 1 Driver
Trip 1 -> 0..* Location
Trip 1 -> 0..1 Payment
4.6 Location

Координаты.

Поля:

latitude: Float
longitude: Float
timestamp: DateTime

Используется для:

точки посадки;
точки назначения;
текущего положения водителя;
хранения маршрута поездки.
4.7 Payment

Платёж.

Поля:

id: String
tripId: String
userId: String
amount: Float
status: PaymentStatus
paymentMethod: String
createdAt: DateTime

Методы:

authorize()
capture()
refund()

Статусы платежа:

PENDING
AUTHORIZED
PAID
FAILED
REFUNDED
5. UML-подобная доменная модель
User 1 -------- 0..* Order

Driver 1 ------ 0..* Order

Order 1 ------- 0..1 Trip

Trip 1 -------- 0..1 Payment

Trip 1 -------- 0..* Location

Driver 1 ------ 1 Vehicle

Driver 1 ------ 1 Location

Order 1 ------- 2 Location
6. Архитектура системы
6.1 Общая схема компонентов
Passenger App
Driver App
Admin Panel
    |
API Gateway
    |
-------------------------------------------------
| User Service                                  |
| Driver Service                                |
| Order Service                                 |
| Matching Service                              |
| Trip Service                                  |
| Location Service                              |
| Pricing Service                               |
| Payment Service                               |
| Notification Service                          |
| History Service                               |
| Rating / Fraud Service                        |
-------------------------------------------------
    |
Kafka / Pulsar
    |
-------------------------------------------------
| PostgreSQL / MySQL                            |
| Redis Cluster                                 |
| Geo Index                                     |
| Cassandra / ScyllaDB                          |
| ClickHouse                                    |
| Object Storage / S3                           |
-------------------------------------------------
6.2 API Gateway

API Gateway принимает запросы от мобильных приложений.

Основные задачи:

авторизация;
rate limiting;
маршрутизация запросов;
проверка токенов;
защита от перегрузки;
логирование.
6.3 Order Service

Order Service отвечает за жизненный цикл заказа.

Функции:

создание заказа;
отмена заказа;
изменение статуса заказа;
передача заказа в Matching Service;
сохранение заказа в историю.
6.4 Matching Service

Matching Service отвечает за подбор водителя.

Алгоритм:

1. Получить pickup location.
2. Найти H3 / Geohash ячейку.
3. Получить свободных водителей в этой ячейке.
4. Если водителей мало — проверить соседние ячейки.
5. Отфильтровать водителей по тарифу, статусу и рейтингу.
6. Посчитать ETA до пассажира.
7. Отправить offer лучшему кандидату.
8. Если отказ или timeout — попробовать следующего.
6.5 Location Service

Location Service — самый нагруженный сервис.

Он принимает координаты от водителей:

driver_id
latitude
longitude
speed
heading
timestamp

Далее сервис:

обновляет Redis;
обновляет Geo Index;
отправляет событие в Kafka;
передаёт координаты пассажиру через WebSocket;
асинхронно сохраняет маршрут поездки.
6.6 Trip Service

Trip Service отвечает за выполнение поездки.

Статусы поездки:

DRIVER_ASSIGNED
DRIVER_ARRIVING
IN_PROGRESS
COMPLETED
CANCELLED

Функции:

начать поездку;
завершить поездку;
обновить статус;
передать финальную стоимость в Payment Service;
отправить событие в History Service.
6.7 Payment Service

Payment Service отвечает за оплату.

Функции:

авторизация платежа;
списание денег;
возврат денег;
создание чека;
обработка ошибок платежа.

Для платежей важна идемпотентность, чтобы повторный запрос не списал деньги дважды.

6.8 History Service

History Service хранит историю поездок.

Основные запросы:

GET /users/{user_id}/trips
GET /drivers/{driver_id}/trips
GET /trips/{trip_id}

Для хранения истории подходит Cassandra / ScyllaDB, так как данных много и их удобно партиционировать по user_id, driver_id или trip_id.

7. Хранилища
7.1 PostgreSQL / MySQL

Используется для транзакционных данных:

users
drivers
vehicles
tariffs
payments
driver_documents

Преимущества:

транзакции;
уникальные ограничения;
строгая консистентность;
удобные индексы.
7.2 Redis Cluster

Используется для горячих данных:

online drivers
active trips
active orders
temporary locks
driver status

Redis нужен для операций с низкой задержкой.

7.3 Geo Index

Используется для поиска ближайших водителей.

Возможные реализации:

H3
Geohash
S2
Redis GEO

Пример структуры:

city_id -> h3_cell -> available_driver_ids
driver_id -> current_location
7.4 Cassandra / ScyllaDB

Используется для истории поездок.

Примеры таблиц:

trips_by_user
trips_by_driver
trip_events_by_trip

Примеры ключей:

(user_id, trip_date)
(driver_id, trip_date)
(trip_id)
7.5 Kafka / Pulsar

Используется для асинхронных событий.

Примеры событий:

order_created
driver_offered
driver_accepted
driver_rejected
trip_started
trip_finished
payment_completed
location_updated

Kafka / Pulsar позволяет развязать сервисы между собой.

7.6 ClickHouse

Используется для аналитики.

Примеры аналитических запросов:

количество поездок по городам;
средний чек;
среднее время ожидания;
конверсия заказов;
отказы водителей;
загрузка районов;
surge pricing.
7.7 Object Storage / S3

Используется для дешёвого хранения больших объёмов данных:

сырые координаты;
архив маршрутов;
логи;
события поездок;
резервные копии.
8. Основные API
8.1 Passenger API
POST /orders
GET /orders/{order_id}
POST /orders/{order_id}/cancel
GET /trips/{trip_id}
GET /users/{user_id}/trips

Пример создания заказа:

{
  "passengerId": "user_123",
  "pickupLocation": {
    "latitude": 55.751244,
    "longitude": 37.618423
  },
  "dropoffLocation": {
    "latitude": 55.760000,
    "longitude": 37.640000
  },
  "tariff": "economy",
  "paymentMethod": "card"
}
8.2 Driver API
POST /drivers/{driver_id}/online
POST /drivers/{driver_id}/offline
POST /drivers/{driver_id}/location
POST /orders/{order_id}/accept
POST /orders/{order_id}/reject
POST /trips/{trip_id}/start
POST /trips/{trip_id}/finish

Пример обновления координат:

{
  "driverId": "driver_123",
  "latitude": 55.751244,
  "longitude": 37.618423,
  "speed": 42.5,
  "heading": 180,
  "timestamp": "2026-01-01T12:00:00Z"
}
9. Основные сценарии
9.1 Создание заказа
Passenger App
  -> API Gateway
  -> Order Service
  -> Pricing Service
  -> Matching Service
  -> Notification Service
  -> Driver App

Шаги:

Пассажир создаёт заказ.
Order Service сохраняет заказ.
Pricing Service рассчитывает стоимость.
Matching Service ищет водителя.
Notification Service отправляет заказ водителю.
Водитель принимает или отклоняет заказ.
9.2 Принятие заказа водителем
Driver App
  -> API Gateway
  -> Order Service
  -> Trip Service
  -> Notification Service
  -> Passenger App

Шаги:

Водитель нажимает accept.
Order Service атомарно меняет статус заказа.
Trip Service создаёт поездку.
Notification Service уведомляет пассажира.
Пассажир видит назначенного водителя.
9.3 Выполнение поездки
Driver App
  -> Location Service
  -> Redis / Geo Index
  -> WebSocket Gateway
  -> Passenger App

Шаги:

Водитель едет к пассажиру.
Приложение водителя отправляет координаты.
Location Service обновляет позицию.
Пассажир получает координаты через WebSocket.
После посадки водитель начинает поездку.
После прибытия водитель завершает поездку.
9.4 Завершение поездки
Trip Service
  -> Payment Service
  -> History Service
  -> Rating / Fraud Service
  -> Analytics

Шаги:

Водитель завершает поездку.
Trip Service фиксирует окончание.
Payment Service списывает оплату.
History Service сохраняет поездку.
Rating / Fraud Service проверяет подозрительные события.
Analytics получает данные для отчётов.
10. Оценка памяти
10.1 Состояние водителей

Допустим, одна запись о водителе в горячем хранилище занимает около 500 байт.

5 000 000 × 500 байт = 2.5 GB

С учётом индексов, overhead и репликации:

~10–30 GB RAM
10.2 Активные поездки

Пусть одна активная поездка занимает около 2 KB.

Среднее число активных поездок:

2 млн

Память:

2 000 000 × 2 KB = 4 GB

В пике:

6 000 000 × 2 KB = 12 GB

С overhead и репликацией:

~30–50 GB RAM
10.3 История поездок

100 млн поездок в день.

Если одна запись поездки занимает 2 KB:

100 000 000 × 2 KB = 200 GB/day

В год:

200 GB × 365 ≈ 73 TB/year
10.4 События поездок

Пусть на поездку приходится 10 событий, каждое по 1 KB.

100 000 000 × 10 × 1 KB = 1 TB/day

В год:

365 TB/year
10.5 Координаты поездок

Если сохранять координату каждые 5 секунд:

30 минут = 1800 секунд
1800 / 5 = 360 точек на поездку

В день:

100 000 000 × 360 = 36 млрд точек/day

Если одна точка занимает 100 байт:

36 млрд × 100 байт = 3.6 TB/day

В год:

~1.3 PB/year

Поэтому координаты нельзя писать синхронно в обычную SQL-базу. Их лучше сохранять асинхронно в специализированное хранилище или object storage.

11. Consistency и надёжность
11.1 Где нужна строгая консистентность

Строгая консистентность нужна для:

назначения водителя на заказ;
начала поездки;
завершения поездки;
списания денег;
отмены заказа;
защиты от двойного принятия заказа.
11.2 Где допустима eventual consistency

Eventual consistency допустима для:

аналитики;
истории поездок;
обновления рейтинга;
антифрода;
логов;
архивных координат.
11.3 Идемпотентность

Идемпотентность нужна для операций:

createOrder
acceptOrder
startTrip
finishTrip
capturePayment
cancelOrder

Пример заголовка:

Idempotency-Key: 6b7f2a29-...

Если клиент повторно отправит запрос, backend не должен создать второй заказ или повторно списать деньги.

12. Доступность

Требование:

95–99% в год

Допустимый простой:

95% -> примерно 18.25 дней простоя в год
99% -> примерно 3.65 дней простоя в год

Для достижения доступности используются:

несколько availability zones;
несколько реплик сервисов;
stateless backend;
Redis Cluster с репликами;
Kafka с replication factor 3;
базы данных с репликацией;
circuit breakers;
retries с backoff;
rate limiting;
graceful degradation.
12.1 Graceful degradation

Если часть системы недоступна:

недоступна аналитика — заказы продолжают работать;
недоступна история — поездки можно выполнять, история догонится позже;
недоступен payment provider — поездку можно завершить, оплату обработать позже;
перегружен matching — увеличиваем timeout поиска;
недоступны push-уведомления — используем WebSocket или SMS fallback.
13. Итоговая таблица нагрузки
Метрика	Оценка
Поездок в день	100 млн
Средний RPS заказов	~1.2k/s
Пиковый RPS заказов	~5–10k/s
Активных поездок в среднем	~2 млн
Активных поездок в пике	~5–6 млн
Онлайн-водителей в среднем	~2 млн
Онлайн-водителей в пике	~3–5 млн
Location updates	до 1 млн/s
Память на driver state	~10–30 GB
Память на active trips	~30–50 GB
История поездок	~73 TB/year
События поездок	~365 TB/year
Координаты поездок	до ~1.3 PB/year
14. Ключевая мысль

Главная нагрузка в системе такси — это не создание заказов, а постоянные обновления геолокации водителей и realtime-наблюдение за поездкой.

Создание заказов:

~1.2k/s в среднем
~5–10k/s в пике

Геолокация:

до 1 млн updates/s

Поэтому критическими компонентами являются:

Location Service;
Redis Cluster;
Geo Index;
Kafka / Pulsar;
WebSocket Gateway.
