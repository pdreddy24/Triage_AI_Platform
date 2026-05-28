import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { ShieldAlert, Activity, Server, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";
import "./styles.css";

const DEFAULT_API_URL = "http://localhost:8003/triage";

function getApiUrl() {
  return window.__ENV?.TRIAGE_API_URL || import.meta.env.VITE_TRIAGE_API_URL || DEFAULT_API_URL;
}

function getDecisionStyle(decision) {
  const value = String(decision || "").toUpperCase();
  if (value === "APPROVE") return { icon: CheckCircle2, className: "approve" };
  if (value === "REVIEW") return { icon: AlertTriangle, className: "review" };
  if (value === "BLOCK" || value === "DECLINE") return { icon: XCircle, className: "block" };
  return { icon: Activity, className: "neutral" };
}

function pickNumber(obj, names) {
  for (const name of names) {
    if (obj && obj[name] !== undefined && obj[name] !== null) return Number(obj[name]);
  }
  return null;
}

function formatRisk(value) {
  if (value === null || Number.isNaN(value)) return "—";
  return Number(value).toFixed(4);
}

function App() {
  const apiUrl = useMemo(getApiUrl, []);
  const [form, setForm] = useState({ transaction_id: "txn_1001", user_id: "user_156", amount: 250.0, merchant: "Demo Merchant" });
  const [result, setResult] = useState(null);
  const [raw, setRaw] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function runTriage(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    setRaw(null);

    const payload = {
      transaction_id: form.transaction_id,
      user_id: form.user_id,
      amount: Number(form.amount),
      merchant: form.merchant,
    };

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || `Request failed with status ${response.status}`);

      const decision = data.decision || data.action || data.status || "UNKNOWN";
      const combinedRisk = pickNumber(data, ["combined_risk", "final_risk", "risk_score"]);
      const modelRisk = pickNumber(data, ["model_risk", "score", "model_score"]);
      const graphRisk = pickNumber(data, ["graph_risk", "graph_score"]);

      setResult({ decision, combinedRisk, modelRisk, graphRisk, explanation: data.explanation });
      setRaw(data);
    } catch (err) {
      setError(err.message || "Unable to reach triage API.");
    } finally {
      setLoading(false);
    }
  }

  const DecisionIcon = getDecisionStyle(result?.decision).icon;
  const decisionClass = getDecisionStyle(result?.decision).className;

  return (
    <main className="page">
      <section className="hero">
        <div>
          <div className="eyebrow"><ShieldAlert size={18} /> AI Fraud Decisioning</div>
          <h1>AI Fraud Triage Agent</h1>
          <p>Submit a transaction and receive a model + graph risk decision in real time.</p>
        </div>
        <div className="connection-card">
          <Server size={20} />
          <div>
            <span>Connected endpoint</span>
            <strong>{apiUrl}</strong>
          </div>
        </div>
      </section>

      <section className="grid">
        <form className="panel form-panel" onSubmit={runTriage}>
          <h2>Transaction Input</h2>
          <label>Transaction ID<input value={form.transaction_id} onChange={(e) => updateField("transaction_id", e.target.value)} /></label>
          <label>User ID<input value={form.user_id} onChange={(e) => updateField("user_id", e.target.value)} /></label>
          <label>Amount<input type="number" step="0.01" value={form.amount} onChange={(e) => updateField("amount", e.target.value)} /></label>
          <label>Merchant<input value={form.merchant} onChange={(e) => updateField("merchant", e.target.value)} /></label>
          <button disabled={loading} type="submit">{loading ? "Running triage..." : "Run Triage"}</button>
          {error && <div className="error">{error}</div>}
        </form>

        <section className="panel result-panel">
          <h2>Decision Result</h2>
          {!result && !error && <div className="empty-state"><Activity size={34} /><p>Run a transaction to see the decision, risk scores, and explanation.</p></div>}
          {result && <>
            <div className={`decision ${decisionClass}`}><DecisionIcon size={28} /><div><span>Decision</span><strong>{String(result.decision).toUpperCase()}</strong></div></div>
            <div className="metrics">
              <div><span>Combined Risk</span><strong>{formatRisk(result.combinedRisk)}</strong></div>
              <div><span>Model Risk</span><strong>{formatRisk(result.modelRisk)}</strong></div>
              <div><span>Graph Risk</span><strong>{formatRisk(result.graphRisk)}</strong></div>
            </div>
            <div className="explanation"><h3>Explanation</h3><p>{result.explanation || "Model and graph scores were combined to produce the final decision."}</p></div>
            <details><summary>Raw API response</summary><pre>{JSON.stringify(raw, null, 2)}</pre></details>
          </>}
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
