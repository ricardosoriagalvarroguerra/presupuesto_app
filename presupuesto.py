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

# Crear la página con ambas vistas
def pagina_vpo():
    st.title("VPO - Presupuesto")
    
    # Cargar datos
    datos = cargar_datos()

    # Agregar selectbox para seleccionar la vista
    vistas = ["Presupuesto", "Presupuesto K2B"]
    vista_seleccionada = st.selectbox("Seleccionar Vista:", vistas)

    if vista_seleccionada == "Presupuesto":
        # Mostrar tabla original con filtros
        st.subheader("Presupuesto")

        # Crear filtros en la barra lateral
        pais = st.sidebar.multiselect("Seleccionar País(es):", options=datos['pais'].unique(), default=datos['pais'].unique())
        tipo_objetivo = st.sidebar.multiselect("Seleccionar Tipo(s) de Objetivo:", options=datos['tipo_objetivo'].unique(), default=datos['tipo_objetivo'].unique())
        subcategoria = st.sidebar.multiselect("Seleccionar Subcategoría(s):", options=datos['subcategoria'].unique(), default=datos['subcategoria'].unique())
        item_presupuesto = st.sidebar.multiselect("Seleccionar Item(s) de Presupuesto:", options=datos['item'].unique(), default=datos['item'].unique())

        # Filtrar datos
        datos_filtrados = datos[
            (datos['pais'].isin(pais)) &
            (datos['tipo_objetivo'].isin(tipo_objetivo)) &
            (datos['subcategoria'].isin(subcategoria)) &
            (datos['item'].isin(item_presupuesto))
        ]

        # Calcular el total
        total_monto = datos_filtrados['sum_monto'].sum()

        # Mostrar el total
        st.metric(label="Total (sum_monto)", value=f"{total_monto:,.2f}")

        # Mostrar la tabla filtrada
        if datos_filtrados.empty:
            st.warning("No se encontraron datos para los filtros seleccionados.")
        else:
            st.dataframe(datos_filtrados)

    elif vista_seleccionada == "Presupuesto K2B":
        st.subheader("Presupuesto K2B")

        # Filtrar para consolidar únicamente las misiones
        misiones = datos[datos['categoria'] == 'Misiones']

        # Consolidar por país, categoría y subcategoría
        consolidado = misiones.groupby(['pais', 'categoria', 'subcategoria'], as_index=False)['sum_monto'].sum()

        # Calcular totales por país
        totales_por_pais = consolidado.groupby('pais', as_index=False)['sum_monto'].sum()
        total_general = totales_por_pais['sum_monto'].sum()

        # Mostrar el diseño estilizado
        st.write(f"### Total General: {total_general:,.2f}")

        for pais in totales_por_pais['pais'].unique():
            # Crear contenedor expandible por país
            with st.expander(f"{pais} - Total: {totales_por_pais[totales_por_pais['pais'] == pais]['sum_monto'].values[0]:,.2f}"):
                # Obtener las categorías del país
                categorias_pais = consolidado[consolidado['pais'] == pais]['categoria'].unique()
                for categoria in categorias_pais:
                    # Mostrar la categoría como un subtítulo
                    st.markdown(f"**{categoria}**")
                    
                    # Mostrar las subcategorías y montos de la categoría
                    subcategorias_categoria = consolidado[(consolidado['pais'] == pais) & (consolidado['categoria'] == categoria)]
                    for _, row in subcategorias_categoria.iterrows():
                        st.markdown(f"- {row['subcategoria']}: **{row['sum_monto']:,.2f}**")

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
