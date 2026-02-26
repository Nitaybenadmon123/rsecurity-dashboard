# Security Activity Dashboard – Frontend

This project was developed as part of a Fullstack technical assignment (Part 1 – Frontend).

It is a responsive security activity dashboard built with React that loads and visualizes event data from a JSON file.

---

## 🚀 Features

- Load and display data from a JSON file
- Sortable data table (by clicking column headers)
- Search by user or IP address
- Bar chart – Events by action
- Pie chart – Login success vs failed
- KPI summary cards
- Responsive layout (desktop & mobile)
- Clean UI design
- Sticky table header
- "No results" state handling

The dataset used in this dashboard was derived from the provided CSV log file and converted to JSON format using a small Python script.

---

## 📂 Project Structure
```
frontend/
│
├── src/
│ ├── components/
│ ├── data/
│ │ └── sampleData.json
│ ├── App.js
│ └── ...
├── package.json
└── README.md
```

---

## ▶️ How to Run

1. Navigate to the project directory:
cd frontend


2. Install dependencies:
npm install 


3. Start the development server:
npm start 


4. Open in browser:
http://localhost:3000


---

## 🧠 Assumptions

- The provided CSV file represents raw event logs.
- The CSV file was converted to JSON format for frontend visualization.
- The dashboard is designed for local development and demonstration purposes.
- No backend integration was required for this part of the assignment.

---

## ✨ Extra Notes

- The UI automatically updates when filtering or sorting.
- Charts dynamically recalculate based on filtered data.
- The table supports dynamic sorting (ascending/descending).
- Layout adjusts for smaller screen sizes.

---

## 📌 Possible Improvements

- Pagination for large datasets
- Dark mode toggle
- Backend integration
- Export filtered data to CSV
