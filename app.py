import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import json
import os
from datetime import datetime
import uuid

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Setup Streamlit page
st.set_page_config(page_title="🌟 Ghibli Fashion Portal", layout="wide")
st.title("🌟 AIアバターファッションポータル")

# JSON data file for saving favorites
DATA_FILE = "favorites.json"
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        st.session_state.favorites = json.load(f)

def save_favorite(entry):
    st.session_state.favorites.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.favorites, f, indent=2)

# Tabs for functionality
tabs = st.tabs(["生成", "ポータル"])

# --- Tab 1: Generate Ghibli-style Fashion ---
with tabs[0]:
    st.subheader("📷 写真と情報をもとにファッションを生成")
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
            concept = st.text_input("好きなコンセプト (夏系, ギャル系, ヨーロッパ系 etc)")
            submitted = st.form_submit_button("ジブリ風コーディネート生成")

    if submitted and uploaded_image:
        prompt = f"Fashion concept: {concept}. Please create a Studio Ghibli inspired anime fashion illustration. Soft watercolor style, magical and whimsical mood, character in a natural setting, rich colors, artistic clothing details, fantasy-like background. Character is a {age}-year-old {gender}, {body_shape} body shape, height {height}cm, weight {weight}kg."

        with st.spinner("AIファッション生成中..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            ghibli_image = Image.open(BytesIO(image_response.content))

        st.image(ghibli_image, caption="生成されたジブリ風コーディネート", use_column_width=True)

        if st.button("❤️ お気に入りとして登録"):
            new_favorite = {
                "id": str(uuid.uuid4()),
                "image_url": image_url,
                "gender": gender,
                "age": age,
                "body_shape": body_shape,
                "height": height,
                "weight": weight,
                "concept": concept,
                "timestamp": datetime.now().isoformat()
            }
            save_favorite(new_favorite)
            st.success("お気に入りに登録しました！")

# --- Tab 2: Portal View ---
with tabs[1]:
    st.subheader("📃 みんなのお気に入りコーディネート")
    favorites = st.session_state.get("favorites", [])
    if favorites:
        for entry in sorted(favorites, key=lambda x: x["timestamp"], reverse=True):
            with st.container():
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(entry["image_url"], use_column_width=True)
                with cols[1]:
                    st.markdown(f"**コンセプト**: {entry['concept']}")
                    st.markdown(f"**性別**: {entry['gender']} | **年齢**: {entry['age']} | **体型**: {entry['body_shape']}")
                    st.markdown(f"**身長/体重**: {entry['height']}cm / {entry['weight']}kg")
                    st.markdown(f"[商品を見る](https://example.com/search?q=ghibli+{entry['concept'].replace(' ', '+')})")
    else:
        st.info("まだお気に入り登録がありません")