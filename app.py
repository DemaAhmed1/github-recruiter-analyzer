from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    username = request.form["username"]

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    data = response.json()

    # سكّور
    score = (data.get("public_repos", 0) * 2) + (data.get("followers", 0) * 1)

    # مستوى الحساب
    if score >= 50:
        level = "Pro 🔥"
    elif score >= 20:
        level = "Intermediate 🟡"
    else:
        level = "Beginner 🟢"

    # احتفال
    celebrate = score >= 50

    return render_template(
        "result.html",
        name=data.get("name"),
        followers=data.get("followers"),
        repos=data.get("public_repos"),
        avatar=data.get("avatar_url"),
        score=score,
        level=level,
        celebrate=celebrate
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    