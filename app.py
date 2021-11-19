import os
import streamlit as st
import numpy as np
from PIL import  Image
import pandas as pd
# Custom imports
from multipage import MultiPage
from pages import Landing,  OCplot, Rplot, Feedback # import your pages here


OCfiles_selected=[]
# IRfiles_selected=[]

# Create an instance of the app
app = MultiPage()

st.set_page_config(layout='wide')
st.sidebar.image("apl.png", use_column_width=True)
st.sidebar.title('Dragonfly Surface Composition Modeling')


app.add_page("Home", Landing.app)
app.add_page("Optical Constant Modeling", OCplot.app)
app.add_page("Reflectance Spectra Modeling", Rplot.app)
app.add_page("Beta Tester Feedback", Feedback.app)


# The main app
app.run()
