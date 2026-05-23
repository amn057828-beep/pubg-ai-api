import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Users,
  BarChart3,
  DollarSign,
  Shield,
  Crown,
  Gamepad2,
  Image,
  Activity,
  Ban,
  CheckCircle,
  XCircle,
  RefreshCw,
} from "lucide-react";
import "./style.css";

const API = "https://pubg-ai-api.onrender.com";

function Card({ icon, title, value, sub }) {
  return (
    <div className="card">
      <div className="cardTop">
        <div className="icon">{icon}</div>
        <span>{title}</span>
      </div>
      <h2>{value}</h2>
      <p>{sub}</p>
    </div>
  );
}

function Sidebar({ page, setPage }) {
  const items = [
    ["home", "📊 الرئيسية"],
    ["users", "👥 المستخدمون"],
    ["subs", "💎 الاشتراكات"],
    ["analytics", "🧠 التحليلات"],
    ["api", "🛡️ مراقبة API"],
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <Gamepad2 />
        <div>
          <h1>PUBG AI</h1>
          <p>Admin Panel</p>
        </div>
      </div>

      {items.map(([key, label]) => (
        <button
          key={key}
          onClick={() => setPage(key)}
          className={page === key ? "active" : ""}
        >
          {label}
        </button>
      ))}
    </aside>
  );
}

function Login({ setToken }) {
  const [login, setLogin] = useState({
    username: "admin",
    password: "admin123",
  });

  async function doLogin() {
    const r = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(login),
    });

    const d = await r.json();

    if (d.access_token) {
      localStorage.setItem("token", d.access_token);
      setToken(d.access_token);
    } else {
      alert("فشل الدخول");
    }
  }

  return (
    <main className="login" dir="rtl">
      <h1>🎮 PUBG AI Analyzer</h1>
      <p>لوحة الإدارة الاحترافية</p>

      <input
        value={login.username}
        onChange={(e) => setLogin({ ...login, username: e.target.value })}
        placeholder="اسم المستخدم"
      />

      <input
        type="password"
        value={login.password}
        onChange={(e) => setLogin({ ...login, password: e.target.value })}
        placeholder="كلمة المرور"
      />

      <button onClick={doLogin}>دخول</button>
    </main>
  );
}

function Home({ stats, refresh }) {
  return (
    <>
      <div className="pageHeader">
        <div>
          <h1>📊 لوحة التحكم</h1>
          <p>نظرة عامة على أداء منصة PUBG AI Analyzer</p>
        </div>
        <button onClick={refresh}>
          <RefreshCw size={18} /> تحديث
        </button>
      </div>

      <section className="grid">
        <Card
          icon={<Users />}
          title="عدد المستخدمين"
          value={stats?.users ?? "-"}
          sub="إجمالي الحسابات"
        />
        <Card
          icon={<BarChart3 />}
          title="عدد التحليلات"
          value={stats?.analyses ?? "-"}
          sub="تحليلات الإحصائيات والصور"
        />
        <Card
          icon={<Shield />}
          title="متوسط التقييم"
          value={stats?.avg_score ?? "-"}
          sub="متوسط Score العام"
        />
        <Card
          icon={<DollarSign />}
          title="أرباح تقديرية"
          value={`$${stats?.revenue_estimate_usd ?? "-"}`}
          sub="حسب الاشتراكات المدفوعة"
        />
      </section>

      <section className="panel">
        <h2>🚀 حالة النظام</h2>
        <div className="statusGrid">
          <span>✅ API Online</span>
          <span>✅ PostgreSQL Connected</span>
          <span>✅ Telegram Webhook Ready</span>
          <span>✅ AI Engine Active</span>
        </div>
      </section>
    </>
  );
}

function UsersPage({ users, token, loadUsers }) {
  async function banUser(id) {
    await fetch(`${API}/admin/users/${id}/ban`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    loadUsers();
  }

  async function setPlan(id, plan) {
    await fetch(`${API}/admin/users/${id}/plan/${plan}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    loadUsers();
  }

  return (
    <section className="panel">
      <h2>👥 إدارة المستخدمين</h2>

      <div className="table">
        <div className="row head">
          <span>ID</span>
          <span>المستخدم</span>
          <span>الخطة</span>
          <span>الاستهلاك</span>
          <span>الحالة</span>
          <span>إجراء</span>
        </div>

        {users.map((u) => (
          <div className="row" key={u.id}>
            <span>{u.id}</span>
            <span>{u.username || u.telegram_id || "-"}</span>
            <span className="plan">{u.plan}</span>
            <span>{u.daily_used}</span>
            <span>{u.is_banned ? "محظور" : "نشط"}</span>
            <span className="actions">
              <button className="small" onClick={() => setPlan(u.id, "pro")}>
                Pro
              </button>
              <button className="small" onClick={() => setPlan(u.id, "premium")}>
                Premium
              </button>
              <button className="small danger" onClick={() => banUser(u.id)}>
                <Ban size={14} />
              </button>
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

function SubsPage({ requests, token, loadRequests }) {
  async function decide(id, status) {
    await fetch(`${API}/admin/upgrade-requests/${id}/decision`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        status,
        admin_note: status === "approved" ? "تم التفعيل يدوياً" : "تم الرفض",
      }),
    });

    loadRequests();
  }

  return (
    <section className="panel">
      <h2>
        <Crown size={22} /> طلبات الاشتراك اليدوي
      </h2>

      <div className="table">
        <div className="row head">
          <span>ID</span>
          <span>المستخدم</span>
          <span>الخطة</span>
          <span>التواصل</span>
          <span>الحالة</span>
          <span>إجراء</span>
        </div>

        {requests.map((r) => (
          <div className="row" key={r.id}>
            <span>{r.id}</span>
            <span>{r.username || r.telegram_id || "-"}</span>
            <span>{r.requested_plan}</span>
            <span>{r.contact || "-"}</span>
            <span className={r.status}>{r.status}</span>
            <span className="actions">
              <button className="small ok" onClick={() => decide(r.id, "approved")}>
                <CheckCircle size={14} /> قبول
              </button>
              <button className="small danger" onClick={() => decide(r.id, "rejected")}>
                <XCircle size={14} /> رفض
              </button>
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

function AnalyticsPage() {
  return (
    <section className="panel">
      <h2>🧠 AI Analytics</h2>

      <div className="analyticsGrid">
        <div className="mini">
          <Image />
          <h3>OCR Analyzer</h3>
          <p>تحليل صور نتائج PUBG واستخراج الأرقام تلقائيًا.</p>
        </div>

        <div className="mini">
          <Activity />
          <h3>Player Styles</h3>
          <p>تصنيف اللاعبين: هجومي، تكتيكي، Sniper، Support.</p>
        </div>

        <div className="mini">
          <Gamepad2 />
          <h3>Weapon AI</h3>
          <p>اقتراح أفضل سلاح حسب أداء اللاعب.</p>
        </div>
      </div>
    </section>
  );
}

function ApiPage() {
  return (
    <section className="panel">
      <h2>🛡️ مراقبة API</h2>

      <div className="statusGrid">
        <span>✅ JWT Authentication</span>
        <span>✅ API Keys</span>
        <span>✅ Rate Limiting</span>
        <span>✅ Error Handling</span>
        <span>✅ Swagger Documentation</span>
        <span>✅ Render Deployment</span>
      </div>
    </section>
  );
}

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [page, setPage] = useState("home");
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [requests, setRequests] = useState([]);

  async function loadStats() {
    const r = await fetch(`${API}/admin/stats`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (r.ok) setStats(await r.json());
  }

  async function loadUsers() {
    const r = await fetch(`${API}/admin/users`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (r.ok) setUsers(await r.json());
  }

  async function loadRequests() {
    const r = await fetch(`${API}/admin/upgrade-requests`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (r.ok) setRequests(await r.json());
  }

  async function refreshAll() {
    await loadStats();
    await loadUsers();
    await loadRequests();
  }

  useEffect(() => {
    if (token) refreshAll();
  }, [token]);

  if (!token) return <Login setToken={setToken} />;

  return (
    <main className="layout" dir="rtl">
      <Sidebar page={page} setPage={setPage} />

      <section className="content">
        <div className="topbar">
          <span>🔥 PUBG AI Analyzer SaaS</span>
          <button
            onClick={() => {
              localStorage.clear();
              location.reload();
            }}
          >
            خروج
          </button>
        </div>

        {page === "home" && <Home stats={stats} refresh={refreshAll} />}
        {page === "users" && (
          <UsersPage users={users} token={token} loadUsers={loadUsers} />
        )}
        {page === "subs" && (
          <SubsPage
            requests={requests}
            token={token}
            loadRequests={loadRequests}
          />
        )}
        {page === "analytics" && <AnalyticsPage />}
        {page === "api" && <ApiPage />}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
