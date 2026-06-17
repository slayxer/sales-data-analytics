# 📊 SalesIQ — Sales Analytics Dashboard

A full-stack sales analytics web application built with **Flask**, **Pandas**, and **Chart.js**. Tracks revenue, orders, products, and city-wise performance with real-time data entry — no database required, powered entirely by CSV.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-FF6384)

---

## 🚀 Features

- **🏠 Dashboard** — Live KPI cards (Total Revenue, Orders, Products, Cities), revenue-by-product bar chart, and revenue-by-city doughnut chart
- **📦 Products** — Filterable product-wise summary with monthly revenue trend lines and detailed breakdown table
- **🏙️ Cities** — Filterable city-wise summary with revenue comparison and stacked product-mix charts
- **📈 Reports** — Month-by-month performance breakdown, best-performing product/city highlights, and average order value
- **➕ Data Entry** — Add new sales records through a form with autocomplete; updates the CSV and reflects instantly across all dashboards
- **🎨 Modern UI** — Dark sidebar navigation, gradient KPI cards, responsive grid layout, and interactive Chart.js visualizations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Data Processing | Pandas |
| Data Storage | CSV (file-based, no database setup needed) |
| Frontend | HTML, CSS (custom), Jinja2 templating |
| Charts | Chart.js |

---

## 📁 Project Structure

```
sales-data-analytics/
├── app/
│   ├── app.py                 # Flask routes and application logic
│   ├── static/
│   │   └── style.css          # Dashboard styling
│   └── templates/
│       ├── sidebar.html       # Shared navigation sidebar
│       ├── index.html         # Dashboard page
│       ├── products.html      # Products analysis page
│       ├── cities.html        # Cities analysis page
│       ├── reports.html       # Monthly reports page
│       └── entry.html         # Data entry form
├── data/
│   └── sales.csv              # Sales records (source of truth)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/slayxer/sales-data-analytics.git
cd sales-data-analytics
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python -m app.app
```

**4. Open in your browser**
```
http://127.0.0.1:5000
```

That's it — no database setup, no environment variables. The app reads and writes directly to `data/sales.csv`.

---

## 📊 Data Format

The app expects `data/sales.csv` with the following columns:

| Column | Type | Description |
|---|---|---|
| `order_id` | int | Unique order identifier |
| `product` | string | Product name |
| `quantity` | int | Units sold |
| `price` | float | Price per unit (₹) |
| `city` | string | City of sale |
| `date` | date (YYYY-MM-DD) | Order date |

Revenue is calculated automatically as `quantity × price`.

---

## 🔮 Future Improvements

- Export reports as PDF/Excel
- Date-range filtering across all pages
- Authentication for multi-user data entry
- Migrate to a proper database (PostgreSQL/MySQL) for scalability

---

## 📄 License

This project is licensed under the MIT License.