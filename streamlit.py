import streamlit as st
import json
import time
import random

#------Title of page------
st.set_page_config(page_title ="Smart Python Quiz", layout="centered")

st.title("Smart Python Assessment Platform")

#------load the question--------
@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
         return json.load(f)["question"]
        
questions = load_questions() 

#-------SideBar---
st.sidebar.header("Quiz Settings")

difficulty = st.sidebar.selectbox(
    "Select Difficulty level",
    ["easy", "medium","hard"]
)

filtered_questions = [q for q in questions if q["difficulty"] == difficulty]

num_questions = st.sidebar.number_input(
    "Maximum number of Questions",
    min_value =1,
    max_value = len(filtered_questions),
    value = min(5, len(filtered_questions))
)

# -----Start Quiz Button------
if st.sidebar.button("Start Quiz"):
    st.session_state.quiz = random.sample(filtered_questions, num_questions)
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.finished = False

#------Quiz Logic------
if "quiz" in st.session_state and not st.session_state.finished:
   quiz = st.session_state.quiz
   index = st.session_state.q_index

   if index < len(quiz):
       
       q = quiz[index]

       #progress
       progress = (index +1)/len(quiz)
       st.progress(progress)
       st.write(f"Question {index +1} of {len(quiz)}")
       st.write(q["question"])

       selected = st.radio(
           "Choose an option: ",
           q["options"],
           key=index
       )

       if st.button("Submit Answer"):
           if selected == q["answer"]:
               st.success("Correct")
               st.session_state.score += 1   # ✅ FIXED: score was not increasing
           else:
               st.error("Wrong")

           st.session_state.q_index += 1
           st.rerun()

   else:
       st.session_state.finished = True   # ✅ FIXED: Properly mark quiz as finished




#------Quiz Results------
if "finished" in st.session_state and st.session_state.finished:
    
    total = round(time.time() - st.session_state.start_time,2)
    max_score  = len(st.session_state.quiz)

    st.success("Quiz Completed!")

    st.metric("Score",st.session_state.score)
    st.metric("Max Score", max_score)
    st.metric("Accuracy", f"{round(st.session_state.score / max_score *100,2)}%")
    st.metric("Time Taken", f"{total} seconds")
    
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
