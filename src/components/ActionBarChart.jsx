import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function ActionBarChart({ rows }) {
  
  const counts = rows.reduce((acc, row) => {
    acc[row.action] = (acc[row.action] || 0) + 1;
    return acc;
  }, {});


  const chartData = Object.entries(counts).map(([action, count]) => ({
    action,
    count,
  }));

  return (
    <div style={{ width: "100%", height: 300 }}>
      <h3 style={{ margin: "12px 0" }}>Events by Action</h3>

      <ResponsiveContainer>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="action"
            interval={0}
            height={60}
            tickFormatter={(v) => v.replaceAll("_", " ")}
          />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#1209bd" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}