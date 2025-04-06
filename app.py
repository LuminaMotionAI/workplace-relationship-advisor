import subprocess
import sys
import warnings
import numpy as np
import pandas as pd

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

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

st.title("테스트 앱")
st.write("간단한 테스트입니다.")

if st.button("테스트 버튼"):
    st.success("앱이 정상적으로 작동합니다!") 