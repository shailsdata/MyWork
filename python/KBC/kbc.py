'''
Algorithm
Required data sets : questions , options , correct answer , amout
output : Final win amount
design
1.have a ui with question , amount dispalyed , options -radio button
2.User response : aswer
3.have 50:50 , flip the questions
a. zip the questions and option, option50 , answer
b. track the amount won in a variable and add the amount
c. check if option 50 or flip is required
track the counters for them only once can be taken
once done display the amout with congradulations






'''
import random


def questions():
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
               ['A.Sarat Chandra Chattopadhyay', 'B.Rabindranath Tagore', 'C.Bankim Chandra Chatterjee',
                'D.Ishwar Chandra Vidyasagar'],
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
    combined = list(zip(questions, options, options50, answers))
    random.shuffle(combined)
    return combined


def ask_questions(question_zip):
    life_line_cnt = {'fif': 0, 'flip': 0}
    money = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1250000, 2500000, 5000000,
             10000000]
    iteration_cnt = 0
    for i in question_zip:
        print("\nQuestion: " + i[0])
        print("Options: " + ', '.join(i[1]))
        answer = input("Your answer: ")
        if life_line_cnt["fif"] == 0 and life_line_cnt["flip"] == 0:
            ask_life_line = int(input("Would you like to take life line ? Type 1 for Yes 0 for no: "))
            if ask_life_line == 1:
                life_line_options = int(
                    input("Which life line you would like to take ? type 1 for 50:50 , type 2 for flip question: "))
                if life_line_options == 1:
                    life_line_cnt["fif"] = 1
                    answer = life_line_fifty(life_line_options, i)
                elif life_line_options == 2:
                    life_line_cnt["flip"] = 1
                    continue

        elif life_line_cnt["fif"] == 1 and life_line_cnt["flip"] == 0:
            ask_life_line = int(input("Would you like to take life line flip ? Type 1 for Yes 0 for no: "))
            if ask_life_line == 1:
                life_line_options = 2
                life_line_cnt["flip"] = 1
                continue

        elif life_line_cnt["fif"] == 0 and life_line_cnt["flip"] == 1:
            ask_life_line = int(input("Would you like to take life line 50/50 ? Type 1 for Yes 0 for no: "))
            if ask_life_line == 1:
                life_line_options = 1
                life_line_cnt["fif"] = 1
                answer = life_line_fifty(life_line_options, i)

        else:
            answer = input("You have already used both life lines. Guess the answer or type 'quite' to quit: ")

        if answer.lower() == 'quite':
            print("Thanks for playing! You won Rs." + str(money[iteration_cnt - 1] if iteration_cnt > 0 else 0))
            break

        if answer.upper() == i[3]:
            print("Awesome! Your answer is correct!! The correct answer is: " + i[3])
            print("Your total earned money is: Rs." + str(money[iteration_cnt]))
            iteration_cnt += 1
        else:
            print("Oh no.. Your answer is wrong!! The correct answer is: " + i[3])
            print("Your total earned money is: Rs." + str(money[iteration_cnt - 1] if iteration_cnt > 0 else 0))
            break


def life_line_fifty(option, question):
    if option == 1:
        print("50:50 lifeline activated")
        print("Question: " + question[0])
        print("Options: " + ', '.join(question[2]))
        answer = input("Choose your answer from above options: ")
    else:
        answer = input("Invalid lifeline option. Please enter your answer: ")
    return answer


def main():
    questions_set = questions()
    ask_questions(questions_set)


if __name__ == "__main__":
    main()







