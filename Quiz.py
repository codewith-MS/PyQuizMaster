import random
import json 
import time


#read the json file
def load_questions():
    with open("questions.json","r") as f:
        questions = json.load(f)["question"]

    return questions

### Bag has 5 questions User asks for 7 → we can’t give 7 → give 5


#random question 
def get_random_question(question, num_questions):             
    if num_questions > len(question):                   #len(question)How many questions are actually in your bag      
        num_questions = len(question)                   #check if user asked for more questions than we have
                                                        
    random_questions = random.sample(question,num_questions)
    return random_questions

#ask the user the question
def ask_question(question):
    print(question['question'])
    for i, option in enumerate(question["options"]):
        print(str(i+1)+ ".", option)

    #adding try block because if user enter non - interger number.   
    try:
        number = int(input("Select the correct number: "))
    except:
        print ("Invalid input, defaulting to wrong answer.")
        return False

        
    if number <1 or number >len(question["options"]):
        print("Invalid choice")
        return False
    
    correct = question["options"][number - 1] == question["answer"]
    return correct 


#load the random question
questions = load_questions()

level = ["easy", "medium", "hard"]

while True:
    difficulty_level = input("which level do you want to play? [Easy , Medium , Hard] ").lower()
    if difficulty_level in level:
        print("You have selected", difficulty_level, "level")
        break
    else:
        print("Invalid Level")

#list Comprehension
user_level_questions = list(filter(lambda q : q["difficulty"] == difficulty_level , questions))

"""filter() → goes through the list and picks items that match the condition
lambda → defines the condition quickly
list() → converts the result into a normal Python list"""


total_questions = int(input("Enter the number of Questions:  "))
random_questions = get_random_question(user_level_questions , total_questions)


correct = 0
start_time = time.time()
    
wrong_answer = []

for question in random_questions:
    is_correct = ask_question(question)
    if is_correct:
        correct +=1
    if not is_correct:
        wrong_answer.append(question)    #saves the whole question to  dictionary so we know the question text, options, and correct answer
    
    print("------------------")

completed_time = time.time() - start_time


print("Summary")
print("Total Question:",total_questions)
print("Correct Answer", correct)
print("Score:",str(round( correct/total_questions *100,2)) + "%")
print("Total Time" ,round(completed_time,2), "seconds")

if wrong_answer:
    print("\n-----Questions You Got Wrong:------")
    for i , q in enumerate(wrong_answer, start= 1):
        print(f"\n{i}.Question: {q['question']}")
        print(f"Correct Answer: {q['answer']}")
    


