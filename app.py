import json
import os

import yaml
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

CONFIG_FILE_PATH = "./REGISTERED"

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"yaml", "yml"}

# from OpenSSL import SSL

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "abcdefg"

# // For a List of Hash, create a table
def create_list_table(item, body:str):
    child_key_list = []
    for sub_item in item:
        child_key_list = sub_item.keys()

    body += "<table><tr>"
    for child_item in child_key_list:
        body += "<th>" + child_item + "</th>"

    body += "</tr>"


    return body

def process_list_data(list_data, body):

    for list_item in list_data:
        if isinstance(list_item, dict):
            body = convert(list_item, body)
        else:
            # // If the value is a string element
            body += "<li>" + list_item + "</li>"

    return body

    # #  If the value is an object
    # if isinstance(first_item, dict):
    #     body = convert(item, body)
    # else:
    #     # // If the value is a string element
    #     for list_item in list_data:
    #         body += "<li>" + list_item + "</li>"


def convert(item, body:str):

    if isinstance(item, list):
        list_data = item

        body = process_list_data(list_data, body)
    else:
        for key, value in item.items():
            if isinstance(value, dict) or isinstance(value, list):
                try:
                    body += "<tr><th>" + key + "</th>"
                    body += "<td><table>"
                    body = convert(value, body)
                    body += "</table></td></tr>"
                except Exception as e:
                    raise e
            else:
                try:
                    body += "<tr><th>" + key + "</th>"
                    body += "<td>" + value + "</td></tr>"
                except Exception as e:
                    raise e


    return body


def json_to_html(json_data):
    try:
        table = convert(json_data, "")
    except Exception as e:
        raise e
    html_body_content = f"<table border='1'>{table}</table>"
    html_body = f"<body>{html_body_content}</body>"
    return f"<html>{html_body}</html>"

@app.route('/')
def index():
    return render_template("hello.html")


@app.route("/click", methods=["GET", "POST"])
def click():
    return {"return":"Success"}


@app.route("/table")
def table():
    if request.method == "GET":
        jsonfile = os.path.join(app.config["UPLOAD_FOLDER"], "values.json")
        with open(jsonfile, "r") as file:
            json_data = json.load(file)
            return render_template("hello.html", json_data=json_data)
    return "Success"

@app.route("/convert", methods=["POST"])
def convert_file():
    if request.method == "POST":
        filename = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded.yaml")
        jsonfile = os.path.join(app.config["UPLOAD_FOLDER"], "values.json")
        print(filename)
        with open(filename, "r") as file:
            configuration = yaml.safe_load(file)

        html = json_to_html(configuration)

        # with open(jsonfile, "w") as json_file:
        #     json.dump(configuration, json_file)
    return html


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], "uploaded.yaml"))
            flash("No file part")
            return "Success"

    return "Not supported"



@app.post('/v1/apiRoot/oCloudAvailableNotification')
def ocloud_available():
    # return render_template("hello.html", ocloud_data=request.json)
    body = request.json
    gcloud_id = ""
    try:
        if body:
            gcloud_id = body.get("gCloudId")
    except ValueError:
        return "Invalid body"

    os.makedirs(gcloud_id, exist_ok=True)
    data = json.dumps(body, indent=4)
    file_name = os.path.join(gcloud_id, f"ocloud_{gcloud_id}.json")
    try:
        with open(file_name, "w") as newfile:
            newfile.write(data)
    except Exception:
        return "Failed to write file"

    return f"Success for gcloud id: {gcloud_id}"
