# 🎮 CyberHub — Platform for the Gaming Community

**CyberHub** is a web platform that combines a **blog**, a **tournament module**, and **personal gamer profiles**.  
Create an account, publish gaming posts, and apply for tournaments.

---

## 🚀 Main Features

- 👤 **User Profile**  
  Create an account with a nickname, Discord, and Telegram. View and edit your profile, see your posts, and participate in tournaments.

- 📝 **Blog Section**  
  - Create / edit / delete posts  
  - Commenting  
  - Search posts  
  - Filter by game  
  - Pagination  
  - Display number of comments  

- 🏆 **Tournaments**  
  - Tournament catalog  
  - Filter by status: `registration`, `in progress`, `finished`  
  - Tournament detail page  
  - Submit an application (only 1 active application per user)  
  - Show participation status  

---

## ⚙️ Technologies

- Backend: [Django 5.2]  
- Frontend: [Bootstrap 5]  
- Database: SQLite  
- Testing: `pytest`, `pytest-django`, `coverage`  
- Code Style: `flake8`  

---

## 🗂 Project Structure

<pre>
cyber-hub/
├── 📂accounts/        # Registration, profiles, authentication
├── 📂blog/            # Posts and comments
├── 📂tournaments/     # Tournaments and applications
│   └── 📂fixtures/    # Test data (JSON)
├── 📂templates/       # HTML templates
├── 📂static/          # Static files (Bootstrap, icons)
├── 📂tests/           # All tests (forms, models, views)
├── 📂config/          # Django settings
├── 📄manage.py        # Entry point
└── 📄requirements.txt # Dependencies
</pre>

---

## 💻 How to Run Locally

```bash
git clone https://github.com/<your-username>/cyber-hub.git
cd cyber-hub
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
