import streamlit as st
import pandas as pd
import numpy as np
from feature import FeatureExtraction

model = pd.read_pickle(open("model.pkl", "rb"))


def prediction(url):
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1, 30)
    result = model.predict(x)[0]
    y_pro_phishing = model.predict_proba(x)[0, 0]
    y_pro_non_phishing = model.predict_proba(x)[0, 1]
    # 1 is safe
    # -1 is unsafe
    print("y_pro_phishing", y_pro_phishing)
    print("y_pro_non_phishing", y_pro_non_phishing)
    if result == 1:
        return "Safe" + " It is {0:.2f} % safe to go ".format(y_pro_non_phishing * 100)
    elif result == -1:
        return "Unsafe" + " It is {0:.2f} % unsafe".format(y_pro_phishing * 100)
    else:
        return "Something went wrong!"


st.title("Phishing URL Detection")
resultant_url = st.text_input("Enter the URL")
if st.button("Click here..", type="primary"):
    st.subheader(prediction(resultant_url))
