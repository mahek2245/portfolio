from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = "your_secret_key"

DATA_FILE = "data.json"

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file, resetting data.")
            return {"projects": [], "events": []}
    return {"projects": [], "events": []}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    return render_template(
        'index.html',
        github_url="https://github.com/mahek2245",
        linkedin_url="https://in.linkedin.com/in/mahek-thakur-095381324"
    )

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login credentials!", "error")
            return redirect(url_for("admin"))

    return render_template("admin.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))

    data = load_data()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        content_type = request.form.get("type", "").strip()
        files = request.files.getlist("file")  # Get multiple files

        print("Debug: Form Data Received")
        print("Title:", title)
        print("Description:", description)
        print("Content Type:", content_type)
        print("Files:", [f.filename for f in files if f])

        if not title or not description or content_type not in ["projects", "events"]:
            flash("Error: All fields are required!", "error")
            return redirect(url_for("dashboard"))

        file_paths = []
        if files:
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    # Convert Windows backslashes to forward slashes
                    file_path = file_path.replace("\\", "/")
                    file_paths.append(file_path)
                    print(" File Saved at:", file_path)

        new_entry = {
            "title": title,
            "description": description,
            "file_paths": file_paths if file_paths else None  # Ensure file paths are stored
        }

        print("📌 Final Entry:", new_entry)

        data[content_type].append(new_entry)
        save_data(data)

        flash("✅ Upload successful!", "success")
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", data=data)

@app.route("/projects")
def projects():
    data = load_data()
    return render_template("projects.html", projects=data.get("projects", []))

@app.route("/events")
def events():
    data = load_data()
    return render_template("events.html", events=data.get("events", []))

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
