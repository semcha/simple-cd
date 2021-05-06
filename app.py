import os
import subprocess
import json
from ipaddress import ip_network, ip_address

import requests
from flask import Flask, request, Response

app = Flask(__name__)


def get_github_network_ips():
    response = requests.get("https://api.github.com/meta")
    json_data = response.json()
    github_network = [ip_network(x) for x in json_data.get("hooks")]
    return github_network


@app.route("/simple-cd", methods=["POST"])
def respond():
    github_network = get_github_network_ips()
    github_ip_check = any(
        True if ip_address(str(request.remote_addr)) in x else False
        for x in github_network
    )

    if not github_ip_check:
        return Response(status=403)

    payload = None
    content_type = request.headers.get("content-type")
    if content_type == "application/x-www-form-urlencoded":
        payload_text = request.form.get("payload", None)
        payload = json.loads(payload_text)
    elif content_type == "application/json":
        payload = request.get_json()
    else:
        return Response(status=400)

    if payload is None:
        return Response(status=400)

    repository_name = payload.get("repository").get("name")
    ref = payload.get("ref")
    branch_name = ref.split("/").pop()
    script_path = f"./scripts/{repository_name}-{branch_name}.sh"
    if os.path.exists(script_path):
        subprocess.call(["sh", script_path])

    return Response(status=200)
