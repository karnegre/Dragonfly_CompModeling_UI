import streamlit as st
import os
import os.path
# ------------------------------------------------------
def app():

    st.header("Beta testers, provide feedback here!")

    contact_form = """
    <form action="https://formsubmit.co/Karla.Negrete@jhuapl.edu" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder ="Your name" required>
         <input type="email" name="email" placeholder ="Your email" required>
         <textarea name="message" placeholder="Your feedback here"></textarea>
         <button type="submit">Send</button>
     </form>
     """

    st.markdown(contact_form, unsafe_allow_html = True)

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    cwd =os.getcwd()
    path= os.path.join( cwd,'style','style.css')

    local_css(path)
