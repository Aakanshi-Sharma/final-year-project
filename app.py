import streamlit as st
import pandas as pd
import numpy as np


st.title("sdffdv")

model=pd.read_pickle(open("model.pkl", "rb"))

st.header(model.predict([[0,1,1,1,1,1,-1,0,1,-1,1,1,-1,1,0,-1,-1,1,1,0,1,1,1,1,-1,-1,0,-1,1,1]]))