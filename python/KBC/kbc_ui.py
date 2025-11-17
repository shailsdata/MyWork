from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a strong secret key

def get_questions():
    questions = ['Which god is also known as ‘Gauri Nandan’?',
                 'What does not grow on tree according to a popular Hindi saying?',
                 'Which city is known as Pink City in India?',
                 "Who wrote India's National Anthem?",
                 'How many major religions are there in India?',
                 'When is the National Hindi Diwas celebrated?',
                 'What is the name of the game developer ?',
                 'How many states are there in India?',
                 'Where in India Gate located?',
                 'Who wrote Vande Mataram?',
                 'Which one of the following places is famous for the Great Vishnu Temple?',
                 'Which Indian monument was originally built as a victory tower to commemorate the defeat of the Khan of Khambhat?',
                 "Who among the following was killed during 'Operation Bluestar' of 1984?",
                 'Which former Indian President died as a result of a road accident?',
                 'Who is the founder of the political party Dravida Munnetra Kazhagam (DMK)?',
                 'Who was the first Indian woman to win a medal in the Olympics?']
    options = [['A.Agni', 'B.Indra', 'C.Hanuman', 'D.Ganesha'],
               ['A.Money', 'B.Flowers', 'C.Leaves', 'D.Fruits'],
               ['A.Banglore', 'B.Maysore', 'C.Jaipur', 'D.Kochi'],
               ['A.Rabindranath Tagore', 'B.Lal Bahadur Shastri', 'C.Chetan Bhagat', 'D.RK Narayan'],
               ['A.6', 'B.7', 'C.8', 'D.9'],
               ['A.13 September', 'B.14 September', 'C.14 July', 'D.15 August'],
               ['A.Adarsh', 'B.Aakarsh', 'C.Aakash', 'D.Akash'],
               ['A.28', 'B.29', 'C.31', 'D.31'],
               ['A.Agra', 'B.Punjab', 'C.Mumbai', 'D.New Delhi'],
               ['A.Sarat Chandra Chattopadhyay', 'B.Rabindranath Tagore', 'C.Bankim Chandra Chatterjee', 'D.Ishwar Chandra Vidyasagar'],
               ['A.Bordubar, Indonesia', 'B.Bamiyan, Afghanistan', 'C.Panja Sahib, Pakistan', 'D.Ankorvat, Cambodia'],
               ['A.Qutub Minar', 'B.India Gate', 'C.Charminar', 'D.Vijay Stambha'],
               ['A.Baba Santa Singh', 'B.Haji Mastan', 'C.Jarnail Singh Bhindrawale', 'D.Homi Jehangir Bhabha'],
               ['A.Rajendra Prasad', 'B.Faqruddin Ali Ahmed', 'C.Giani Zail Singh', 'D.R.Venkatraman'],
               ['A.C.N. Annadurai', 'B.M. Karunanidhi', 'C.M.G. Ramachandran', 'D.Jayalalitha'],
               ['A.P.T. Usha', 'B.Kunjarani Devi', 'C.Bachendri Pal', 'D.Karnam Maleshwari']]
    options50 = [['A.Agni', 'B.', 'C.', 'D.Ganesha'],
                 ['A.Money', 'B.', 'C.Leaves', 'D.'],
                 ['A.', 'B.Maysore', 'C.Jaipur', 'D.'],
                 ['A.Rabindranath Tagore', 'B.', 'C.Chetan Bhagat', 'D.'],
                 ['A.6', 'B.7', 'C.', 'D.'],
                 ['A.', 'B.14 September', 'C.', 'D.15 August'],
                 ['A.', 'B.Aakarsh', 'C.Aakash', 'D.'],
                 ['A.28', 'B.', 'C.', 'D.31'],
                 ['A.', 'B.', 'C.Mumbai', 'D.New Delhi'],
                 ['A.', 'B.Rabindranath Tagore', 'C.Bankim Chandra Chatterjee', 'D.'],
                 ['A.Bordubar, Indonesia', 'B.', 'C.', 'D.Ankorvat, Cambodia'],
                 ['A.', 'B.India Gate', 'C.', 'D.Vijay Stambha'],
                 ['A.Baba Santa Singh', 'B.', 'C.Jarnail Singh Bhindwale', 'D.'],
                 ['A.Rajendra Prasad', 'B.', 'C.Giani Zail Singh', 'D.'],
                 ['A.C.N. Annadurai', 'B.', 'C.', 'D.Jayalalitha'],
                 ['A.', 'B.', 'C.Bachendri Pal', 'D.Karnam Maleshwari']]
    answers = ['D', 'A', 'C', 'A', 'A', 'B', 'B', 'A', 'D', 'C', 'D', 'D', 'C', 'C', 'A', 'D']
    money = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1250000, 2500000, 5000000, 10000000, 20000000]

    combined = list(zip(questions, options, options50, answers, money))
    random.shuffle(combined)
    return combined

@app.route("/", methods=["GET", "POST"])
def quiz():
    if "quiz_data" not in session:
        session["quiz_data"] = get_questions()
        session["current_index"] = 0
        session["earned_money"] = 0
        session["lifelines"] = {"fifty_fifty": False, "flip": False}

    data = session["quiz_data"]
    index = session["current_index"]
    lifelines = session["lifelines"]

    if index >= len(data):
        earned = session.get("earned_money", 0)
        session.clear()
        return render_template("result.html", earned=earned, completed=True)

    question, options, options50, answer, amount = data[index]

    if request.method == "POST":
        selected = request.form.get("option")

        # Lifeline use
        if "use_lifeline" in request.form:
            lifeline_type = request.form.get("lifeline")
            if lifeline_type == "50:50" and not lifelines["fifty_fifty"]:
                lifelines["fifty_fifty"] = True
            elif lifeline_type == "flip" and not lifelines["flip"]:
                lifelines["flip"] = True
                # Flip question: skip current question to next
                session["current_index"] += 1
                session.modified = True
                return redirect(url_for("quiz"))

            session.modified = True
            return redirect(url_for("quiz"))

        if selected:
            if selected == answer:
                session["earned_money"] = amount
                session["current_index"] += 1
                session.modified = True
                # continue to next question
                return redirect(url_for("quiz"))
            else:
                earned = session.get("earned_money", 0)
                session.clear()
                return render_template("result.html", earned=earned, completed=False)

        if request.form.get("quit") == "quit":
            earned = session.get("earned_money", 0)
            session.clear()
            return render_template("result.html", earned=earned, completed=False)

    display_options = options50 if lifelines["fifty_fifty"] else options

    return render_template("quiz.html", question=question, options=display_options, lifelines=lifelines, current_index=index+1, total=len(data), earned_money=session["earned_money"])


if __name__ == "__main__":
    app.run(debug=True)
