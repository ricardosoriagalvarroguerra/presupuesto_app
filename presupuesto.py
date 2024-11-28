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

# Crear la página con la nueva vista
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

        # Mostrar el diseño
        st.write(f"### Total General: {total_general:,.2f}")

        for pais in totales_por_pais['pais'].unique():
            # Mostrar el país y su total
            total_pais = totales_por_pais[totales_por_pais['pais'] == pais]['sum_monto'].values[0]
            st.write(f"**{pais} - Total: {total_pais:,.2f}**")

            # Mostrar las subcategorías y montos del país
            subcategorias_pais = consolidado[consolidado['pais'] == pais]
            for _, row in subcategorias_pais.iterrows():
                st.write(f"- {row['subcategoria']}: {row['sum_monto']:,.2f}")

        # Total General
        st.write(f"**Total General:** {total_general:,.2f}")

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
