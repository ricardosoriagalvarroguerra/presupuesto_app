import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

# Configurar contraseñas por página
PASSWORDS = {
    "Inicio": "password_inicio",
    "VPD": "password_vpd",
    "VPF": "password_vpf",
    "VPO": "password_vpo",
    "VPE": "password_vpe",
    "PE": "password_pe",
    "Consolidado": "password_consolidado"
}

# Función para verificar contraseña
def verificar_contraseña(pagina):
    st.sidebar.header("Autenticación")
    contraseña = st.sidebar.text_input("Introduce la contraseña:", type="password")
    if contraseña == PASSWORDS[pagina]:
        st.sidebar.success("Acceso concedido")
        return True
    elif contraseña:
        st.sidebar.error("Contraseña incorrecta")
    return False

# Cargar los datos desde el archivo
def cargar_datos():
    return pd.read_excel("Prueba_VPD.xlsx", sheet_name="main_vpo")

# Configurar el menú de la aplicación
st.set_page_config(page_title="Presupuesto - 2025 VPD", layout="wide")

# Crear la página con vista desplegable
def pagina_vpo():
    st.title("VPO - Presupuesto")
    
    # Cargar datos
    datos = cargar_datos()

    # Filtrar datos para la vista consolidada de Misiones
    consolidado = datos[datos['categoria'] == 'Misiones'].groupby(
        ['pais', 'subcategoria'], as_index=False
    ).agg({'sum_monto': 'sum'})

    # Crear jerarquía para tabla desplegable
    consolidado['parent'] = consolidado['pais']
    consolidado.loc[consolidado['subcategoria'] == 'Misiones', 'parent'] = ''

    # Crear tabla en formato desplegable con st_aggrid
    st.subheader("Presupuesto K2B")

    # Configurar opciones para la tabla
    gb = GridOptionsBuilder.from_dataframe(consolidado)
    gb.configure_grid_options(treeData=True, groupDefaultExpanded=-1)
    gb.configure_column("pais", headerName="Presupuesto para K2B")
    gb.configure_column("subcategoria", headerName="Subcategoría")
    gb.configure_column("sum_monto", headerName="Importe", type=["numericColumn", "numberColumnFilter"])
    
    grid_options = gb.build()

    # Mostrar la tabla interactiva
    AgGrid(consolidado, gridOptions=grid_options, enable_enterprise_modules=True)

# Menú de navegación con selectbox
menu = st.sidebar.selectbox(
    "Selecciona una página:",
    ["Inicio", "VPD", "VPO", "VPF", "VPE", "PE", "Consolidado"]
)

# Mostrar contenido según autenticación
if menu == "Inicio":
    if verificar_contraseña("Inicio"):
        st.title("Presupuesto - 2025 VPD")
elif menu == "VPO":
    if verificar_contraseña("VPO"):
        pagina_vpo()
elif menu == "VPD":
    if verificar_contraseña("VPD"):
        st.title("VPD - Presupuesto")
        st.write("Esta página estará disponible próximamente.")
elif menu == "VPF":
    if verificar_contraseña("VPF"):
        st.title("VPF - Presupuesto")
        st.write("Esta página estará disponible próximamente.")
elif menu == "VPE":
    if verificar_contraseña("VPE"):
        st.title("VPE - Presupuesto")
        st.write("Esta página estará disponible próximamente.")
elif menu == "PE":
    if verificar_contraseña("PE"):
        st.title("PE - Presupuesto")
        st.write("Esta página estará disponible próximamente.")
elif menu == "Consolidado":
    if verificar_contraseña("Consolidado"):
        st.title("Consolidado - Presupuesto")
        st.write("Esta página estará disponible próximamente.")
