import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.set_page_config (layout="wide")

st.markdown("<h1 style='text-align: center;'>CUMA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>METAL MANUFACTURING SA DE CV</h4>", unsafe_allow_html=True)
st.divider()

st.markdown("<h4 style='text-align: center;'> Production Master Planning </h4>", unsafe_allow_html=True)
st.subheader("")

# Inicializar variables, cliente_input, user_name
if 'Production_master_plan' not in st.session_state :
    st.session_state.Production_master_plan= ''
    
    
conn = st.connection("gsheets", type=GSheetsConnection)

Production_master_plan = conn.read(worksheet="Production_MasterPlan",ttl=5)
Production_master_plan = Production_master_plan.dropna(how = 'all')
st.session_state.Production_master_plan= pd.DataFrame(Production_master_plan)

st.subheader("Production Master Planning Currently ...")
st.write(st.session_state.Production_master_plan)