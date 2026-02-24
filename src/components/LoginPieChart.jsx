import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function LoginPieChart({ rows }) {

  const loginCounts = rows.reduce(
    (acc, row) => {
      if (row.action === "login_success") acc.success += 1;
      if (row.action === "login_failed") acc.failed += 1;
      return acc;
    },
    { success: 0, failed: 0 }
  );

  const chartData = [
    { name: "Success", value: loginCounts.success },
    { name: "Failed", value: loginCounts.failed }
  ];

  const COLORS = ["#4CAF50", "#F44336"]; 

  return (
    <div style={{ width: "100%", height: 300 }}>
      <h3 style={{ margin: "12px 0" }}>Login Success vs Failed</h3>

      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            outerRadius={100}
            label
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>

          <Tooltip />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}