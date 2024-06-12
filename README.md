# AllJobsCMS

Для запуска проекта реализован docker-compose.yml файл

Перед запуском необходимо сделать копию файла .env.default с названием .env и заполнить его
- POSTGRES_NAME - Название бд
- POSTGRES_USER - Имя юзера бд
- POSTGRES_PASSWORD - Пароль юзера бд
- POSTGRES_HOST - Хост бд(по умолчанию db)
- POSTGRES_PORT - Порт бд
- OPENAI_API_KEY - API ключ от OpenAI(Можно использовать g4f библиотеку в качестве альтернативы, но она не стабильна)
- VACANCY_API_URI - URL бота отправки вакансий
- DJANGO_SETTINGS_MODULE - путь до настроек. По умолчанию [all_jobs.settings.production](all_jobs%2Fsettings%2Fproduction.py)

В docker-compose 3 сервиса
- db - База данных
- dev - CMS
- bot_manager - менеджер задач. Необходим для фоновой обработки вакансий и работников