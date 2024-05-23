from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from textblob import TextBlob
import webbrowser
import threading

count = 0

app = Flask(__name__)

# Initialize the ChatBot
english_bot = ChatBot(
    "ChatterBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter"
)

# Train the ChatBot if it hasn't been trained yet
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global count
    userText = request.args.get('msg')
    obj = TextBlob(userText)
    sentiment, subjectivity = obj.sentiment
    print(obj.sentiment)
    if sentiment > 0:
        count += 1
    elif sentiment < 0:
        count -= 1
    print("count", count)

    try:
        response = str(english_bot.get_response(userText))
    except Exception as e:
        print(f"Error: {e}")
        response = "I'm sorry, but I am unable to process your request right now."
    
    return response

def open_url(url):
    webbrowser.open_new(url)

@app.route("/forward/", methods=['POST'])
def get_song_playlist():
    global count
    try:
        if count > 0:
            threading.Thread(target=open_url, args=("https://www.last.fm/tag/happy",)).start()
        elif count < 0:
            threading.Thread(target=open_url, args=("https://www.last.fm/tag/sad",)).start()
        else:
            threading.Thread(target=open_url, args=("https://www.last.fm/tag/neutral",)).start()
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while trying to open the playlist.", 500

    return "Opening playlist..."

if __name__ == '__main__':
    app.run(debug=True)
