import streamlit as st
import random
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="수학 놀이터", page_icon="🎮", layout="wide")

# --- 세션 상태 초기화 (점수, 문제 등을 저장하기 위함) ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'enemy_score' not in st.session_state:
    st.session_state.enemy_score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
if 'num2' not in st.session_state:
    st.session_state.num2 = 0
if 'problem_type' not in st.session_state:
    st.session_state.problem_type = "+" # +, -, *

# --- 문제 생성 함수 ---
def generate_problem(type="+"):
    if type == "+": # 십의 자리 + 일의 자리
        st.session_state.num1 = random.randint(10, 50)
        st.session_state.num2 = random.randint(1, 9)
    elif type == "-": # 십의 자리 - 일의 자리 (결과가 양수)
        st.session_state.num1 = random.randint(20, 90)
        st.session_state.num2 = random.randint(1, 9)
    elif type == "*": # 구구단 (일의 자리)
        st.session_state.num1 = random.randint(2, 9)
        st.session_state.num2 = random.randint(1, 9)
    st.session_state.problem_type = type

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.header("🎮 놀이 선택")
    selected_game = st.radio(
        "어떤 놀이를 할까요?",
        ("🏠 홈 화면", "1. 🤖 로봇 조립 공장", "2. 🐞 곤충 채집 모험", "3. 🏎️ 로봇 vs 사슴벌레", "4. 🔋 로봇 에너지 충전")
    )
    
    # 게임을 바꿀 때 점수 초기화 로직
    if selected_game != st.session_state.get('current_view', '🏠 홈 화면'):
        st.session_state.score = 0
        st.session_state.enemy_score = 0
        generate_problem("+")
        st.session_state.current_view = selected_game
        st.rerun()

# ==========================================
# 🏠 홈 화면
# ==========================================
if selected_game == "🏠 홈 화면":
    st.title("수학 탐험대 본부 🚀")
    st.write("### 안녕! 나는 너의 수학 파트너야.")
    st.write("왼쪽 메뉴에서 하고 싶은 놀이를 골라봐!")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eXF6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdOojqaw8duG8/giphy.gif", caption="준비됐니?", width=300)

# ==========================================
# 1. 🤖 로봇 조립 공장 (덧셈)
# ==========================================
elif selected_game == "1. 🤖 로봇 조립 공장":
    st.title("🤖 나만의 슈퍼 로봇 만들기")
    st.markdown("**문제를 맞춰서 로봇 부품을 모으자! (총 4단계)**")

    # 로봇 상태 시각화
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="현재 부품 수", value=f"{st.session_state.score} / 4")
    
    with col2:
        if st.session_state.score == 0:
            st.info("시작하려면 문제를 풀어봐!")
        elif st.session_state.score == 1:
            st.warning("머리 장착 완료! 🤖")
        elif st.session_state.score == 2:
            st.warning("몸통 연결 완료! 🤖👕")
        elif st.session_state.score == 3:
            st.warning("다리 연결 완료! 🤖👕👖")
        elif st.session_state.score >= 4:
            st.success("슈퍼 로봇 완성! 출동 준비! 🤖👕👖⚔️")
            st.balloons()
            if st.button("새 로봇 만들기"):
                st.session_state.score = 0
                st.rerun()

    if st.session_state.score < 4:
        st.divider()
        st.subheader(f"문제: {st.session_state.num1} + {st.session_state.num2} = ?")
        
        with st.form("game1_form"):
            answer = st.number_input("정답 입력", min_value=0, step=1)
            submitted = st.form_submit_button("부품 조립하기")
            
            if submitted:
                if answer == st.session_state.num1 + st.session_state.num2:
                    st.success("정답! 띠링~ 부품 획득!")
                    st.session_state.score += 1
                    generate_problem("+")
                    time.sleep(1) # 잠시 대기 후
                    st.rerun()    # 화면 갱신
                else:
                    st.error("앗! 나사가 헐거워요. 다시 계산해볼까?")

# ==========================================
# 2. 🐞 곤충 채집 모험 (뺄셈)
# ==========================================
elif selected_game == "2. 🐞 곤충 채집 모험":
    st.title("🐞 희귀 곤충을 잡아라!")
    st.markdown("**뺄셈 공격으로 곤충의 체력을 0으로 만들자!**")
    
    # 곤충 체력 설정 (기본 100, 한 문제당 25 데미지)
    max_hp = 100
    current_hp = max_hp - (st.session_state.score * 25)
    
    if current_hp < 0: current_hp = 0

    st.write(f"### 야생의 장수풍뎅이 체력: {current_hp}")
    st.progress(current_hp / max_hp)

    if current_hp == 0:
        st.success("🎉 채집 성공! 장수풍뎅이를 잡았다!")
        st.image("https://emojigraph.org/media/apple/beetle_1fab2.png", width=100)
        st.balloons()
        if st.button("다른 곤충 찾으러 가기"):
            st.session_state.score = 0
            st.rerun()
    else:
        st.divider()
        # 문제 타입이 -가 아니면 변경
        if st.session_state.problem_type != "-":
            generate_problem("-")
            
        st.subheader(f"공격 준비: {st.session_state.num1} - {st.session_state.num2} = ?")
        
        with st.form("game2_form"):
            answer = st.number_input("정답 입력", min_value=0, step=1)
            submitted = st.form_submit_button("잠자리채 휘두르기! 🕸️")
            
            if submitted:
                if answer == st.session_state.num1 - st.session_state.num2:
                    st.success("공격 성공! 곤충이 약해졌어!")
                    st.session_state.score += 1
                    generate_problem("-")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("빗나갔다! 곤충이 너무 빨라!")

# ==========================================
# 3. 🏎️ 로봇 vs 사슴벌레 (혼합 연산 - 달리기)
# ==========================================
elif selected_game == "3. 🏎️ 로봇 vs 사슴벌레":
    st.title("🏎️ 숲속 레이싱 대회")
    st.markdown("**누가 먼저 5점에 도착할까?**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🤖 **나의 로봇**")
        st.progress(min(st.session_state.score * 20, 100))
    with col2:
        st.write("🦌 **라이벌 사슴벌레**")
        st.progress(min(st.session_state.enemy_score * 20, 100))

    # 승리 조건 체크
    if st.session_state.score >= 5:
        st.success("🏆 우승!! 로봇이 더 빨랐어!")
        st.balloons()
        if st.button("재경기 하기"):
            st.session_state.score = 0
            st.session_state.enemy_score = 0
            st.rerun()
    elif st.session_state.enemy_score >= 5:
        st.error("아쉽다.. 사슴벌레가 이겼어 ㅠㅠ")
        if st.button("다시 도전!"):
            st.session_state.score = 0
            st.session_state.enemy_score = 0
            st.rerun()
    else:
        st.divider()
        # 랜덤 연산
        if st.session_state.problem_type not in ["+", "-"]:
             generate_problem("+")

        op_symbol = st.session_state.problem_type
        st.subheader(f"부스터 발동: {st.session_state.num1} {op_symbol} {st.session_state.num2} = ?")

        with st.form("game3_form"):
            answer = st.number_input("정답 입력", min_value=0, step=1)
            submitted = st.form_submit_button("가속!")
            
            if submitted:
                real_answer = 0
                if op_symbol == "+": real_answer = st.session_state.num1 + st.session_state.num2
                else: real_answer = st.session_state.num1 - st.session_state.num2
                
                if answer == real_answer:
                    st.success("부스터 작동! 슈웅~")
                    st.session_state.score += 1
                    # 사슴벌레도 랜덤하게 이동 (50% 확률)
                    if random.choice([True, False]):
                        st.session_state.enemy_score += 1
                        st.warning("사슴벌레도 쫓아오고 있어!")
                else:
                    st.error("미끄러졌다! 사슴벌레가 앞서갑니다!")
                    st.session_state.enemy_score += 1
                
                # 다음 문제 랜덤 생성
                generate_problem(random.choice(["+", "-"]))
                time.sleep(1)
                st.rerun()

# ==========================================
# 4. 🔋 로봇 에너지 충전 (곱셈)
# ==========================================
elif selected_game == "4. 🔋 로봇 에너지 충전":
    st.title("🔋 배고픈 로봇 밥 주기")
    st.markdown("**구구단을 외워서 로봇 배터리를 100%로 만들자!**")
    
    # 배터리 (문제당 20% 충전)
    battery = st.session_state.score * 20
    if battery > 100: battery = 100
    
    st.metric("현재 에너지", f"{battery}%")
    
    # 배터리 상태 이모지
    if battery < 40:
        st.write("로봇 상태: 😵 (배고파요..)")
    elif battery < 80:
        st.write("로봇 상태: 🙂 (조금만 더!)")
    else:
        st.write("로봇 상태: ⚡🤖⚡ (파워 풀!!)")

    if battery >= 100:
        st.success("에너지 충전 완료! 로봇이 춤을 춥니다!")
        st.video("https://www.youtube.com/watch?v=317jz-PUxBg") # 로봇 춤 영상 예시
        if st.button("다시 충전하기"):
            st.session_state.score = 0
            st.rerun()
    else:
        st.divider()
        if st.session_state.problem_type != "*":
            generate_problem("*")
            
        st.subheader(f"에너지 캡슐: {st.session_state.num1} x {st.session_state.num2} = ?")
        
        with st.form("game4_form"):
            answer = st.number_input("정답 입력", min_value=0, step=1)
            submitted = st.form_submit_button("에너지 주입!")
            
            if submitted:
                if answer == st.session_state.num1 * st.session_state.num2:
                    st.success("냠냠! 맛있는 숫자다!")
                    st.session_state.score += 1
                    generate_problem("*")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("퉤! 맛없는 오답이야!")
