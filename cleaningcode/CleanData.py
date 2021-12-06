import numpy as np              # standard numerical recipes library
import matplotlib.pyplot as plt # standard plotting library
import pandas as pd             # standard excel-style arrays library
import shutil
import os
import os.path
import streamlit as st
import glob as glob

deltawave=0.001
interpwaves= np.arange(0.4,2.6,deltawave)
cwd =os.getcwd()
OCfiles_path_dirty= os.path.join( cwd,'dirty','OC')
OCfiles_path_clean= os.path.join( cwd,'cleaned','OC')
IRfiles_path_dirty= os.path.join( cwd,'dirty','IR')
IRfiles_path_clean= os.path.join( cwd,'cleaned','R')

def CleanOC():
    for file in os.listdir(OCfiles_path_dirty):
        if os.path.isfile(os.path.join(OCfiles_path_dirty, file)) and not os.path.isfile(os.path.join(OCfiles_path_clean, file)) :
            if file.endswith(".txt"):
                df= pd.read_csv(os.path.join(OCfiles_path_dirty,file),sep='\t')
                unitcheck = df['wave'].iat[0]
                # nm check
                if (unitcheck > 100):
                    df['wave'] =  df['wave'] / 1000

                st.subheader('Dirty')
                st.write(file)
                st.write(df)

                st.subheader('~~~~~Cleaning Now~~~~~')
                n_interp=np.interp(interpwaves,df.wave,df.n)
                k_interp=np.interp(interpwaves,df.wave,df.k)
                dfClean=pd.DataFrame(list(zip(interpwaves,n_interp,k_interp)),columns=['wave','n','k'])

                st.subheader('Clean')
                st.write(file)
                st.write(dfClean)

                dfClean.to_csv(os.path.join(OCfiles_path_clean,file),index=False)
                st.write('File cleaned and added')
                st.write('---------------------------------------------------------------------')

def CleanIR():
    for file in os.listdir(IRfiles_path_dirty):
        if os.path.isfile(os.path.join(IRfiles_path_dirty, file)) and not os.path.isfile(os.path.join(IRfiles_path_clean, file)) :
            if file.endswith(".txt"):
                df= pd.read_csv(os.path.join(IRfiles_path_dirty,file),sep='\t')
                unitcheck = df['wave'].iat[0]
                # nm check
                if (unitcheck > 100):
                    df['wave'] =  df['wave'] / 1000

                st.subheader('Dirty')
                st.write(file)
                st.write(df)

                st.subheader('~~~~~Cleaning Now~~~~~')
                interp=np.interp(interpwaves,df.wave,df.r)
                dfClean=pd.DataFrame(list(zip(interpwaves,interp)),columns=['wave','r'])

                st.subheader('Clean')
                st.write(file)
                st.write(dfClean)

                dfClean.to_csv(os.path.join(IRfiles_path_clean,file),index=False)
                st.write('File cleaned and added')
                st.write('---------------------------------------------------------------------')
#------------------------------------------------------------------------------------------------------------------


dataset= ["OC", "IR"]
choice = st.radio("What do you want to clean?", dataset)

if choice == "OC":
    if st.button('Go'):
        CleanOC()
elif choice == "IR":
    if st.button('Go'):
        CleanIR()
