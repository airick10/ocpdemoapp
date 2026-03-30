from flask import Flask, render_template_string
import mysql.connector
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "mysql"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "demo"),
    "password": os.environ.get("MYSQL_PASSWORD", "demo"),
    "database": os.environ.get("MYSQL_DATABASE", "demodb"),
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>OpenShift Demo App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #1a1a2e;
      color: #eee;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .card {
      background: #16213e;
      border: 1px solid #0f3460;
      border-radius: 12px;
      padding: 40px 50px;
      max-width: 520px;
      width: 100%;
      text-align: center;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .logo { font-size: 2.5rem; margin-bottom: 8px; }
    h1 { font-size: 1.6rem; color: #e94560; margin-bottom: 6px; }
    .subtitle { font-size: 0.9rem; color: #888; margin-bottom: 30px; }
    .status-block {
      background: #0f3460;
      border-radius: 8px;
      padding: 16px 20px;
      margin-top: 20px;
      text-align: left;
    }
    .status-block h2 { font-size: 0.8rem; text-transform: uppercase;
      letter-spacing: 1px; color: #888; margin-bottom: 12px; }
    .status-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 6px 0;
      font-size: 0.9rem;
      border-bottom: 1px solid #1a1a3e;
    }
    .status-row:last-child { border-bottom: none; }
    .badge {
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: bold;
    }
    .ok   { background: #1a472a; color: #5dbb63; }
    .fail { background: #4a1a1a; color: #e94560; }
    .pod-name { font-size: 0.7rem; color: #555; margin-top: 16px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">🚀</div>
    <h1>OpenShift Demo App</h1>
    <p class="subtitle">A minimal deployment demo — web + database</p>

    <div class="status-block">
      <h2>Service Status</h2>
      <div class="status-row">
        <span>Web Pod</span>
        <span class="badge ok">● Running</span>
      </div>
      <div class="status-row">
        <span>MySQL Connection</span>
        <span class="badge {{ db_status_class }}">{{ db_status }}</span>
      </div>
      {% if db_version %}
      <div class="status-row">
        <span>MySQL Version</span>
        <span style="color:#aaa; font-size:0.85rem;">{{ db_version }}</span>
      </div>
      {% endif %}
    </div>

    <p class="pod-name">Pod: {{ pod_name }}</p>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    db_status = "● Connected"
    db_status_class = "ok"
    db_version = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()[0]
        conn.close()
    except Exception as e:
        db_status = "● Unreachable"
        db_status_class = "fail"

    pod_name = os.environ.get("HOSTNAME", "local")

    return render_template_string(
        HTML,
        db_status=db_status,
        db_status_class=db_status_class,
        db_version=db_version,
        pod_name=pod_name,
    )

@app.route("/healthz")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
