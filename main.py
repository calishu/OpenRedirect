import os
import yaml
import importlib
from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/<path:subpath>")
def handle_redirect(subpath):
    url = db_instance.get_url(subpath)
    if url != "404": return redirect(url, 302)
    print(url)
    return "Redirect not found", 404

if __name__ == "__main__":
    try: config = yaml.safe_load(open("config.yml", "r"))
    except yaml.YAMLError as err: print(err); exit(1)

    #for cfg in config:
    #    if cfg is None: print("You need change the config!"); exit(1)

    db_type = config["storage"]["db"]
    config = config["storage"]["credentials"]["host"], config["storage"]["credentials"]["user"], config["storage"]["credentials"]["password"], config["storage"]["credentials"]["database"]
    db_instance = getattr(importlib.import_module(f"database.{db_type}"), db_type)(*config)

    db_instance.setup()
    app.run(threaded=True)