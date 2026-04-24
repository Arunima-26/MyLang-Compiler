from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response



def analyze_code(code):
    suggestions = []

    lines = code.split("\n")

    if not code.strip().startswith("start"):
        suggestions.append("Program should start with 'start'")

    if not code.strip().endswith("stop"):
        suggestions.append("Program should end with 'stop'")

   
    declared = set()

    for i, line in enumerate(lines, start=1):
        tokens = line.split()

        if not tokens:
            continue

       
        if tokens[0] == "let":
            if len(tokens) >= 4:
                declared.add(tokens[1])

        
        if tokens[0] == "print":
            if len(tokens) >= 2 and tokens[1].isalpha():
                if tokens[1] not in declared:
                    suggestions.append(f"Line {i}: Variable '{tokens[1]}' not declared")

        
        if tokens[0] in ["if", "while", "for"]:
            if "end" not in code:
                suggestions.append(f"Line {i}: Missing 'end' for block")

    if not suggestions:
        suggestions.append("No issues found. Code looks good!")

    return suggestions



@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get("code", "")

    try:
       
        with open("input.mylang", "w") as f:
            f.write(code)

        
        subprocess.run("compiler.exe", shell=True)

        subprocess.run("g++ output.cpp -o output.exe", shell=True)

     
        result = subprocess.run("output.exe", shell=True, capture_output=True, text=True)

       
        suggestions = analyze_code(code)

        return jsonify({
            "output": result.stdout,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({
            "output": str(e),
            "suggestions": ["Error occurred during execution"]
        })



@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message", "").lower()

    if "loop" in msg:
        reply = """Loops repeat instructions.

Types:
1. for loop
2. while loop

Example:
for i = 1 to 5
print i
end"""

    elif "for" in msg:
        reply = """For loop:

for i = 1 to 5
print i
end"""

    elif "while" in msg:
        reply = """While loop:

while x < 10
print x
end"""

    elif "if" in msg:
        reply = """If condition:

if x > 5
print x
end"""

    elif "variable" in msg:
        reply = """Declare variables:

let x = 10
let y = x + 5"""

    elif "print" in msg:
        reply = "Use 'print x' to display output."

    elif "error" in msg:
        reply = """Common errors:
- Missing end
- Variable not declared
- Missing start/stop"""

    else:
        reply = "Ask about loops, variables, conditions, or syntax."

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)