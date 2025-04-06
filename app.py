import streamlit as st
import pandas as pd
import random
import re
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="직장 인간관계 조언 봇",
    page_icon="💼",
    layout="wide"
)

# CSS 스타일 수정 - 새로운 그라데이션 색상으로 업데이트
st.markdown("""
<style>
    /* 반응형 설정 */
    .main > div {
        padding-top: 1rem;
    }
    
    /* 모던한 버튼 스타일 - 색상 변경 (첨부된 색상표 기반) */
    .stButton button {
        background-color: #43B0B5 !important;
        color: white !important;
    }
    
    .stButton button:hover {
        background-color: #219FC3 !important;
    }
    
    .stButton button:active {
        background-color: #448BC6 !important;
    }
    
    /* 카드 스타일 */
    .advice-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #43B0B5; /* Default 색상 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 모바일 최적화 */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        .stButton button {
            font-size: 1rem !important;
            padding: 0.6rem 1rem !important;
        }
    }
    
    /* 데스크톱/노트북 최적화 */
    @media (min-width: 992px) {
        .stButton button {
            font-size: 1.4rem !important;
            padding: 1rem 2rem !important;
        }
    }
    
    /* 카테고리 버튼 스타일 */
    .category-btn {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .category-btn:hover {
        background-color: #e9ecef;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .category-btn-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    
    .category-btn-text {
        font-weight: 500;
    }
    
    /* 도서 카드 스타일 수정 */
    .book-card {
        flex: 1; 
        min-width: 250px; 
        background-color: white; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        padding: 20px;
        margin: 10px;
    }
    
    .book-tag {
        background-color: #f1f8ff; 
        border-radius: 4px; 
        padding: 8px; 
        color: #7371B6; /* 그라데이션의 보라색 */
        font-size: 14px; 
        margin-top: 10px;
    }

    /* 인포 메시지 색상 변경 */
    .stAlert {
        background-color: #43B0B5 !important; /* Default 색상 */
        color: white !important;
    }
    
    /* 링크 색상 수정 */
    a {
        color: #448BC6 !important; /* Pressed 색상 */
    }
    a:hover {
        color: #7371B6 !important; /* 보라색 */
    }
    
    /* 사이드바 선택 색상 */
    .st-eb {
        background-color: #43B0B5 !important; /* Default 색상 */
    }
    
    /* 프로그래스 바 색상 */
    .stProgress > div > div {
        background-color: #448BC6 !important; /* Pressed 색상 */
    }
    
    /* 라디오 버튼 색상 */
    .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        background-color: #43B0B5 !important; /* Default 색상 */
    }
</style>
""", unsafe_allow_html=True)

# 헤더 및 소개 부분
st.title("직장 인간관계 조언 봇")
st.markdown("데일 카네기의 『인간관계론』을 바탕으로 직장 생활의 문제를 해결하는 데 도움을 드립니다.")

# 키워드 사전 (단어 입력으로도 조언을 제공하기 위한 설정)
keywords = {
    "비판과 불만": ["비판", "불만", "짜증", "화", "불평", "부정적", "공격", "지적", "비난", "싫어", "미워", "화나", "불쾌"],
    "갈등 해결": ["갈등", "다툼", "충돌", "의견차이", "대립", "논쟁", "다른생각", "불화", "싸움", "해결", "화해", "중재"],
    "인정과 칭찬": ["인정", "칭찬", "격려", "동기부여", "인센티브", "보상", "감사", "존중", "인식", "가치", "성취"],
    "영향력 행사": ["영향력", "설득", "리더십", "관리", "지도", "이끌다", "영향", "주도", "동기부여", "지시", "안내"],
    "스트레스 관리": ["스트레스", "불안", "걱정", "압박", "부담", "긴장", "번아웃", "과로", "피로", "우울", "쉼", "휴식"]
}

# 데일 카네기 원칙들
carnegie_principles = {
    "비판과 불만": [
        "직접적인 비판을 피하고 간접적으로 개선점을 제안하세요.",
        "상대방의 입장에서 생각해보고 그들의 관점을 이해하려고 노력하세요.",
        "자신의 실수를 먼저 인정하면 상대방도 방어적인 태도를 줄일 수 있습니다.",
        "질문 형식으로 제안하면 명령하는 것보다 수용성이 높아집니다.",
        "상대방의 자존심을 지켜주며 대화하세요.",
        "어떤 상황에서도 부정적인 감정을 직접적으로 표현하지 마세요.",
        "상대방을 변화시키려 하기 전에 자신의 태도부터 점검하세요."
    ],
    "갈등 해결": [
        "논쟁에서 이기려 하지 말고, 해결책을 찾는 데 집중하세요.",
        "상대방의 의견을 존중하고 경청하세요.",
        "공통점을 먼저 찾고, 그 다음에 차이점을 논의하세요.",
        "감정이 격해졌을 때는 즉각 반응하지 말고 시간을 두고 생각하세요.",
        "상대방이 동의할 수 있는 부분부터 시작하세요.",
        "원만한 해결책이 무엇인지 함께 고민하는 자세를 보여주세요.",
        "잘못이 있다면 솔직하게 인정하고 사과하는 용기를 가지세요."
    ],
    "인정과 칭찬": [
        "진심 어린 감사와 인정을 표현하세요.",
        "작은 성취도 구체적으로 칭찬하세요.",
        "사람들은 인정받고 싶어 합니다. 그들의 강점을 알아보세요.",
        "칭찬은 구체적이고 즉각적일 때 가장 효과적입니다.",
        "상대방이 가치 있게 느끼도록 만드세요.",
        "칭찬은 비판보다 더 강력한 변화의 도구입니다.",
        "타인의 장점을 찾아 진심으로 감사를 표현하는 습관을 들이세요."
    ],
    "영향력 행사": [
        "명령하기보다 질문하여 상대방이 스스로 답을 찾게 하세요.",
        "상대방의 이익을 중심으로 대화하세요.",
        "사람들의 이름을 기억하고 불러주세요. 그것은 가장 달콤한 소리입니다.",
        "진정한 관심과 미소로 상대방을 대하세요.",
        "상대방의 의견을 존중하고 중요하게 생각한다는 것을 보여주세요.",
        "지시하기보다 제안하는 형태로 의견을 전달하세요.",
        "상대방이 원하는 것이 무엇인지 먼저 이해하려고 노력하세요."
    ],
    "스트레스 관리": [
        "문제를 세 가지 질문으로 분석하세요: 최악의 상황은? 가능성은? 어떻게 대처할 수 있는가?",
        "오늘 할 수 있는 일에 집중하고, 나머지는 내려놓으세요.",
        "일의 우선순위를 정하고 한 번에 하나씩 처리하세요.",
        "걱정에 시간을 할애하기보다 행동에 시간을 투자하세요.",
        "과거에 얽매이지 말고 현재와 미래에 집중하세요.",
        "작은 성취를 통해 자신감을 키우고 스트레스를 줄이세요.",
        "규칙적인 휴식과 운동으로 정신적 균형을 유지하세요."
    ]
}

# 단어 입력을 분석하여 카테고리 식별하는 함수
def identify_category(text):
    if not text:
        return None
    
    # 입력된 텍스트에서 키워드 검색
    text = text.lower()
    scores = {category: 0 for category in keywords}
    
    for category, words in keywords.items():
        for word in words:
            if word.lower() in text:
                scores[category] += 1
    
    # 가장 높은 점수의 카테고리 반환 (동점일 경우 첫 번째 항목)
    max_score = max(scores.values())
    if max_score == 0:  # 일치하는 키워드가 없는 경우
        return random.choice(list(keywords.keys()))  # 랜덤 카테고리 반환
    
    for category, score in scores.items():
        if score == max_score:
            return category
    
    return None

# 카테고리별 아이콘 매핑
category_icons = {
    "비판과 불만": "🛡️",
    "갈등 해결": "🤝",
    "인정과 칭찬": "⭐",
    "영향력 행사": "🔮",
    "스트레스 관리": "🧘"
}

# 사이드바 카테고리 선택
with st.sidebar:
    st.header("카테고리 선택")
    category = st.radio(
        "어떤 유형의 문제가 있으신가요?",
        list(carnegie_principles.keys())
    )
    
    st.markdown("---")
    st.markdown("### 데일 카네기 인간관계론")
    st.markdown("『인간관계론』은 1936년 출판된 이후 전 세계적으로 3천만 부 이상 판매된 자기계발서입니다. 사람들과의 관계를 개선하고 영향력을 행사하는 방법을 제시합니다.")
    st.markdown("---")
    
    # 간단한 도움말 추가
    st.markdown("### 사용 방법")
    st.markdown("1. 문제 상황을 자세히 설명하거나")
    st.markdown("2. 간단한 키워드만 입력해도 됩니다")
    st.markdown("3. '조언 받기' 버튼을 클릭하세요")

# 메인 콘텐츠 영역
st.header("회사 생활 문제 상담")

problem_description = st.text_area("현재 겪고 있는 직장 내 문제에 대해 설명해주세요:", height=120, 
                                   placeholder="문제 상황을 설명하거나, 관련 키워드만 입력해도 됩니다 (예: 비판, 갈등, 스트레스 등)")

# 단일 버튼 사용 (세련된 디자인)
if st.button("조언 받기"):
    if problem_description:
        # 입력이 간단한 단어나 짧은 문장인 경우, 카테고리 자동 식별
        if len(problem_description.split()) < 5:
            detected_category = identify_category(problem_description)
            if detected_category and detected_category != category:
                st.info(f"입력하신 내용을 분석한 결과, '{detected_category}' 관련 문제로 파악됩니다.")
                category = detected_category
        
        st.subheader(f"{category_icons.get(category, '💡')} 데일 카네기의 조언")
        
        # 선택된 카테고리의 원칙들 중에서 2-3개 선택
        selected_principles = random.sample(carnegie_principles[category], min(3, len(carnegie_principles[category])))
        
        for i, principle in enumerate(selected_principles, 1):
            st.markdown(f"""
            <div class="advice-card">
                <h3>조언 {i}</h3>
                <p>{principle}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 실천 방법 제안
        st.subheader("실천 방법")
        
        # 카테고리별 실천 방법
        practice_methods = {
            "비판과 불만": [
                "문제 상황을 객관적으로 서술해보세요. 감정을 배제하고 사실만 나열합니다.",
                "상대방의 입장에서 같은 상황을 바라보려고 노력해보세요.",
                "\"나\" 메시지를 사용하세요. \"당신이 ~했기 때문에\" 대신 \"내가 ~할 때 어려움을 느꼈어요\"라고 표현합니다."
            ],
            "갈등 해결": [
                "감정이 격해졌을 때는 즉시 대응하지 말고 24시간 기다려보세요.",
                "대화할 때 먼저 상대방의 의견을 충분히 듣고 요약해보세요.",
                "해결책을 함께 모색하는 자세로 접근하세요.",
                "감정보다 사실에 초점을 맞추어 대화하세요."
            ],
            "인정과 칭찬": [
                "매일 적어도 한 명에게 진심 어린 칭찬을 하는 습관을 들이세요.",
                "칭찬할 때는 구체적인 행동이나 결과를 언급하세요.",
                "칭찬 일기를 써보세요. 동료들의 긍정적인 행동을 기록합니다.",
                "감사 메시지를 정기적으로 보내세요."
            ],
            "영향력 행사": [
                "상대방에게 질문하여 그들의 생각을 이끌어내세요.",
                "제안하기 전에 상대방의 필요와 우선순위를 파악하세요.",
                "요청할 때 그것이 상대방에게 어떤 이점이 있는지 설명하세요.",
                "모든 사람을 중요하게 대하고 이름을 불러주세요."
            ],
            "스트레스 관리": [
                "업무 일지를 작성하여 우선순위를 정하고 성취를 기록하세요.",
                "하루 5분씩 명상이나 심호흡으로 마음을 진정시키는 시간을 가지세요.",
                "걱정되는 상황의 최악, 최선, 가능성 높은 시나리오를 작성해보세요.",
                "업무와 휴식의 균형을 유지하세요."
            ]
        }
        
        selected_practices = random.sample(practice_methods[category], min(3, len(practice_methods[category])))
        
        for i, practice in enumerate(selected_practices, 1):
            st.markdown(f"""
            <div class="advice-card" style="border-left-color: #7371B6;">
                <p><strong>💪 실천 {i}:</strong> {practice}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 관련 데일 카네기 인용구
        st.subheader("데일 카네기의 명언")
        quotes = [
            "당신이 꿀을 원한다면, 식초 단지를 걷어차지 마세요.",
            "비판은 비둘기와 같습니다. 항상 집으로 돌아옵니다.",
            "미소 짓는 데는 인상을 쓰는 것보다 더 적은 근육이 필요합니다.",
            "사람들의 마음을 얻는 유일한 방법은 그들에게 그들이 원하는 것을 주는 것입니다.",
            "우리는 다른 사람들의 관점에서 세상을 보지 않는 한 결코 그들을 이해할 수 없습니다.",
            "자신감을 얻는 가장 좋은 방법은 자신감이 없는 일을 하는 것입니다.",
            "사람들에게 영향을 미치는 비결은 그들의 관점에서 사물을 보는 것입니다.",
            "사람들은 자신이 도달한 결론은 믿지만, 남이 알려준 결론은 의심합니다.",
            "남을 비판하는 사람들은 칭찬과 인정을 갈구하는 사람들입니다.",
            "인간관계에서 가장 중요한 원칙은 존중입니다.",
            "성공의 비결은 타인의 입장에서 사물을 보고 자신의 관점에서도 볼 수 있는 능력입니다."
        ]
        
        st.markdown(f"""
        <div class="advice-card" style="background-color: #f7f7f7; border-left-color: #945493;">
            <p><em>\"{random.choice(quotes)}\"</em></p>
            <p style="text-align: right;"><strong>- 데일 카네기</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.warning("문제 상황이나 키워드를 입력해주세요.")

# 새로운 섹션: 빠른 조언
st.markdown("---")
st.header("빠른 키워드 조언")

# 빠른 카테고리 선택 버튼 (올바른 버튼 사용)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("비판 대처", key="quick-비판과_불만"):
        st.session_state.quick_category = "비판과 불만"
with col2:
    if st.button("갈등 해결", key="quick-갈등_해결"):
        st.session_state.quick_category = "갈등 해결"
with col3:
    if st.button("동기 부여", key="quick-인정과_칭찬"):
        st.session_state.quick_category = "인정과 칭찬"
with col4:
    if st.button("리더십", key="quick-영향력_행사"):
        st.session_state.quick_category = "영향력 행사"
with col5:
    if st.button("스트레스", key="quick-스트레스_관리"):
        st.session_state.quick_category = "스트레스 관리"

# 세션 상태를 확인하여 빠른 카테고리 조언 표시
if 'quick_category' in st.session_state:
    quick_category = st.session_state.quick_category
    st.subheader(f"{category_icons.get(quick_category, '💡')} {quick_category}에 관한 빠른 조언")
    quick_advice = random.choice(carnegie_principles[quick_category])
    st.markdown(f"""
    <div class="advice-card" style="background-color: #f8f9fa; border-left-color: #219FC3;">
        <p><strong>{quick_advice}</strong></p>
    </div>
    """, unsafe_allow_html=True)

# 기능 설명
st.markdown("---")
st.header("기능")

# 마크다운으로 기능 설명 (HTML 코드 대신)
st.markdown("""
* **상황별 조언**: 비판과 불만, 갈등 해결, 인정과 칭찬, 영향력 행사, 스트레스 관리 등 다양한 카테고리에 맞는 조언 제공
* **키워드 인식**: 짧은 단어나 문장만으로도 문제 상황을 파악하고 적절한 조언 제공
* **실천 방법 제안**: 조언과 함께 구체적인 실천 방법 안내
* **데일 카네기 명언**: 상황에 맞는 데일 카네기의 명언 제공
""")

# 데일 카네기 책 추천 (수정된 HTML 구조)
st.markdown("---")
st.header("추천 도서")

# 올바른 HTML 구조로 도서 카드 생성
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="book-card">
        <h3 style="margin-top: 0;">인간관계론</h3>
        <p style="color: #555;">인간관계의 기본 원칙과 타인에게 영향을 미치는 방법에 대한 고전</p>
        <div class="book-tag">1936년 출간</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="book-card">
        <h3 style="margin-top: 0;">걱정 없는 인생</h3>
        <p style="color: #555;">일상의 걱정과 스트레스를 효과적으로 관리하는 방법</p>
        <div class="book-tag">1948년 출간</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="book-card">
        <h3 style="margin-top: 0;">현명한 화술</h3>
        <p style="color: #555;">효과적인 의사소통과 설득의 기술에 관한 실용적 가이드</p>
        <div class="book-tag">1962년 출간</div>
    </div>
    """, unsafe_allow_html=True)

# 하단 정보
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 20px 0;">
    <p>© 2025 직장 인간관계 조언 봇 - 데일 카네기의 『인간관계론』을 기반으로 합니다.</p>
</div>
""", unsafe_allow_html=True) 