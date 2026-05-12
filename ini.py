from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Painel Inicial")


def render_ini_page() -> str:
    return """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Painel</title>
  <style>
    :root {
      --bg-1: #071429;
      --bg-2: #0b1f3a;
      --surface: #102845;
      --surface-soft: #0d223c;
      --text: #e8f1ff;
      --muted: #a8bfdc;
      --accent: #2f6df6;
      --border: #1b3c64;
      --ok: #50d890;
      --warn: #f3c86a;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", "Helvetica Neue", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 15% 20%, #15365f 0%, transparent 38%),
        radial-gradient(circle at 85% 80%, #113059 0%, transparent 40%),
        linear-gradient(135deg, var(--bg-1), var(--bg-2));
    }
    .layout {
      display: grid;
      grid-template-columns: 260px 1fr;
      min-height: 100vh;
    }
    .sidebar {
      border-right: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
      padding: 24px 16px;
      backdrop-filter: blur(6px);
    }
    .brand {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.4px;
      margin: 0 0 18px;
    }
    .menu-title {
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      margin: 18px 8px 8px;
      letter-spacing: 1px;
    }
    .menu {
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 8px;
    }
    .menu a {
      display: block;
      color: var(--text);
      text-decoration: none;
      padding: 10px 12px;
      border: 1px solid transparent;
      border-radius: 10px;
      background: rgba(255,255,255,0.02);
      transition: background .2s ease, border-color .2s ease;
    }
    .menu a:hover {
      background: rgba(47,109,246,0.12);
      border-color: rgba(47,109,246,0.45);
    }
    .content {
      display: grid;
      grid-template-rows: 72px 1fr;
    }
    .topbar {
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      background: rgba(0,0,0,0.14);
      backdrop-filter: blur(4px);
    }
    .topbar h1 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
    }
    .topbar .badge {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 12px;
      color: var(--muted);
    }
    .topbar-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .dashboard-select {
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.08);
      color: var(--text);
      border-radius: 10px;
      padding: 8px 12px;
      font-size: 13px;
      outline: none;
      color-scheme: dark;
    }
    .dashboard-select option {
      background: #0d223c;
      color: var(--text);
    }
    .logout-btn {
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: rgba(255, 255, 255, 0.08);
      color: var(--text);
      border-radius: 10px;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 13px;
      transition: background .2s ease, border-color .2s ease;
    }
    .logout-btn:hover {
      background: rgba(255, 255, 255, 0.14);
      border-color: rgba(255, 255, 255, 0.4);
    }
    .dashboard {
      padding: 24px;
      display: grid;
      gap: 18px;
      grid-template-columns: repeat(12, minmax(0, 1fr));
    }
    .empty-state {
      display: none;
      min-height: 280px;
      margin: 24px;
      border: 1px dashed var(--border);
      border-radius: 14px;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.02);
      font-size: 15px;
    }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 12px 26px rgba(0,0,0,.25);
    }
    .kpi { grid-column: span 3; }
    .wide { grid-column: span 8; min-height: 220px; }
    .side { grid-column: span 4; min-height: 220px; }
    .title {
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 13px;
      letter-spacing: .2px;
    }
    .value {
      margin: 0;
      font-size: 30px;
      font-weight: 700;
    }
    .trend-up { color: var(--ok); font-size: 13px; }
    .trend-warn { color: var(--warn); font-size: 13px; }
    .bars {
      margin-top: 14px;
      display: grid;
      gap: 10px;
    }
    .bar {
      height: 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      overflow: hidden;
    }
    .bar span {
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #2f6df6, #73a1ff);
    }
    .list {
      margin: 0;
      padding-left: 18px;
      color: #d5e4ff;
      display: grid;
      gap: 8px;
      font-size: 14px;
    }
    @media (max-width: 980px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { border-right: 0; border-bottom: 1px solid var(--border); }
      .kpi { grid-column: span 6; }
      .wide, .side { grid-column: span 12; }
    }
    @media (max-width: 640px) {
      .dashboard { grid-template-columns: repeat(6, minmax(0, 1fr)); }
      .kpi { grid-column: span 6; }
      .topbar { padding: 0 14px; }
      .dashboard { padding: 14px; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h2 class="brand">Meu Painel</h2>
      <div class="menu-title">Menu Principal</div>
      <ul class="menu">
        <li><a href="#">Dashboard</a></li>
        <li><a href="#">Automações</a></li>
        <li><a href="#">Relatorios</a></li>
      </ul>
      <div class="menu-title">Administracao</div>
      <ul class="menu">
        <li><a href="#">Usuarios</a></li>
        <li><a href="#">Configuracoes</a></li>
      </ul>
    </aside>
    <section class="content">
      <header class="topbar">
        <h1>SSA - DashBoard</h1>
        <div class="topbar-actions">
          <p>Automações:</p>
          <select id="dashboardType" class="dashboard-select">
            <option value="contratos">Alteracao Contratos</option>
            <option value="vazio1">Vazio</option>
            <option value="vazio2">Vazio</option>
          </select>
          <span class="badge">Ambiente Demonstrativo</span>
          <form method="post" action="/logout">
            <button class="logout-btn" type="submit">Logout</button>
          </form>
        </div>
      </header>
      <main id="contractsDashboard" class="dashboard">
        <article class="card kpi">
          <p class="title">Contratos Pendentes</p>
          <p class="value">R$ 1000</p>
          <span class="trend-up">+8,4% vs mes anterior</span>
        </article>
        <article class="card kpi">
          <p class="title">Contratos Em Andamento</p>
          <p class="value">342</p>
          <span class="trend-up">+3,1% na semana</span>
        </article>
        <article class="card kpi">
          <p class="title"> Contratos Concluídos</p>
          <p class="value">27</p>
          <span class="trend-warn">5 com alta prioridade</span>
        </article>
      
        <article class="card wide">
          <p class="title">Desempenho por canal (ficticio)</p>
          <div class="bars">
            <div class="bar"><span style="width:82%"></span></div>
            <div class="bar"><span style="width:67%"></span></div>
            <div class="bar"><span style="width:49%"></span></div>
            <div class="bar"><span style="width:90%"></span></div>
          </div>
        </article>
        <article class="card side">
          <p class="title">Logs Robo</p>
          <ul class="list">
            <li>Contrato #2043 aprovado com sucesso</li>
            <li>Contrato #2044 aprovado com sucesso</li>
            <li>Contrato #2045 aprovado com sucesso</li>
            <li>Contrato #2046 aprovado com sucesso</li>
          </ul>
        </article>
      </main>
      <section id="emptyDashboard" class="empty-state">
        Nenhum dashboard configurado para esta opcao.
      </section>
    </section>
  </div>
  <script>
    const dashboardType = document.getElementById("dashboardType");
    const contractsDashboard = document.getElementById("contractsDashboard");
    const emptyDashboard = document.getElementById("emptyDashboard");

    function updateDashboardView() {
      if (dashboardType.value === "contratos") {
        contractsDashboard.style.display = "grid";
        emptyDashboard.style.display = "none";
      } else {
        contractsDashboard.style.display = "none";
        emptyDashboard.style.display = "flex";
      }
    }

    dashboardType.addEventListener("change", updateDashboardView);
    updateDashboardView();
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def ini_page() -> str:
    return render_ini_page()
