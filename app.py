from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    username = request.form.get("username")

    data = requests.get(
        f"https://api.github.com/users/{username}"
    ).json()

    score = (data.get("public_repos", 0) * 2) + (data.get("followers", 0) * 1)
    celebrate=score >=50

    if score >= 100:
        level = "gold"
        message = "🎉 Amazing Profile! You're a Top Developer!"
    elif score >= 50:
        level = "silver"
        message = "🔥 Great Profile! Keep going!"
    else:
        level = "bronze"
        message = "🙂 Good start! Keep improving!"

    return render_template(
        "result.html",
        name=data.get("name"),
        followers=data.get("followers"),
        repos=data.get("public_repos"),
        avatar=data.get("avatar_url"),
        score=score,
        message=message,
        level=level
        celebrate=celebrate
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    