import streamlit as st
import pandas as pd

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
    return pd.read_excel("Prueba_VPD.xlsx")

# Configurar el menú de la aplicación
st.set_page_config(page_title="Presupuesto - 2025 VPD", layout="wide")

# Crear las páginas
def pagina_principal():
    st.title("Presupuesto - 2025 VPD")

def pagina_vpd():
    st.title("VPD - Presupuesto")
    
    # Cargar datos
    datos = cargar_datos()
    
    # Crear filtros
    st.sidebar.header("Filtros")
    area = st.sidebar.selectbox("Seleccionar Área (vpd_area):", options=datos['vpd_area'].unique())
    pais = st.sidebar.selectbox("Seleccionar País:", options=datos['pais'].unique())
    total_min = st.sidebar.number_input("Monto mínimo (Totales):", min_value=0, value=0)

    # Filtrar datos
    datos_filtrados = datos[
        (datos['vpd_area'] == area) &
        (datos['pais'] == pais) &
        (datos['total'] >= total_min)
    ]
    
    # Mostrar tabla filtrada
    st.dataframe(datos_filtrados)

def pagina_vpf():
    st.title("VPF - Presupuesto")
    st.write("Esta página estará disponible próximamente.")

def pagina_vpo():
    st.title("VPO - Presupuesto")
    st.write("Esta página estará disponible próximamente.")

def pagina_vpe():
    st.title("VPE - Presupuesto")
    st.write("Esta página estará disponible próximamente.")

def pagina_pe():
    st.title("PE - Presupuesto")
    st.write("Esta página estará disponible próximamente.")

def pagina_consolidado():
    st.title("Consolidado - Presupuesto")
    st.write("Esta página estará disponible próximamente.")

# Menú de navegación con selectbox
menu = st.sidebar.selectbox(
    "Selecciona una página:",
    ["Inicio", "VPD", "VPF", "VPO", "VPE", "PE", "Consolidado"]
)

# Mostrar contenido según autenticación
if menu == "Inicio":
    if verificar_contraseña("Inicio"):
        pagina_principal()
elif menu == "VPD":
    if verificar_contraseña("VPD"):
        pagina_vpd()
elif menu == "VPF":
    if verificar_contraseña("VPF"):
        pagina_vpf()
elif menu == "VPO":
    if verificar_contraseña("VPO"):
        pagina_vpo()
elif menu == "VPE":
    if verificar_contraseña("VPE"):
        pagina_vpe()
elif menu == "PE":
    if verificar_contraseña("PE"):
        pagina_pe()
elif menu == "Consolidado":
    if verificar_contraseña("Consolidado"):
        pagina_consolidado()
