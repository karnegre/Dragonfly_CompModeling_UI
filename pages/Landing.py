import streamlit as st
import numpy as np
import pandas as pd
from PIL import  Image
from IPython.display import HTML
import os

def app():

    display = Image.open('LandingLogo.png')
    display = np.array(display)

#LOGO Orientation-----------------------------
    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.write("")

    with col2:
        st.image(display, width=600)

    with col3:
        st.write("")

#DESCRIPTION Orientation-----------------------------
    col4, col5, col6 = st.columns([1,4,2])

    with col4:
        st.write("")

    with col5:

        st.markdown(
            """
            _________________________________________________________________________________________________________________________________
            ### Description
            + The Dragonfly Surface Composition Modeling (DSCM) App is a linear mixing model, which utilizes optical constants and reflectance spectra avaliable in literature to model..
            + Developed using the Shkuratov Model (1999), albedo (reflectance) of a surface can be calculated and serve as an approximation tool for the Dragonfly mission to Titan.
            + Insert link to Shkuratov paper here??

            ### Notation
            + Tholins are named in accordance to syntax in papers. Visit DOI for more information.
            _________________________________________________________________________________________________________________________________
            """
            )
    with col6:
        st.write("")

#LIB Orientation-----------------------------
    col7, col8, col9 = st.columns([1,4,3])

    with col7:
        st.write("")

    with col8:

        st.header("Database Libraries")
        libpick = st.selectbox(
        "Select a Library",
        ('Optical Constant Library', 'Reflectance Spectra Library'))

        #Platform independence
        cwd =os.getcwd()

        filename = "Lib.xlsx"
        path_file = os.sep.join([cwd, filename])

        if libpick == 'Optical Constant Library':

            dfOLib=pd.read_excel(path_file,sheet_name="O Library").set_index("Possible Compounds on Titans Surface")
            st.table(dfOLib)

        if libpick == 'Reflectance Spectra Library':

            dfRLib=pd.read_excel(path_file,sheet_name="R Library").set_index("Possible Compounds on Titans Surface")
            st.table(dfRLib)

        else:
            st.write('')

    with col9:
        st.write("")
