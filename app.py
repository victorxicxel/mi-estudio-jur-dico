import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Gestión Jurídica", layout="wide")

# Título de la app
st.title("⚖️ Panel de Control - Estudio Jurídico")

# Simulación de Base de Datos (En una app real, esto iría a un archivo o nube)
if 'casos' not in st.session_state:
    st.session_state.casos = [
        {"ID": "2024-001", "Cliente": "Juan Pérez", "Caso": "Divorcio", "Total": 1500, "Pagado": 500, "Estado": "En Trámite"},
        {"ID": "2024-002", "Cliente": "Maria Sosa", "Caso": "Despido", "Total": 2000, "Pagado": 2000, "Estado": "Cerrado"}
    ]

# --- BARRA LATERAL ---
st.sidebar.header("Menú de Navegación")
opcion = st.sidebar.selectbox("Ir a:", ["Resumen General", "Historial y Pagos", "Registrar Nuevo Caso"])

# --- OPCIÓN 1: RESUMEN GENERAL ---
if opcion == "Resumen General":
    st.subheader("Listado de Casos Activos")
    df = pd.DataFrame(st.session_state.casos)
    df["Pendiente"] = df["Total"] - df["Pagado"]
    
    # Mostrar métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Casos", len(df))
    col2.metric("Recaudado", f"${df['Pagado'].sum()}")
    col3.metric("Por Cobrar", f"${df['Pendiente'].sum()}", delta_color="inverse")
    
    st.table(df)

# --- OPCIÓN 2: HISTORIAL Y PAGOS ---
elif opcion == "Historial y Pagos":
    st.subheader("Consulta de Historial")
    id_buscar = st.selectbox("Seleccione el N° de Expediente", [c["ID"] for c in st.session_state.casos])
    
    caso_sel = next(item for item in st.session_state.casos if item["ID"] == id_buscar)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Cliente:** {caso_sel['Cliente']}")
        st.write(f"**Asunto:** {caso_sel['Caso']}")
    with col2:
        pendiente = caso_sel['Total'] - caso_sel['Pagado']
        st.warning(f"**Saldo Pendiente: ${pendiente}**")

    st.markdown("---")
    st.info("🕒 **Historial de Actuaciones**")
    st.write("- 01/01/2024: Apertura de expediente.")
    st.write("- 10/01/2024: Recepción de pruebas iniciales.")
    
# --- OPCIÓN 3: REGISTRAR ---
elif opcion == "Registrar Nuevo Caso":
    st.subheader("Añadir nuevo expediente")
    with st.form("nuevo_caso"):
        id_n = st.text_input("Número de Expediente")
        cl_n = st.text_input("Nombre del Cliente")
        as_n = st.text_input("Asunto/Carátula")
        tt_n = st.number_input("Honorarios Totales", min_value=0)
        enviar = st.form_submit_button("Guardar Caso")
        
        if enviar:
            st.session_state.casos.append({"ID": id_n, "Cliente": cl_n, "Caso": as_n, "Total": tt_n, "Pagado": 0, "Estado": "Abierto"})
            st.success("Caso guardado con éxito")
