from flask import Flask, render_template, request
import pickle
import datetime
import os

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Create log file if it doesn't exist
if not os.path.exists("web_log.txt"):
    with open("web_log.txt", "w", encoding="utf-8") as f:
        f.write("📄 Spam Web Log\n\n")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        msg = request.form["message"]
        if msg.strip() == "":
            result = "⚠️ Please enter a message."
        else:
            vec = vectorizer.transform([msg])
            pred = model.predict(vec)[0]
            result = "🚨 SPAM" if pred == "spam" else "✅ NOT spam"

            # Log entry safely with UTF-8 encoding
            with open("web_log.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}]\nMessage: {msg}\nResult: {result}\n{'-'*50}\n")

    return render_template("index.html", result=result)

@app.route("/history")
def history():
    try:
        with open("web_log.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No log history yet!"
    return render_template("history.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)