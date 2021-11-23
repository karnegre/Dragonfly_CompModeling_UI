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
from plotly import express as px
import base64

from streamlit import caching
st.legacy_caching.clear_cache()

number_of_elements =0
CompDict={}
CompNameList=[]
SpecDF= pd.DataFrame()
dfLib= pd.DataFrame()
q=0.50;

#Platform independence
cwd =os.getcwd()
OCfiles_path= os.path.join( cwd,'cleaningcode','cleaned','OC')

session_state = SessionState.get(SpectraDict = [],CurrentSpectraIndex=0,Num_Spectra_Prev=0,OC_select=[],restart=0,IR_select=[])
# -----------------------------------------MAIN------------------------------------------------
def app():
    global OCfiles_selected
    if (st.sidebar.button("Restart OC Modeling")):
        session_state.restart=1
        session_state.OC_select=[]
        session_state.Num_Spectra_Prev=0
        session_state.CurrentSpectraIndex=0
        session_state.SpectraDict=[]
        session_state.GrainDict=[]
        OCfiles_selected =[]
        number_of_elements=0
        st.balloons()
    create_dictionary(OCfiles_path)
    process_sidebar()

# -----------------------------------------------------------------------------------------------------
@st.cache(suppress_st_warning=True)
def create_dictionary(path):
    global CompNameList
    global CompDict

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith(".txt"):
                namef= os.path.splitext(name)[0]
                CompNameList.append(namef)
                df = pd.read_csv(os.path.join(OCfiles_path,name))
                df.set_index(['wave'],drop=False,inplace=True)
                df['N']=[complex(n,k) for n,k in zip(df.n,df.k)]
                CompDict[namef]=df
# -----------------------------------------------------------------------------------------------------
def ReadOCLib():
    global dfLib
    #global OCfiles_selected
    global number_of_elements

    if (number_of_elements==0):
        return
    cwd =os.getcwd()
    filename = "Lib.xlsx"
    path_file = os.sep.join([cwd, filename])

    dfLib=pd.read_excel(path_file,sheet_name="O Library")
    st.header('Compound Information Table')

    if (number_of_elements==1):
        st.table(dfLib[dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[0])])
    elif (number_of_elements==2):
        st.table(dfLib[dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[0]) |
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[1])])
    elif (number_of_elements==3):
        st.table(dfLib[dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[0]) |
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[1])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[2])])
    elif (number_of_elements==4):
        st.table(dfLib[dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[0]) |
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[1])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[2])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[3])])
    elif (number_of_elements>=5):
        st.table(dfLib[dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[0]) |
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[1])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[2])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[3])|
        dfLib['Possible Compounds on Titans Surface'].str.match(session_state.OC_select[4])])

# ----------------------------------------

def createthismix(mix):
    global number_of_elements
    if (number_of_elements==2):
        thismix=[[a,b] for a,b in zip(mix[session_state.OC_select[0]],mix[session_state.OC_select[1]])]
    elif (number_of_elements==3):
        thismix=[[a,b,c] for a,b,c in zip(mix[session_state.OC_select[0]],mix[session_state.OC_select[1]],mix[session_state.OC_select[2]])]
    elif (number_of_elements==4):
        thismix=[[a,b,c,d] for a,b,c,d in zip(mix[session_state.OC_select[0]],mix[session_state.OC_select[1]],mix[session_state.OC_select[2]],mix[session_state.OC_select[3]])]
    elif (number_of_elements==5):
        thismix=[[a,b,c,d,e] for a,b,c,d,e in zip(mix[session_state.OC_select[0]],mix[session_state.OC_select[1]],mix[session_state.OC_select[2]],mix[session_state.OC_select[3]],mix[session_state.OC_select[4]])]
    else:
        thismix=[]

    return thismix
# ------------------------------------------------
def StartCalculation(files,S,p,mixesArray):
    global CompDict
    global number_of_elements
    i=0
    dataname=[session_state.OC_select[i] for i in range(number_of_elements)]
    datanamecombo='-'.join(dataname)
    icesstr=[]
    mix=pd.DataFrame({'wave':CompDict[session_state.OC_select[0]].wave})
    mix.set_index(mix.wave,inplace=True)
    result=pd.DataFrame(index=mix.index)
    visresult=pd.DataFrame()

    for i in range(number_of_elements):
        mix[session_state.OC_select[i]]=CompDict[session_state.OC_select[i]].N
    print(mix)

    for m in mixesArray:

        concentrations=[mm/100 for mm in m]
        thismix=createthismix(mix)
    #     thismix=[[a,b] for a,b in zip(mix[icesstr[0]],mix[icesstr[1]])] #mix in our case is CompDict
        colname=''
        colnamearray=[]
        for n,i in enumerate(session_state.OC_select):
            # to limit the amount of compounds to 5 possible selections by the user
            if(n<=4):
                if (n==number_of_elements-1):
                    colname+=str(m[n])[0:3]
                else:
                    colname+=str(m[n])[0:3]+"_"#[0:2]

        mix[colname]=[shkrtv.shkuratov_coarsemix(concentrations,a,p,S,w) for a,w in zip(thismix,mix.wave)]
        result[colname]=mix[colname]
        visresult[colname]=result[colname].copy().truncate(after=1.05)


    fig1 = px.line(visresult)
    fig1.update_xaxes(title_text='Wavelength (μm)')
    fig1.update_yaxes(title_text='Albedo')
    fig1.update_layout(legend_title_text='Concentrations')
    fig1.update_layout(showlegend=True, width=1100,height=700,margin= dict(l=1,r=1,b=1,t=1), font=dict(color='#383635', size=20))

    fig2 = px.line(result)
    fig2.update_xaxes(title_text='Wavelength (μm)')
    fig2.update_yaxes(title_text='Albedo')
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

# ----------------------------------------
def process_sidebar():

        global number_of_elements
        global OCfiles_selected
        global CompNameList
        global CompDict
        global SpecDF
        global grainarray

        OCList=[]

        st.sidebar.title('Optical Constants Modeling')

#----------------------ITEM 1: Select desired compounds---------------------------------------
        st.sidebar.header('Select Compounds')
        OCfile_list = CompNameList

        Group_list = ['Ice','Organic','Oceanic','Tholin','Higher Order Organic']
        Group_selected = st.sidebar.selectbox(label="Grouping",options=Group_list)

        cwd =os.getcwd()
        filename = "Lib.xlsx"
        path_file = os.sep.join([cwd, filename])
        Lib=pd.read_excel(path_file,sheet_name="O Library")

        GroupLib=Lib[Lib.Grouping.str.contains(Group_selected)]
        OCfile_list = GroupLib['Possible Compounds on Titans Surface'].tolist()
        OCfiles_selected = st.sidebar.multiselect(label="Compounds",options=OCfile_list)

        number_oc = len(OCfiles_selected)
        number_oc_statelist = len(session_state.OC_select)

        if (len(OCfiles_selected)>=1):
            for index in range(number_oc):
                #st.write(OCfiles_selected[index])
                if (number_oc_statelist>0):
                    #for ix in range(number_oc_statelist):

                        if not (OCfiles_selected[index] in session_state.OC_select):
                            #st.write('ADDED')
                            session_state.OC_select.append(OCfiles_selected[index])

                        #if not (session_state.OC_select[ix].str.contains(OCfiles_selected[index])):
                            #session_state.OC_select.append(OCfiles_selected[index])
                else:
                    if (session_state.restart==0):
                        session_state.OC_select.append(OCfiles_selected[index])

        if (session_state.restart==1):
            session_state.restart=0
        number_of_elements = len(session_state.OC_select)

        #To limit the amount of elements to 5. If user selects more than 5, its truncate to 5
        if (number_of_elements>5):
            number_of_elements=5

        if (number_of_elements==0):
            session_state.Num_Spectra_Prev=0
            session_state.CurrentSpectraIndex=0
            session_state.SpectraDict=[]
            session_state.GrainDict=[]

        ReadOCLib()

        if (number_of_elements>=2):
#-----------------------ITEM 2: Select # of spectra--------------------------------------
            st.sidebar.header('Select Number of Spectra')
            Num_Spectra= st.sidebar.number_input(
            "# of Spectra" ,min_value=1, max_value=5,step= 1, help= "Max is 5 spectra")
            # st.write(session_state.Num_Spectra_Prev)

            if (session_state.Num_Spectra_Prev>Num_Spectra):
                session_state.SpectraDict.pop()

            session_state.Num_Spectra_Prev=Num_Spectra
            arr=[]
            len1=len(session_state.SpectraDict)

            if (len1<Num_Spectra):
                for index in range(Num_Spectra):
                    if ((len1==0) or (index>=len1)):
                        for idx in range(number_of_elements):
                            if (idx<(number_of_elements-1)):
                                arr.append(0)
                            else:
                                arr.append(100)
                        session_state.SpectraDict.append(arr)

    #---------------------------ITEM 3: Select Spectrum to edit----------------------------------
            st.sidebar.header('Select Spectrum to edit')
            SpecPick = st.sidebar.selectbox('Which Spectrum?', [(i+1) for i in range(Num_Spectra)],index=session_state.CurrentSpectraIndex)
            SpecPick =SpecPick-1
            session_state.CurrentSpectraIndex=SpecPick

            concarray=[]
            number_conc=0

#---------------------ITEM 3A: GRAINSIZE----------------------------------------
            st.sidebar.subheader('Select Grain Sizes (μm)')
            grainarray=[]
            for i in range(number_of_elements):
                OC_grainsize_selected= st.sidebar.number_input(
                "Grain size for " + session_state.OC_select[i],min_value=10, max_value=500,step= 1, help= "Must be between 10-500 μm")
                grainarray.append(OC_grainsize_selected)

#---------------------ITEM 3B: CONCENTRATION----------------------------------------
            st.sidebar.subheader('Select Concentration')
            for index in range(number_of_elements):
                number_conc = len(concarray)
                if (number_conc==0): #first slider - always 1 to 100
                    OC_conc= st.sidebar.slider(
                    "Concentration [%] for " + session_state.OC_select[index] , 0, 100,step=10)
                else:
                    if  (number_conc< number_of_elements-1):
                        Sum_conc=0
                        for i in range(number_conc):
                            Sum_conc=Sum_conc+concarray[i]
                        if (Sum_conc>100): Sum_conc=100

                        OC_conc= st.sidebar.slider(
                        "Concentration [%] for " + session_state.OC_select[index] , 0, 100-Sum_conc,value=0,step=10)
                    else:
                        Sum_conc=0
                        for i in range(number_conc):
                            if (Sum_conc>100): Sum_conc=100
                            Sum_conc=Sum_conc+concarray[i]

                        OC_conc=100-Sum_conc
                        st.sidebar.write("Concentration for "+ session_state.OC_select[index] + " is "+str(OC_conc)+ "%")

                concarray.append(OC_conc)
            session_state.SpectraDict[SpecPick]=concarray

# -----   TABLE FOR USER TO MONITOR SPECTRA INPUT FOR DESIRED OC CONSTANTS --------
            indexname= ["Spectrum #"+str(i+1) for i in range(Num_Spectra)]
            colname=[session_state.OC_select[i] for i in range(number_of_elements)]

            dfComp=pd.DataFrame(session_state.SpectraDict,columns=colname, index=indexname)
            dfGrain=pd.DataFrame(grainarray,index=colname,columns=["Grain size (μm)"])
            st.header("Spectrum Model Parameters")

            col1, col2 = st.columns((1,1))

            with col1:
                st.subheader("Grain Size Table")
                st.caption('Constant for all spectrum')
                st.table(dfGrain)

            with col2:
                st.subheader("Compound Concentration Table")
                st.caption('Compound Concentrations for each Spectrum')
                st.table(dfComp)

            if (number_of_elements>=2 ):
                    if (st.sidebar.button("Start Calculation")):
                        OCmix_grain=StartCalculation(session_state.OC_select,grainarray,q,session_state.SpectraDict)
