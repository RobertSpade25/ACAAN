import time
from playsound import playsound
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session.__init__ import Session

app = Flask(__name__)
app.config['SESSION_PERMANT'] = False
app.config['SESSION_TYPE'] ='filesystem'
Session(app)

suits = ["♣️", "♥️", "♠️", "♦️"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = []
deckDict = {}

for value in values:
    for suit in suits:
        card = value + suit
        deck.append(card)

for card in deck:
    if card[1] == "♥️":
        deckDict[card] = card.replace("♥️", "H")
    if card[1] == "♦️":
        deckDict[card] = card.replace("♦️", "D")
    if card[1] == "♠️":
        deckDict[card] = card.replace("♠️", "S")
    if card[1] == "♣️":
        deckDict[card] = card.replace("♣️", "C")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        seconds = request.form["timer_input"]
        time.sleep(int(seconds))
        playsound('text_tone.mp3')
        return redirect(url_for("card"))
    else:
        return render_template("index.html")

@app.route("/card", methods=["GET", "POST"])
def card():
    if request.method == "POST":
        session['card'] = request.form["submit_button"]
        return redirect(url_for("first_digit"))
    else:
        return render_template("card.html", deck=deck, deckDict=deckDict)

@app.route("/first_digit", methods=["GET", "POST"])
def first_digit():
    if request.method == "POST":
        session['number1'] = request.form["submit_button1"]
        return redirect(url_for("second_digit"))
    else:
        return render_template("first_digit.html")

@app.route("/second_digit", methods=["GET", "POST"])
def second_digit():
    if request.method == "POST":
        print("Works")
        session['number2'] = request.form["submit_button2"]
        return redirect(url_for("display"))
    else:
        return render_template("second_digit.html")

@app.route("/display")
def display():
    card = session.get('card')
    card = card.replace("♥️", "H")
    card = card.replace("♦️", "D")
    card = card.replace("♠️", "S")
    card = card.replace("♣️", "C")    
    number1 = session.get('number1')
    number2 = session.get('number2')
    number = int(number1 + number2)
    mnemonica = ["4C","2H","7D","3C","4H","6D","AS","5H","9S","2S","QH","3D","QC","8H","6S","5S","9H","KC","2D","JH","3S","8S","6H","10C","5D","KD","2C","3H","8D","5C","KS","JD","8C","10S","KH","JC","7S","10H","AD","4S","7H","4D","AC","9C","JS","QD","7C","QS","10D","6C","AH","9D"]
    stack_number = mnemonica.index(card) + 1
    if stack_number > number:
        shift_number = stack_number - (number + 1)
        shift_card = mnemonica[shift_number]
    elif stack_number == number:
        shift_number = 51
        shift_card = mnemonica[shift_number]
    else:
        shift_number = 51 - (number - stack_number)
        shift_card = mnemonica[shift_number]
        card = session.get('card')
    if "D" in shift_card or "H" in shift_card:
        color = "red"
    else:
        color = "black"
    shift_card = shift_card.replace("H", "♥️")
    shift_card = shift_card.replace("D", "♦️")
    shift_card = shift_card.replace("S", "♠️")
    shift_card = shift_card.replace("C", "♣️") 
    return render_template("display.html", shift_card=shift_card, color=color)
        # to refrence final answer, use shift_card