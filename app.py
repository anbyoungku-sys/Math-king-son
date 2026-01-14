import streamlit as st
import random
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="수학 놀이터", page_icon="🎮", layout="wide")

# --- 세션 상태 초기화 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'enemy_score' not in st.session_state:
    st.session_state.enemy_score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
if 'num2' not in st.session_state:
    st.session_state.num2 = 0
if 'problem_type' not in st.session_state:
    st.session_state.problem_type = "+"

# --- [수정됨] 0~19 범위 문제 생성 함수 ---
def generate_problem(type="+"):
    if type == "+":
        # 합이 19 이하가 되도록 설정
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, 9)
    elif type == "-":
        # 결과가 0 이상이고 시작 숫자가 19 이하
        st.session_state.num1 = random.randint(5, 19)
        st.session_state.num2 = random.randint(0, st.session_state.num1)
    elif type == "*":
        # 구구단 중 결과가 19 이하인 것만 (2단~4단 위주)
        st.session_state.num1 = random.randint(1, 4)
        st.session_state.num2 = random.randint(1, 4)
    st.session_state.problem_type = type

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.header("🎮 놀이 선택")
    selected_game = st.radio(
        "어떤 놀이를 할까요?",
        ("🏠 홈 화면", "1. 🤖 로봇 조립 공장", "2. 🐞 곤충 채집 모험", "3. 🏎️ 로봇 vs 사슴벌레", "4. 🔋 로봇 에너지 충전")
    )
    
    if selected_game != st.session_state.get('current_view', '🏠 홈 화면'):
        st.session_state.score = 0
        st.session_state.enemy_score = 0
        generate_problem("+")
        st.session_state.current_view = selected_game
        st.rerun()

# 🏠 홈 화면
if selected_game == "🏠 홈 화면":
    st.title("수학 탐험대 본부 🚀")
    st.write("### 0부터 19까지! 숫자 대모험을 떠나볼까?")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOojqaw8duG8/giphy.gif", width=300)

# 1. 🤖 로봇 조립 공장 (덧셈)
elif selected_game == "1. 🤖 로봇 조립 공장":
    st.title("🤖 덧셈 로봇 조립")
    if st.session_state.score >= 4:
        st.success("🤖 슈퍼 로봇 완성!!")
        st.balloons()
        if st.button("다시 만들기"): 
            st.session_state.score = 0
            st.rerun()
    else:
        st.subheader(f"문제: {st.session_state.num1} + {st.session_state.num2} = ?")
        ans = st.number_input("정답", min_value=0, max_value=19, key="g1")
        if st.button("조립!"):
            if ans == st.session_state.num1 + st.session_state.num2:
                st.session_state.score += 1
                generate_problem("+")
                st.rerun()
            else: st.error("다시 해보자!")

# 2. 🐞 곤충 채집 모험 (뺄셈)
elif selected_game == "2. 🐞 곤충 채집 모험":
    st.title("🐞 뺄셈 곤충 채집")
    if st.session_state.score >= 4:
        st.success("🐞 곤충 채집 성공!")
        st.balloons()
        if st.button("다음 곤충"): 
            st.session_state.score = 0
            st.rerun()
    else:
        if st.session_state.problem_type != "-": generate_problem("-")
        st.subheader(f"문제: {st.session_state.num1} - {st.session_state.num2} = ?")
        ans = st.number_input("정답", min_value=0, max_value=19, key="g2")
        if st.button("포획!"):
            if ans == st.session_state.num1 - st.session_state.num2:
                st.session_state.score += 1
                generate_problem("-")
                st.rerun()
            else: st.error("곤충이 도망갔어!")

# 3. 🏎️ 로봇 vs 사슴벌레 (혼합)
elif selected_game == "3. 🏎️ 로봇 vs 사슴벌레":
    st.title("🏎️ 레이싱 대결")
    col1, col2 = st.columns(2)
    col1.metric("내 로봇", f"{st.session_state.score}점")
    col2.metric("사슴벌레", f"{st.session_state.enemy_score}점")
    
    if st.session_state.score >= 5: st.success("승리!"); st.balloons()
    elif st.session_state.enemy_score >= 5: st.error("패배..")
    
    if st.session_state.score < 5 and st.session_state.enemy_score < 5:
        st.subheader(f"문제: {st.session_state.num1} {st.session_state.problem_type} {st.session_state.num2} = ?")
        ans = st.number_input("정답", min_value=0, max_value=19, key="g3")
        if st.button("가속!"):
            correct = st.session_state.num1 + st.session_state.num2 if st.session_state.problem_type == "+" else st.session_state.num1 - st.session_state.num2
            if ans == correct:
                st.session_state.score += 1
            else:
                st.session_state.enemy_score += 1
            generate_problem(random.choice(["+", "-"]))
            st.rerun()

# 4. 🔋 로봇 에너지 충전 (쉬운 곱셈)
elif selected_game == "4. 🔋 로봇 에너지 충전":
    st.title("🔋 에너지 충전 (구구단)")
    battery = st.session_state.score * 25
    st.progress(min(battery, 100))
    
    if battery >= 100:
        st.success("⚡ 충전 완료!")
        if st.button("다시 하기"): st.session_state.score = 0; st.rerun()
    else:
        if st.session_state.problem_type != "*": generate_problem("*")
        st.subheader(f"문제: {st.session_state.num1} x {st.session_state.num2} = ?")
        ans = st.number_input("정답", min_value=0, max_value=19, key="g4")
        if st.button("충전!"):
            if ans == st.session_state.num1 * st.session_state.num2:
                st.session_state.score += 1
                generate_problem("*")
                st.rerun()
