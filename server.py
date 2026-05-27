from flask import Flask, request, jsonify
import subprocess
import os
import time

app = Flask(__name__)

# ======================
# HOME ROUTE
# ======================
@app.route("/")
def home():
    return open("index.html").read()


# ======================
# ENHANCED AI
# ======================
def ai_suggestions(code):
    suggestions = []
    lines = code.split("\n")

    # Structure checks
    if not code.strip().startswith("start"):
        suggestions.append("❌ Program should start with 'start'")
    if not code.strip().endswith("stop"):
        suggestions.append("❌ Program should end with 'stop'")

    # Line-based analysis
    for i, line in enumerate(lines):
        l = line.strip()

        if l.startswith("let") and "=" not in l:
            suggestions.append(f"⚠️ Line {i+1}: Missing '=' in variable declaration")

        if l.startswith("print") and len(l.split()) < 2:
            suggestions.append(f"⚠️ Line {i+1}: Nothing to print")

        if "&&" in l:
            suggestions.append(f"⚠️ Line {i+1}: '&&' not supported")

        if l.startswith("for") and "to" not in l:
            suggestions.append(f"⚠️ Line {i+1}: 'for' loop missing 'to'")

    if len(suggestions) == 0:
        suggestions.append("✅ Code looks good!")

    return suggestions


# ======================
# RUN CODE
# ======================
@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data["code"]

    with open("input.txt", "w") as f:
        f.write(code)

    subprocess.run("g++ compiler.cpp -o compiler.exe", shell=True)
    subprocess.run("compiler.exe", shell=True)

    os.system("taskkill /IM output.exe /F >nul 2>&1")

    exe = f"output_{int(time.time())}.exe"

    compile_process = subprocess.run(
        f"g++ output.cpp -o {exe}",
        shell=True,
        capture_output=True,
        text=True
    )

    if compile_process.returncode != 0:
        return jsonify({
            "output": compile_process.stderr,
            "ai": ai_suggestions(code)
        })

    run_process = subprocess.run(
        exe,
        shell=True,
        capture_output=True,
        text=True
    )

    return jsonify({
        "output": run_process.stdout,
        "ai": ai_suggestions(code)
    })


if __name__ == "__main__":
    app.run(debug=True)
