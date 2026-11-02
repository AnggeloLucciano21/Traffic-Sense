# TrafficSense

> **Monitoreo de flujo vehicular y detección de motociclistas sin casco mediante YOLO y tracking multi-objeto**

* **Institución:** Universidad Nacional de San Martín (UNSM)
* **Facultad:** Ingeniería de Sistemas e Informática
* **Curso:** Proyectos de Inteligencia Artificial
* **Ubicación:** Tarapoto, San Martín, Perú

---

## 1. Descripción General del Proyecto

**TrafficSense** es un sistema de visión por computadora diseñado para analizar secuencias de video de tránsito urbano. Su propósito es responder a la problemática de seguridad vial y movilidad en la región San Martín, caracterizada por un parque automotor compuesto predominantemente por motocicletas.

El sistema contempla de manera progresiva:
1. Conteo y aforo vehicular clasificado (`car`, `motorcycle`, `bus`, `truck`) mediante líneas virtuales.
2. Identificación persistente de vehículos en movimiento con identificadores únicos (`track_id`).
3. Asociación espacial entre motocicletas y sus ocupantes (conductor y acompañante).
4. Evaluación del uso de casco de seguridad cuando se integre un detector especializado.
5. Almacenamiento local de aforos y alertas en SQLite.
6. Visualización de estadísticas y revisión de evidencias en un panel web (Streamlit).

---

## 2. Estado Actual del Desarrollo (Fase 1: Estructura Inicial)

> [!NOTE]
> **Aclaración sobre el estado real del software:**  
> El proyecto se encuentra actualmente en la **Fase 1 (Estructura modular, dependencias y configuración inicial)**.  
> * **Lo que ya existe:** Estructura de directorios, configuración centralizada (`configs/config.yaml`), especificación de dependencias (`requirements.txt`), reglas de exclusión en Git (`.gitignore`) y pruebas unitarias de configuración.
> * **Lo que aún NO está implementado:** La inferencia con modelos YOLO, el tracking con ByteTrack, el conteo vehicular por línea virtual, la base de datos SQLite y el panel Streamlit se implementarán progresivamente en las fases 2 a 5.
> * El detector de cascos se encuentra explícitamente configurado en estado `SIN_MODELO_CASCO` hasta que se realice el entrenamiento correspondiente en Google Colab/Kaggle.

---

## 3. Tecnologías Previstas

La arquitectura del sistema está diseñada enteramente en **Python (>= 3.10, compatible con 3.12)**:

* **Visión por Computadora:** [Ultralytics YOLO](https://docs.ultralytics.com/) (`yolo11n.pt` para detección vehicular general y `helmet_yolo11n.pt` para cascos).
* **Procesamiento de Video:** [OpenCV](https://opencv.org/) (`opencv-python`).
* **Seguimiento Multi-Objeto:** [ByteTrack](https://docs.ultralytics.com/modes/track) (asociación en dos etapas mediante Filtro de Kalman e IoU).
* **Persistencia de Datos:** [SQLite 3](https://docs.python.org/3/library/sqlite3.html) (almacenamiento relacional local sin servidor).
* **Panel de Control / Dashboard:** [Streamlit](https://streamlit.io/) (interfaz reactiva de monitoreo e historial de alertas).
* **Manipulación de Datos:** Pandas y NumPy.
* **Pruebas Automatizadas:** `pytest` y `unittest`.

---

## 4. Arquitectura Conceptual

El flujo de procesamiento sigue una secuencia modular en 7 etapas desacopladas:

```text
[Video de Entrada] 
       │
       ▼
[1. Preprocesamiento] (Redimensionado, ROI, control de FPS)
       │
       ▼
[2. Detección Base COCO] (yolo11n.pt: autos, motos, buses, camiones, personas)
       │
       ▼
[3. Seguimiento ByteTrack] (Asignación y persistencia de track_id)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[4A. Línea Virtual de Conteo]        [4B. Asociación Moto ↔ Ocupantes]
(Cruce vectorial y deduplicación)    (IoA >= 0.35 sobre caja extendida)
       │                                         │
       │                                         ▼
       │                             [5. Detector de Casco]
       │                             (Si existe: helmet_yolo11n.pt en Head ROI;
       │                              Si no: Estado 'SIN_MODELO_CASCO')
       │                                         │
       │                                         ▼
       │                             [Ventana Temporal K de N Cuadros]
       │                             (Confirmación y deduplicación de alerta)
       │                                         │
       └────────────────────┬────────────────────┘
                            ▼
              [6. Persistencia en SQLite]
              (trafficsense.db + data/evidence/crop.jpg con difuminado)
                            │
                            ▼
              [7. Panel de Monitoreo Streamlit]
              (Monitoreo en vivo, KPIs, historial y exportación CSV)
```

---

## 5. Estructura del Repositorio

```text
Traffic-Sense/
│
├── configs/
│   └── config.yaml               # Parámetros globales del sistema
│
├── data/
│   ├── raw_videos/               # Videos crudos de prueba y de San Martín
│   ├── datasets/                 # Datasets públicos de casco (Kaggle/Roboflow)
│   ├── processed/                # Dataset curado y particionado (train/val/test)
│   ├── output/                   # Videos anotados exportados
│   ├── evidence/                 # Recortes JPG de alertas (con difuminado)
│   └── database/                 # Archivo de base de datos SQLite (trafficsense.db)
│
├── models/                       # Pesos de modelos (.pt, .onnx)
│
├── notebooks/                    # Notebooks de entrenamiento y experimentación
│
├── scripts/                      # Scripts de utilidad (conversión, verificación de datos)
│
├── src/                          # Código fuente modular
│   ├── __init__.py
│   ├── config_loader.py          # Lector y validador de configs/config.yaml
│   ├── video/                    # Adquisición y streaming de video
│   ├── detection/                # Wrappers de modelos YOLO
│   ├── tracking/                 # Gestión de ByteTrack y trayectorias
│   ├── rules/                    # Geometría, conteo de línea y regla de casco
│   ├── database/                 # Gestor de base de datos SQLite
│   └── utils/                    # Anotaciones visuales y difuminado de privacidad
│
├── app/                          # Interfaz de usuario en Streamlit
│
├── tests/                        # Suite de pruebas automatizadas
│   ├── __init__.py
│   └── test_config.py            # Pruebas de configuración e importación
│
├── docs/                         # Documentación técnica y académica adicional
│
├── requirements.txt              # Especificación de dependencias del proyecto
├── README.md                     # Guía principal del proyecto
├── .gitignore                    # Reglas de exclusión para Git
└── Trafficsense.md               # Plan maestro técnico y metodológico
```

---

## 6. Requisitos Preliminares y Preparación del Entorno

### Requisitos del Sistema
* **Sistema Operativo:** Windows 10/11, Linux (Ubuntu 20.04+) o macOS.
* **Python:** Versión `>= 3.10` y `<= 3.12` (verificado en Python 3.12.6).
* **Git:** Para control de versiones.

### Configuración del Entorno Virtual (Recomendado)

1. **Clonar el repositorio o abrir la carpeta del proyecto:**
   ```bash
   cd Traffic-Sense
   ```

2. **Crear un entorno virtual aislado:**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual:**
   * En Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * En Windows (CMD):
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   * En Linux / macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Instalación de dependencias (cuando sea autorizado en la fase respectiva):**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 7. Ejecución de Pruebas Iniciales

Actualmente, el proyecto incluye pruebas de verificación de la estructura y configuración que pueden ejecutarse con el módulo estándar de Python:

```bash
python -m unittest discover tests -v
```

Una vez instalado `pytest` en el entorno virtual, las pruebas también podrán ejecutarse mediante:

```bash
pytest tests/ -v
```

---

## 8. Cumplimiento de Privacidad y Normativa

En observancia de la **Ley N.º 29733 (Ley de Protección de Datos Personales en el Perú)**, las imágenes y fotogramas guardados como evidencia visual de posibles infracciones son sometidos a un difuminado Gaussiano en los rostros y placas vehiculares para salvaguardar la identidad de los ciudadanos.
