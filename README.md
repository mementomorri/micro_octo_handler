# micro_octo_handler
Микросевисное приложение обработки сообщений на основе архитектуры REST.  
## Дословная формулировка т/з  
> Реализовать приложение, принимающее запросы на обработку через REST.
>Сообщения обрабатываются двумя провайдерами:  
> - бесплатным
> - и платным,
>   
> путем общения через REST.
>
>По бесплатному провайдеру есть ограничение: он может принять какое-то количество запросов, затем блокирует обращения на определённый промежуток времени.  
>Возможно получить отказ в обслуживании формированием рабочего запроса на бесплатный сервис, однако правильнее обрабатывать количество отправленных запросов в сервис и сравнивать с доступным количеством.  
>При блокировке запросы следует отправлять в платный сервис. При доступности бесплатного сервиса следует переключиться на бесплатный, минимизируя использование платного провайдера.
>При разработке иметь в виду, что приложение может работать на нескольких изолированных подах без использования общей памяти.  
>Необходимо наличие тестов.

## Интуиция
1. Поскольку подразумивается, что приложение может быть разделено на несколько подов, то имеет смысл реализовать микросервисную архитектуру. Приложение будет разделено на два сервиса: 
    - бесплатный провайдер;  
    - платный провайдер;
2. По-умолчанию буду направлять клиента на бесплатный провайдер, если пороговое значение запросов превышено, то клиент будет перенаправлен на платный провайдер. Для имитации работы платного провайдера условно ограничу его использование по ключевому аттрибуту.  
3. Поскольку в т/з не уточняется как реализовать обмен данными между сервисами и в случае если это делать через разделяему БД, то какую конкретно БД использовать, необходимо ли наличие кэширования.  
В таком случае, буду использовать SQLite, ведь нет необходимости использовать PostgreSQL или Redis.
