import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

# ⚡️ OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ページタイトル
st.set_page_config(page_title="🌟 AIアバターファッションポータル", layout="wide")
st.title("AIアバターファッションポータル")
st.markdown("Webに写真を送り、情報を入力してジブリ風ファッションを生成しましょう")

# ユーザー入力
with st.form("user_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("自分の写真をアップロード", type=["jpg", "jpeg", "png"])
        gender = st.selectbox("性別", ["男", "女", "その他"])
        age = st.slider("年齢", 10, 80, 25)
        height = st.number_input("身長(cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("体重(kg)", min_value=30, max_value=150, value=60)
    with col2:
        body_shape = st.selectbox("体型", ["スリム", "マッチョ", "ガッチリ"])
        concept = st.text_input("好きなファッションコンセプ (例: 夏系, 明るい系, ストリート系)")
        submitted = st.form_submit_button("ジブリ風コーディネート生成")

# ジブリ風衣装の生成
if submitted and uploaded_image:
    prompt = f"Generate a Studio Ghibli style fashion outfit for a {age}-year-old {gender} with a {body_shape} body shape, height {height}cm and weight {weight}kg. The concept is: {concept}. Output should be poetic and artistic."

    with st.spinner("生成中... 待ちください"):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        ghibli_image = Image.open(BytesIO(image_response.content))

    st.image(ghibli_image, caption="生成されたジブリ風ファッション", use_column_width=True)

    # 例) 商品一覧を仮に表示
    st.markdown("### このファッションに合う商品")
    example_products = [
        {"name": "ストローハット Tシャツ", "url": "https://example.com/product/1"},
        {"name": "リネンコスカート", "url": "https://example.com/product/2"},
        {"name": "ギャザーサンダル", "url": "https://example.com/product/3"}
    ]

    for product in example_products:
        st.markdown(f"- [{product['name']}]({product['url']})")

    st.success("アバターコーディネートの生成が終わりました！")
