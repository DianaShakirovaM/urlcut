# URLCut - Сервис сокращения URL и загрузки файлов

Сервис для сокращения длинных URL-адресов и удобной загрузки файлов на Яндекс.Диск с генерацией коротких ссылок.
- [![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
- [![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)

## Возможности

- **Сокращение URL**: Преобразование длинных ссылок в короткие и удобные
- **Кастомные короткие ссылки**: Возможность задать собственное имя для короткой ссылки
- **Загрузка файлов**: Множественная загрузка файлов прямо на Яндекс.Диск
- **REST API**: Полноценное JSON API для интеграции с другими сервисами
- **Валидация данных**: Проверка корректности вводимых URL и идентификаторов
- **Асинхронная загрузка**: Быстрая загрузка файлов с использованием aiohttp

## Технологии

- **Backend**: Python 3.7+, Flask
- **База данных**: SQLite (с возможностью миграции на другие СУБД)
- **Формы**: Flask-WTF, WTForms
- **Асинхронные запросы**: aiohttp, asyncio
- **Хранение файлов**: Яндекс.Диск API
- **Валидация**: WTForms validators, кастомные валидаторы

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/DianaShakirovaM/urlcut.git
cd yacut
```
### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Инициализация базы данных
```bash
flask db init
flask db migrate
flask db upgrade
```
### 5. Запуск приложения
```bash
flask run
```
## Использование
### Веб-интерфейс
- Сокращение URL: Перейдите на главную страницу, введите длинный URL и короткий идентификатор
- Загрузка файлов: Используйте форму загрузки файлов для отправки на Яндекс.Диск
### REST API
Создание короткой ссылки
```html
POST /api/id/
```
```json
{"url": "https://example.com/very/long/url", "custom_id": "my-link"}
```
Ответ
```json
{
  "short_link": "http://localhost:5000/my-link",
  "url": "https://example.com/very/long/url"
}
```
