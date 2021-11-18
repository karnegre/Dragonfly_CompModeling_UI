### JUST AN EXAMPLE: please feel free to take this down whatever path you like
import streamlit as st

def linearmixingmodel(ConcenArray,ReflectArray,wavelength):
    m_ix=0
    for ix_con in range(len(ConcenArray)):
        m_ix+=ConcenArray[ix_con]*ReflectArray[ix_con]
    return m_ix
