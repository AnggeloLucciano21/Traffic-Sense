"""
Panel de monitoreo y dashboard interactivo de TrafficSense (Streamlit).
Proporciona dos pestañas operativas:
1. '📹 Monitoreo en Vivo / Video': visualización en tiempo real, KPIs de aforo y alertas.
2. '⚙️ Configuración e Historial': calibración de línea virtual, auditoría y exportación CSV.
"""

from datetime import datetime
from pathlib import Path
import time
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

from src.config_loader import get_helmet_model_status, load_config
from src.database.db_manager import DatabaseManager
from src.pipeline import TrafficSensePipeline

# Configuración inicial de la página
st.set_page_config(
    page_title="TrafficSense — Monitoreo y Detección Vial",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para apariencia moderna y sobria
st.markdown("""
<style>
    .metric-card {
        background-color: #1e2129;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border-left: 4px solid #3b82f6;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #9ca3af;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #f3f4f6;
        font-weight: 700;
    }
    .status-badge-ok {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge-warning {
        background-color: rgba(234, 179, 8, 0.2);
        color: #eab308;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-badge-alert {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_system_components():
    """Inicializa la configuración y la base de datos de manera persistente en la sesión de Streamlit."""
    config = load_config()
    db = DatabaseManager(config.get("database", {}).get("db_path", "data/database/trafficsense.db"))
    return config, db


config, db = get_system_components()
status_info = get_helmet_model_status(config)

# ==============================================================================
# BARRA LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.title("🚦 TrafficSense")
    st.caption("UNSM — Proyectos de Inteligencia Artificial")
    st.divider()

    st.subheader("Estado del Sistema")
    st.write(f"**Dispositivo:** `{config.get('project', {}).get('target_device', 'cpu').upper()}`")
    st.write(f"**Detector Base:** `YOLO11n (COCO)`")
    st.write(f"**Tracker:** `ByteTrack`")

    if status_info["available"]:
        st.markdown('<span class="status-badge-ok">● MODELO CASCO ACTIVO</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge-warning">▲ SIN MODELO CASCO (Modo Base)</span>', unsafe_allow_html=True)
        st.caption("Aforo y tracking 100% operativos. Clasificación de casco pendiente de pesos entrenados.")

    st.divider()
    st.info("💡 **Consejo:** Para calibrar la línea virtual de conteo, diríjase a la pestaña 'Configuración e Historial'.")

# ==============================================================================
# TABS PRINCIPALES
# ==============================================================================
tab_monitor, tab_history = st.tabs(["📹 Monitoreo en Vivo / Video", "⚙️ Configuración e Historial"])

# ------------------------------------------------------------------------------
# PESTAÑA 1: MONITOREO
# ------------------------------------------------------------------------------
with tab_monitor:
    col_video, col_metrics = st.columns([7, 5])

    with col_video:
        st.subheader("Entrada de Video")
        
        # Buscar videos existentes en data/raw_videos/
        raw_videos_dir = Path("data/raw_videos")
        video_files = list(raw_videos_dir.glob("*.mp4")) + list(raw_videos_dir.glob("*.avi"))
        video_options = ["Subir archivo (.mp4 / .avi)"] + [str(v) for v in video_files]

        selected_source_type = st.selectbox("Seleccionar fuente de video:", video_options)

        video_path_to_process = None
        if selected_source_type == "Subir archivo (.mp4 / .avi)":
            uploaded_file = st.file_uploader("Cargar video de tráfico:", type=["mp4", "avi", "mov"])
            if uploaded_file is not None:
                temp_video_path = raw_videos_dir / f"upload_{uploaded_file.name}"
                temp_video_path.parent.mkdir(parents=True, exist_ok=True)
                with open(temp_video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                video_path_to_process = str(temp_video_path)
        else:
            video_path_to_process = selected_source_type

        col_btn1, col_btn2 = st.columns(2)
        start_processing = col_btn1.button("▶ Iniciar Procesamiento", use_container_width=True, type="primary")
        stop_processing = col_btn2.button("⏹ Detener", use_container_width=True)

        video_placeholder = st.empty()
        telemetry_placeholder = st.empty()

    with col_metrics:
        st.subheader("Métricas de Aforo en Tiempo Real")

        # 4 Tarjetas KPI
        kpi_col1, kpi_col2 = st.columns(2)
        with kpi_col1:
            kpi_vehiculos = st.empty()
            kpi_motos = st.empty()
        with kpi_col2:
            kpi_alertas = st.empty()
            kpi_cumplimiento = st.empty()

        # Gráfico horario
        st.subheader("Flujo Vehicular por Hora")
        chart_placeholder = st.empty()

        # Galería de evidencias recientes
        st.subheader("Últimas Infracciones Registradas")
        alerts_gallery_placeholder = st.empty()

    # Valores iniciales de KPIs antes de procesar
    initial_kpis = db.get_kpis()
    kpi_vehiculos.metric("Vehículos Totales", initial_kpis["total_vehiculos"])
    kpi_motos.metric("Motocicletas", initial_kpis["total_motos"])
    kpi_alertas.metric("Alertas sin Casco", initial_kpis["total_sin_casco"])
    kpi_cumplimiento.metric("% Cumplimiento", f"{initial_kpis['cumplimiento_pct']}%")

    # Renderizado de gráfico inicial
    df_hourly = db.get_hourly_counts()
    if not df_hourly.empty:
        chart_placeholder.bar_chart(df_hourly.pivot(index="hora_franja", columns="tipo_vehiculo", values="cantidad").fillna(0))
    else:
        chart_placeholder.info("Aún no hay datos de cruce registrados en la base de datos.")

    # Ejecución del bucle de procesamiento en vivo si se pulsa 'Iniciar'
    if start_processing and video_path_to_process:
        pipeline = TrafficSensePipeline(config=config)

        for frame_annotated, stats in pipeline.process_stream(
            source=video_path_to_process,
            save_db=True
        ):
            # Convertir frame BGR a RGB para renderizar en Streamlit
            frame_rgb = cv2.cvtColor(frame_annotated, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            # Actualizar KPIs
            kpi_vehiculos.metric("Vehículos Totales", stats["total_vehiculos"])
            kpi_motos.metric("Motocicletas", stats["motos_contadas"])
            kpi_alertas.metric("Alertas sin Casco", stats["total_alertas"])
            
            total_motos = stats["motos_contadas"]
            motos_sin_casco = stats["total_alertas"]
            cumpl_pct = round(((total_motos - motos_sin_casco) / max(1, total_motos)) * 100.0, 1) if status_info["available"] else 0.0
            kpi_cumplimiento.metric("% Cumplimiento", f"{cumpl_pct}%" if status_info["available"] else "N/A")

            # Barra de telemetría inferior
            telemetry_placeholder.caption(
                f"⏱ FPS: **{stats['fps']}** | "
                f"Sentido IN: **{stats['sentido_in']}** | Sentido OUT: **{stats['sentido_out']}** | "
                f"Estado Detector: `{stats['detector_casco']}`"
            )

            # Actualizar galería de evidencias si hay nuevas alertas
            recent_alerts = db.get_alertas(limit=3)
            if recent_alerts:
                with alerts_gallery_placeholder.container():
                    cols_gal = st.columns(len(recent_alerts))
                    for idx, al in enumerate(recent_alerts):
                        with cols_gal[idx]:
                            ruta = al.get("ruta_evidencia")
                            if ruta and Path(ruta).is_file():
                                st.image(str(ruta), caption=f"ID #{al['track_id']} - {al['hora']}")
                            else:
                                st.write(f"ID #{al['track_id']} ({al['hora']})")

            if stop_processing:
                break

# ------------------------------------------------------------------------------
# PESTAÑA 2: CONFIGURACIÓN E HISTORIAL
# ------------------------------------------------------------------------------
with tab_history:
    col_cfg, col_hist = st.columns([5, 7])

    with col_cfg:
        st.subheader("Parámetros de la Línea Virtual")
        st.caption("Ajuste las coordenadas para adaptarlas a la perspectiva de la vía.")

        p1_x = st.slider("P1 - X (Inicio)", 0, 1920, int(config["counting"]["line_p1"][0]))
        p1_y = st.slider("P1 - Y (Inicio)", 0, 1080, int(config["counting"]["line_p1"][1]))
        p2_x = st.slider("P2 - X (Fin)", 0, 1920, int(config["counting"]["line_p2"][0]))
        p2_y = st.slider("P2 - Y (Fin)", 0, 1080, int(config["counting"]["line_p2"][1]))

        st.subheader("Umbrales Algorítmicos")
        conf_thresh = st.slider("Umbral de Confianza YOLO", 0.1, 0.95, float(config["detection"]["confidence_threshold"]), 0.05)
        window_frames = st.slider("Ventana Temporal (N cuadros)", 4, 20, int(config["helmet"]["window_size_frames"]))
        min_votes = st.slider("Confirmación Mínima (K votos)", 2, window_frames, int(config["helmet"]["min_confirm_frames"]))

        st.subheader("Exportación de Datos (RF-09)")
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv_conteos_path = Path("data/output/reporte_conteos.csv")
            if st.button("Exportar Conteos CSV"):
                db.export_csv("conteos_vehiculares", csv_conteos_path)
                with open(csv_conteos_path, "rb") as f:
                    st.download_button("📥 Descargar Conteos", f, file_name="conteos_trafficsense.csv", mime="text/csv")

        with col_exp2:
            csv_alertas_path = Path("data/output/reporte_alertas.csv")
            if st.button("Exportar Alertas CSV"):
                db.export_csv("alertas_infraccion", csv_alertas_path)
                with open(csv_alertas_path, "rb") as f:
                    st.download_button("📥 Descargar Alertas", f, file_name="alertas_trafficsense.csv", mime="text/csv")

    with col_hist:
        st.subheader("Historial de Alertas y Revisión Humana")
        
        filter_estado = st.selectbox("Filtrar por estado de revisión:", ["Todos", "Pendiente", "Confirmada", "Descartada"])
        alertas = db.get_alertas(limit=50, estado=filter_estado)

        if alertas:
            df_alertas = pd.DataFrame(alertas)
            st.dataframe(
                df_alertas[["alerta_id", "fecha", "hora", "track_id", "tipo_vehiculo", "clasificacion_casco", "confianza", "estado_revision"]],
                use_container_width=True
            )

            # Módulo de edición de estado
            st.subheader("Gestión de Estado de Alerta")
            col_sel, col_act = st.columns([4, 4])
            with col_sel:
                alerta_ids = [a["alerta_id"] for a in alertas]
                selected_id = st.selectbox("Seleccione ID de Alerta:", alerta_ids)
            with col_act:
                nuevo_estado = st.selectbox("Nuevo Estado:", ["Confirmada", "Descartada", "Pendiente"])
                if st.button("Actualizar Estado"):
                    if db.update_alerta_revision(selected_id, nuevo_estado):
                        st.success(f"Alerta #{selected_id} actualizada a '{nuevo_estado}' en SQLite.")
                        st.rerun()

            # Previsualización del recorte de la alerta seleccionada
            selected_alert_info = next((a for a in alertas if a["alerta_id"] == selected_id), None)
            if selected_alert_info and selected_alert_info.get("ruta_evidencia"):
                crop_p = Path(selected_alert_info["ruta_evidencia"])
                if crop_p.is_file():
                    st.image(str(crop_p), caption=f"Evidencia visual de Alerta #{selected_id} (Ley N.º 29733)")
        else:
            st.info("No se encontraron registros de alertas con los filtros especificados.")
