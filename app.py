{\rtf1\ansi\ansicpg932\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # app.py\
import streamlit as st\
import openai\
from PIL import Image\
\
st.set_page_config(page_title="Ghibli AI Fashion Portal", layout="centered")\
st.title("\uc0\u55358 \u56794 \u8205 \u9792 \u65039  \u12472 \u12502 \u12522 \u39080  AI\u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u12509 \u12540 \u12479 \u12523 ")\
\
st.markdown("""\
\uc0\u12371 \u12398 \u12450 \u12503 \u12522 \u12391 \u12399 \u12289 \u20197 \u19979 \u12398 \u24773 \u22577 \u12434 \u20837 \u21147 \u12377 \u12427 \u12371 \u12392 \u12391 \u12289 \u12354 \u12394 \u12383 \u12398 \u38996 \u12434 \u12472 \u12502 \u12522 \u39080 \u12395 \u22793 \u25563 \u12375 \u12289 \
\uc0\u12373 \u12425 \u12395 \u20284 \u21512 \u12358 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u12434 AI\u12364 \u25552 \u26696 \u12375 \u12414 \u12377 \u12290 \
""")\
\
with st.form("user_profile"):\
    uploaded_file = st.file_uploader("\uc0\u55357 \u56420  \u38996 \u12414 \u12383 \u12399 \u20840 \u36523 \u12364 \u20889 \u12387 \u12383 \u20889 \u30495 \u12434 \u12450 \u12483 \u12503 \u12525 \u12540 \u12489 ", type=["jpg", "jpeg", "png"])\
    gender = st.selectbox("\uc0\u24615 \u21029 ", ["\u22899 \u24615 ", "\u30007 \u24615 ", "\u12381 \u12398 \u20182 "])\
    age = st.number_input("\uc0\u24180 \u40802 ", min_value=1, max_value=100, value=25)\
    height = st.number_input("\uc0\u36523 \u38263  (cm)", min_value=100, max_value=250, value=160)\
    weight = st.number_input("\uc0\u20307 \u37325  (kg)", min_value=30, max_value=200, value=55)\
    body_type = st.text_input("\uc0\u20307 \u22411  (\u20363 : \u12473 \u12522 \u12512 \u12289 \u31563 \u32905 \u36074 )")\
    style = st.text_input("\uc0\u22909 \u12365 \u12394 \u38640 \u22258 \u27671  (\u20363 : \u22799 \u31995 \u12289 \u26126 \u12427 \u12356 \u31995 )")\
    submitted = st.form_submit_button("\uc0\u10024  \u12472 \u12502 \u12522 \u39080 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u12434 \u29983 \u25104 ")\
\
if submitted and uploaded_file:\
    st.image(uploaded_file, caption="\uc0\u12450 \u12483 \u12503 \u12525 \u12540 \u12489 \u30011 \u20687 ", width=200)\
    with st.spinner("AI\uc0\u12364 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u12434 \u29983 \u25104 \u20013 ..."):\
        openai.api_key = st.secrets["OPENAI_API_KEY"]\
        prompt = f"\uc0\u24180 \u40802 \{age\}\u27507 \u12289 \{gender\}\u12289 \u20307 \u22411 \u12399 \{body_type\}\u12289 \u36523 \u38263 \{height\}cm\u12289 \u20307 \u37325 \{weight\}kg\u12289 \u22909 \u12365 \u12394 \u38640 \u22258 \u27671 \u12399 \{style\}\u31995 \u12290 \u12472 \u12502 \u12522 \u26144 \u30011 \u12395 \u20986 \u12390 \u12365 \u12381 \u12358 \u12394 \u12461 \u12515 \u12521 \u12463 \u12479 \u12540 \u39080 \u12398 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u12434 \u25552 \u26696 \u12375 \u12390 \u12367 \u12384 \u12373 \u12356 \u12290 "\
\
        response = openai.ChatCompletion.create(\
            model="gpt-4",\
            messages=[\
                \{"role": "system", "content": "\uc0\u12354 \u12394 \u12383 \u12399 \u19968 \u27969 \u12398 AI\u12473 \u12479 \u12452 \u12522 \u12473 \u12488 \u12391 \u12377 \u12290 "\},\
                \{"role": "user", "content": prompt\}\
            ]\
        )\
\
        fashion_text = response.choices[0].message.content\
        st.success("\uc0\u55356 \u57225  \u12473 \u12479 \u12452 \u12523 \u12364 \u23436 \u25104 \u12375 \u12414 \u12375 \u12383 \u65281 ")\
        st.markdown("### \uc0\u55357 \u56481  AI\u12398 \u12362 \u12377 \u12377 \u12417 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 ")\
        st.write(fashion_text)\
\
        st.image("https://via.placeholder.com/400x400.png?text=Ghibli+Style", caption="\uc0\u12472 \u12502 \u12522 \u39080 \u12501 \u12449 \u12483 \u12471 \u12519 \u12531 \u30011 \u20687 \u65288 \u20363 \u65289 ")\
        st.button("\uc0\u55357 \u57042  \u12371 \u12398 \u12473 \u12479 \u12452 \u12523 \u12395 \u21512 \u12358 \u21830 \u21697 \u12434 \u25506 \u12377 ")\
else:\
    st.info("\uc0\u19978 \u35352 \u12501 \u12457 \u12540 \u12512 \u12395 \u24773 \u22577 \u12434 \u20837 \u21147 \u12375 \u12289 \u12508 \u12479 \u12531 \u12434 \u25276 \u12375 \u12390 \u12367 \u12384 \u12373 \u12356 \u12290 ")\
}