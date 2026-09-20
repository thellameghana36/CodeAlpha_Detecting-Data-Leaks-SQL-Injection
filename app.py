from flask import Flask, request, render_template_string
import sqlite3, base64, secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
AES_KEY = b'ThisIsA32ByteKeyForAES256CodeAl2'

def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    ct = base64.b64encode(ct_bytes).decode()
    return iv + ":" + ct

def decrypt_data(enc):
    iv, ct = enc.split(":")
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

def is_sql_injection(s):
    bad = ["' OR ", "'--", "1=1", "DROP", "UNION", ";--"]
    for b in bad:
        if b.lower() in s.lower():
            return True
    return False

def init_db():
    conn = sqlite3.connect('secure.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, cap TEXT)')
    conn.commit()
    conn.close()
init_db()

HTML = """
<h2>CodeAlpha - Task 2: Detecting Data Leaks via SQL Injection</h2>
<p><b>Capability Code Example:</b> Will be generated after register</p>
<h3>Register (AES-256 Encryption)</h3>
<form method="post" action="/register">
<input name="username" placeholder="username" required>
<input name="password" placeholder="password" required>
<button>Register</button>
</form>
<hr>
<h3>Login (Try SQL Injection like ' OR '1'='1)</h3>
<form method="post" action="/login">
<input name="username" placeholder="username" required>
<input name="password" placeholder="password" required>
<input name="cap" placeholder="Capability Code" required>
<button>Login</button>
</form>
<h3>{{msg}}</h3>
"""

@app.route('/')
def home():
    return render_template_string(HTML, msg="")

@app.route('/register', methods=['POST'])
def register():
    u = request.form['username']
    p = request.form['password']
    if is_sql_injection(u) or is_sql_injection(p):
        return render_template_string(HTML, msg="🚨 SQL Injection Blocked - Layer 1 Security")
    enc = encrypt_data(p)
    cap = secrets.token_hex(4)
    conn = sqlite3.connect('secure.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?)", (u, enc, cap))
    conn.commit()
    conn.close()
    return render_template_string(HTML, msg=f"✅ Registered! AES Encrypted. Your Capability Code: {cap}")

@app.route('/login', methods=['POST'])
def login():
    u = request.form['username']
    p = request.form['password']
    cap = request.form['cap']
    if is_sql_injection(u):
        return render_template_string(HTML, msg="❌ ALERT! SQL Injection Detected & Blocked - Data Leak Prevented")
    conn = sqlite3.connect('secure.db')
    c = conn.cursor()
    c.execute("SELECT password, cap FROM users WHERE username=?", (u,))
    row = c.fetchone()
    conn.close()
    if row:
        dec = decrypt_data(row[0])
        if dec==p and row[1]==cap:
            return render_template_string(HTML, msg="✅ Login Success - Double Layer Security Passed")
    return render_template_string(HTML, msg="❌ Login Failed")

if __name__ == '__main__':
    app.run(debug=True)