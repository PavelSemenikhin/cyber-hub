# 🎮 CyberHub — Платформа для кіберспільноти

**CyberHub** — це веб-платформа, що поєднує **блог**, **турнірний модуль** та **особисті профілі геймерів**. Створи обліковий запис, публікуй геймерські пости, подавай заявки на турніри.

---

## 🚀 Основні можливості

- 👤 **Користувацький профіль**  
  Створення акаунту з нікнеймом, Discord та Telegram. Перегляд і редагування профілю, власні пости та участь у турнірах.

- 📝 **Блог-секція**  
  - Створення/редагування/видалення постів  
  - Коментування  
  - Пошук постів  
  - Фільтрація за грою  
  - Пагінація  
  - Відображення кількості коментарів  

- 🏆 **Турніри**  
  - Каталог турнірів  
  - Фільтрація за статусом: `registration`, `in progress`, `finished`  
  - Детальна сторінка турніру  
  - Подача заявки (1 активна заявка на користувача)  
  - Відображення статусу участі  

---

## ⚙️ Технології

- Backend: [Django 5.2]
- Frontend: [Bootstrap 5]
- База даних: SQLite
- Тести: `pytest`, `pytest-django`, `coverage`
- Code Style: `flake8`

---

## 🗂 Структура проєкту

<pre>
cyber-hub/
├── 📂accounts/        # Реєстрація, профілі, автентифікація
├── 📂blog/            # Пости та коментарі
├── 📂tournaments/     # Турніри та заявки
│   └── 📂fixtures/    # Тестові дані (JSON)
├── 📂templates/       # HTML-шаблони
├── 📂static/          # Статика (Bootstrap, іконки)
├── 📂tests/           # Усі тести (форми, моделі, вʼю)
├── 📂config/          # Налаштування Django
├── 📄manage.py        # Точка входу
└── 📄requirements.txt # Залежності
</pre>

---

## 💻 Як запустити локально

```bash
git clone https://github.com/<your-username>/cyber-hub.git
cd cyber-hub
python -m venv .venv
source .venv/bin/activate  # або .venv\Scripts\activate на Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver




📦 Тестові дані

Щоб підвантажити демо-дані для турнірів, виконай:

python manage.py loaddata fixtures/tournaments_fixture_final.json
