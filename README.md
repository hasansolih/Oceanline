

🛠 Prerequisites

Make sure you have:

Python 3.10+

MySQL Server

pip package manager

2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

Install dependencies

pip install -r requirements.txt


▶ Running the App
python app.py

Visit:
http://127.0.0.1:5000

CREATE USER 'oceanline_user'@'localhost' IDENTIFIED BY 'Admin12345!';
CREATE DATABASE oceanline_db;
GRANT ALL PRIVILEGES ON oceanline_db.* TO 'oceanline_user'@'localhost';
FLUSH PRIVILEGES;