import React, {useEffect, useState} from 'react'
import {createRoot} from 'react-dom/client'
import {Users, BarChart3, DollarSign, Shield, Crown} from 'lucide-react'
import './style.css'

const API = 'http://localhost:8000'

function Card({icon, title, value}) {
  return <div className="card"><div className="icon">{icon}</div><p>{title}</p><h2>{value}</h2></div>
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [login, setLogin] = useState({username:'admin', password:'admin123'})
  const [stats, setStats] = useState(null)
  const [requests, setRequests] = useState([])

  async function doLogin() {
    const r = await fetch(`${API}/auth/login`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(login)
    })
    const d = await r.json()
    if(d.access_token) {
      localStorage.setItem('token', d.access_token)
      setToken(d.access_token)
    } else alert('فشل الدخول')
  }

  async function loadStats() {
    const r = await fetch(`${API}/admin/stats`, {headers:{Authorization:`Bearer ${token}`}})
    if(r.ok) setStats(await r.json())
  }

  async function loadRequests() {
    const r = await fetch(`${API}/admin/upgrade-requests`, {headers:{Authorization:`Bearer ${token}`}})
    if(r.ok) setRequests(await r.json())
  }

  async function decide(id, status) {
    const r = await fetch(`${API}/admin/upgrade-requests/${id}/decision`, {
      method:'POST',
      headers:{'Content-Type':'application/json', Authorization:`Bearer ${token}`},
      body: JSON.stringify({status, admin_note: status === 'approved' ? 'تم التفعيل يدوياً' : 'تم الرفض'})
    })
    if(r.ok) loadRequests()
  }

  useEffect(()=>{ if(token) { loadStats(); loadRequests(); } }, [token])

  if(!token) return <main className="login" dir="rtl">
    <h1>PUBG AI Analyzer</h1>
    <p>لوحة الإدارة</p>
    <input value={login.username} onChange={e=>setLogin({...login, username:e.target.value})} />
    <input type="password" value={login.password} onChange={e=>setLogin({...login, password:e.target.value})} />
    <button onClick={doLogin}>دخول</button>
  </main>

  return <main className="app" dir="rtl">
    <header>
      <div><h1>🎮 PUBG AI Analyzer</h1><p>لوحة تحكم SaaS + اشتراكات يدوية</p></div>
      <button onClick={()=>{localStorage.clear(); location.reload()}}>خروج</button>
    </header>

    <section className="grid">
      <Card icon={<Users/>} title="عدد المستخدمين" value={stats?.users ?? '-'} />
      <Card icon={<BarChart3/>} title="عدد التحليلات" value={stats?.analyses ?? '-'} />
      <Card icon={<Shield/>} title="متوسط التقييم" value={stats?.avg_score ?? '-'} />
      <Card icon={<DollarSign/>} title="أرباح تقديرية $" value={stats?.revenue_estimate_usd ?? '-'} />
    </section>

    <section className="panel">
      <h2><Crown size={22}/> طلبات الحجز والترقية اليدوية</h2>
      <div className="table">
        <div className="row head"><span>ID</span><span>المستخدم</span><span>الخطة</span><span>التواصل</span><span>الحالة</span><span>إجراء</span></div>
        {requests.map(r => <div className="row" key={r.id}>
          <span>{r.id}</span>
          <span>{r.username || r.telegram_id || '-'}</span>
          <span>{r.requested_plan}</span>
          <span>{r.contact || '-'}</span>
          <span className={r.status}>{r.status}</span>
          <span>
            <button className="small" onClick={()=>decide(r.id, 'approved')}>قبول</button>
            <button className="small danger" onClick={()=>decide(r.id, 'rejected')}>رفض</button>
          </span>
        </div>)}
      </div>
    </section>

    <section className="panel"><h2>ميزات Viral</h2><p>بطاقة مشاركة، نصائح يومية، Ranking، Badges، ومقارنة لاعبين.</p></section>
  </main>
}

createRoot(document.getElementById('root')).render(<App/>)
