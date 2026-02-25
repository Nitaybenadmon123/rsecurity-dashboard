import React, { useMemo } from "react";

function isInternalIp(ip) {
  return (
    ip.startsWith("10.") ||
    ip.startsWith("192.168.") ||
    /^172\.(1[6-9]|2\d|3[0-1])\./.test(ip)
  );
}

function Card({ label, value, sub }) {
  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {sub ? <div className="kpi-sub">{sub}</div> : null}
    </div>
  );
}

export default function KpiCards({ rows }) {
  const stats = useMemo(() => {
    const totalEvents = rows.length;

    const uniqueUsers = new Set(rows.map((r) => r.user)).size;

    const failedLogins = rows.filter((r) => r.action === "login_failed").length;

    const externalIps = new Set(
      rows.filter((r) => r.ip && !isInternalIp(r.ip)).map((r) => r.ip)
    ).size;

    const failedRate = totalEvents
      ? Math.round((failedLogins / totalEvents) * 100)
      : 0;

    return { totalEvents, uniqueUsers, failedLogins, externalIps, failedRate };
  }, [rows]);

  return (
    <div className="kpi-grid">
      <Card label="Total Events" value={stats.totalEvents} />
      <Card label="Unique Users" value={stats.uniqueUsers} />
      <Card
        label="Failed Logins"
        value={stats.failedLogins}
        sub={`Failure rate: ${stats.failedRate}%`}
      />
      <Card label="External IPs" value={stats.externalIps} sub="Non-private ranges" />
    </div>
  );
}