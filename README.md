# 🗺️ Google Maps Web Scraper

A simple and efficient web scraper for **Google Maps** built using **HTML**, **CSS**, **JavaScript** for the frontend and **Python (Flask)** for the backend.  
This tool allows you to search for places/businesses on Google Maps and scrape key details such as names, addresses, ratings, and contact information.

---

## 🚀 Features
- 🌐 **Google Maps Search** – Search for places or businesses directly from the app.
- 📋 **Scraping Details** – Fetch details like:
  - Business Name
  - Address
  - Phone Number
  - Ratings & Reviews
- 📂 **Export Data** – Option to download the scraped data as a CSV file.
- ⚡ **Fast & Lightweight** – Simple UI and optimized scraping logic.
- 🔗 **Flask Backend** – Smooth communication between frontend and backend.

---

## 🛠️ Tech Stack
**Frontend**  
- HTML5  
- CSS3  
- JavaScript  

**Backend**  
- Python 3.x  
- Flask  
- Requests / BeautifulSoup / Selenium (depending on your scraping method)  

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/piyush0s/web-scrapper.git
cd web-scrapper
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open the app in your browser**:  
```
http://127.0.0.1:5000
```

3. **Enter your search query** and click **Scrape**.

4. **View results** in the table or download as CSV.

---

## 📂 Project Structure
```
web-scrapper/
│
├── static/                # CSS, JS, and frontend assets
├── templates/             # HTML templates
├── app.py                 # Flask backend
├── scraper.py             # Scraping logic
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚠️ Disclaimer
This project is for **educational purposes only**. Scraping Google Maps may violate their Terms of Service. Use this tool responsibly and avoid sending excessive requests.

---

## 📜 License
This project is licensed under the **MIT License** – feel free to use and modify it.

---

## 💡 Future Improvements
- 🔍 Add location filters  
- 📊 Visualize results on a map  
- ⏳ Async scraping for faster results  
- 📱 Mobile-friendly UI  

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

### ⭐ If you found this useful, give it a star on GitHub!
