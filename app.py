import streamlit as st
import pandas as pd
import numpy as np
from feature import FeatureExtraction
import requests
from urllib.parse import urlparse, quote

# -------------MODEL CALLING-------------

model = pd.read_pickle(open("model.pkl", "rb"))


# -------------FUNCTIONS-----------------
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


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


def check_url(url):
    isCHeckedUrl = is_valid_url(url)
    if not isCHeckedUrl:
        return -2, 0
    encoded_url = quote(url, safe='')
    response = requests.get(
        f"https://www.ipqualityscore.com/api/json/url/K5dF12S2K4fPXIjmo7NDTT5ipDrtVhfw/{encoded_url}")
    if response.status_code == 200:
        try:
            data = response.json()
            if (data["parking"] or data["spamming"] or data["malware"] or data["phishing"] or data["suspicious"] or
                    data["unsafe"]):
                print("This site is unsafe")
                return -1, data["risk_score"]
            elif data["risk_score"] >= 85:
                print("this site is unsafe")
                return -1, data["risk_score"]

            return 1, data["risk_score"]
        except ValueError:
            return -3, 0
    else:
        return -3, 0


st.title("Phishing URL Detection")
resultant_url = st.text_input("Enter the URL")
if st.button("Click here...", type="primary"):
    with st.spinner('Wait for it...'):
        res = check_url(resultant_url)
        if res[0] == -1:
            st.error("Unsafe 🚨" + " The risk factor is {0:.2f} % .".format(res[1]))
        elif res[0] == 1:
            st.success("Safe ✅" + " The risk factor is {0:.2f} % .".format(res[1]))
        elif res[0] == -2:
            st.warning("Invalid URL ⚠️")
        else:
            st.warning("Something went wrong!")
