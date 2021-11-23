#****IMPORTS***
import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import SessionState
import os
import os.path
import cmath
import math
import shkuratov_ssa_models as shkrtv
import rmodel as rm
from plotly import express as px
import base64

from streamlit import caching
st.legacy_caching.clear_cache()

number_of_elements =0
CompDict={}
CompNameList=[]
SpecDF= pd.DataFrame()
dfRLib= pd.DataFrame()

#Platform independence
cwd =os.getcwd()
cleanIR_path= os.path.join( cwd,'cleaningcode','cleaned','R')

session_state = SessionState.get(SpectraDict = [],CurrentSpectraIndex=0,Num_Spectra_Prev=0,OC_select=[],restart=0,IR_select=[])
# ------------------------------------------------------
def app():
    global IRfiles_selected
    #session_state.IR_select=[]
    if (st.sidebar.button("Restart RS Modeling")):
        session_state.restart=1
        session_state.IR_select=[]
        session_state.Num_Spectra_Prev=0
        session_state.CurrentSpectraIndex=0
        session_state.SpectraDict=[]
        session_state.GrainDict=[]
        IRfiles_selected =[]
        number_of_elements=0
        st.balloons()
    create_dictionary(cleanIR_path)
    process_sidebar()
# # -------------------------------------------------------
@st.cache(suppress_st_warning=True)
def create_dictionary(path):
    global CompNameList
    global CompDict

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith(".txt"):
                namef= os.path.splitext(name)[0]
                CompNameList.append(namef)
                df = pd.read_csv(os.path.join(cleanIR_path,name))
                df.set_index(['wave'],drop=False,inplace=True)
                CompDict[namef]=df
 # -----------------------------------------------------------------------------------------------------
def ReadIRLib():
    global dfRLib
    #global IRfiles_selected
    global number_of_elements

    if (number_of_elements==0):
        return

    cwd =os.getcwd()
    filename = "Lib.xlsx"
    path_file = os.sep.join([cwd, filename])

    dfRLib=pd.read_excel(path_file,sheet_name="R Library")
    st.header('Compound Information Table')

    if (number_of_elements>=1):
        st.header('Selected IR Information')
        if (number_of_elements==1):
            st.table(dfRLib[dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[0])])
        elif (number_of_elements==2):
            st.table(dfRLib[dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[0]) |
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[1])])
        elif (number_of_elements==3):
            st.table(dfRLib[dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[0]) |
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[1])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[2])])
        elif (number_of_elements==4):
            st.table(dfRLib[dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[0]) |
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[1])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[2])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[3])])
        elif (number_of_elements>=5):
            st.table(dfRLib[dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[0]) |
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[1])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[2])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[3])|
            dfRLib['Possible Compounds on Titans Surface'].str.fullmatch(session_state.IR_select[4])])
# -----------------------------------------------------------------------------------------------------
def createthismix(mix):
    global number_of_elements
    if (number_of_elements==2):
        thismix=[[a,b] for a,b in zip(mix[session_state.IR_select[0]],mix[session_state.IR_select[1]])]
    elif (number_of_elements==3):
        thismix=[[a,b,c] for a,b,c in zip(mix[session_state.IR_select[0]],mix[session_state.IR_select[1]],mix[session_state.IR_select[2]])]
    elif (number_of_elements==4):
        thismix=[[a,b,c,d] for a,b,c,d in zip(mix[session_state.IR_select[0]],mix[session_state.IR_select[1]],mix[session_state.IR_select[2]],mix[session_state.IR_select[3]])]
    elif (number_of_elements==5):
        thismix=[[a,b,c,d,e] for a,b,c,d,e in zip(mix[session_state.IR_select[0]],mix[session_state.IR_select[1]],mix[session_state.IR_select[2]],mix[session_state.IR_select[3]],mix[session_state.IR_select[4]])]
    else:
        thismix=[]
    return thismix
# -----------------------------------------------------------------------------------------------------
def StartCalculation(files,mixesArray):
    global CompDict
    global number_of_elements
    dataname=[session_state.IR_select[i] for i in range(number_of_elements)]
    datanamecombo='-'.join(dataname)

    mix=pd.DataFrame({'wave':CompDict[session_state.IR_select[0]].wave})
    mix.set_index(mix.wave,inplace=True)
    result=pd.DataFrame(index=mix.index)
    visresult=pd.DataFrame()

    for i in range(number_of_elements):
        mix[session_state.IR_select[i]]=CompDict[session_state.IR_select[i]].r
    print(mix)

    concentrations=[mm/100 for mm in mixesArray]

    if number_of_elements == 1:
        thismix = mix
        thismix.drop(['wave'], axis=1, inplace=True)
    else:
        thismix=createthismix(mix)

    if (number_of_elements==1):
        result=thismix
        visresult=result.copy().truncate(after=1.05)
        fig1 = px.line(visresult)
        fig1.update_xaxes(title_text='Wavelength (μm)')
        fig1.update_yaxes(title_text='Reflectance')
        fig1.update_layout(legend_title_text='Concentrations')
        fig1.update_layout(showlegend=True, width=1100,height=700,margin= dict(l=1,r=1,b=1,t=1), font=dict(color='#383635', size=20))


        fig2 = px.line(result)
        fig2.update_xaxes(title_text='Wavelength (μm)')
        fig2.update_yaxes(title_text='Reflectance')
        fig2.update_layout(legend_title_text='Concentrations')
        fig2.update_layout(showlegend=True, width=1100,height=700,margin= dict(l=1,r=1,b=1,t=1), font=dict(color='#383635', size=20))

        col1, col2 = st.columns((1,1))
        with col1:
            st.header("Visible Spectra")
            st.plotly_chart(fig1, use_container_width=True)
            st.header("Visible Spectra Data")
            st.dataframe(visresult)
            csv = visresult.to_csv(index=True)
            st.download_button(label="Download data as CSV",data=csv,file_name=datanamecombo +'.csv', mime='text/csv')
        with col2:
            st.header("Visible + IR Spectra")
            st.plotly_chart(fig2, use_container_width=True)
            st.header("Visible + IR Spectra Data")
            st.dataframe(result)
            csv2 = result.to_csv(index=True)
            st.download_button(label="Download data as CSV",data=csv2,file_name=datanamecombo +'.csv', mime='text/csv')

        return mix
    elif (number_of_elements>=2):
        colname=''
        colnamearray=[]
        for n,i in enumerate(session_state.IR_select):
                # to limit the amount of compounds to 5 possible selections by the user
            if(n<=4):
                if (n==number_of_elements-1):
                    colname+=str(mixesArray[n])[0:3]
                else:
                    colname+=str(mixesArray[n])[0:3]+"_"#[0:2]

        mix[colname]=[rm.linearmixingmodel(concentrations,a,w) for a,w in zip(thismix,mix.wave)]
        result[colname]=mix[colname]

        for i in range(number_of_elements):
            result[session_state.IR_select[i]]=CompDict[session_state.IR_select[i]].r

        visresult=result.copy().truncate(after=1.05)
        fig1 = px.line(visresult)
        fig1.update_xaxes(title_text='Wavelength (μm)')
        fig1.update_yaxes(title_text='Reflectance')
        fig1.update_layout(legend_title_text='Concentrations')
        fig1.update_layout(showlegend=True, width=1100,height=700,margin= dict(l=1,r=1,b=1,t=1), font=dict(color='#383635', size=20))

        fig2 = px.line(result)
        fig2.update_xaxes(title_text='Wavelength (μm)')
        fig2.update_yaxes(title_text='Reflectance')
        fig2.update_layout(legend_title_text='Concentrations')
        fig2.update_layout(showlegend=True, width=1100,height=700,margin= dict(l=1,r=1,b=1,t=1), font=dict(color='#383635', size=20))

        col1, col2 = st.columns((1,1))
        with col1:
            st.header("Visible Spectra")
            st.plotly_chart(fig1, use_container_width=True)
            st.header("Visible Spectra Data")
            st.dataframe(visresult)
            csv = visresult.to_csv(index=True)
            st.download_button(label="Download data as CSV",data=csv,file_name=datanamecombo +'.csv', mime='text/csv')
        with col2:
            st.header("Visible + IR Spectra")
            st.plotly_chart(fig2, use_container_width=True)
            st.header("Visible + IR Spectra Data")
            st.dataframe(result)
            csv2 = result.to_csv(index=True)
            st.download_button(label="Download data as CSV",data=csv2,file_name=datanamecombo +'.csv', mime='text/csv')

        return mix
# ---------------------------------------------------------
def process_sidebar():

        global number_of_elements
        global IRfiles_selected
        global CompNameList
        global CompDict
        global SpecDF
        global grainarray

        IRList=[]
        concarray=[]
        number_conc=0

        st.sidebar.title('Reflectance Modeling')

#----------------------ITEM 1: Select desired compounds---------------------------------------
        st.sidebar.header('Select Compounds')
        IRfile_list = CompNameList

        Group_list = ['Ice','Organic','Oceanic','Tholin','Higher Order Organic']
        Group_selected = st.sidebar.selectbox(label="Grouping",options=Group_list)

        cwd =os.getcwd()
        filename = "Lib.xlsx"
        path_file = os.sep.join([cwd, filename])
        Lib=pd.read_excel(path_file,sheet_name="R Library")

        GroupLib=Lib[Lib.Grouping.str.contains(Group_selected)]
        IRfile_list = GroupLib['Possible Compounds on Titans Surface'].tolist()
        IRfiles_selected = st.sidebar.multiselect(label="Compounds",options=IRfile_list)

        number_ir = len(IRfiles_selected)
        number_ir_statelist = len(session_state.IR_select)

        if (len(IRfiles_selected)>=1):
            for index in range(number_ir):
                if (number_ir_statelist>0):
                        if not (IRfiles_selected[index] in session_state.IR_select):
                            session_state.IR_select.append(IRfiles_selected[index])
                else:
                    if (session_state.restart==0):
                        session_state.IR_select.append(IRfiles_selected[index])

        if (session_state.restart==1):
            session_state.restart=0

        number_of_elements = len(session_state.IR_select)
        #st.write(number_of_elements)
        #To limit the amount of elements to 5. If user selects more than 5, its truncate to 5
        if (number_of_elements>5):
            number_of_elements=5

        if (number_of_elements==0):
            session_state.Num_Spectra_Prev=0
            session_state.CurrentSpectraIndex=0
            session_state.SpectraDict=[]
            session_state.GrainDict=[]

        ReadIRLib()

        if (number_of_elements==1):
            IR_conc=100
            concarray.append(IR_conc)
            index=[session_state.IR_select[i] for i in range(number_of_elements)]

            dfComp=pd.DataFrame(concarray,index=index, columns=['Concentration'])
            st.header('Model Spectrum Parameters')
            st.table(dfComp)

            if (number_of_elements>=1 ):
                    if (st.sidebar.button("Start Calculation")):
                        IRmodel=StartCalculation(IRfiles_selected,concarray)

        elif (number_of_elements>=2):
#-----------------------ITEM 2: Select concentration--------------------------------------
            st.sidebar.subheader('Select Concentration')
            for index in range(number_of_elements):
                #st.write(index)
                number_conc = len(concarray)
                if (number_conc==0): #first slider - always 1 to 100
                    IR_conc= st.sidebar.slider(
                    "[%] for:" + session_state.IR_select[index] , 0, 100,step=10)
                else:
                    if  (number_conc< number_of_elements-1):
                        Sum_conc=0
                        for i in range(number_conc):
                            Sum_conc=Sum_conc+concarray[i]
                        if (Sum_conc>100): Sum_conc=100

                        IR_conc= st.sidebar.slider(
                        "[%] for:" + session_state.IR_select[index] , 0, 100-Sum_conc,value=0,step=10)
                    else:
                        Sum_conc=0
                        for i in range(number_conc):
                            if (Sum_conc>100): Sum_conc=100
                            Sum_conc=Sum_conc+concarray[i]

                        IR_conc=100-Sum_conc
                        st.sidebar.write("[%] for:"+ session_state.IR_select[index] + ": "+str(IR_conc)+ "%")

                concarray.append(IR_conc)
# -----   TABLE FOR USER TO MONITOR SPECTRA INPUT FOR DESIRED OC CONSTANTS --------THINK ABOUT THIS

            index=[session_state.IR_select[i] for i in range(number_of_elements)]

            dfComp=pd.DataFrame(concarray,index=index, columns=['Concentration'])

            st.header('Model Spectrum Parameters')
            st.table(dfComp)

            if (number_of_elements>=1 ):
                    if (st.sidebar.button("Start Calculation")):
                        IRmodel=StartCalculation(session_state.IR_select,concarray)
