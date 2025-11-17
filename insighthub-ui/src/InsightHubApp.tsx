import React, { useEffect, useState, useCallback } from "react";

export default function InsightHubApp() {
  // --------------------------------------------------------
  // STATE
  // --------------------------------------------------------
  const [token, setToken] = useState(localStorage.getItem("ih_token") || "");
  const [view, setView] = useState(token ? "dashboard" : "login");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [insights, setInsights] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(false);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  const [extractResult, setExtractResult] = useState(null);

  // 🆕 UPDATE MODAL STATE
  const [editInsight, setEditInsight] = useState(null);

  // --------------------------------------------------------
  // API HELPER
  // --------------------------------------------------------
  const API = useCallback(
    (p: string) =>
      `${(window as any).__INSIGHTHUB_API_BASE__ || "http://127.0.0.1:8000"}${p}`,
    []
  );

  useEffect(() => {
    if (token) fetchInsights();
  }, [token]);

  // --------------------------------------------------------
  // AUTH
  // --------------------------------------------------------
  async function login(e) {
    e.preventDefault();
    const r = await fetch(API("/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!r.ok) return alert("Login failed");

    const d = await r.json();
    localStorage.setItem("ih_token", d.access_token);
    setToken(d.access_token);
    setView("dashboard");
  }

  async function register(e) {
    e.preventDefault();
    const r = await fetch(API("/auth/register"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!r.ok) return alert("Register failed");

    alert("Registered — login now");
    setView("login");
  }

  function logout() {
    localStorage.removeItem("ih_token");
    setToken("");
    setView("login");
  }

  // --------------------------------------------------------
  // CRUD
  // --------------------------------------------------------
  async function fetchInsights() {
    setLoading(true);
    const r = await fetch(API("/insights/"), {
      headers: { Authorization: `Bearer ${token}` },
    });
    const d = await r.json();
    setInsights(d);
    setLoading(false);
  }

  async function createInsight(e) {
    e.preventDefault();
    const r = await fetch(API("/insights/"), {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, content, tags }),
    });

    if (!r.ok) return alert("Create failed");
    setTitle("");
    setContent("");
    setTags("");
    fetchInsights();
  }

  // 🆕 UPDATE INSIGHT
  async function updateInsight() {
    const r = await fetch(API(`/insights/${editInsight.id}`), {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: editInsight.title,
        content: editInsight.content,
        tags: editInsight.tags,
      }),
    });

    if (!r.ok) return alert("Update failed");
    setEditInsight(null);
    fetchInsights();
  }

  // 🆕 DELETE INSIGHT
  async function deleteInsight(id: number) {
    if (!confirm("Delete this insight permanently?")) return;
    await fetch(API(`/insights/${id}`), {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchInsights();
  }

  // --------------------------------------------------------
  // CLUSTERS
  // --------------------------------------------------------
  async function loadClusters() {
    const r = await fetch(API("/insights/clusters"), {
      headers: { Authorization: `Bearer ${token}` },
    });
    const d = await r.json();
    setClusters(d.clusters);
    setView("clusters");
  }

  // --------------------------------------------------------
  // EXTRACTION
  // --------------------------------------------------------
  async function extractInsight(id: number) {
    const r = await fetch(API(`/insights/${id}/extract`), {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!r.ok) return alert("Extract failed");

    const d = await r.json();
    setExtractResult({ id, ...d });
    setView("extract");
  }

  // --------------------------------------------------------
  // HELPERS
  // --------------------------------------------------------
  function Section({ title, items }) {
    if (!items?.length) return null;
    return (
      <div>
        <h4 className="font-semibold">{title}</h4>
        <ul className="ml-4 list-disc text-gray-600">
          {items.map((v, i) => (
            <li key={i}>{v}</li>
          ))}
        </ul>
      </div>
    );
  }

  // --------------------------------------------------------
  // UI COMPONENTS
  // --------------------------------------------------------
  const Header = () => (
    <header className="w-full bg-white/60 backdrop-blur-sm border-b">
      <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between">
        <div className="flex gap-3 items-center">
          <div className="w-10 h-10 bg-black text-white rounded-lg flex items-center justify-center">
            IH
          </div>
          <div>
            <h1 className="font-semibold">InsightHub</h1>
            <p className="text-xs text-gray-500">Smarter notes.</p>
          </div>
        </div>

        {token && (
          <div className="flex gap-2 text-sm">
            <button className="border px-3 py-1 rounded" onClick={fetchInsights}>
              Refresh
            </button>
            <button
              className="bg-black text-white px-3 py-1 rounded"
              onClick={loadClusters}
            >
              Clusters
            </button>
            <button className="border px-3 py-1 rounded" onClick={logout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );

  const Dashboard = () => (
    <main className="max-w-4xl mx-auto px-6 py-8">
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* LEFT */}
        <div className="md:col-span-2">
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <h2 className="font-semibold mb-2">Create Insight</h2>

            <form onSubmit={createInsight} className="space-y-3">
              <input
                className="p-3 border rounded w-full"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />

              <textarea
                className="p-3 border rounded w-full"
                rows={6}
                placeholder="Write content…"
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />

              <input
                className="p-3 border rounded w-full"
                placeholder="tags,comma,separated"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
              />

              <button className="bg-black text-white px-4 py-2 rounded">
                Save & Analyze
              </button>
            </form>
          </div>

          <div className="mt-6">
            <h3 className="font-semibold mb-2">Your Insights</h3>

            {insights.map((ins) => (
              <article
                key={ins.id}
                className="p-4 bg-white rounded-xl shadow-sm border mb-3"
              >
                <h4 className="font-semibold">{ins.title}</h4>
                <p className="text-gray-600 text-sm">{ins.summary}</p>

                <div className="flex gap-3 mt-2 text-xs">
                  <button
                    className="underline text-blue-600"
                    onClick={() => extractInsight(ins.id)}
                  >
                    ➜ Extract
                  </button>

                  <button
                    className="underline text-yellow-600"
                    onClick={() => setEditInsight(ins)}
                  >
                    ✏ Edit
                  </button>

                  <button
                    className="underline text-red-600"
                    onClick={() => deleteInsight(ins.id)}
                  >
                    🗑 Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>

        {/* RIGHT */}
        <aside className="space-y-4">
          <div className="bg-white p-4 rounded-xl shadow-sm">
            <h4 className="font-semibold">Quick Actions</h4>
            <button className="border w-full p-2 rounded" onClick={fetchInsights}>
              Refresh
            </button>
            <button
              className="bg-black text-white w-full p-2 rounded mt-2"
              onClick={loadClusters}
            >
              View Clusters
            </button>
          </div>
        </aside>
      </section>
    </main>
  );

  const ExtractView = () =>
    extractResult && (
      <main className="max-w-3xl mx-auto px-6 py-8">
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-2">Insight Extraction</h2>

          <Section title="Key Points" items={extractResult.key_points} />
          <Section title="Action Items" items={extractResult.action_items} />
          <Section title="Questions" items={extractResult.questions} />

          <p className="mt-3">
            <b>Tone:</b> {extractResult.tone}
          </p>

          <button
            className="mt-6 border px-4 py-2 rounded"
            onClick={() => setView("dashboard")}
          >
            ⬅ Back
          </button>
        </div>
      </main>
    );

  const ClustersView = () => (
    <main className="max-w-3xl mx-auto px-6 py-6">
      <h2 className="text-xl font-semibold mb-4">Clusters</h2>

      {clusters.map((c) => (
        <div key={c.cluster_id} className="p-4 mb-2 border rounded-lg bg-white">
          <p>
            <b>Cluster {c.cluster_id}</b>
          </p>
          <p className="text-sm text-gray-600">{c.representative}</p>
          <p className="text-xs text-gray-400 mt-1">
            IDs: {c.insight_ids.join(", ")}
          </p>
        </div>
      ))}

      <button
        className="mt-6 border px-4 py-2 rounded"
        onClick={() => setView("dashboard")}
      >
        ⬅ Back
      </button>
    </main>
  );

  // 🆕 UPDATE MODAL
  const EditModal = () =>
    editInsight && (
      <div className="fixed inset-0 bg-black/30 flex justify-center items-center">
        <div className="bg-white p-6 rounded-xl w-96 space-y-3 shadow-xl">
          <h3 className="font-semibold text-lg">Edit Insight</h3>

          <input
            className="border w-full p-2 rounded"
            value={editInsight.title}
            onChange={(e) =>
              setEditInsight({ ...editInsight, title: e.target.value })
            }
          />

          <textarea
            className="border w-full p-2 rounded"
            rows={5}
            value={editInsight.content}
            onChange={(e) =>
              setEditInsight({ ...editInsight, content: e.target.value })
            }
          />

          <input
            className="border w-full p-2 rounded"
            value={editInsight.tags}
            onChange={(e) =>
              setEditInsight({ ...editInsight, tags: e.target.value })
            }
          />

          <div className="flex gap-3">
            <button
              className="bg-black text-white px-4 py-2 rounded"
              onClick={updateInsight}
            >
              Save
            </button>
            <button
              className="border px-4 py-2 rounded"
              onClick={() => setEditInsight(null)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );

  // --------------------------------------------------------
  // FINAL RENDER
  // --------------------------------------------------------
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      {view === "login" && <Login />}
      {view === "register" && <Register />}
      {view === "dashboard" && <Dashboard />}
      {view === "clusters" && <ClustersView />}
      {view === "extract" && <ExtractView />}

      {/* 🆕 EDIT MODAL */}
      {EditModal()}
    </div>
  );
}
