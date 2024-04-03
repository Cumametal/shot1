# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st. set_page_config(layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<h1 style='text-align: center;'>CUMA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>METAL MANUFACTURING SA DE CV</h4>", unsafe_allow_html=True)
st.divider()

st.markdown("<h4 style='text-align: center;'> Traveller </h4>", unsafe_allow_html=True)
st.subheader("")

# Inicializar variables, cliente_input, user_name

if 'client_input' not in st.session_state or 'user_name' not in st.session_state or 'descripcion' not in st.session_state or 'pm_asignado' not in st.session_state or 'rfq_inquiry_date' not in st.session_state or 'rfq_mail' not in st.session_state or 'numero_RFQ' not in st.session_state:
    st.session_state.client_input = ''
    st.session_state.user_name = ''
    st.session_state.descripcion = ''
    st.session_state.pm_asignado = ''
    st.session_state.rfq_inquiry_date = ''
    st.session_state.rfq_mail = ''
    st.session_state.numero_RFQ = '' 
    
if 'Production_finish_date' not in st.session_state or 'number_of_operations'not in st.session_state or 'Fabrication_order_number' not in st.session_state or 'selected_fabrication_order'not in st.session_state:
    st.session_state.Production_finish_date= ''
    st.session_state.number_of_operations= ''
    st.session_state.selected_fabrication_order= ''
    st.session_state.Fabrication_order_number= ''


# Mostrar dataframes Master_plan and selected_fabrication_order

st.subheader("Master_plan")
Master_plan = conn.read(worksheet="Master_plan",ttl=5)
Master_plan = Master_plan.dropna(how = 'all')
st.write(Master_plan.tail(5))

# Mostrar dataframe Master_traveller lo que contiene antes de agregar numero de operaciones

# Mostrar dataframes Master_traveller 

st.subheader("Master_traveller")
Master_traveller = conn.read(worksheet="Master_traveller",ttl=5)
Master_traveller = Master_traveller.dropna(how = 'all')
st.write(Master_traveller)

General_operations = conn.read(worksheet="Fixed_data", usecols=[12] , ttl=5)
General_operations = General_operations.dropna(how = 'all')

#------------------------------------------------------------------------------------------


Master_plan_df = pd.DataFrame(Master_plan)
Master_traveller_df = pd.DataFrame(Master_traveller)
#st.session_state.Master_traveller_df = Master_traveller_df

# Función para extraer valores basados en el estado "Open"
def extract_open_values(Master_plan_df):
    # Filtrar el DataFrame por el estado "Open"
    Master_plan_df_open_data = Master_plan_df[Master_plan_df['RFQ_status'] == 'Open']
    if not Master_plan_df_open_data.empty:
        # Guardar todas las columnas necesarias en session_state
        for column_name in ['Fabrication_order_number', 'Customer', 'Description', 'Part_number']:
            st.session_state[column_name] = Master_plan_df_open_data[column_name]
        #st.write("Master Plan Open Data", Master_plan_df_open_data)

# Llamar a la función para guardar los valores
extract_open_values(Master_plan_df)



# Mostrar los datos guardados en un DataFrame
if 'Fabrication_order_number' in st.session_state:
    open_data = pd.DataFrame({
        'Fabrication_order_number': st.session_state['Fabrication_order_number'],
        'Customer': st.session_state['Customer'],
        'Part_number': st.session_state['Part_number'],
        'Description': st.session_state['Description']
    })
    

else:
    st.write("No hay datos con el estado 'Open'.")

#-----------------------------------------------------------------------------------------------------------------------------------
# Actualizar Master_traveller con Master_plan_open_data

st.write("Open Data", open_data)


#Funcion para actualizar Master_traveller_df con nuevos "open"

def combinar_dataframes(Master_traveller_df, open_data):
    # Combinar los DataFrames usando merge
    combined_df = pd.merge(Master_traveller_df, open_data, how='outer', indicator=True)
    
    # Filtrar las filas que están solo en open_data
    new_rows = combined_df[combined_df['_merge'] == 'right_only'][open_data.columns]
    
    # Agregar las filas nuevas a Master_traveller_df
    Master_traveller_df = pd.concat([Master_traveller_df, new_rows], ignore_index=True)
    
    # Eliminar la columna de indicador
    #Master_traveller_df.drop('_merge', axis=1, inplace=True)
    
    return Master_traveller_df

actualizar_mt = st.button("Actualizar Master_traveller_df" )

if actualizar_mt:
 # Show the updated "Master_traveller_df" DataFrame
    st.session_state.Master_traveller_df = combinar_dataframes(Master_traveller_df, open_data)
    st.write("Updated Master_traveller_df", st.session_state.Master_traveller_df)

#------------------------------------------------------------------------------------------------------------------------------------------


st.write("")

# Boton de seleccionar orden de fabricación para editar

def fab_order():
    st.session_state.selected_fabrication_order = st.session_state.fab_order_key
    st.session_state.fab_order_key = None

if 'Fabrication_order_number' in st.session_state:
    selected_fabrication_order = st.selectbox('Seleccionar orden de fabricación', st.session_state['Fabrication_order_number'].unique(), index=None, placeholder="Selecciona numero de órden de fabricación", on_change=fab_order, key='fab_order_key' )
    st.warning(f'Orden de fabricación seleccionada: { st.session_state.selected_fabrication_order}')
    

# ----------------------------------------------------------------------------------------------------------------------------------------

#Entrada de fecha para fecha tentativa de entrega 
    
    
def Production_finish_datedate():
    st.session_state.Production_finish_date = st.session_state.Production_finish_date_key
    st.session_state.Production_finish_date_key = None

Production_finish_date = st.date_input("Fecha para terminar la pieza", format="YYYY.MM.DD", value=None, key='Production_finish_date_key', on_change=Production_finish_datedate)

st.warning(f'Fecha elegida para terminar la pieza: {st.session_state.Production_finish_date}')
st.divider()

# ----------------------------------------------------------------------------------------------------------------------------------------

# Boton de creacion de columas por número de operaciones requeridas



def create_operation_columns():
    # Generate column names based on number_of_operations
    column_names = []
    for i in range(1, st.session_state.number_of_operations + 1):
        process_col = f"process_{i}"
        operation_status_col = f"operation_status{i}"
        machine_hr_col = f"machine_hr{i}"
        labour_hours_col = f"labour_hours{i}"
        picture_col = f"picture{i}"

        # Use the generated column names as needed
        st.write(f"Operación {i}, columas creadas")
        st.write(process_col," --- ", operation_status_col," --- ", machine_hr_col," --- ", labour_hours_col," --- ", picture_col)
        
        # Add the generated column names to the list
        column_names.extend([process_col, operation_status_col, machine_hr_col, labour_hours_col, picture_col])

    return column_names



def num_of_op():
     st.session_state.number_of_operations = st.session_state.num_of_op_key

st.number_input("Numero de operaciones requeridas", value=None, key='num_of_op_key', on_change=num_of_op, placeholder="Escribe un número entero...",step= 1)
st.warning(f'Numero de operaciones a cargar: {st.session_state.number_of_operations}')

# Assuming df is your existing DataFrame
if st.button("Crear Operaciones"):

    column_names = create_operation_columns()
    for col_name in column_names:
        if col_name in st.session_state.Master_traveller_df.columns:
            # Update the existing column
             pass
        else:
            # Add a new column
            st.session_state.Master_traveller_df[col_name] = ""

    st.write(st.session_state.Master_traveller_df)

# Dictionary to store selected values for each process_col
selected_values = {}

# Iterate over the range of number_of_operations and save selected values
for i in range(1, st.session_state.number_of_operations + 1):
    process_col = f"process_{i}"
    selected_operation_key = f"selected_operation_{process_col}"
    selected_values[process_col] = st.selectbox(f"Select operation for {process_col}", General_operations, index=None, placeholder="Selecciona ")
    st.session_state.Master_traveller_df.loc[st.session_state.Master_traveller_df['Fabrication_order_number'] == st.session_state.selected_fabrication_order, process_col] = selected_values[process_col]

# Display selected values
for process_col, selected_value in selected_values.items():
    st.write(f"{process_col} = {selected_value}")

st.write(st.session_state.Master_traveller_df)
st.write(General_operations)






# Agregar toogle para agregar comentarios importantes * General_comments



# Mostrar los datos a cargar

st.markdown("<h4 style='text-align: center;'>Datos a cargar </h4>", unsafe_allow_html=True)

update_data = st.button("Actualizar" )


# Restablecer valores cuando se agregan datos a df
    
if update_data:

# Write the updated data to the sheet starting from cell A1
    conn.update(worksheet="Master_traveller", data=st.session_state.Master_traveller_df)

    st.success("datos actualizados")



#-------------------------------------------------------

# def create_operation_columns():
#     # Generate column names based on number_of_operations
#     for i in range(1, st.session_state.number_of_operations + 1):
#         process_col = f"process_{i}"
#         operation_status_col = f"operation_status{i}"
#         machine_hr_col = f"machine_hr{i}"
#         labour_hours_col = f"labour_hours{i}"
#         picture_col = f"picture{i}"

#         # Use the generated column names as needed
#         st.write(f"Operación {i}, columas creadas")
#         st.write(process_col," --- ", operation_status_col," --- ", machine_hr_col," --- ", labour_hours_col," --- ", picture_col)




# if st.button("Create Columns"):
#     create_operation_columns()   

#------------------------------------------



# def update_values():
#     # Update the values for each set of columns
#     for i in range(1, st.session_state.number_of_operations + 1):
#         process_val = st.session_state.get(f"process_input_{i}", "")
#         operation_status_val = st.session_state.get(f"operation_status_input_{i}", "")
#         machine_hr_val = st.session_state.get(f"machine_hr_input_{i}", "")
#         labour_hours_val = st.session_state.get(f"labour_hours_input_{i}", "")
#         picture_val = st.session_state.get(f"picture_input_{i}", "")

#         # Use the values as needed, for example, print them
#         st.write(f"Process {i}: {process_val}")
#         st.write(f"Operation Status {i}: {operation_status_val}")
#         st.write(f"Machine HR {i}: {machine_hr_val}")
#         st.write(f"labour_hours  {i}: {labour_hours_val}")
#         if picture_val is not None:
#             st.image(picture_val)

# if st.button("Update Values"):
#     update_values()


# Boton para crear RFQ

# if st.button("Crear RFQ"):
#      actualizar_consecutivo(st.session_state.Datos)
#      st.success(f"Nuevo número de RFQ para el cliente {st.session_state.Datos}: {st.session_state.numero_RFQ}")




# new_data = {
#     "RFQ_num": [st.session_state.numero_RFQ],
#     "RFQ_mail": [st.session_state.rfq_mail],
#     "RFQ_inquiry_date": [st.session_state.rfq_inquiry_date],
#     "PM_asignado": [st.session_state.pm_asignado],
#     "Cliente": [st.session_state.Datos],
#     "Usuario":[st.session_state.user_name],
#     "Descripcion": [st.session_state.descripcion],
#     "Status": [st.session_state.order_status]
# }   

#my_df = pd.DataFrame(new_data)

#st.write(my_df)
#st.warning("Revisar si los datos están correctos para poder cargarlos al sistema y confirmar")


#Agregar datos a la base principal RFQ Control

#add_data = st.button("Agregar datos" )


# Restablecer valores cuando se agregan datos a df
    
# if add_data:
#     rfq_control = rfq_control.append(my_df, ignore_index=True)
#     st.header("New File")
#     st.write(rfq_control)
#     conn.update(worksheet="1 rfq control", data= rfq_control)

    




    