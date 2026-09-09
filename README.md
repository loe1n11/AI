# AI Knowledge Assistant

## 🤖 Intelligent Question Answering System

Приложение на Python для взаимодействия с AI (OpenAI GPT) с красивым графическим интерфейсом. Система может отвечать на ваши вопросы и накапливать знания из веб-источников.

### 🎯 Основные возможности

- ✅ **Интерактивное общение с AI** - Задавайте вопросы и получайте ответы
- ✅ **Красивый графический интерфейс** - Элегантный дизайн с эмодзи и таблицами
- ✅ **Векторная база данных** - Сохранение и поиск по вашим знаниям
- ✅ **Добавление веб-источников** - Интеграция контента с сайтов
- ✅ **История вопросов** - Отслеживание ваших запросов
- ✅ **Статистика** - Реальные данные о вашей базе знаний

### 📋 Требования

- Python 3.8+
- OpenAI API ключ
- Интернет соединение

### 🚀 Установка

#### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/loe1n11/AI.git
cd AI
```

#### 2. Создайте виртуальное окружение:
```bash
python -m venv venv

# На Linux/Mac:
source venv/bin/activate

# На Windows:
venv\Scripts\activate
```

#### 3. Установите зависимости:
```bash
pip install -r requirements.txt
```

#### 4. Создайте файл `.env`:
```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте ваш API ключ:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

> 🔑 Получить API ключ: https://platform.openai.com/api-keys

### 💬 Использование

Запустите приложение:
```bash
python main.py
```

Вы увидите красивый интерфейс:
```
╔═══════════════════════════════════════════════════════════╗
║   🤖  INTELLIGENT ASSISTANT with KNOWLEDGE BASE          ║
║   Version 2.0  |  Powered by OpenAI + ChromaDB           ║
╚═══════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════╗
║  📊 Stats: 42 documents in database                       ║
╠═══════════════════════════════════════════════════════════╣
║  [1] ❓ Ask a question                                    ║
║  [2] 🌐 Add website to knowledge base                    ║
║  [3] 📋 Show question history                            ║
║  [4] 🗑️  Clear database                                  ║
║  [5] 📊 Database statistics                              ║
║  [6] 🚀 Exit                                             ║
╚═══════════════════════════════════════════════════════════╝
```

### 📁 Структура проекта

```
AI/
├── README.md              # Документация
├── requirements.txt       # Зависимости
├── config.json            # Конфигурация
├── .env.example           # Пример переменных окружения
├── main.py                # Точка входа
├── core/
│   ├── __init__.py
│   ├── agent.py          # AI агент логика
│   ├── database.py       # Работа с ChromaDB
│   ├── processor.py      # Обработка веб-страниц
│   └── config.py         # Управление конфигурацией
├── ui/
│   ├── __init__.py
│   └── console.py        # Красивый интерфейс консоли
└── data/
    └── chroma_db/        # Хранилище векторной базы
```

### 📝 Лицензия

MIT License - Свободное использование

### 🤝 Способствовать проекту

Приветствуются PR и Issues!

### 📬 Контакты

- GitHub: https://github.com/loe1n11
- Issues: https://github.com/loe1n11/AI/issues

---

**Создано с ❤️ для удобного взаимодействия с AI**
