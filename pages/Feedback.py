import streamlit as st

# ------------------------------------------------------
def app():

    st.header("Beta testers, provide feedback here!")

    contact_form = "" <form action="https://formsubmit.co/your@email.com" method="POST">
     <input type="text" name="name" required>
     <input type="email" name="email" required>
     <button type="submit">Send</button>
     </form>""

     st.markdown (contact_form, unsafe_allow html = True)
