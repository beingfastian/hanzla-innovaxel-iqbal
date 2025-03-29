URL Shortener
Installation

Backend Setup

Clone the repository:

git clone https://github.com/beingfastian/hanzla-innovaxel-iqbal.git
cd hanzla-innovaxel-iqbal

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


Install dependencies: pip install -r requirements.txt
Run migrations: 
cd ../urlshortener
python manage.py migrate
Start the Django server: python manage.py runserver

Frontend Setup

Navigate to the frontend folder: cd ../frontend
Install dependencies:npm install
Run the development server: npm run dev
Open http://localhost:3000 to view it in the browser.

Usage
Make sure the backend server is running on http://127.0.0.1:8000/
Start the frontend on http://localhost:3000/
Test API endpoints using Postman or a frontend UI
