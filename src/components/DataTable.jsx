import React, { useMemo, useState } from "react";

export default function DataTable({ rows }) {
  const [sortBy, setSortBy] = useState({ key: "timestamp", dir: "desc" });

  const sortedRows = useMemo(() => {
    const copy = [...rows];

    copy.sort((a, b) => {
      const key = sortBy.key;

      const av = a[key];
      const bv = b[key];

      
      if (av === bv) return 0;
      const order = sortBy.dir === "asc" ? 1 : -1;

      return av > bv ? order : -order;
    });

    return copy;
  }, [rows, sortBy]);

  function toggleSort(key) {
    setSortBy((prev) => {
      if (prev.key === key) {
        return { key, dir: prev.dir === "asc" ? "desc" : "asc" };
      }
      return { key, dir: "asc" };
    });
  }

  const Th = ({ label, colKey }) => (
    <th
      onClick={() => toggleSort(colKey)}
      style={{
        cursor: "pointer",
        userSelect: "none",
        textAlign: "left",
        padding: "10px 8px",
        borderBottom: "1px solid #e5e7eb",
        whiteSpace: "nowrap",
      }}
      title="Click to sort"
    >
      {label}{" "}
      {sortBy.key === colKey ? (sortBy.dir === "asc" ? "▲" : "▼") : ""}
    </th>
  );

  function rowStyle(action) {
    if (action === "login_failed") return { background: "#fff1f2" }; 
    if (action === "login_success") return { background: "#f0fdf4" }; 
    return {};
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <Th label="Timestamp" colKey="timestamp" />
            <Th label="User" colKey="user" />
            <Th label="Action" colKey="action" />
            <Th label="IP" colKey="ip" />
          </tr>
        </thead>

        <tbody>
          {sortedRows.map((row) => (
            <tr key={row.id} style={rowStyle(row.action)}>
              <td style={{ padding: "10px 8px", borderBottom: "1px solid #f3f4f6" }}>
                {row.timestamp}
              </td>
              <td style={{ padding: "10px 8px", borderBottom: "1px solid #f3f4f6" }}>
                {row.user}
              </td>
              <td style={{ padding: "10px 8px", borderBottom: "1px solid #f3f4f6" }}>
                {row.action}
              </td>
              <td style={{ padding: "10px 8px", borderBottom: "1px solid #f3f4f6" }}>
                {row.ip}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}