import React, { useEffect, useState } from "react";

function MachinesTable() {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    os: "",
    disk_encryption: "",
    antivirus: "",
  });

  useEffect(() => {
    fetchMachines();
  }, [filters]);

  const fetchMachines = async () => {
    setLoading(true);
    // Build query params from filters
    const params = new URLSearchParams();
    if (filters.os) params.append("os", filters.os);
    if (filters.disk_encryption) params.append("disk_encryption", filters.disk_encryption);
    if (filters.antivirus) params.append("antivirus", filters.antivirus);

    const response = await fetch(`http://127.0.0.1:8000/machines?${params.toString()}`);
    const data = await response.json();
    setMachines(data);
    setLoading(false);
  };

  // Helper to flag issues
  const hasIssues = (machine) => {
    return (
      !machine.disk_encryption ||
      !machine.os_updates ||
      !machine.antivirus ||
      !machine.sleep_settings
    );
  };

  return (
    <div>
      <h2>System Health Dashboard</h2>

      {/* Filters */}
      <div style={{ marginBottom: "1rem" }}>
        <label>
          OS:
          <input
            type="text"
            value={filters.os}
            onChange={(e) => setFilters({ ...filters, os: e.target.value })}
            placeholder="e.g. Windows 10"
          />
        </label>

        <label style={{ marginLeft: "1rem" }}>
          Disk Encryption:
          <select
            value={filters.disk_encryption}
            onChange={(e) => setFilters({ ...filters, disk_encryption: e.target.value })}
          >
            <option value="">Any</option>
            <option value="true">Encrypted</option>
            <option value="false">Not Encrypted</option>
          </select>
        </label>

        <label style={{ marginLeft: "1rem" }}>
          Antivirus:
          <select
            value={filters.antivirus}
            onChange={(e) => setFilters({ ...filters, antivirus: e.target.value })}
          >
            <option value="">Any</option>
            <option value="true">Running</option>
            <option value="false">Not Running</option>
          </select>
        </label>
      </div>

      {/* Table */}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table border="1" cellPadding="8" cellSpacing="0">
          <thead>
            <tr>
              <th>Machine ID</th>
              <th>OS</th>
              <th>Disk Encryption</th>
              <th>OS Updates</th>
              <th>Antivirus</th>
              <th>Sleep Settings</th>
              <th>Last Check-in</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((m) => (
              <tr key={m.machine_id} style={{ backgroundColor: hasIssues(m) ? "#ffdddd" : "white" }}>
                <td>{m.machine_id}</td>
                <td>{m.os}</td>
                <td>{m.disk_encryption ? "Yes" : "No"}</td>
                <td>{m.os_updates ? "Up-to-date" : "Outdated"}</td>
                <td>{m.antivirus ? "Running" : "Not Running"}</td>
                <td>{m.sleep_settings ? "OK" : "Not OK"}</td>
                <td>{new Date(m.timestamp).toLocaleString()}</td>
                <td>{hasIssues(m) ? "⚠️ Issues" : "✅ OK"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default MachinesTable;