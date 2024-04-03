import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.set_page_config (
    page_title="Multipage App",
    page_icon="📎",
    layout="wide"
)

st.title("Main")


conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<h1 style='text-align: center;'>CUMA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>METAL MANUFACTURING SA DE CV</h4>", unsafe_allow_html=True)
st.divider()

st.markdown("<h4 style='text-align: center;'> RFQ creation </h4>", unsafe_allow_html=True)
st.subheader("")

# Inicializar variables, cliente_input, user_name
if 'Master_plan' not in st.session_state or 'clientes_df'not in st.session_state:
    st.session_state.Master_plan= ''
    st.session_state.clientes_df= ''


if 'client_input' not in st.session_state or 'user_name' not in st.session_state or 'descripcion' not in st.session_state or 'pm_asignado' not in st.session_state or 'rfq_inquiry_date' not in st.session_state or 'rfq_mail' not in st.session_state or 'numero_RFQ' not in st.session_state:
    st.session_state.client_input = ''
    st.session_state.user_name = ''
    st.session_state.descripcion = ''
    st.session_state.pm_asignado = ''
    st.session_state.rfq_inquiry_date = ''
    st.session_state.rfq_mail = ''
    st.session_state.numero_RFQ = ''  

if 'tentative_delivery_date' not in st.session_state or 'number_of_operations'not in st.session_state or 'number_of_operations'not in st.session_state or 'selected_fabrication_order'not in st.session_state:
    st.session_state.tentative_delivery_date= ''
    st.session_state.number_of_operations= ''
    st.session_state.selected_fabrication_order= ''

# Mostrar dataframes Master_plan & Clientes_df


Master_plan = conn.read(worksheet="Master_plan",ttl=5)
Master_plan = Master_plan.dropna(how = 'all')
st.session_state.Master_plan= pd.DataFrame(Master_plan)

clientes_df = conn.read(worksheet="Fixed_data", ttl=5)
clientes_df = clientes_df.dropna(how = 'all')
st.session_state.clientes_df= pd.DataFrame(clientes_df)

st.subheader("Master Plan Currently ...")
st.write(st.session_state.Master_plan)

st.subheader("Control clientes")
st.write(st.session_state.clientes_df)
