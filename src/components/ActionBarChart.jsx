import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function ActionBarChart({ rows }) {
  const counts = rows.reduce((acc, row) => {
    const k = row.action || "unknown";
    acc[k] = (acc[k] || 0) + 1;
    return acc;
  }, {});

  // הופכים למערך + ממיינים (אפשר להסיר sort אם אתה רוצה לפי סדר אלפביתי)
  const chartData = Object.entries(counts)
    .map(([action, count]) => ({ action, count }))
    .sort((a, b) => b.count - a.count);

  // גובה דינמי לפי מספר קטגוריות (כדי שיראו הכל בלי צפיפות)
  const rowHeight = 28; // גובה לכל פעולה
  const minHeight = 320;
  const height = Math.max(minHeight, chartData.length * rowHeight + 80);

  return (
    <div style={{ width: "100%", height }}>
      <h3 style={{ margin: "12px 0" }}>Events by Action</h3>

      <ResponsiveContainer>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 10, right: 20, bottom: 10, left: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" allowDecimals={false} />
          <YAxis
            type="category"
            dataKey="action"
            width={170}
            tickFormatter={(v) => String(v).replaceAll("_", " ")}
          />
          <Tooltip />
          <Bar dataKey="count" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}