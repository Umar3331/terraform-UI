from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import hcl2
import os
import subprocess
import re
import time

app = Flask(__name__, static_folder="static")
CORS(app)

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/modules")
def list_modules():
    modules = sorted([
        d for d in os.listdir("tf_modules")
        if os.path.isdir(os.path.join("tf_modules", d))
    ])
    return jsonify(modules)

# @app.route("/logos/<filename>")
# def get_logo(filename):
#     return send_from_directory("static/logos", filename)

@app.route("/modules/<module_name>/variables", methods=["GET"])
def get_module_variables(module_name):
    module_path = os.path.join("tf_modules", module_name, "variables.tf")
    if not os.path.exists(module_path):
        return jsonify({"error": "Module not found"}), 404

    with open(module_path, 'r') as f:
        obj = hcl2.load(f)

    variables = []
    for var in obj.get("variable", []):
        for name, props in var.items():
            variables.append({
                "name": name,
                "description": props.get("description", ""),
                "type": props.get("type", "string"),
                "default": props.get("default", None)
            })

    return jsonify(variables)

@app.route("/modules/<module_name>/configure", methods=["POST"])
def save_tfvars(module_name):
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    filename = os.path.join("user_configs", f"{module_name}-config.tfvars")
    try:
        with open(filename, "w") as f:
            for key, value in data.items():
                if isinstance(value, str):
                    value = f"\"{value}\""
                f.write(f'{key} = {value}\n')
        return jsonify({"message": "tfvars file created", "path": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stream/<module_name>/<step>")
def stream_logs(module_name, step):
    def generate():
        tf_dir = os.path.join("tf_modules", module_name)
        tfvars_path = os.path.join("user_configs", f"{module_name}-config.tfvars")

        if not os.path.exists(tf_dir) or not os.path.exists(tfvars_path):
            yield f"data: ERROR: module or tfvars not found\n\n"
            yield "event: done\ndata: complete\n\n"
            return

        cmd = ["terraform", step]
        if step in ["plan", "apply"]:
            cmd += ["-var-file", os.path.relpath(tfvars_path, tf_dir)]
            if step == "apply":
                cmd.insert(2, "-auto-approve")

        process = subprocess.Popen(cmd, cwd=tf_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ''):
            clean = strip_ansi_codes(line.rstrip())
            yield f"data: {clean}\n\n"

        yield "event: done\ndata: complete\n\n"

    return app.response_class(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)