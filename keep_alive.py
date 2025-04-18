from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return """
    <style>
        body {
            background-color: #1a1a1a;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            text-align: center;
            margin-top: 50px;
        }
        .container {
            padding: 20px;
            background-color: #2d2d2d;
            border-radius: 10px;
            max-width: 600px;
            margin: 0 auto;
        }
        h1 {
            color: #ff0059;
        }
        .status {
            color: #00ffff;
            font-size: 1.2em;
            margin: 20px 0;
        }
        .info {
            color: #9300ff;
            font-style: italic;
        }
    </style>
    <div class="container">
        <h1>🤖 Orvix Bot System</h1>
        <div class="status">⚡ STATUS: ONLINE</div>
        <div class="info">Monitoring and maintaining digital realm stability...</div>
    </div>
    """

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start() 