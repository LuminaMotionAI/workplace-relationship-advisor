import sys
import streamlit as st

st.write(f"Python 버전: {sys.version}")
st.write(f"Streamlit 버전: {st.__version__}")

try:
    import numpy as np
    st.write(f"NumPy 버전: {np.__version__}")
except ImportError:
    st.warning("NumPy를 가져올 수 없습니다.")

try:
    import pandas as pd
    st.write(f"Pandas 버전: {pd.__version__}")
except ImportError:
    st.warning("Pandas를 가져올 수 없습니다.")

st.title("직장 인간관계 조언 봇")
st.markdown("데일 카네기의 『인간관계론』을 바탕으로 한 조언")

option = st.selectbox(
    "어떤 유형의 문제가 있나요?",
    ["비판과 불만", "갈등 해결", "인정과 칭찬", "영향력 행사", "스트레스 관리"]
)

if option:
    st.subheader(f"선택: {option}")
    
    if option == "비판과 불만":
        st.write("- 직접적인 비판을 피하고 간접적으로 개선점을 제안하세요.")
        st.write("- 상대방의 입장에서 생각해보고 그들의 관점을 이해하려고 노력하세요.")
    elif option == "갈등 해결":
        st.write("- 논쟁에서 이기려 하지 말고, 해결책을 찾는 데 집중하세요.")
        st.write("- 상대방의 의견을 존중하고 경청하세요.")
    elif option == "인정과 칭찬":
        st.write("- 진심 어린 감사와 인정을 표현하세요.")
        st.write("- 작은 성취도 구체적으로 칭찬하세요.")
    elif option == "영향력 행사":
        st.write("- 명령하기보다 질문하여 상대방이 스스로 답을 찾게 하세요.")
        st.write("- 상대방의 이익을 중심으로 대화하세요.")
    else:
        st.write("- 오늘 할 수 있는 일에 집중하고, 나머지는 내려놓으세요.")
        st.write("- 일의 우선순위를 정하고 한 번에 하나씩 처리하세요.")

if st.button("다른 조언 받기"):
    st.success("버튼이 작동합니다!") 