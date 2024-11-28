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
    return pd.read_excel("Prueba_VPD.xlsx", sheet_name="main_vpo")

# Configurar el menú de la aplicación
st.set_page_config(page_title="Presupuesto - 2025 VPD", layout="wide")

# Crear la página con diseño estilizado
def pagina_vpo():
    st.title("VPO - Presupuesto")
    
    # Cargar datos
    datos = cargar_datos()

    # Agregar selectbox para seleccionar la vista
    vistas = ["Vista Original", "Presupuesto K2B"]
    vista_seleccionada = st.selectbox("Seleccionar Vista:", vistas)

    if vista_seleccionada == "Vista Original":
        # Mostrar tabla original con filtros
        st.subheader("Vista Original")
        st.dataframe(datos)
    
    elif vista_seleccionada == "Presupuesto K2B":
        st.subheader("Presupuesto K2B")

        # Filtrar para consolidar únicamente las misiones
        misiones = datos[datos['categoria'] == 'Misiones']

        # Consolidar por país y subcategoría
        consolidado = misiones.groupby(['pais', 'subcategoria'], as_index=False)['sum_monto'].sum()

        # Calcular totales por país
        totales_por_pais = consolidado.groupby('pais', as_index=False)['sum_monto'].sum()
        total_general = totales_por_pais['sum_monto'].sum()

        # Mostrar el diseño estilizado
        st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>Total General: {total_general:,.2f}</h2>", unsafe_allow_html=True)

        for pais in totales_por_pais['pais'].unique():
            # Mostrar el país como un título
            total_pais = totales_por_pais[totales_por_pais['pais'] == pais]['sum_monto'].values[0]
            st.markdown(f"<h3 style='color: #2E86C1;'>{pais} - Total: {total_pais:,.2f}</h3>", unsafe_allow_html=True)

            # Mostrar las subcategorías con un diseño estilizado
            subcategorias_pais = consolidado[consolidado['pais'] == pais]
            for _, row in subcategorias_pais.iterrows():
                st.markdown(
                    f"<p style='margin-left: 20px; color: #34495E;'>• {row['subcategoria']}: <b>{row['sum_monto']:,.2f}</b></p>",
                    unsafe_allow_html=True,
                )

        # Total General al final
        st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>Total General: {total_general:,.2f}</h2>", unsafe_allow_html=True)

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
