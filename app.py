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

st.title("테스트 앱")
st.write("기본 Streamlit 앱입니다.")
st.image("https://example.com/image.jpg") 