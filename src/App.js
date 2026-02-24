import React, { useState } from "react";
import data from "./data/sampleData.json";
import DataTable from "./components/DataTable";
import ActionBarChart from "./components/ActionBarChart";
import LoginPieChart from "./components/LoginPieChart";
import KpiCards from "./components/KpiCards";
import "./App.css";

function App() {
  const [search, setSearch] = useState("");

  const filteredData = data.filter((row) =>
    row.user.toLowerCase().includes(search.toLowerCase()) ||
    row.ip.includes(search)
  );

  return (
  <div className="page">
    <div className="header">
      <h1>Activity Dashboard</h1>
      <p>Search, charts, and sortable table</p>
    </div>

    <div className="card">
      <input
        className="search"
        type="text"
        placeholder="Search by user or IP..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
    </div>
    {filteredData.length === 0 ? (
      <div className="no-results" style={{ marginTop: 16 }}>
        <h3 style={{ margin: "0 0 6px", color: "var(--text)" }}>No results</h3>
        <div>Try a different search (user or IP).</div>
      </div>
    ) : (
      <>
        <KpiCards rows={filteredData} />
        <div className="card">
          <h3 className="section-title">Events</h3>
          <DataTable rows={filteredData} />
        </div>
      </>
    )}

    <div className="charts-grid">
      <div className="card">
        <ActionBarChart rows={filteredData} />
      </div>
      <div className="card">
        <LoginPieChart rows={filteredData} />
      </div>
    </div>

  </div>
);
}

export default App;


