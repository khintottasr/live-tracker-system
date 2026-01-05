import os
import datetime
from flask import Flask, render_template, jsonify, send_file
from io import BytesIO

app = Flask(__name__)

# --- CONFIG ---
LOG_FILE = "opens.txt"
PIXEL_DATA = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track/<email>')
def track(email):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {email}\n")
    
    print(f"[*] Email Opened: {email} at {timestamp}")
    return send_file(BytesIO(PIXEL_DATA), mimetype='image/png')

@app.route('/stats')
def stats():
    all_opens = []
    unique_emails = set()
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    all_opens.append(line)
                    # Unique Visitor logic
                    email_part = line.split(" | ")[1]
                    unique_emails.add(email_part)
    
    # Sift data l-index.html
    return jsonify({
        "opens": all_opens[::-1][:30],      # Akhir 30 log
        "total_count": len(all_opens),      # Total clicks
        "unique_count": len(unique_emails)   # Total unique emails
    })

if __name__ == '__main__':
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    app.run(port=5000, debug=True)