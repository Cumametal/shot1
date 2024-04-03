
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st. set_page_config(layout="wide")

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


# Función para actualizar el DataFrame y obtener el número de RFQ

def actualizar_consecutivo(cliente):
    print("Cliente ingresado:", cliente)
    print("Valores en la columna 'cliente':", clientes_df['Customer'].values)
    
    # Verificar si el cliente existe en el DataFrame
    if cliente in st.session_state.clientes_df['Customer'].values:
        st.write("Cliente encontrado en la base de datos.")
        # Obtener el índice del cliente en el DataFrame
        idx = st.session_state.clientes_df.index[st.session_state.clientes_df['Customer'] == cliente].tolist()[0]
        st.write("Índice del cliente encontrado:", idx)
        # Incrementar la columna 'consecutivo_de_cliente' en 1
        st.session_state.clientes_df.at[idx, 'Customer_consecutive'] += 1
        # Actualizar la columna 'orden_RFQ' del registro correspondiente
        st.session_state.clientes_df.at[idx, 'RFQ_order_number'] = f"{st.session_state.clientes_df.at[idx, 'Id_customer']}-{st.session_state.clientes_df.at[idx, 'Customer_consecutive']}"
        # Guardar el valor actualizado de 'orden_RFQ' en la variable 'numero_RFQ'
        st.session_state.numero_RFQ = st.session_state.clientes_df.at[idx, 'RFQ_order_number']
        st.success(f"Se ha actualizado el consecutivo para el cliente {cliente}. Número de RFQ: {st.session_state.numero_RFQ}")
        conn.update(worksheet="Fixed_data", data= st.session_state.clientes_df)
    else:
        print("Cliente no encontrado en la base de datos.")
        st.error(f"No se encontró el cliente {cliente} en la base de datos.")

# Función para mostrar orden_RFQ actual

def show_current_ordenRFQ(customer):
    # Verificar si el cliente existe en el DataFrame
    if customer in st.session_state.clientes_df['Customer'].values:
        # Obtener el índice del cliente
        idx = st.session_state.clientes_df.index[st.session_state.clientes_df['Customer'] == customer].tolist()[0]
        # Obtener el valor de 'orden_RFQ' correspondiente
        orden_RFQ = st.session_state.clientes_df.at[idx, 'RFQ_order_number']
        return orden_RFQ
    else:
        return None



# Entrada de dato para cliente_input
def customer():
    st.session_state.client_input = st.session_state.customer_key
    st.session_state.customer_key = None

client_input= st.selectbox('Selecciona Cliente', st.session_state.clientes_df['Customer'], index=None, placeholder="Selecciona cliente", key='customer_key', on_change=customer)
# client_input = st.selectbox('Cliente', ('ETM', 'WOLVENG', 'BOSCH','BRP','UL','CONTROL DIGITAL','3CON','BAKER HUGHES','PLASTICSMART',
#                                          'SAARGUMMI','EPS','NRMACHINING','CRG','KIMBERLY CLARK','DIICSA','DACOM','HARMAN','XOMERTRY',
#                                          'ICARUS','THYSSENKRUPP','SHUNK','IBERFLUID'), index=None, placeholder="Selecciona cliente", key='customer_key', on_change=customer)

st.write(f'Cliente seleccionado: {st.session_state.client_input}')

# Mostrar ultimo numero de orden_RFQ

if st.button("Mostrar Orden RFQ"):
    orden_RFQ = show_current_ordenRFQ(st.session_state.client_input)
    if orden_RFQ is not None:
        st.success(f"El valor actual de orden RFQ para {st.session_state.client_input} es: {orden_RFQ}")
    else:
        st.error(f"No se encontró el cliente {st.session_state.client_input} en la base de datos.")

st.divider()

# Entrada de dato para user_name

def username():
    st.session_state.user_name = st.session_state.user_name_key
    st.session_state.user_name_key = ''

st.text_input('Nombre y apellido de usuario', key='user_name_key', on_change=username, placeholder="Proporciona nombre + apellido")

st.write(f'Nombre de usuario proporcionado: {st.session_state.user_name}')
st.divider()
    
# Entrada de dato para descripcion

def description():
    st.session_state.descripcion = st.session_state.descripcion_key
    st.session_state.descripcion_key = ''

st.text_input('Descripción', key='descripcion_key', on_change=description, placeholder='Describe la pieza a fabricar')

st.write(f'Descripción proporcionada: {st.session_state.descripcion}')
st.divider()

# Entrada de dato para pm_asignado
def assigned_pm():
    st.session_state.pm_asignado = st.session_state.pm_asignado_key
    st.session_state.pm_asignado_key = None

pm_asignado = st.selectbox('Project Manager asignado', ('Rodrigo Ramirez', 'Elian Sanabria','Sergio Santos'), index=None, placeholder="Selecciona encargado", key='pm_asignado_key', on_change=assigned_pm)
st.write(f'Representante de CUMA para el proyecto: {st.session_state.pm_asignado}')
st.divider()

# Entrada de dato para rfq_inquiry_date
def inquiry_date():
    st.session_state.rfq_inquiry_date = st.session_state.rfq_inquiry_date_key
    st.session_state.rfq_inquiry_date_key = None

rfq_inquiry_date = st.date_input("Fecha en que se solicita RFQ", format="DD.MM.YYYY", value=None, key='rfq_inquiry_date_key', on_change=inquiry_date)

st.write(f'Fecha en que se solicita la cotización {st.session_state.rfq_inquiry_date}')
st.divider()

# Entrada de dato para RFQ_email

def email_keywords():
    st.session_state.rfq_mail = st.session_state.rfq_mail_key
    st.session_state.rfq_mail_key = ''

rfq_mail = st.text_input("Palabras clave de correo", placeholder="Texto para buscar en correo", key='rfq_mail_key', on_change=email_keywords)

st.write(f'Texto clave a buscar en el correo: {st.session_state.rfq_mail}')
st.divider()

# Creación de status como primer status = open

st.session_state.order_status = "Open"
st.write("El status de la orden comienza en: ", st.session_state.order_status)
st.divider()


# Boton para crear RFQ

if st.button("Crear RFQ"):
     actualizar_consecutivo(st.session_state.client_input)
     st.success(f"Nuevo número de RFQ para el cliente {st.session_state.client_input}: {st.session_state.numero_RFQ}")

# Mostrar los datos a cargar

st.markdown("<h4 style='text-align: center;'>Datos a cargar </h4>", unsafe_allow_html=True)

new_data = {
    "RFQ_order_number": [st.session_state.numero_RFQ],
    "RFQ_mail_keywords": [st.session_state.rfq_mail],
    "RFQ_inquiry_date": [st.session_state.rfq_inquiry_date],
    "PM_assigned": [st.session_state.pm_asignado],
    "Customer": [st.session_state.client_input],
    "User":[st.session_state.user_name],
    "Description": [st.session_state.descripcion],
    "RFQ_status": [st.session_state.order_status]
}   

my_df = pd.DataFrame(new_data)
st.warning("Revisar si los datos están correctos para poder cargarlos al sistema y confirmar")
st.write(my_df)



#Agregar datos a la base principal RFQ Control

add_data = st.button("Agregar datos" )


# Restablecer valores cuando se agregan datos a df
    
if add_data:
    Master_plan = Master_plan._append(my_df, ignore_index=True)
    st.header("New File")
    st.write(Master_plan.tail(5))
    conn.update(worksheet="Master_plan", data= Master_plan)
    # Reestablecer variables state
    st.session_state.client_input = ''
    st.session_state.user_name = ''
    st.session_state.descripcion = ''
    st.session_state.pm_asignado = ''
    st.session_state.rfq_inquiry_date = ''
    st.session_state.rfq_mail = ''
    st.session_state.numero_RFQ = '' 
    st.session_state.tentative_delivery_date= ''
    st.session_state.number_of_operations= ''
    st.session_state.selected_fabrication_order= ''







    