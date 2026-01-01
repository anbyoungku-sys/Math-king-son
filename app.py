import streamlit as st
import random

# --- 1. 화면 설정 (공룡 테마) ---
st.set_page_config(page_title="🦖씩씩한 7살 수학 대장", page_icon="🦖")

# --- 2. 변수 초기화 (점수, 현재 문제 등 저장) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "더하기 (쉬움)" # 기본값
if 'num1' not in st.session_state:
    st.session_state.num1 = 1
if 'num2' not in st.session_state:
    st.session_state.num2 = 1
if 'op_symbol' not in st.session_state:
    st.session_state.op_symbol = '+'
if 'real_answer' not in st.session_state:
    st.session_state.real_answer = 2
if 'problem_solved' not in st.session_state:
    st.session_state.problem_solved = False

# --- 3. 문제 생성 함수 (핵심 로직) ---
def generate_problem(mode):
    st.session_state.current_mode = mode
    st.session_state.problem_solved = False # 문제 풀기 상태로 변경

    # 1) 더하기
    if mode == "더하기 (쉬움)":
        st.session_state.num1 = random.randint(1, 9)
        st.session_state.num2 = random.randint(1, 9)
        st.session_state.op_symbol = '+'
        st.session_state.real_answer = st.session_state.num1 + st.session_state.num2

    elif mode == "더하기 (도전)":
        st.session_state.num1 = random.randint(10, 50)
        st.session_state.num2 = random.randint(10, 50)
        st.session_state.op_symbol = '+'
        st.session_state.real_answer = st.session_state.num1 + st.session_state.num2

    # 2) 빼기 (음수 안 나오게 처리)
    elif mode == "빼기 (쉬움)":
        n1 = random.randint(2, 9)
        n2 = random.randint(1, n1) # n1보다 작거나 같은 수
        st.session_state.num1 = n1
        st.session_state.num2 = n2
        st.session_state.op_symbol = '-'
        st.session_state.real_answer = n1 - n2

    elif mode == "빼기 (도전)":
        n1 = random.randint(20, 99)
        n2 = random.randint(10, n1)
        st.session_state.num1 = n1
        st.session_state.num2 = n2
        st.session_state.op_symbol = '-'
        st.session_state.real_answer = n1 - n2

    # 3) 곱하기 (구구단)
    elif mode == "곱하기 (쉬움)":
        st.session_state.num1 = random.randint(2, 5) # 2~5단
        st.session_state.num2 = random.randint(1, 9)
        st.session_state.op_symbol = 'x'
        st.session_state.real_answer = st.session_state.num1 * st.session_state.num2

    elif mode == "곱하기 (도전)":
        st.session_state.num1 = random.randint(6, 9) # 6~9단
        st.session_state.num2 = random.randint(1, 9)
        st.session_state.op_symbol = 'x'
        st.session_state.real_answer = st.session_state.num1 * st.session_state.num2

    # 4) 나누기 (나머지 없이 딱 떨어지게 만들기)
    elif mode == "나누기 (쉬움)":
        # 정답(몫)을 먼저 정하고 역산
        answer = random.randint(2, 5)
        divisor = random.randint(2, 5)
        dividend = answer * divisor # 나누어지는 수

        st.session_state.num1 = dividend
        st.session_state.num2 = divisor
        st.session_state.op_symbol = '÷'
        st.session_state.real_answer = answer

    elif mode == "나누기 (도전)":
        answer = random.randint(2, 9)
        divisor = random.randint(2, 9)
        dividend = answer * divisor

        st.session_state.num1 = dividend
        st.session_state.num2 = divisor
        st.session_state.op_symbol = '÷'
        st.session_state.real_answer = answer


# --- 4. UI 구성 ---
st.title("🦖 씩씩한 7살 수학 대장")
st.markdown(f"### 현재 도전 중: :blue[{st.session_state.current_mode}]")
st.write("문제를 고르면 새로운 문제가 나와요!")

# --- 2행 4열 버튼 배치 ---
# 첫 번째 줄: 더하기 / 빼기
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➕ 더하기\n(쉬움)", use_container_width=True):
        generate_problem("더하기 (쉬움)")
with col2:
    if st.button("🔥 더하기\n(도전)", use_container_width=True):
        generate_problem("더하기 (도전)")
with col3:
    if st.button("➖ 빼기\n(쉬움)", use_container_width=True):
        generate_problem("빼기 (쉬움)")
with col4:
    if st.button("🔥 빼기\n(도전)", use_container_width=True):
        generate_problem("빼기 (도전)")

# 두 번째 줄: 곱하기 / 나누기
col5, col6, col7, col8 = st.columns(4)
with col5:
    if st.button("✖️ 곱하기\n(쉬움)", use_container_width=True):
        generate_problem("곱하기 (쉬움)")
with col6:
    if st.button("🔥 곱하기\n(도전)", use_container_width=True):
        generate_problem("곱하기 (도전)")
with col7:
    if st.button("➗ 나누기\n(쉬움)", use_container_width=True):
        generate_problem("나누기 (쉬움)")
with col8:
    if st.button("🔥 나누기\n(도전)", use_container_width=True):
        generate_problem("나누기 (도전)")

st.divider()

# --- 5. 문제 표시 화면 ---
# 숫자를 아주 크게 보여주기 위해 header 사용
c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1.5, 1, 1.5])
with c1:
    st.header(st.session_state.num1)
with c2:
    st.header(st.session_state.op_symbol)
with c3:
    st.header(st.session_state.num2)
with c4:
    st.header("=")
with c5:
    st.header("❓")

st.write("") # 여백

# --- 6. 정답 입력 및 확인 ---
# 폼(Form)을 사용하면 엔터키로 제출이 가능해서 편합니다.
with st.form("answer_form"):
    user_input = st.number_input("정답은 무엇일까요?", min_value=0, step=1)
    submit_btn = st.form_submit_button("🚀 정답 확인!")

    if submit_btn:
        if user_input == st.session_state.real_answer:
            if not st.session_state.problem_solved: # 중복 점수 방지
                st.balloons()
                st.success("딩동댕! 정답입니다! 참 잘했어요! 🎉")
                st.session_state.score += 10
                st.session_state.problem_solved = True # 문제 해결됨 표시
            else:
                st.info("이미 맞춘 문제입니다. 위에서 새로운 문제를 골라보세요!")
        else:
            st.error("땡! 다시 한번 생각해볼까요? 할 수 있어요! 🔥")

# --- 7. 점수판 ---
st.divider()
st.metric(label="🏆 내가 모은 공룡 알 점수", value=f"{st.session_state.score} 점")

# 칭찬 메시지 로직
if st.session_state.score > 0 and st.session_state.score % 50 == 0:
    st.info("와우! 50점 달성! 오늘은 치킨 먹는 날? 🍗")