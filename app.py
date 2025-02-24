import streamlit as st
import re
import json

def if_general_conversation(s):  #request 뒤에만 갖고올 수 있도록 세팅
  pattern = "(?<=\n\*REQUEST\* : ).*"
  new_s = re.search(pattern,s)
  if new_s == None:
    return s
  else:
    return new_s.group()


st.title("하이헬로우")
#turn_num = st.text_area("턴 수를 입력하세요:")
turn_num = st.radio(label='▶️ 턴 수 선택',	options=['1','2','3','4','5','6 이상'], key='radiobox',horizontal=True)
if turn_num == '6 이상':
  turn_num = st.text_area("턴 수를 입력하세요:")
raw_txt = st.text_area("log를 입력하세요:")

if st.button("해줘."):
  ##코드시작
  dict_obj = json.loads(raw_txt) #json 형태 딕셔너리로 변환
  text = dict_obj[0] #리스트 형태로 들어있어서 따로 지정

  ###history (첫발화부터~)
  history = text['bookkeeping_data']['run_data']['history']
  turn = 0
  turn_num = int(turn_num)
  for i in range(0,turn_num+1,3):
  ##n턴 반복
  #user
    user_txt = history[i]["role"] , history[i]["content"]
    # planner
    planner_txt = history[i+1]["name"] , history[i+1]["tool_calls"][0]["function"]['name'] , history[i+1]["tool_calls"][0]["function"]['arguments']['text_input']
    # function_agent
    executor_txt = history[i+2]["name"] , history[i+2]["content"]

    turn += 1 #출력을 위한 턴 수 업데이트
    st.write(f"## {turn}**번째 턴** ")
    st.write("### 📝 User")
    st.write(f"**Content:** {user_txt[1]}")
    st.write("### 🧠 Planner")
    st.write(f"**Agent Name:** {planner_txt[1]}")
    st.write(f"**Content:** {if_general_conversation(planner_txt[2])}")
    st.write("### ⚙️ Executor")
    st.write(f"**Agent Name:** {executor_txt[0]}")
    st.write(f"**Content:** {if_general_conversation(executor_txt[1])}")

    # print("*"*100)
    # print(turn,"번째 턴")
    # print(">>>user:\n content:",user_txt[1])
    # print(">>>planner:\n agent_name:",planner_txt[1],"\n content:",if_general_conversation(planner_txt[2]))
    # print(">>>executor:\n agent_name:",executor_txt[0],"\n content:",if_general_conversation(executor_txt[1]))


  ###planner_message (마지막 발화)
  planner_message = text['bookkeeping_data']["run_data"]["planner_message"]["2"]
  #user
  first_user_txt = text['bookkeeping_data']['input']['task']
  # planner
  first_planner_txt = planner_message[0]["tool_calls"][0]["function"]['name'] , planner_message[0]["tool_calls"][0]["function"]['arguments']['text_input']  #planner_message[0]["name"] 얘 값: planner
  # function_agent
  first_executor_txt = planner_message[1]["name"] , planner_message[1]["content"]

  st.write("## **마지막 턴**")
  st.write("### 📝 User")
  st.write(f"**Content:** {first_user_txt}")
  st.write("### 🧠 Planner")
  st.write(f"**Agent Name:** {first_planner_txt[0]}")
  st.write(f"**Content:** {if_general_conversation(first_planner_txt[1])}")
  st.write("### ⚙️ Executor")
  st.write(f"**Agent Name:** {first_executor_txt[0]}")
  st.write(f"**Content:** {if_general_conversation(first_executor_txt[1])}")
  # print("*"*100)
  # print("마지막 턴")
  # print(">>>user:",first_user_txt)
  # print(">>>planner:\n agent_name:",first_planner_txt[0],"\n content:",if_general_conversation(first_planner_txt[1]))
  # print(">>>executor:\n agent_name:",first_executor_txt[0],"\n content:",if_general_conversation(first_executor_txt[1]))





