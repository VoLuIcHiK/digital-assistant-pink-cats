## Реализованная функциональность

1. Навигация пользователя по сайту;
2. Помощь в заполнении документов;
3. Прототип голосового помощника;
4. Функция уведомления;

## Особенности проекта

1. Кисуня - кот, специально разработанный нашим дизанером;
2. Использование предобученной нейронной сети и стэмминга;
3. Цифровой помощник может быть быстро адаптирован и интегрирован в сайт.

## Стек решения: javascript, react, php, python, vosk, pydub

## Ссылка на сайт с помощником: http://f0781092.xsph.ru/frontend/project.html#

## Как установить ChatBot API и Telegram Connection

Для этого нужно иметь систему Docker 
1. Клонирование репозитория  
`git clone`
2. Далее запустить контейнеры через систему Docker. Также нужно указать токен к боту телеграм (необязательно).  
`docker-comkpose up -e TELEGRAM_BOT_TOKEN=pass_your_token`

## Навигация по файлам
Сайт с цифровым помощником - https://github.com/VoLuIcHiK/digital-assistant-pink-cats/tree/main/frontend

Телеграм бот - https://github.com/VoLuIcHiK/digital-assistant-pink-cats/tree/main/bot

Api и модель - https://github.com/VoLuIcHiK/digital-assistant-pink-cats/tree/main/api

