<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kick Follow Manager</title>

  <style>
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background: #0d1117;
      color: #e6edf3;
    }

    .container {
      max-width: 1000px;
      margin: auto;
      padding: 40px 20px;
    }

    h1 {
      font-size: 42px;
      margin-bottom: 10px;
    }

    h2 {
      margin-top: 50px;
      border-bottom: 1px solid #30363d;
      padding-bottom: 10px;
    }

    p {
      color: #c9d1d9;
    }

    a {
      color: #58a6ff;
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    .hero {
      text-align: center;
      padding: 60px 20px;
    }

    .hero p {
      font-size: 18px;
      max-width: 700px;
      margin: 10px auto 30px;
    }

    .btn {
      display: inline-block;
      padding: 12px 20px;
      border-radius: 8px;
      background: #238636;
      color: white;
      font-weight: 600;
      margin: 5px;
    }

    .btn.secondary {
      background: #30363d;
    }

    .features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }

    .card {
      background: #161b22;
      padding: 20px;
      border-radius: 10px;
      border: 1px solid #30363d;
    }

    code {
      background: #161b22;
      padding: 3px 6px;
      border-radius: 4px;
    }

    pre {
      background: #161b22;
      padding: 15px;
      border-radius: 8px;
      overflow-x: auto;
      border: 1px solid #30363d;
    }

    ul {
      padding-left: 20px;
    }

    footer {
      margin-top: 60px;
      text-align: center;
      font-size: 14px;
      color: #8b949e;
    }
  </style>
</head>

<body>

<div class="container">

  <section class="hero">
    <h1>Kick Follow Manager</h1>
    <p>
      Easily export and re-follow all your Kick.com channels on a new account.
      Built with stealth automation and a smart parser to handle messy data automatically.
    </p>

    <a class="btn" href="https://github.com/Pkkls/Kick-follow-Manager" target="_blank">
      View on GitHub
    </a>

    <a class="btn secondary" href="https://pkkls.github.io/Kick-follow-Manager/" target="_blank">
      Project Page
    </a>
  </section>

  <section>
    <h2>Features</h2>

    <div class="features">
      <div class="card">
        <strong>Stealth Chrome</strong>
        <p>Uses <code>undetected-chromedriver</code> to bypass bot detection.</p>
      </div>

      <div class="card">
        <strong>Bilingual UI</strong>
        <p>Choose between English and Japanese at startup.</p>
      </div>

      <div class="card">
        <strong>Smart Parsing</strong>
        <p>Handles duplicates, LIVE tags, headers, and messy input automatically.</p>
      </div>

      <div class="card">
        <strong>No Credentials Stored</strong>
        <p>Manual login only. No tokens or sensitive data saved.</p>
      </div>

      <div class="card">
        <strong>Auto Reports</strong>
        <p>Generates a detailed .txt report after each run.</p>
      </div>

      <div class="card">
        <strong>Cross-platform</strong>
        <p>Works on Windows, macOS, and Linux.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Quick Start</h2>

    <pre>
pip install undetected-chromedriver selenium
python kick_selenium.py
    </pre>
  </section>

  <section>
    <h2>Project Structure</h2>

    <pre>
.
├── kick_selenium.py
├── kick_follows.txt
    </pre>
  </section>

  <section>
    <h2>Export Your Follow List</h2>

    <ol>
      <li>Go to https://kick.com/following</li>
      <li>Scroll to the bottom</li>
      <li>Press Ctrl + A then Ctrl + C</li>
      <li>Paste into <code>kick_follows.txt</code></li>
    </ol>

    <p>The script automatically cleans:</p>
    <ul>
      <li>Duplicates</li>
      <li>LIVE labels</li>
      <li>Formatting issues</li>
    </ul>
  </section>

  <section>
    <h2>Requirements</h2>

    <ul>
      <li>Python 3.8+</li>
      <li>Google Chrome installed</li>
    </ul>
  </section>

  <section>
    <h2>Notes</h2>

    <ul>
      <li>Manual login is required</li>
      <li>No personal data is stored</li>
      <li>Use responsibly to avoid rate limits</li>
    </ul>
  </section>

  <footer>
    <p>© 2026 Kick Follow Manager — Open Source Project</p>
  </footer>

</div>

</body>
</html>
