import numpy as np              # standard numerical recipes library
import matplotlib.pyplot as plt # standard plotting library
import pandas as pd             # standard excel-style arrays library
import shutil
import os
import os.path
import streamlit as st
import glob as glob

htmlfilenames=[]
deltawave=0.001
interpwaves= np.arange(0.4,2.6,deltawave)

path="C:\OC_App\Reflectance\ChapterO_OrganicCompounds"

ASDFR_fname=glob.glob('C:\OC_App\Reflectance\ChapterO_OrganicCompounds\*ASDFR*AREF.txt')
ASDHR_fname=glob.glob('C:\OC_App\Reflectance\ChapterO_OrganicCompounds\*ASDHR*AREF.txt')
# NIC4_fname=glob.glob('C:\OC_App\Reflectance\ChapterO_OrganicCompounds\*NIC4*RREF.txt')

def getUSGSDOI():

    global ASDFR_fname
    global ASDHR_fname
    global htmlfilenames

    for f in ASDFR_fname:
        base=os.path.basename(f)
        base2=os.path.splitext(base)[0]
        basef= base2[9:]
        htmlfilenames.append(basef)

    for f in ASDHR_fname:
        base=os.path.basename(f)
        base2=os.path.splitext(base)[0]
        basef= base2[9:]
        htmlfilenames.append(basef)


# getUSGSDOI()
st.write(htmlfilenames)
# tempname=glob.glob('C:\OC_App\Reflectance\mixing\IR_dirty\ASDHR\t\*.txt')
# for t in tempname:
#     thiscompound=t[t.rfind("\\"):t.find("_",t.rfind("\\"))] #grabbing the name of the compound from the filename
#     st.write(thiscompound)

dirtyIR_path="C:\\OC_App\Reflectance\\mixing\\IR_dirty\\USGS_OrganicsCombined"
cleanIR_path="C:\\Users\\negrek1\\Desktop\\ASDHRRT - Clean"


# The purpose of this script is to:
# 1. Read files from USGS in local
# 2. Skip if already in directory or grab info+wave and plop into csv with file name= compound
# 3. Clean file and throw into clean IR
# 4. Link file to metadata to somehow propagate IR lib.....................




# -------------------------------------------------------
def getUSGS():
    for f in ASDFR_fname:
        wave=wave1.copy()
        thiscompound=f[f.rfind("\\")+10:f.find("_",f.rfind("\\")+10)] #grabbing the name of the compound from the filename
        thisspec=pd.read_csv(f,skiprows=1,names=['r'])
        wave['r']=thisspec
        wave.set_index(['wave_um'],inplace=True)#
        wave.to_csv('C:\\OC_App\Reflectance\\mixing\\IR_dirty\\ASDFR\\' + str(thiscompound) + '.txt', sep='\t')


    for f in ASDHR_fname:
        wave=wave1.copy()
        thiscompound=f[f.rfind("\\")+10:f.find("_A",f.rfind("\\")+10)]
        # tempcomp="K"
        # if tempcomp in thiscompound:
        #     templist=thiscompound
        #     # st.write(templist)
        # st.write(templist)
        # for j in templist:
        thisspec=pd.read_csv(f,skiprows=1,names=['r'])
        wave['r']=thisspec
        wave.set_index(['wave_um'],inplace=True)#
        wave.to_csv('C:\\OC_App\Reflectance\\mixing\\IR_dirty\\ASDHR\\temp\\' + str(thiscompound) + '.txt', sep='\t')

    for f in ASDHR_fname:

        wave=wave1.copy()
        thiscompound=f[f.rfind("\\")+10:f.find("_",f.rfind("\\")+10)] #grabbing the name of the compound from the filename
        thisspec=pd.read_csv(f,skiprows=1,names=['r'])
        wave['r']=thisspec
        wave.set_index(['wave_um'],inplace=True)#
        wave.to_csv('C:\\OC_App\Reflectance\\mixing\\IR_dirty\\ASDHR\\rt\\' + str(thiscompound) + '.txt', sep='\t')

    for f in NIC4_fname:
        wave=wave1.copy()
        thiscompound=f[f.rfind("\\")+10:f.find("_",f.rfind("\\")+10)] #grabbing the name of the compound from the filename
        thisspec=pd.read_csv(f,skiprows=1,names=['r'])
        wave['r']=thisspec
        wave.set_index(['wave_um'],inplace=True)#
        wave.to_csv('C:\\OC_App\Reflectance\\mixing\\IR_dirty\\NIC4\\' + str(thiscompound) + '.txt', sep='\t')
#---------------------------------------------------------------------------------------------------------------------
def renameUSGS():
    for file in os.listdir("C:\\Users\\negrek1\\Desktop\\ASDHRRT\\"):
        if os.path.isfile(os.path.join("C:\\Users\\negrek1\\Desktop\\ASDHRRT\\", file)):
            if file.endswith(".txt"):
                source = "C:\\Users\\negrek1\\Desktop\\ASDHRRT\\" + file
                thiscompound=file[file.rfind("\\")+10:file.find("_",file.rfind("\\")+10)]
                new = "C:\\Users\\negrek1\\Desktop\\ASDHRRT\\" + thiscompound + ".txt"
                os.rename(source,new)
                st.write(new)

#--------------------------------------------------------------------------
def cleanUSGS():
    for file in os.listdir("C:\\Users\\negrek1\\Desktop\\ASDHRRT\\"):
        if os.path.isfile(os.path.join("C:\\Users\\negrek1\\Desktop\\ASDHRRT\\", file)):
            if file.endswith(".txt"):
                dfDirty= pd.read_csv(os.path.join("C:\\Users\\negrek1\\Desktop\\ASDHRRT\\",file),sep='\t')
                interp=np.interp(interpwaves,dfDirty.wave_um,dfDirty.r)
                dfClean=pd.DataFrame(list(zip(interpwaves,interp)),columns=['wave','r'])
                dfClean.to_csv(os.path.join(cleanIR_path,file),index=False)
#--------------------------------------------------------------------------
def getnames():
    CompNameList=[]
    for name in os.listdir("C:\\OC_App\\Reflectance\\CRISM\\"):
        if os.path.isfile(os.path.join("C:\\OC_App\\Reflectance\\CRISM\\", name)):
            if name.endswith(".txt"):
                base=os.path.basename(name)
                base2=os.path.splitext(base)[0]
                basef= base2[15:]
                CompNameList.append(basef)
                df=pd.DataFrame(CompNameList)
    df.to_excel("C:\\OC_App\\Reflectance\\mixing\\done.xlsx")
# --------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
def cleanCrism():
    for file in os.listdir("C:\\OC_App\\Reflectance\\CRISM\\"):
        if os.path.isfile(os.path.join("C:\\OC_App\\Reflectance\\CRISM\\", file)):
            if file.endswith(".txt"):
                dfDirty= pd.read_csv(os.path.join("C:\\OC_App\\Reflectance\\CRISM\\",file),sep='\t')
                interp=np.interp(interpwaves,dfDirty.wave_um,dfDirty.r)
                dfClean=pd.DataFrame(list(zip(interpwaves,interp)),columns=['wave','r'])
                base=os.path.basename(file)
                basef= base[15:]
                st.write(basef)
                st.write(dfClean)
                dfClean.to_csv(os.path.join(cleanIR_path,basef),index=False)

cleanUSGS()
