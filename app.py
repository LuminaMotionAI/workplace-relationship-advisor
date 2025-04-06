import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 필요한 패키지 설치
try:
    import pandas as pd
except ImportError:
    install("pandas")
    import pandas as pd

try:
    from PIL import Image
except ImportError:
    install("pillow==8.4.0")
    from PIL import Image

import streamlit as st

st.title("직장 인간관계 조언 봇")
st.write("데일 카네기의 『인간관계론』을 바탕으로 직장 생활의 문제를 해결하는 데 도움을 드립니다.")

if st.button("테스트 버튼"):
    st.success("앱이 정상적으로 작동합니다!") 