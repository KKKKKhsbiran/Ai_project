import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime

# ------------------------------
# 📊 [데모] 데모용 가짜 데이터 생성 함수
# ------------------------------
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

@st.cache_data
def create_fake_data(symbols):
    """데모용 가짜 주식 데이터를 생성하여 DataFrame으로 반환합니다."""
    print("--- (create_fake_data) 함수 1회 실행 (캐시 생성) ---")
    dates = pd.date_range(end=datetime.now(), periods=40, freq='h')
    data = {}
    base_prices = {"AAPL": 180, "MSFT": 450, "GOOGL": 170, "AMZN": 190, "TSLA": 180}

    for s in symbols:
        base_price = base_prices.get(s, 200)
        price_changes = np.random.randn(40).cumsum() * np.random.uniform(0.3, 1.2)
        prices = base_price + price_changes
        data[s] = pd.Series(prices, index=dates)

    df = pd.DataFrame(data).ffill().bfill()
    print("✅ (create_fake_data) 데모용 가짜 데이터 생성 완료.")
    return df

# ------------------------------
# 🧠 데이터 분석 + AI 코멘트 함수
# ------------------------------
def get_systematic_comment(style, selected_stock, df):
    valid_styles = ["공격적 투자", "안정적 투자", "방어적 투자"]
    if style not in valid_styles:
        return "‘공격적 투자’, ‘안정적 투자’, ‘방어적 투자’ 중 하나를 입력해주세요."
    if not selected_stock:
        return "분석할 종목을 드롭다운에서 선택해주세요."
    if df is None or df.empty:
        return "데이터가 아직 로드되지 않았습니다. 잠시 후 다시 시도해주세요."

    try:
        stock_series = df[selected_stock]
        recent_data = stock_series.tail(10)
        momentum_score = (recent_data.iloc[-1] - recent_data.iloc[0]) / recent_data.iloc[0] * 100
        volatility_score = stock_series.std()

        if momentum_score > 3: momentum_text = "강한 상승 모멘텀"
        elif momentum_score < -3: momentum_text = "강한 하락 모멘텀"
        else: momentum_text = "중립적 횡보"

        if volatility_score > 5: volatility_text = "높은 변동성"
        elif volatility_score < 2: volatility_text = "낮은 변동성"
        else: volatility_text = "평균 변동성"

    except Exception as e:
        return f"'{selected_stock}' 종목 분석 중 오류가 발생했습니다."

    time.sleep(1.0) 
    comment = f"[{selected_stock} | {style} 성향 분석]\n"
    comment += "────────────────────\n"
    comment += f"📊 데이터 분석 결과:\n"
    comment += f"  - 최근 모멘텀: {momentum_text} (Score: {momentum_score:.2f}%)\n"
    comment += f"  - 전체 변동성: {volatility_text} (Score: {volatility_score:.2f})\n\n"
    comment += "🧠 AI 투자 조언 (Demo):\n"
    
    if style == "공격적 투자":
        if volatility_text == "높은 변동성":
            comment += f"  > 높은 변동성은 공격적 성향에 부합합니다. {momentum_text}을 고려한 단기 트레이딩 전략을 추천합니다."
        else:
            comment += f"  > 변동성이 낮아 아쉽지만, {momentum_text}이 확인됩니다. 포트폴리오의 안정적 수익원으로 고려할 수 있습니다."
    elif style == "안정적 투자":
        if volatility_text == "낮은 변동성" and momentum_text == "강한 상승 모멘텀":
            comment += f"  > '낮은 변동성'과 '상승 모멘텀'은 안정적 성향에 가장 이상적입니다. 비중 확대를 긍정적으로 검토하세요."
        elif volatility_text == "높은 변동성":
            comment += f"  > 변동성이 높아 주의가 필요합니다. {momentum_text}에도 불구하고 비중을 축소하거나 분산 투자를 권장합니다."
        else:
            comment += f"  > {volatility_text}과 {momentum_text}을 보이고 있습니다. 현재 비중을 유지하며 시장 상황을 관망하는 것이 좋습니다."
    elif style == "방어적 투자":
        if volatility_text == "높은 변동성" or momentum_text == "강한 하락 모멘텀":
            comment += f"  > 위험 신호({volatility_text}, {momentum_text})가 감지되었습니다. 방어적 투자 성향에 부적합하므로 비중 축소 또는 매도를 권고합니다."
        else:
            comment += f"  > {volatility_text}과 {momentum_text}을 보이고 있습니다. 안정적인 자산 방어 수단으로 유효합니다."

    return comment

# ------------------------------
# 📈 Plotly 그래프 생성
# ------------------------------
def plot_stock(df, selected_symbols):
    fig = go.Figure()

    if df is None or df.empty or not selected_symbols:
        fig.update_layout(title="표시할 종목을 왼쪽 체크리스트에서 선택해주세요.", template="plotly_dark")
        return fig

    for col in selected_symbols:
        if col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col))

    fig.update_layout(
        title="📊 5일간 주요 종목 시간별 종가 (데모 데이터)",
        xaxis_title="날짜 및 시간", yaxis_title="가격 (USD)",
        template="plotly_dark",
        legend_title="종목",
        font=dict(family="Arial, sans-serif", size=14, color="#FFFFFF")
    )
    return fig

# ------------------------------
# 🌐 Streamlit 앱 구성 (Main)
# ------------------------------

# 1. 페이지 설정 (가장 먼저 실행)
st.set_page_config(layout="wide", page_title="AI 투자 어드바이저")

# 2. 데이터 로드 (캐시)
df = create_fake_data(SYMBOLS)

# 3. 사이드바 UI 구성 (✨ 'run_button'이 여기서 정의됩니다!)
with st.sidebar:
    st.image("https://emojicdn.elk.sh/💹", width=80)
    st.title("AI 투자 어드바이저")
    st.markdown("---")
    
    st.subheader("Step 1: 투자 성향 입력")
    style = st.text_input("투자 성향", value="안정적 투자", label_visibility="collapsed")
    
    st.subheader("Step 2: 분석 종목 선택")
    selected_stock = st.selectbox("분석 종목", SYMBOLS, index=0, label_visibility="collapsed")
    
    # 'run_button' 변수 생성
    run_button = st.button("AI 분석 실행", use_container_width=True, type="primary")
    st.markdown("---")

    st.subheader("그래프 종목 필터")
    selected_symbols = st.multiselect(
        "그래프 종목 필터", 
        SYMBOLS, 
        default=SYMBOLS, 
        label_visibility="collapsed"
    )
    
    st.info("ⓒ 2025 University Project (Demo)")

# 4. 메인 페이지 - 그래프
st.plotly_chart(plot_stock(df, selected_symbols), use_container_width=True)
st.markdown("---")

# 5. 메인 페이지 - AI 분석 결과 (✨ 여기가 수정된 최종 순서입니다!)
st.subheader("🧠 AI 종합 분석 결과")

# 5-1. 'ai_advice' 변수를 "먼저" 초기화 (AttributeError 방지)
if 'ai_advice' not in st.session_state:
    st.session_state.ai_advice = "왼쪽 패널에서 'AI 분석 실행' 버튼을 눌러주세요."

# 5-2. "다음으로" 버튼 클릭 확인 (NameError 방지)
if run_button:
    with st.spinner(f"'{selected_stock}' 종목을 '{style}' 성향에 맞춰 분석 중..."):
        ai_advice = get_systematic_comment(style, selected_stock, df)
        st.session_state.ai_advice = ai_advice # 변수 업데이트

# 5-3. "마지막에" 화면에 표시 (오류가 났던 그 라인)
st.pre(st.session_state.ai_advice)
