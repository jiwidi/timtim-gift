#Made with <3  hehe
from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import datetime
from datetime import timedelta 


app = Flask(__name__, template_folder='templates')




hints = {
    "1": "TimTim is hard in the outside but really sweet in the inside like a _ _ _ _ _ _ _ _ _ _",
    "2": "In this sudoku: https://imgur.com/SgvaMQj which is the result of multiplying the numbers on the cells with a black circle?",
    "3": "What is '1'+'1'",
    "4": "Which is the building number of Jaime's place?",
    "5": "Bonanit",
    "6": "What has to be broken before you can eat it?",
    "7": "What kind of tree fits in your hand?",
    "8": "Hola",
    "9": "How much does Jaime misses you?",
    "10": "Netflix and chill, Imax and _ _ _ _ _ _",
    "11": "Tu regalo de navidad esta en el cajon donde estan los objetos que siguen la luz"
}

hintsAnswers = {
    "1": "watermelon",
    "2": "16",
    "3": "11",
    "4": "86",
    "5": "bondia",
    "6": "egg",
    "7": "palm tree",
    "8": "guapa",
    "9": "infinity",
    "10": "climax",
    "11": ""
}


CurrentDate = datetime.datetime.now()
def gethintn():
    try:
        f = open("demofile.txt", "r")
        hintnumber = f.readline()
        if(hintnumber==''):
            hintnumber = "1"
        f.close()
        return hintnumber
    except:
        return "1"
def increasehitn(currentN):
    try:
        f = open("demofile.txt", "w+")
        hintnumber = str(int(currentN) + 1)
        if (hintnumber in hintsAnswers.keys()):
            f.write(hintnumber)
        else: 
            hintnumber = str(int(hintnumber) - 1)
            f.write(hintnumber)
        f.close()
        return hintnumber
    except:
        f = open("demofile.txt", "w+")
        f.write(currentN)
        f.close()
    return currentN

def checkAnswer(text,hitn):
    hintn = hitn
    result = False
    try:
        if (text==hintsAnswers[hintn]):
            result=True
    except:
         pass
    return result





hintnumber = gethintn()
maxhit = hintnumber
hint = hints[hintnumber]
nextbutton="Validate"

@app.route('/')
def index():
    #Retrieve current hint
    maxhit = gethintn()
    #Default values for strings
    puzzlecount = "Solved {}/{} puzzles".format(maxhit,len(hints))
    return render_template('index.html',hint=hint,hintnumber=hintnumber, backbutton="none", nextbutton="Start!", hintsolved=puzzlecount,textENABLED="none", bigtextL="TimTim christmas puzzle", mediumtextL="Solve the hints and find your christmas gift :) ")

@app.route('/goback')
def goback():
    #Retrieve current hint
    maxhit = gethintn()
    #Default values for strings
    puzzlecount = "Solved {}/11 puzzles".format(maxhit)
    return render_template('index.html',hint=hint,hintnumber=hintnumber, backbutton="none", nextbutton="Start!", hintsolved=puzzlecount,textENABLED="none", bigtextL="TimTim christmas puzzle", mediumtextL="Solve the hints and find your christmas gift :) ")



@app.route('/start' ,methods=['GET', 'POST'])
def start():
    #Retrieve current hint
    maxhit = gethintn()
    puzzlecount = "Solved {}/{} puzzles".format(maxhit,len(hints))
    #Default values for strings
    bigtext = "Puzzle n{}".format(int(maxhit))
    mediumtext = hints[maxhit]
    return render_template('index.html', hint=hint,hintnumber=hintnumber, backbutton="",nextbutton="Validate", hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext)

@app.route('/next', methods=['GET', 'POST'])
def next():
    text = request.form['text']
    hitn = request.args.get("hintnumber")
    #Default values for strings
    maxhit = gethintn()
    puzzlecount = "Solved {}/{} puzzles".format(maxhit,len(hints))
    bigtext = "Puzzle n{}".format(int(hitn))
    mediumtext = hints[hitn]
    resultText = ""
    nextbutton = "Next" if (int(hitn)+1)<=int(maxhit) else "Validate"

    #Checks is okay to solve hint today
    basedate = "12/12/2019 23:59"
    basedate = datetime.datetime.strptime(basedate, "%d/%m/%Y %H:%M")
    CurrentDate = datetime.datetime.now()
    basedate = basedate + timedelta(days=int(hitn)) 

    
    if(CurrentDate<basedate):
        resultText = "Too soon to solve the hint, wait {0} hours".format( str(round((basedate-CurrentDate).seconds/60/60, 2)) )
        return render_template('index.html', hint=hint,hintnumber=int(hitn), backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

    #processing
    processed_text = text.lower().strip()
    result = checkAnswer(processed_text,hitn)
    resultText = "WRONG ANSWER TIMTIM"
    if(result):
        hitn = increasehitn(hitn)
        bigtext = "Puzzle n{}".format(int(hitn))
        mediumtext = hints[hitn]
        resultText = "CORRECT ANSWER TIMTIM"
    elif(int(hitn)<int(maxhit)):
        result=True
        hitn = str(int(hitn)+1)
        bigtext = "Puzzle n{}".format(int(hitn))
        mediumtext = hints[hitn]
        hintnumber=int(hitn)
        resultText=""
        return render_template('index.html', hint=hint,hintnumber=hitn, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)
        
    return render_template('index.html', hint=hint,hintnumber=hitn, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

@app.route('/previous', methods=['GET', 'POST'])
def previous():
    hintnumber = request.args.get("hintnumber")
    newhint = int(hintnumber) - 1
    newhint = newhint if newhint>=1 else 1
    maxhit = gethintn()
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    nextbutton = "Next" if int(newhint)<int(maxhit) else "Validate"
    hintnumber = str(newhint)
    #Default values for strings
    bigtext = "Puzzle n{}".format(int(hintnumber))
    mediumtext = hints[hintnumber]
    resultText = ""
    return render_template('index.html', hint=hint,hintnumber=hintnumber, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

def create_app():
    app.run(host='0.0.0.0', port=80,debug=True)
