# TrafficSense

> **Monitoreo de flujo vehicular y detección de motociclistas sin casco mediante YOLO y tracking multi-objeto**

* **Institución:** Universidad Nacional de San Martín (UNSM) — Tarapoto, San Martín, Perú
* **Facultad:** Ingeniería de Sistemas e Informática
* **Curso:** Proyectos de Inteligencia Artificial
* **Estado:** Primera versión funcional operativa (Fases 1, 2, 3, 4 y 5 integradas)

---

## 1. Descripción General del Proyecto

**TrafficSense** es un sistema de visión por computadora diseñado para analizar secuencias de video de tránsito urbano y responder a la problemática de seguridad vial y movilidad en la región San Martín, caracterizada por un parque automotor compuesto mayoritariamente por motocicletas.

El sistema implementa de forma modular:
1. **Detección vehicular y peatonal** mediante Ultralytics YOLO (`yolo11n.pt`) sobre clases oficiales de COCO (`car`, `motorcycle`, `bus`, `truck`, `person`).
2. **Seguimiento multi-objeto (ByteTrack)** que asigna identificadores únicos persistentes (`track_id`) a través de los fotogramas y gestiona oclusiones temporales.
3. **Aforo vehicular por cruce de línea virtual** mediante cálculo de producto cruz 2D sobre el punto inferior central de las llantas, con detección del sentido de circulación (`Entrada` / `Salida`) y prevención estricta de doble conteo.
4. **Asociación Persona–Motocicleta** con soporte para múltiples ocupantes (conductor y acompañante) mediante Intersección sobre Área ($\text{IoA} \ge 0.35$) sobre la caja extendida de la moto y extracción del tercio craneal (*Head ROI*).
5. **Regla de casco y confirmación temporal** mediante ventana deslizante ($K=5$ de $N=8$ cuadros), reporte transparente `SIN_MODELO_CASCO` cuando no se dispone de pesos especializados y deduplicación de alertas por motocicleta.
6. **Almacenamiento transaccional en SQLite** (`trafficsense.db`) con 3 tablas estructuradas (`sesiones_monitoreo`, `conteos_vehiculares`, `alertas_infraccion`).
7. **Generación de recortes de evidencia visual** (`.jpg`) con difuminado Gaussiano de rostros y placas en observancia de la **Ley N.º 29733 (Ley de Protección de Datos Personales de Perú)**.
8. **Dashboard interactivo en Streamlit** con visor de video en vivo, KPIs en tiempo real, gráfico de flujo horario, galería de evidencias, calibración de línea virtual y exportador CSV.

---

## 2. Arquitectura del Sistema

```text
[Video de Entrada (MP4 / Cámara / RTSP)] 
                   │
                   ▼
       [1. VideoStream (OpenCV)]
    (Redimensionado y control de FPS)
                   │
                   ▼
     [2. YOLODetector (yolo11n.pt)]
  (Detección COCO: car, moto, bus, truck, person)
                   │
                   ▼
      [3. TrackerManager (ByteTrack)]
        (Asignación de track_id único)
                   │
         ┌─────────┴─────────────────────────┐
         ▼                                   ▼
[4. LineCounter (Línea Virtual)]    [5. HelmetInfractionRule]
- Producto cruz 2D en llantas       - Asociación Moto ↔ Ocupantes (IoA >= 0.35)
- Sentido: Entrada / Salida         - Extracción Head ROI craneal
- Anti-duplicados (counted_ids)     - Ventana temporal K de N cuadros
         │                          - Modo honesto: SIN_MODELO_CASCO
         │                          - Deduplicación (alerted_moto_ids)
         │                                   │
         └─────────────────┬─────────────────┘
                           ▼
              [6. DatabaseManager (SQLite)]
         - Base de datos: data/database/trafficsense.db
         - Recortes JPG:  data/evidence/ (con difuminado Ley 29733)
                           │
                           ▼
          [7. Dashboard Web (Streamlit)]
   - Pestaña 1: Monitoreo en vivo, KPIs, gráfico de aforo y alertas
   - Pestaña 2: Calibración de línea, revisión humana y exportar CSV
```

---

## 3. Estructura del Repositorio

```text
Traffic-Sense/
│
├── configs/
│   ├── config.yaml                    # Parámetros globales del sistema y umbrales
│   └── dataset_helmet.yaml            # Configuración YOLO para entrenamiento de cascos
│
├── data/
│   ├── raw_videos/
│   │   ├── .gitkeep
│   │   └── sample_traffic.mp4         # Video de prueba generado para validación
│   ├── datasets/                      # Almacén de datasets de entrenamiento
│   ├── processed/                     # Dataset procesado (train/val/test)
│   ├── output/                        # Videos anotados exportados y reportes CSV
│   ├── evidence/                      # Recortes JPG de alertas con difuminado
│   └── database/
│       └── trafficsense.db            # Base de datos SQLite relacional
│
├── models/
│   ├── yolo11n.pt                     # Pesos oficiales COCO (descarga automática)
│   └── helmet_yolo11n.pt              # Pesos especializados de cascos (post-entrenamiento)
│
├── notebooks/
│   └── 01_train_helmet_yolo11.ipynb   # Notebook reproducible para Google Colab / Kaggle
│
├── scripts/
│   ├── generate_sample_video.py       # Generador de video de tráfico para pruebas
│   ├── convert_voc_to_yolo.py         # Conversor de PASCAL VOC (XML) a YOLO TXT
│   ├── split_dataset_by_video.py      # Partición 70/20/10 agrupada por video (anti-leakage)
│   └── verify_dataset.py              # Auditoría de coordenadas en [0,1] e integridad
│
├── src/
│   ├── __init__.py
│   ├── config_loader.py               # Cargador robusto de configs/config.yaml
│   ├── pipeline.py                    # Orquestador del flujo cuadro a cuadro y CLI
│   ├── video/
│   │   ├── __init__.py
│   │   └── video_stream.py            # Captura y streaming con OpenCV
│   ├── detection/
│   │   ├── __init__.py
│   │   └── yolo_detector.py           # Wrapper YOLOv8 / YOLO11 para vehículos y cascos
│   ├── tracking/
│   │   ├── __init__.py
│   │   └── tracker_manager.py         # Seguimiento con ByteTrack y ciclo de vida de tracks
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── geometry.py                # IoU, IoA, expansión de cajas y cruce vectorial
│   │   ├── line_counter.py            # Cruce de línea virtual, sentidos y anti-duplicados
│   │   └── helmet_rule.py             # Asociación Persona-Moto y confirmación multi-cuadro
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py              # Gestor SQLite (sesiones, aforo, alertas y CSV)
│   └── utils/
│       ├── __init__.py
│       └── visualizer.py              # Dibujo de cajas, telemetría y recortes con privacidad
│
├── app/
│   └── streamlit_app.py               # Panel web de monitoreo (Pestaña 1 y Pestaña 2)
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py                 # Pruebas de configuración y parser alternativo
│   ├── test_geometry_and_line.py      # Pruebas de IoU, IoA y conteo por línea
│   ├── test_helmet_rule.py            # Pruebas de asociación multi-ocupante y casco
│   └── test_db_manager.py             # Pruebas de base de datos SQLite y exportación CSV
│
├── requirements.txt                   # Especificación reproducible de dependencias
├── .gitignore                         # Exclusión de pesos pesados, videos y evidencias
├── README.md                          # Documentación técnica integral
└── Trafficsense.md                    # Plan maestro original
```

---

## 4. Guía Rápida de Instalación y Ejecución en Windows

### Paso 1: Activar el Entorno Virtual (`venv`)
Abra PowerShell en la carpeta raíz del proyecto y active el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

*(Si PowerShell bloquea la ejecución de scripts, ejecute previamente: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*.

---

### Paso 2: Ejecutar la Suite de Pruebas Automatizadas
Verifique que los 23 casos de prueba unitaria pasen exitosamente:

```powershell
pytest tests/ -v
```

---

### Paso 3: Generar el Video de Prueba Local (Opcional)
Si desea generar una secuencia de tráfico para demostración inmediata:

```powershell
python scripts/generate_sample_video.py
```

---

### Paso 4: Iniciar el Dashboard en Streamlit
Inicie la interfaz gráfica interactiva:

```powershell
streamlit run app/streamlit_app.py
```

El navegador web se abrirá automáticamente en `http://localhost:8501`. Desde allí podrá:
* Seleccionar el video de prueba o cargar un video propio.
* Iniciar y pausar el procesamiento cuadro a cuadro.
* Observar los KPIs de aforo y el gráfico de tráfico horario.
* Calibrar las coordenadas de la línea virtual con vista previa.
* Gestionar las alertas de infracción con revisión humana (`Pendiente`, `Confirmada`, `Descartada`).
* Exportar reportes en CSV (`RF-09`).

---

### Paso 5: Ejecución por Línea de Comandos (CLI)
Para procesar un video directamente sin interfaz gráfica y exportar el video anotado:

```powershell
python -m src.pipeline --source data/raw_videos/sample_traffic.mp4 --save-db --output data/output/demo_anotada.mp4 --display
```

---

## 5. Estado de la Detección de Casco (`SIN_MODELO_CASCO`)

Por rigor académico y cumplimiento de las directivas del curso:
* **El sistema NO simula ni inventa detecciones de casco.**
* Hasta que se complete el entrenamiento del modelo `helmet_yolo11n.pt` en Google Colab con el notebook `notebooks/01_train_helmet_yolo11.ipynb`, el detector de casco se reporta explícitamente en consola y en el dashboard como:
  ```text
  SIN_MODELO_CASCO (Modo Base Activo)
  ```
* Durante este modo, la detección vehicular general, el seguimiento ByteTrack, el conteo por línea virtual y la asociación espacial Persona-Motocicleta se encuentran **100% operativos con pesos reales**.

---

## 6. Procedimiento para Cerrar el Sistema

* Para detener el dashboard de Streamlit: Presione `Ctrl + C` en la terminal de PowerShell donde se ejecutó `streamlit run`.
* Para desactivar el entorno virtual: Ejecute el comando `deactivate`.
