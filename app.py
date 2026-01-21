import streamlit as st
import random
import time

# --- 1. 페이지 설정 및 현대적인 스타일(CSS) 적용 ---
st.set_page_config(page_title="수학 로봇 탐험대", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    /* 메인 배경색 및 폰트 설정 */
    .main { background-color: #f0f2f6; }
    
    /* 카드 스타일 디자인 */
    .st-emotion-cache-1r6slb0 {
        border-radius: 20px;
        background: white;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* 버튼 현대화 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
    }
    
    /* 제목 스타일 */
    .main-title {
        color: #2C3E50;
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 세션 상태 관리 ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'enemy_score' not in st.session_state: st.session_state.enemy_score = 0
if 'ans_submitted' not in st.session_state: st.session_state.ans_submitted = False
if 'num1' not in st.session_state: st.session_state.num1 = 0
if 'num2' not in st.session_state: st.session_state.num2 = 0
if 'current_op' not in st.session_state: st.session_state.current_op = "+"

# --- 3. 문제 생성 로직 (0-19 범위) ---
def generate_problem(mode):
    if mode == "plus":
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, 9)
        st.session_state.current_op = "+"
    elif mode == "minus":
        st.session_state.num1 = random.randint(5, 19)
        st.session_state.num2 = random.randint(0, st.session_state.num1)
        st.session_state.current_op = "-"
    elif mode == "multi":
        pairs = [(2,2), (2,3), (2,4), (2,5), (3,2), (3,3), (4,2)]
        st.session_state.num1, st.session_state.num2 = random.choice(pairs)
        st.session_state.current_op = "x"
    elif mode == "race":
        op = random.choice(["+", "-"])
        if op == "+":
            st.session_state.num1 = random.randint(0, 10)
            st.session_state.num2 = random.randint(0, 9)
        else:
            st.session_state.num1 = random.randint(5, 19)
            st.session_state.num2 = random.randint(0, st.session_state.num1)
        st.session_state.current_op = op

# --- 4. 사이드바 디자인 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.title("탐험 메뉴")
    choice = st.radio("장소를 선택하세요", 
                      ["🏠 중앙 기지", "🤖 로봇 공장", "🐞 곤충 숲", "🏎️ 레이싱 로드", "🔋 충전소"])
    
    if "prev_choice" not in st.session_state or st.session_state.prev_choice != choice:
        st.session_state.score = 0
        st.session_state.enemy_score = 0
        st.session_state.ans_submitted = False
        st.session_state.prev_choice = choice
        mode_map = {"🤖 로봇 공장":"plus", "🐞 곤충 숲":"minus", "🏎️ 레이싱 로드":"race", "🔋 충전소":"multi"}
        if choice in mode_map: generate_problem(mode_map[choice])
        st.rerun()

# --- 5. 메인 화면 구성 ---

# 상단 배너 (현대적인 카드 형태)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #4A90E2, #50E3C2); padding: 25px; border-radius: 20px; color: white; margin-bottom: 25px;">
        <h1 style='margin:0;'>{choice}</h1>
        <p style='margin:0; opacity: 0.9;'>재미있는 숫자의 세계로 떠나요!</p>
    </div>
    """, unsafe_allow_html=True)

# 게임별 로직
if choice == "🏠 중앙 기지":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("### 👋 반가워요, 대장님!")
        st.write("오늘도 로봇들과 곤충들을 도와줄 준비가 되었나요? 왼쪽 메뉴를 눌러 모험을 시작하세요.")
    with col2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOojqaw8duG8/giphy.gif")

else:
    # 카드형 레이아웃 안에 문제 배치
    container = st.container()
    with container:
        col_q, col_v = st.columns([1, 1])
        
        with col_q:
            st.markdown("### 📝 오늘의 문제")
            st.info(f"## {st.session_state.num1} {st.session_state.current_op} {st.session_state.num2} = ?")
            
            if not st.session_state.ans_submitted:
                # 입력창 초기화 로직 (key에 score 포함)
                user_ans = st.number_input("정답을 입력하세요", min_value=0, max_value=19, value=None, key=f"input_{st.session_state.score}_{st.session_state.enemy_score}")
                if st.button("확인하기 ✔️"):
                    # 정답 체크
                    if st.session_state.current_op == "+": correct = st.session_state.num1 + st.session_state.num2
                    elif st.session_state.current_op == "-": correct = st.session_state.num1 - st.session_state.num2
                    elif st.session_state.current_op == "x": correct = st.session_state.num1 * st.session_state.num2
                    
                    if user_ans == correct:
                        st.session_state.ans_submitted = True
                        st.session_state.score += 1
                        st.rerun()
                    else:
                        st.error("앗, 다시 한번만 더 계산해볼까?")
            else:
                st.success("🎉 정답이야! 정말 대단해!")
                if st.button("다음 문제로 ➡️"):
                    st.session_state.ans_submitted = False
                    mode_map = {"🤖 로봇 공장":"plus", "🐞 곤충 숲":"minus", "🏎️ 레이싱 로드":"race", "🔋 충전소":"multi"}
                    generate_problem(mode_map[choice])
                    # 레이싱의 경우 적군도 이동
                    if choice == "🏎️ 레이싱 로드":
                        if random.random() > 0.5: st.session_state.enemy_score += 1
                    st.rerun()

        with col_v:
            st.markdown("### 📊 진행 상황")
            # 각 게임별 시각적 요소
            if choice == "🤖 로봇 공장":
                st.write(f"조립 완료: {st.session_state.score}/5")
                st.progress(st.session_state.score * 20)
                if st.session_state.score >= 5: 
                    st.balloons()
                    st.success("🤖 슈퍼 로봇 합체 완료!")
            
            elif choice == "🐞 곤충 숲":
                hp = 100 - (st.session_state.score * 20)
                st.write(f"곤충의 체력: {max(hp, 0)}%")
                st.progress(max(hp, 0) / 100)
                if hp <= 0: st.success("🐞 곤충 채집 완료! 도감에 추가!")
            
            elif choice == "🏎️ 레이싱 로드":
                st.write("🏃 나의 로봇")
                st.progress(st.session_state.score * 20)
                st.write("🦌 사슴벌레")
                st.progress(st.session_state.enemy_score * 20)
                if st.session_state.score >= 5: st.balloons(); st.success("🏆 승리!")
            
            elif choice == "🔋 충전소":
                battery = st.session_state.score * 20
                st.write(f"에너지: {battery}%")
                st.progress(battery / 100)
                if battery >= 100: st.snow(); st.success("⚡ 풀 충전 완료!")

# --- 6. 하단 배지 시스템 (아이디어 적용) ---
st.markdown("---")
st.markdown("### 🏅 획득한 배지")
badge_cols = st.columns(5)
with badge_cols[0]:
    if st.session_state.score >= 1: st.markdown("🌟 **초보 모험가**")
with badge_cols[1]:
    if choice == "🤖 로봇 공장" and st.session_state.score >= 3: st.markdown("🔧 **주니어 엔지니어**")
with badge_cols[2]:
    if choice == "🐞 곤충 숲" and st.session_state.score >= 3: st.markdown("🕸️ **곤충 박사**")
