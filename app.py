import streamlit as st
import pandas as pd
import numpy as np
from feature import FeatureExtraction
from urllib.parse import urlparse
import google.generativeai as genai

# -------------GLOBAL VARIABLES--------

with open("key.txt", "r") as f:
    GOOGLE_API_KEY = f.read()

genai.configure(api_key=GOOGLE_API_KEY)

model = pd.read_pickle(open("model.pkl", "rb"))


def get_response_genai(url):
    model1 = genai.GenerativeModel('gemini-pro')
    response = model1.generate_content(f"Predict whether the url {url} is safe or unsafe and give the percentage and reason in 1 line")
    print(response.text)
    return response.text

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def predict(url):
    obj = get_response_genai(url)
    return obj

def prediction(url):
    isCHeckedUrl = is_valid_url(url)
    if not isCHeckedUrl:
        return -2, 0, 0
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1, 30)
    result = model.predict(x)[0]
    y_pro_phishing = model.predict_proba(x)[0, 0]
    y_pro_non_phishing = model.predict_proba(x)[0, 1]
    # 1 is safe
    # -1 is unsafe
    print("y_pro_phishing", y_pro_phishing)
    print("y_pro_non_phishing", y_pro_non_phishing)
    return result, y_pro_phishing, y_pro_non_phishing


st.title("Phishing URL Detection")
resultant_url = st.text_input("Enter the URL")
if st.button("Click here...", type="primary"):
    st.success(predict(resultant_url))
# if st.button("Click here..", type="primary"):
#     with st.spinner('Wait for it...'):
#         res = prediction(resultant_url)
#         if res[0] == 1:
#             st.success("Safe ✅" + " It is {0:.2f} % safe to go ".format(res[2] * 100))
#         elif res[0] == -1:
#             st.error("Unsafe 🚨" + " It is {0:.2f} % unsafe".format(res[1] * 100))
#         elif res[0] == -2:
#             st.warning("Invalid URL ⚠️")
#         else:
#             st.warning("Something went wrong!")
