# Plan Maestro Técnico y Metodológico: Segundo Entregable del Proyecto TrafficSense (Semanas 1 a 10)

**Proyecto:** TrafficSense — Monitoreo de flujo vehicular y detección de motociclistas sin casco mediante YOLO y tracking multi-objeto

**Institución:** Universidad Nacional de San Martín (UNSM) — Escuela Profesional de Ingeniería de Sistemas e Informática

**Curso:** Proyectos de Inteligencia Artificial

**Corte académico evaluado:** Final de la Segunda Unidad (Semana 10 de 15) — Meta mínima solicitada: **60 % de avance real y verificable**

**Documento base auditado:** `TrafficSense_Informe_Semanas_1-5 VERDE.docx` (Versión 1.0, Hito 1, 28 de septiembre de 2026)

## ENTREGABLE 1. Diagnóstico Exhaustivo del Documento de la Primera Unidad

El análisis forense del documento entregado en la Unidad 1 (`TrafficSense_Informe_Semanas_1-5 VERDE.docx`) demuestra que el equipo cuenta con una formulación conceptual sólida, bien delimitada y coherente con la realidad vial de la región San Martín. Sin embargo, tal como el propio informe declara en su nota inicial (*"las cifras de desempeño que aparecen en este documento son metas de trabajo, no resultados obtenidos. Las imágenes de la interfaz y de la detección son ilustraciones de ejemplo"*), **el Hito 1 constituye un documento de diseño y planificación (0 % de software validado en el informe), por lo que el Hito 2 (Semana 10) exige pasar de las ilustraciones simuladas a un prototipo funcional con evidencias empíricas**.

### 1.1 Aspectos ya definidos en la Primera Unidad (No repetir sin actualizar)

Los siguientes apartados ya están consolidados y deben mantenerse como base estructural, evitando volver a redactarlos como "propuestas a futuro":

* **Planteamiento del problema y justificación local (Secciones 1.1 a 1.5):** La problemática del uso intensivo de motocicletas en la región San Martín, la limitación de los operativos manuales esporádicos y la necesidad de conteos vehiculares automatizados están claramente justificadas.

* **Identificación de interesados y requerimientos (Secciones 2.1, 2.4 y 2.5):** Los 9 requerimientos funcionales (`RF-01` a `RF-09`) y los 7 requerimientos no funcionales (Desempeño, Precisión, Privacidad bajo la [Ley N.º 29733](https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733), Usabilidad, Portabilidad, Mantenibilidad y Condiciones de uso diurno) ya tienen prioridades y criterios de aceptación definidos.

* **Arquitectura lógica de 7 etapas (Sección 4.1 y Figura 1):** El pipeline secuencial (*1. Captura de video* $\to$ *2. Preprocesamiento* $\to$ *3. Detección YOLO* $\to$ *4. Seguimiento* $\to$ *5. Reglas de negocio* $\to$ *6. Almacenamiento SQLite* $\to$ *7. Panel de monitoreo en Streamlit*) es técnicamente viable, modular y debe respetarse íntegramente.

* **Metas cuantitativas de referencia (Secciones 2.6 y 6.1):** $\text{mAP@0.5} \ge 0.80$ en las clases de casco, error relativo de conteo vehicular $\le 10\%$ frente a conteo manual, y velocidad meta de $\ge 15\text{ FPS}$ en GPU de gama media (aceptando menor tasa en CPU).

### 1.2 Vacíos, Simulaciones y Pendientes Detectados en el Informe de la Unidad 1

Para que el segundo informe tenga rigor universitario, debemos corregir y reemplazar los siguientes elementos provisionales del primer documento:

| Elemento del Informe 1 (Semanas 1–5) | Estado hallado en el documento adjunto | Acción obligatoria para el Informe 2 (Semana 10) | 
| ----- | ----- | ----- | 
| **Datos de portada (Sección inicial)** | Campos `Docente: (completar)` e `Integrantes: (completar)` vacíos; nota de "borrador para revisión". | Completar nombres oficiales, códigos de estudiante, ORCID/correos institucionales y nombre del docente. | 
| **Ficha del dataset (Sección 3.6)** | `TrafficSense-v0.1` tiene los campos *Fuentes y licencias*, *Cantidad de imágenes y videos* y *Responsable* marcados como `"Por definir"`. | Actualizar a `TrafficSense-v1.0` con conteo exacto de imágenes de entrenamiento/validación/prueba, distribución por clase y licencias verificadas. | 
| **Ejemplo de análisis de IA (Sección 5, Figuras 2, 3 y 4)** | Usa dibujos técnicos en blanco y negro de patentes de cascos (*Australian Motorcycle News*) con cajas (`casco 0.93`, `0.90`) dibujadas manualmente. | **Sustituir por completo** con fotogramas reales de tráfico procesados por el pipeline [Ultralytics YOLO](https://docs.ultralytics.com/) + [ByteTrack](https://docs.ultralytics.com/modes/track), mostrando cajas reales generadas por inferencia. | 
| **Prototipo de interfaz (Sección 7, Figuras 5 y 6)** | Bocetos vectoriales estáticos con números ficticios (`1 248 vehículos hoy`, `512 motocicletas`, `37 sin casco`). | Reemplazar o contrastar con capturas reales de la aplicación web en [Streamlit](https://docs.streamlit.io/) conectada a la base de datos [SQLite](https://docs.python.org/3/library/sqlite3.html). | 
| **Referencias bibliográficas (Sección 9)** | Lista preliminar sin formato estándar (sin año, páginas, DOI ni URLs completas en varios artículos). | Normalizar todas las citas en formato IEEE o APA 7.ª edición (según exija el curso) con enlaces verificados. | 

### 1.3 Análisis del Cronograma Original y Conciliación del Corte en la Semana 10

Existe una discrepancia importante que debe explicarse metodológicamente en el segundo informe:

1. **Estructura del curso vs. Cronograma del Informe 1:** El curso se divide en tres unidades de 5 semanas (Unidad 1: Semanas 1–5; Unidad 2: Semanas 6–10; Unidad 3: Semanas 11–15). En cambio, la Sección 6.5 del primer informe planificó las actividades en bloques de dos semanas hasta la semana 14:

   * **Semanas 6 y 7:** Preparación y anotación del dataset, entrenamiento del baseline y primeras métricas.

   * **Semanas 8 y 9:** Ajuste fino del modelo, integración del tracking y conteo por línea virtual.

   * **Semanas 10 y 11:** Regla de infracción, base de datos y primera versión del panel.

   * **Semana 12:** Pruebas con video propio, análisis de errores y mejoras.

   * **Semana 13:** Evaluación final, comparación con el baseline y documentación.

   * **Semana 14:** Entrega final, informe y presentación con demostración.

2. **Implicación exacta al cierre de la Semana 10:** Al estar terminando la **Semana 10**, el equipo ha completado íntegramente los bloques de las **Semanas 6–7** y **Semanas 8–9**, y se encuentra exactamente a la **mitad del bloque Semanas 10–11**. Por lo tanto, no es exigible que el panel web, la regla de infracción y la base de datos estén al 100 % de su versión final pulida, pero **sí deben estar implementados en su primera versión funcional operativa (MVP)** para que se completen y refinen en la Semana 11.

## ENTREGABLE 2. Lista Exacta de lo que Deberíamos Tener Desarrollado al Finalizar la Semana 10 y Análisis Técnico de los Componentes (A–G)

### 2.1 Lista de Entregables Técnicos Exigibles al Cierre de la Semana 10

Siguiendo estrictamente el cronograma original del equipo (Sección 6.5), al finalizar la Semana 10 debemos contar con:

1. **Bloque Semanas 6 y 7 (100 % completado):**

   * Dataset público de cascos descargado, curado, convertido al formato estándar de [Ultralytics YOLO](https://docs.ultralytics.com/) y dividido en `train` (70 %), `val` (20 %) y `test` (10 %) sin fuga de datos entre secuencias.

   * Muestra inicial de videos o fotogramas de tráfico local (o videos de prueba de tráfico diurno equivalentes mientras se consolida la grabación de la Semana 12) extraídos y etiquetados.

   * Evaluación del **Baseline 1** (modelo preentrenado en COCO sin ajuste fino) para detección y conteo de vehículos (`car`, `motorcycle`, `bus`, `truck`, `person`).

   * Entrenamiento del **Baseline 2 / Primer ajuste fino** con datos abiertos para las clases `helmet` y `no_helmet`, con sus primeras curvas y métricas (`Precision`, `Recall`, `mAP@0.5`, `mAP@0.5:0.95` y matriz de confusión).

2. **Bloque Semanas 8 y 9 (100 % completado):**

   * Modelo ajustado (*fine-tuned*) funcional e integrado en el script de inferencia de video.

   * Integración del seguimiento multiobjeto con [ByteTrack](https://docs.ultralytics.com/modes/track) manteniendo identificadores únicos (`track_id`) por vehículo a través de los fotogramas.

   * Módulo de **línea virtual de conteo** implementado geométricamente o con [Roboflow Supervision](https://supervision.roboflow.com/latest/detection/tools/line_zone/), capaz de detectar el cruce, identificar el sentido de circulación, evitar el doble conteo por `track_id` y totalizar por clase (`car`, `motorcycle`, `bus`, `truck`).

3. **Bloque Semanas 10 y 11 — Corte al final de la Semana 10 (50 %–70 % completado, versión funcional inicial):**

   * **Regla de decisión de infracción v1:** Asociación espacial entre motocicleta (`motorcycle`), ocupantes (`person`/`rider`) y cabezas (`helmet`/`no_helmet`), con ventana deslizante de confirmación multi-cuadro ($N$ cuadros consecutivos) y deduplicación para emitir una sola alerta por motocicleta/ocupante.

   * **Base de datos local en SQLite:** Esquema creado y conectado al pipeline de inferencia, guardando cada alerta con su fecha, hora, cámara, `track_id`, tipo de vehículo, clasificación de casco, confianza, ruta al recorte de imagen (`crop`) y estado de revisión (`Pendiente`).

   * **Primera versión funcional del Panel en Streamlit:** Interfaz capaz de cargar y procesar un video, mostrar las estadísticas reales almacenadas en SQLite, visualizar los recortes de evidencia de infracción y exportar los registros a CSV.

### 2.2 Análisis Técnico Profundo de los Componentes del Sistema TrafficSense (A–G)

#### A. Dataset (`TrafficSense-v1.0`)

1. **Selección realista de fuentes de datos:**

   * En el Informe 1 se mencionaron ocho fuentes distintas (COCO, Kaggle Helmet Detection, Roboflow Universe, AI City Challenge, UA-DETRAC, BDD100K, VisDrone y videos propios). **Error común a evitar:** intentar descargar y unificar BDD100K (100,000 videos), UA-DETRAC y VisDrone en la Semana 10 bloqueará al equipo por falta de almacenamiento y tiempo de cómputo.

   * **Estrategia recomendada y viable para la Semana 10:**

     * **Para vehículos (`car`, `motorcycle`, `bus`, `truck`) y personas (`person`):** Aprovechar directamente el conocimiento de [Microsoft COCO](https://docs.ultralytics.com/) ya embebido en los pesos oficiales `yolo11n.pt` / `yolo11s.pt`, sin necesidad de descargar los 20 GB de COCO.

     * **Para cascos (`helmet`, `no_helmet`) y motociclistas (`rider`, `motorcycle`):** Combinar el dataset público [Kaggle Helmet Detection de andrewmvd](https://www.kaggle.com/datasets/andrewmvd/helmet-detection) (764 imágenes con licencia CC0/Dominio Público en formato PASCAL VOC XML) con un dataset curado de [Roboflow Universe (Motorcycle Helmet Detection)](https://universe.roboflow.com/search?q=class%3Ahelmet) bajo licencia CC BY 4.0 exportado en formato YOLO (entre 800 y 1,500 imágenes adicionales), más una muestra inicial de **150 a 300 fotogramas propios** grabados en San Martín (extraídos a 1–2 FPS para evitar cuadros idénticos).

2. **Obtención legal y registro de licencias:**

   * Descargar mediante la API de Kaggle o interfaz web tras verificar la licencia en la ficha del dataset, y desde Roboflow Universe citando al autor conforme a CC BY 4.0. Documentar cada fuente en una tabla de trazabilidad en el Informe 2.

   * En los videos propios grabados en vías públicas de San Martín (Tarapoto/Morales/Banda de Shilcayo), aplicar anonimización (difuminado Gaussiano sobre rostros y placas en las capturas del informe y recortes de evidencia) en cumplimiento de la [Ley N.º 29733 — Ley de Protección de Datos Personales](https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733).

3. **Estructura de carpetas y formato de etiquetas YOLO:**

   * Cada imagen `escena01_frame0045.jpg` debe tener su archivo homónimo `escena01_frame0045.txt` donde cada fila representa un objeto con coordenadas normalizadas entre $0.0$ y $1.0$:
     

     $$
     \text{class\_id} \quad x_{\text{center}} \quad y_{\text{center}} \quad \text{width} \quad \text{height}
     $$

   * **Mapeo de clases unificado (`dataset.yaml`):**

     * Si se entrena el detector especializado de cascos y motociclistas (recomendado, ver sección B): `0: helmet`, `1: no_helmet`, `2: rider`, `3: motorcycle`.

     * Si se entrena el conjunto completo de 7 clases: `0: motorcycle`, `1: rider`, `2: helmet`, `3: no_helmet`, `4: car`, `5: bus`, `6: truck`.

4. **División 70 % / 20 % / 10 % por video o sesión (Prevención de *Data Leakage*):**

   * Al extraer fotogramas de videos (`video_01.mp4`, `video_02.mp4`, etc.), **todos los fotogramas de un mismo video o prefijo de secuencia deben ir al mismo subconjunto** (`train`, `val` o `test`). Nunca hacer un `random.shuffle()` global de fotogramas sueltos, porque el cuadro $t$ y el cuadro $t+1$ son casi idénticos y falsearían el $\text{mAP}$.

5. **Volumen razonable y verificación:**

   * Para el prototipo de la Semana 10, un dataset consolidado de **1,200 a 2,000 imágenes** (p. ej., \~1,400 `train`, \~400 `val`, \~200 `test`) con al menos **1,500 instancias de `helmet` y 800 instancias de `no_helmet`** es manejable en Google Colab gratuito (15–25 minutos de entrenamiento) y suficiente para superar un $\text{mAP@0.5} > 0.75$.

   * **Verificación automática:** Ejecutar un script `scripts/verify_dataset.py` que compruebe que: (a) todo `.jpg` tenga su `.txt`, (b) ningún valor esté fuera de $[0, 1]$, (c) no haya `class_id` fuera de rango, y (d) no existan nombres de secuencia repetidos entre `train` y `test`.

#### B. Modelo de Inteligencia Artificial ([Ultralytics YOLO11](https://docs.ultralytics.com/models/yolo11) / YOLOv8)

1. **Elección de versión y tamaño:**

   * Se recomienda [**YOLO11**](https://docs.ultralytics.com/models/yolo11) en su variante **`yolo11n.pt` (Nano)** para inferencia en CPU o **`yolo11s.pt` (Small)** si se ejecuta en GPU. Frente a YOLOv8, YOLO11 ofrece mayor precisión ($\text{mAP}$) con menor cantidad de parámetros y menor latencia por cuadro, utilizando exactamente la misma API de la librería `ultralytics`.

2. **Dilema crítico de diseño: ¿Detector único de 7 clases o Estrategia Desacoplada (Dos Modelos / Dos Etapas)?**

   * **Problema técnico real:** Si tomamos `yolo11n.pt` (que ya detecta `person`, `car`, `motorcycle`, `bus`, `truck` con altísima calidad gracias a las 118,000 imágenes de COCO) y lo reentrenamos con un dataset de 1,500 imágenes de cascos donde los autos o camiones del fondo **no están etiquetados**, el modelo sufrirá **olvido catastrófico (*catastrophic forgetting*)** y dejará de detectar autos, buses y camiones, o requerirá re-etiquetar todos los vehículos de fondo en miles de imágenes.

   * **Solución técnica recomendada para la Semana 10 (Arquitectura Híbrida / Dos Etapas Ligeras):**

     * **Etapa 1 — Detector de Tráfico y Seguimiento (`yolo11n.pt` oficial preentrenado en COCO):** Detecta y sigue con ByteTrack las clases de COCO `0: person`, `2: car`, `3: motorcycle`, `5: bus`, `7: truck`. Garantiza de inmediato un conteo vehicular robusto y la localización de motocicletas y personas sin perder precisión.

     * **Etapa 2 — Detector Especializado de Casco (`helmet_yolo11n.pt` ajustado por el equipo):** Modelo `yolo11n.pt` entrenado mediante *fine-tuning* exclusivamente sobre las clases `0: helmet` y `1: no_helmet` (o ejecutado sobre el recorte/ROI ampliado de cada motocicleta detectada en la Etapa 1).

     * **Ventajas para la Semana 10:** Permite que el pipeline de conteo vehicular y seguimiento funcione al 100 % desde hoy mismo con `yolo11n.pt`, y que el modelo ajustado `helmet_yolo11n.pt` se concentre únicamente en resolver la clasificación `helmet` vs. `no_helmet` sobre la región de los ocupantes de la motocicleta. Además, si se ejecuta sobre el recorte (*crop*) de la motocicleta, las cabezas pequeñas ganan resolución efectiva al redimensionarse a la entrada del segundo modelo.

3. **Configuración de entrenamiento e hiperparámetros iniciales:**

   * Entorno: Google Colab (GPU NVIDIA T4, 16 GB VRAM) o Kaggle Notebooks (2x T4).

   * Hiperparámetros base recomendados en `model.train()`:

     * `data="configs/dataset_helmet.yaml"`

     * `epochs=50` (con `patience=15` para *early stopping*)

     * `imgsz=640` (o `imgsz=960` si se entrena en fotograma completo con cabezas pequeñas)

     * `batch=16`

     * `optimizer="AdamW"`, `lr0=0.001`, `cos_lr=True`

     * Aumentación de datos activada: `mosaic=1.0`, `hsv_h=0.015`, `hsv_s=0.7`, `hsv_v=0.4`, `fliplr=0.5`.

4. **Alternativa sin GPU local para la demostración en clase:**

   * Entrenar en la nube (Colab/Kaggle), descargar el archivo `best.pt` (\~5.5 MB en `yolo11n`) y exportarlo a **ONNX** (`model.export(format="onnx", dynamic=False, simplify=True)`) o **OpenVINO**, lo que acelera la inferencia en procesadores Intel/AMD de laptops entre un 40 % y un 80 % sin requerir tarjeta gráfica dedicada.

#### C. Tracking Multiobjeto ([ByteTrack](https://docs.ultralytics.com/modes/track))

1. **Cómo funciona y por qué es ideal para TrafficSense:**

   * A diferencia de SORT tradicional (que descarta detecciones con confianza media-baja), **ByteTrack** realiza una asociación en dos etapas usando Filtro de Kalman e IoU:

     * *Primera asociación:* Empareja las detecciones de alta confianza ($\text{conf} \ge \text{track\_high\_thresh}$, p. ej. $0.50$) con las trayectorias activas (`tracks`).

     * *Segunda asociación:* Empareja las detecciones de baja confianza ($0.10 \le \text{conf} < 0.50$, típicas cuando una motocicleta pasa detrás de un auto o mototaxi) con las trayectorias que quedaron sin emparejar en la primera etapa. Esto reduce drásticamente la pérdida o cambio de `track_id` (*ID switch*).

2. **Qué aprovechamos de las librerías vs. qué debemos programar:**

   * **Provisto por [Ultralytics](https://docs.ultralytics.com/modes/track) o [Roboflow Supervision](https://supervision.roboflow.com/latest/trackers/):** La predicción del Filtro de Kalman, la matriz de costos IoU, el algoritmo Húngaro de asignación y la entrega de `track_id` persistente por cada caja detectada.

   * **Lo que debemos programar nosotros (`src/tracking/tracker_manager.py`):**

     * Un diccionario de estado de trayectorias (`active_tracks[track_id]`) que almacene: la lista histórica de centroides $(x_c, y_c)$ para evaluar el cruce de la línea virtual, la clase vehicular estabilizada por votación mayoritaria, la ventana deslizante (`deque`) de estados de casco y las banderas booleanas `counted` y `alert_emitted`.

     * Limpieza periódica de memoria para eliminar del diccionario aquellos `track_id` que no han sido vistos en los últimos $M = 90$ fotogramas (\~3 segundos de video).

#### D. Conteo Vehicular mediante Línea Virtual (`src/rules/line_counter.py`)

1. **Configuración geométrica de la línea:**

   * La línea virtual se define mediante dos puntos en coordenadas de imagen: $P_1 = (x_1, y_1)$ y $P_2 = (x_2, y_2)$, configurables desde el archivo YAML o mediante cursores (*sliders*) en el panel de Streamlit.

2. **Matemática de detección de cruce y sentido de circulación:**

   * Para cada vehículo con `track_id` activo, se toma su punto de anclaje inferior central (*bottom-center*: $x_b = \frac{x_{\min}+x_{\max}}{2}, y_b = y_{\max}$, que representa el contacto de las llantas con el asfalto y es más estable que el centroide ante cambios de perspectiva) en el fotograma anterior $A = (x_{t-1}, y_{t-1})$ y en el fotograma actual $B = (x_t, y_t)$.

   * Se calcula el producto cruz 2D respecto al vector director de la línea $\vec{L} = P_2 - P_1$:
     

     $$
     s(Q) = (x_2 - x_1)(y_Q - y_1) - (y_2 - y_1)(x_Q - x_1)
     $$

   * **Condición de cruce:** Si $s(A)$ y $s(B)$ tienen signos opuestos ($s(A) \cdot s(B) < 0$) y el segmento $\overline{AB}$ intersecta al segmento $\overline{P_1P_2}$:

     * Si $s(A) < 0 \land s(B) \ge 0$: Cruce en **Sentido 1 (Entrada / Norte** $\to$ **Sur)**.

     * Si $s(A) > 0 \land s(B) \le 0$: Cruce en **Sentido 2 (Salida / Sur** $\to$ **Norte)**.

   * Alternativamente, puede emplearse `sv.LineZone` de [Roboflow Supervision](https://supervision.roboflow.com/latest/detection/tools/line_zone/), que implementa exactamente esta verificación vectorial y expone `in_count` y `out_count`.

3. **Prevención de doble conteo y desglose por clase:**

   * Al confirmarse el cruce, el `track_id` se inserta en el conjunto `counted_ids.add(track_id)`. Si un vehículo se detiene sobre la línea por congestión y oscila, el sistema verifica `if track_id in counted_ids: continue`, garantizando **exactamente un conteo por vehículo**.

   * El contador se incrementa en la categoría correspondiente (`car`, `motorcycle`, `bus`, `truck`) y se registra la marca temporal para construir el histograma de flujo vehicular por hora.

#### E. Detección de Motociclistas sin Casco (`src/rules/helmet_rule.py`)

Para cumplir la exigencia del proyecto —**no limitarse a detectar cascos sueltos en la escena y contemplar motocicletas con conductor y acompañante**—, implementaremos el siguiente algoritmo determinista en 9 pasos:

```
[Fotograma t]
   │
   ├─► 1. Obtener motocicletas rastreadas: M_i = (bbox_moto, track_id_moto)
   ├─► 2. Obtener personas detectadas en el cuadro: P_j = (bbox_persona)
   ├─► 3. Asociación Persona ↔ Motocicleta (Soporte Multi-Ocupante: Conductor + Acompañante):
   │      Expandir verticalmente bbox_moto un 35% hacia arriba -> bbox_moto_ext.
   │      Calcular IoA (Intersection over Person Area) = Area(P_j ∩ bbox_moto_ext) / Area(P_j).
   │      Toda persona P_j con IoA >= 0.35 queda vinculada a la lista de ocupantes de M_i.
   ├─► 4. Delimitación de la Región de Cabeza (Head ROI) de cada ocupante P_j:
   │      Para cada ocupante P_j asociado a M_i, definir su sub-caja craneal:
   │      head_roi(P_j) = [x1_p, y1_p, x2_p, y1_p + 0.35 * (y2_p - y1_p)].
   ├─► 5. Detección y Asociación de Casco / Sin Casco sobre cada ocupante:
   │      Ejecutar detector de cascos (sobre el recorte de M_i_ext o cuadro completo).
   │      Para cada predicción H_k in {helmet, no_helmet} con conf >= umbral_conf (0.50):
   │      Verificar si el centroide de H_k cae dentro de head_roi(P_j) o tiene IoU >= 0.25.
   ├─► 6. Evaluación por Ocupante y Estado de la Motocicleta en el Fotograma t:
   │      - Si AL MENOS UN ocupante P_j de la moto M_i tiene clase 'no_helmet' confirmada:
   │        estado_cuadro(M_i, t) = "no_helmet" (infracción: basta que conductor O acompañante no use casco).
   │      - Si TODOS los ocupantes evaluados tienen 'helmet':
   │        estado_cuadro(M_i, t) = "helmet".
   │      - Si las detecciones tienen confianza < umbral o están ocluidas:
   │        estado_cuadro(M_i, t) = "uncertain" (no vota).
   ├─► 7. Confirmación Temporal Multi-Cuadro (Ventana Deslizante por track_id_moto):
   │      Agregar estado_cuadro(M_i, t) a history[track_id_moto] (deque de longitud N = 8 cuadros).
   │      Contar votos 'no_helmet' en la ventana. Si votos_no_helmet >= K (ej. 5 de 8 cuadros):
   │      Infracción confirmada temporalmente.
   ├─► 8. Deduplicación de Alerta por Evento:
   │      Verificar si track_id_moto ya está en alerted_moto_ids.
   │      Si no está: agregar a alerted_moto_ids y disparar evento único de alerta.
   └─► 9. Generación y Guardado de Evidencia Visual:
          Recortar bbox_moto_ext con margen de 15 px, aplicar difuminado opcional en rostro/placa,
          guardar JPEG en data/evidence/ y registrar fila en SQLite.

```

* **Limitaciones técnicas declaradas con transparencia:**

  * En tomas frontales o traseras muy lejanas (donde la cabeza mide menos de $15 \times 15$ píxeles), el acompañante puede quedar parcialmente oculto detrás del conductor (*oclusión inter-ocupante*). Por ello, la línea virtual y la zona de evaluación de casco deben ubicarse en el **tercio medio-inferior del encuadre**, donde las motocicletas están más próximas a la cámara y la perspectiva elevada permite separar las cabezas del conductor y del pasajero.

  * Gorras, capuchas o cascos tipo *bowl* del color del cabello pueden reducir la confianza del clasificador; el filtro de confianza ($\ge 0.50$) y la confirmación en $K$ de $N$ cuadros evitan que un parpadeo de 1 o 2 cuadros genere una falsa alarma.

#### F. Base de Datos (`src/database/db_manager.py`)

1. **Elección tecnológica justificada:**

   * Se selecciona [**SQLite 3**](https://docs.python.org/3/library/sqlite3.html) (incluido nativamente en la librería estándar de Python) frente a PostgreSQL o MySQL.

   * **Justificación técnica:** Para un prototipo universitario monolítico ejecutado en una laptop o estación de trabajo local, SQLite no requiere instalar ni configurar servidores de bases de datos externos, almacena toda la información en un único archivo portable (`data/database/trafficsense.db`), soporta transacciones ACID completas, maneja sin esfuerzo decenas de miles de registros de conteo e infracciones, y se conecta directamente con `pandas` y `Streamlit`.

2. **Diseño del Esquema Relacional (DDL SQL):**

```
-- Tabla 1: Sesiones de procesamiento (videos o conexiones de cámara)
CREATE TABLE IF NOT EXISTS sesiones_monitoreo (
    sesion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_fuente TEXT NOT NULL,           -- Nombre del archivo de video o URL RTSP
    camara TEXT NOT NULL DEFAULT 'Camara_01_Av_Principal',
    fecha_inicio TEXT NOT NULL,            -- ISO-8601 YYYY-MM-DD HH:MM:SS
    modelo_usado TEXT NOT NULL,            -- Ej. 'yolo11n.pt + helmet_yolo11n.pt'
    tracker_usado TEXT NOT NULL DEFAULT 'ByteTrack',
    fps_promedio REAL DEFAULT 0.0,
    total_vehiculos INTEGER DEFAULT 0,
    total_motos INTEGER DEFAULT 0,
    total_infracciones INTEGER DEFAULT 0
);

-- Tabla 2: Conteo vehicular individual por cruce de línea virtual
CREATE TABLE IF NOT EXISTS conteos_vehiculares (
    conteo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sesion_id INTEGER,
    fecha TEXT NOT NULL,                   -- YYYY-MM-DD
    hora TEXT NOT NULL,                    -- HH:MM:SS
    hora_franja TEXT NOT NULL,             -- Ej. '08:00', '14:00' para gráfico horario
    camara TEXT NOT NULL,
    track_id INTEGER NOT NULL,
    tipo_vehiculo TEXT NOT NULL,           -- 'car', 'motorcycle', 'bus', 'truck'
    sentido TEXT NOT NULL,                 -- 'Entrada' | 'Salida'
    confianza REAL NOT NULL,
    FOREIGN KEY (sesion_id) REFERENCES sesiones_monitoreo(sesion_id)
);

-- Tabla 3: Alertas de infracción ( y registro de cumplimiento en motocicletas)
CREATE TABLE IF NOT EXISTS alertas_infraccion (
    alerta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sesion_id INTEGER,
    fecha TEXT NOT NULL,                   -- YYYY-MM-DD
    hora TEXT NOT NULL,                    -- HH:MM:SS
    camara TEXT NOT NULL,                  -- Ej. 'Cámara 01 - Av. Principal'
    track_id INTEGER NOT NULL,             -- ID persistente asignado por ByteTrack
    tipo_vehiculo TEXT NOT NULL DEFAULT 'motorcycle',
    clasificacion_casco TEXT NOT NULL,     -- 'sin_casco' | 'con_casco'
    ocupantes_detectados INTEGER DEFAULT 1,-- Número de personas asociadas a la moto
    confianza REAL NOT NULL,               -- Confianza media en la ventana de confirmación
    cuadros_confirmados INTEGER NOT NULL,  -- Ej. 5 (de 8 cuadros)
    ruta_evidencia TEXT,                   -- Ruta relativa al recorte JPG en disco
    estado_revision TEXT NOT NULL DEFAULT 'Pendiente', -- 'Pendiente' | 'Confirmada' | 'Descartada'
    es_dato_simulado INTEGER NOT NULL DEFAULT 0,       -- 0 = Inferencia real, 1 = Prueba/Demo
    FOREIGN KEY (sesion_id) REFERENCES sesiones_monitoreo(sesion_id)
);

```

#### G. Panel de Monitoreo (`app/streamlit_app.py`)

Implementado en [**Streamlit**](https://docs.streamlit.io/), organizado en dos pestañas (`st.tabs(["📹 Monitoreo en Vivo / Video", "⚙️ Configuración e Historial"])`) que materializan los bocetos de las Figuras 5 y 6 del primer informe:

1. **Pestaña 1 — Monitoreo:**

   * **Columna izquierda (Visor de Video):** Selector de video local (`.mp4`, `.avi`) o cámara web; renderizado cuadro a cuadro con `st.empty()` mostrando cajas delimitadoras coloreadas por estado (`verde` = moto con casco, `rojo` = moto sin casco, `azul` = auto/bus/camión), etiqueta `ID # · clase · conf`, y la línea virtual de conteo superpuesta.

   * **Columna derecha superior (4 Tarjetas KPI alimentadas por SQLite/Estado en memoria):** `Vehículos totales`, `Motocicletas detectadas`, `Alertas sin casco`, y `% Cumplimiento de casco` (calculado dinámicamente como $\frac{\text{Motos con casco}}{\text{Total motos evaluadas}} \times 100$).

   * **Columna derecha central (Gráfico de flujo vehicular):** Gráfico de barras interactivo (`st.bar_chart` o `plotly`/`altair`) agrupando los registros de `conteos_vehiculares` por `hora_franja` y `tipo_vehiculo`.

   * **Columna derecha inferior (Alertas recientes con evidencia):** Tarjetas con las últimas 5 infracciones registradas en `alertas_infraccion`, mostrando la miniatura real (`st.image(ruta_evidencia)`), hora, `track_id` y nivel de confianza.

   * **Barra inferior de telemetría:** Indicadores reales de `FPS`, `Latencia por cuadro (ms)`, `Modelo activo` y `Tracker activo`.

2. **Pestaña 2 — Configuración e Historial:**

   * **Panel izquierdo (Parámetros operativos):** Controles deslizantes (`st.slider`) para ajustar las coordenadas de la línea virtual $(x_1, y_1) \to (x_2, y_2)$ con previsualización sobre el primer fotograma del video, umbral de confianza ($\text{conf} \in [0.25, 0.90]$) y número de cuadros $K$ de $N$ para confirmar infracción.

   * **Panel derecho (Historial y Revisión Humana):** Filtros por `Fecha`, `Cámara`, `Estado de revisión` (`Pendiente`, `Confirmada`, `Descartada`) y `Origen de datos` (Reales vs. Simulados de prueba). Tabla interactiva (`st.data_editor` o selector de ID de alerta) que permite a un operador cambiar el estado de una alerta de `Pendiente` a `Confirmada` o `Descartada` ejecutando un `UPDATE` en SQLite, más un botón `st.download_button` para **Exportar a CSV (`RF-09`)**.

## ENTREGABLE 3. Matriz de Funcionalidades: Implementadas, Parciales y Pendientes

Dado que el documento adjunto corresponde al cierre de la Unidad 1 y aún no se ha adjuntado el código fuente del repositorio actual del equipo, la siguiente matriz distingue con total transparencia entre **el estado verificable hoy desde la documentación**, **el estado objetivo que debemos consolidar al cierre de la Semana 10** y los **elementos pendientes de verificación en el repositorio del equipo**:

| Código / Módulo | Funcionalidad o Componente | Cronograma Original | Estado Verificado en Doc. Unidad 1 | Estado Objetivo Exigible en Semana 10 | Estado Actual Real (Sin acceso al repo) | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **Datos-01** | Descarga, conversión a YOLO y partición 70/20/10 por sesión de datasets públicos de casco | Semanas 6–7 | Planificado | **Implementado y comprobado** | Pendiente de verificación en repositorio | 
| **Datos-02** | Grabación de videos propios en San Martín y anotación de muestra local | Semanas 6–7 y 12 | Planificado | **Implementado parcialmente** (muestra inicial; pruebas masivas en Sem. 12) | Pendiente de verificación en repositorio | 
| **IA-01 (`RF-02`)** | Detección de vehículos (`car`, `motorcycle`, `bus`, `truck`) y personas con modelo base YOLO | Semanas 6–7 | Planificado (ilustración manual en Fig. 3–4) | **Implementado y comprobado** | Pendiente de verificación en repositorio | 
| **IA-02 (`RF-05`)** | Entrenamiento (*fine-tuning*) del modelo detector de `helmet` / `no_helmet` y métricas iniciales | Semanas 6–9 | Planificado | **Implementado y comprobado** (1.ª versión ajustada con métricas en validación) | Pendiente de verificación en repositorio | 
| **RF-01** | Carga y lectura de archivos de video (`.mp4`/`.avi`) y flujo de cámara en OpenCV | Semanas 8–9 | Planificado | **Implementado y comprobado** | Pendiente de verificación en repositorio | 
| **RF-03** | Asignación de IDs únicos persistentes mediante seguimiento multiobjeto (ByteTrack) | Semanas 8–9 | Planificado | **Implementado y comprobado** | Pendiente de verificación en repositorio | 
| **RF-04** | Conteo vehicular por tipo y sentido al cruzar línea virtual configurable sin doble conteo | Semanas 8–9 | Planificado | **Implementado y comprobado** | Pendiente de verificación en repositorio | 
| **RF-06** | Regla de infracción: asociación persona-moto (conductor/acompañante) y confirmación en $N$ cuadros | Semanas 10–11 | Planificado | **Implementado parcialmente** (lógica funcional base en Semana 10; ajuste fino en Sem. 11) | Pendiente de verificación en repositorio | 
| **RF-07** | Almacenamiento en SQLite y guardado automático de recortes de evidencia (`crops` JPG) | Semanas 10–11 | Planificado | **Implementado parcialmente** (esquema SQLite y guardado operativo inicial) | Pendiente de verificación en repositorio | 
| **RF-08** | Panel de monitoreo e historial en Streamlit conectado a datos reales | Semanas 10–11 | Planificado (boceto estático Fig. 5–6) | **Implementado parcialmente** (primera versión funcional conectada a SQLite) | Pendiente de verificación en repositorio | 
| **RF-09** | Exportación de reportes de conteo y alertas en formato CSV | Semanas 10–11 (Prioridad Baja) | Planificado | **Implementado parcialmente** (botón de exportación básica desde SQLite) | Pendiente de verificación en repositorio | 
| **Eval-Final** | Pruebas extensivas con video local en distintas horas, comparativa final con baseline y usabilidad | Semanas 12–14 | Planificado | **No iniciado / Pendiente para Unidad 3** (programado para Semanas 12–14) | No iniciado (Unidad 3) | 

## ENTREGABLE 4. Matriz de Avance Ponderada para Justificar el 60 %

### 4.1 Metodología de Cálculo Transparente

Para evitar porcentajes subjetivos o arbitrarios ante el docente, el avance global del proyecto ($A_{\text{global}}$) se calcula mediante una **suma ponderada basada en evidencias verificables**:

$$
A_{\text{global}} = \sum_{i=1}^{k} \left( P_i \times \frac{C_i}{100} \right)
$$

Donde:

* $P_i$: **Peso porcentual del componente** $i$ sobre el proyecto total ($\sum P_i = 100\%$). Se asigna un **15 %** a la fase de formulación e ingeniería de requerimientos (Unidad 1) y un **85 %** al desarrollo técnico, experimental, integración y validación (Unidades 2 y 3), reflejando que se trata de un curso de desarrollo de proyectos de IA.

* $C_i$: **Porcentaje de cumplimiento real del componente** $i$ ($0\% \le C_i \le 100\%$), el cual **solo puede asignarse si existe el entregable o evidencia técnica verificable** detallada en la columna correspondiente.

### 4.2 Matriz Ponderada de Avance al Cierre de la Semana 10

| N.º | Componente del Proyecto | Actividades Incluidas | Peso Propuesto ($P_i$) | Estado Meta en Semana 10 | Evidencia Verificable Requerida | % Cumplimiento en Sem. 10 ($C_i$) | % Contribución al Proyecto ($P_i \times C_i$) | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **1** | **Ingeniería de Requerimientos, Arquitectura y Planificación (Hito 1)** | Problema, objetivos, RF/RNF, arquitectura de 7 etapas, diseño de interfaz y cronograma. | **15.0 %** | Implementado y comprobado | Informe de Unidad 1 entregado (`TrafficSense_Informe_Semanas_1-5 VERDE.docx`) y repositorio Git creado. | **100 %** | **15.00 %** | 
| **2** | **Ingeniería de Datos y Dataset (`TrafficSense-v1.0`)** | Descarga de datasets públicos, conversión a YOLO, partición 70/20/10 por sesión, script verificador y primera muestra local. | **15.0 %** | Implementado parcialmente (falta muestra final Sem. 12) | Carpeta `data/processed/`, archivo `dataset.yaml`, reporte de `verify_dataset.py` y capturas de etiquetas en CVAT/Roboflow. | **80 %** | **12.00 %** | 
| **3** | **Entrenamiento de Modelos YOLO (Baseline y Fine-Tuning de Casco)** | Evaluación del baseline preentrenado COCO, entrenamiento del modelo ajustado `helmet_yolo11n.pt` y primeras métricas. | **20.0 %** | Implementado parcialmente (1.ª iteración entrenada; falta comparativa final Sem. 13) | Notebook de entrenamiento ejecutado, archivo de pesos `best.pt`, curvas `results.png`, matriz de confusión y tabla de $\text{mAP@0.5}$. | **75 %** | **15.00 %** | 
| **4** | **Tracking Multiobjeto y Conteo por Línea Virtual (`RF-01`, `RF-02`, `RF-03`, `RF-04`)** | Pipeline de lectura OpenCV, integración de ByteTrack con IDs persistentes, cruce vectorial de línea virtual y conteo por tipo. | **15.0 %** | Implementado y comprobado (en videos de prueba) | Módulo `line_counter.py` y `tracker_manager.py`, video de salida anotado con IDs y conteos por clase verificados. | **85 %** | **12.75 %** | 
| **5** | **Regla de Infracción Multi-Cuadro y Base de Datos SQLite (`RF-05`, `RF-06`, `RF-07`)** | Asociación moto-persona-cabeza, ventana deslizante de $N$ cuadros, deduplicación de alertas, recorte JPG y persistencia SQLite. | **15.0 %** | Implementado parcialmente (mitad del bloque Sem. 10–11) | Módulo `helmet_rule.py`, base de datos `trafficsense.db` con registros reales e imágenes en `data/evidence/`. | **55 %** | **8.25 %** | 
| **6** | **Panel Web de Monitoreo e Historial en Streamlit (`RF-08`, `RF-09`)** | Primera versión funcional del dashboard de 2 pestañas, lectura de KPIs desde SQLite, galería de evidencias y exportación CSV. | **10.0 %** | Implementado parcialmente (MVP operativo en Sem. 10) | Script `app/streamlit_app.py` ejecutándose localmente y capturas de ambas pestañas con datos reales del pipeline. | **50 %** | **5.00 %** | 
| **7** | **Validación en Campo (San Martín), Análisis de Errores y Entrega Final** | Pruebas con videos locales en múltiples horarios, medición de error relativo de conteo vs. manual, prueba de usabilidad e informe final. | **10.0 %** | No iniciado / Pendiente (Semanas 12–14) | Se ejecutará en la Unidad 3 (Semanas 11–15). | **0 %** | **0.00 %** | 
| **—** | **TOTAL GLOBAL DEL PROYECTO** | **Suma de todos los componentes** | **100.0 %** | **Corte Semana 10** | **Prototipo funcional + Segundo Informe Académico** | **—** | **68.00 %** | 

### 4.3 Análisis de Sensibilidad y Limitaciones de la Matriz

* **Margen de seguridad sobre el 60 %:** Completando las fases técnicas propuestas en este plan hasta el nivel MVP de la Semana 10, el proyecto alcanza un **68.00 % de avance ponderado**, superando con un margen de 8 puntos el mínimo de 60 % exigido por el docente.

* **Escenario mínimo aceptable (si el entrenamiento propio demora):** Incluso si el componente de panel web estuviera al 40 % ($4.00\%$) y la regla de infracción al 45 % ($6.75\%$), el avance total sería de **65.50 %**, siempre que el dataset, el modelo base/ajustado, el tracking ByteTrack y el conteo por línea virtual estén funcionando y documentados con evidencias reales.

* **Limitaciones metodológicas a declarar:** El porcentaje mide la completitud funcional y experimental de los módulos de software y modelado, pero las métricas de precisión actuales ($\text{mAP}$ y error de conteo) son **preliminares sobre el conjunto de validación inicial** y podrán variar cuando se incorporen las grabaciones completas de campo en la Semana 12.

## ENTREGABLE 5. Índice Completo y Contenido del Segundo Informe Académico

El segundo informe debe mantener el formato, estilo sobrio y numeración lógica del primer documento, pero evolucionando de *"Propuesta / Plan"* a *"Informe de Desarrollo e Implementación del Prototipo (Semanas 1 a 10)"*. A continuación se detalla qué debe contener cada una de las 20 secciones requeridas:

### 1. Introducción y Antecedentes Actualizados

1. **Qué debe escribirse:** Resumen del problema de seguridad vial y flujo vehicular en San Martín, objetivos del proyecto y actualización del estado del arte incorporando los detalles técnicos verificados de [Ultralytics YOLO11](https://docs.ultralytics.com/models/yolo11), [ByteTrack](https://docs.ultralytics.com/modes/track) y [Roboflow Supervision](https://supervision.roboflow.com/).

2. **Qué información debemos obtener:** Datos bibliográficos completos (autores, año, título, revista/conferencia, DOI/URL) de los artículos citados de forma incompleta en la sección 2.2 y 9 del primer informe.

3. **Qué evidencia debemos incorporar:** Tabla comparativa de antecedentes académicos (autor, año, modelo usado, dataset, métricas reportadas y diferencia con TrafficSense).

4. **Qué resultados debemos mostrar:** Síntesis clara de por qué la combinación YOLO + ByteTrack + confirmación multi-cuadro responde a las limitaciones halladas en la literatura.

5. **Qué elementos del primer documento conservar:** Secciones 1.1, 1.3, 1.4 y 1.5 del Informe 1, cambiando los verbos en futuro (*"se propondrá"*) a tiempo presente/pasado (*"el sistema implementa"*).

### 2. Estado Actual del Proyecto

1. **Qué debe escribirse:** Explicación ejecutiva de la transición entre el Hito 1 (Semana 5, formulación) y el Hito 2 (Semana 10, implementación del núcleo de IA, tracking, conteo, base de datos y primera versión del panel).

2. **Qué información debemos obtener:** Estado real de cada módulo del repositorio Git y conciliación del cronograma de 14/15 semanas en el corte de la Semana 10.

3. **Qué evidencia debemos incorporar:** Captura del repositorio del equipo (ramas, commits o estructura de directorios) y tabla comparativa *Hito 1 vs. Hito 2*.

4. **Qué resultados debemos mostrar:** Hitos completados en las semanas 6–7, 8–9 y primera mitad de 10–11.

5. **Qué elementos del primer documento conservar:** La organización del equipo en 5 frentes (Sección 1.6) y los requerimientos `RF-01` a `RF-09` (Sección 2.4) como marco de referencia.

### 3. Desarrollo del Dataset

1. **Qué debe escribirse:** Selección definitiva de fuentes de datos, justificación técnica de por qué se priorizaron [Kaggle Helmet Detection](https://www.kaggle.com/datasets/andrewmvd/helmet-detection), proyectos curados de [Roboflow Universe](https://universe.roboflow.com/search?q=class%3Ahelmet) y grabaciones locales, y análisis de licencias y cumplimiento de la [Ley N.º 29733](https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733).

2. **Qué información debemos obtener:** Número exacto de imágenes aportadas por cada fuente, resolución promedio y condiciones de iluminación.

3. **Qué evidencia debemos incorporar:** **Ficha del Dataset `TrafficSense-v1.0` totalmente completada** (reemplazando los campos *"Por definir"* de la Sección 3.6 del Informe 1).

4. **Qué resultados debemos mostrar:** Tabla de distribución de imágenes e instancias (cajas anotadas) por cada clase (`helmet`, `no_helmet`, `motorcycle`, `rider`, `car`, `bus`, `truck`).

5. **Qué elementos del primer documento conservar:** Tabla de riesgos de datos y privacidad (Sección 3.5) y estructura de la ficha del dataset (Sección 3.6).

### 4. Preparación y Anotación de Datos

1. **Qué debe escribirse:** Flujo de extracción de fotogramas a 1–2 FPS, conversión de etiquetas XML PASCAL VOC a formato TXT YOLO normalizado, proceso de etiquetado manual/asistido en [CVAT](https://www.cvat.ai/) o [Roboflow](https://universe.roboflow.com/), y partición 70 % `train`, 20 % `val`, 10 % `test` agrupada por sesión/video.

2. **Qué información debemos obtener:** Estadísticas arrojadas por el script `verify_dataset.py` (total de etiquetas válidas, proporción de clases, ausencia de archivos corruptos).

3. **Qué evidencia debemos incorporar:** Capturas de pantalla reales de la herramienta de anotación mostrando cajas sobre motociclistas con y sin casco, el contenido real del archivo `dataset.yaml` y la salida de consola de `verify_dataset.py`.

4. **Qué resultados debemos mostrar:** Gráfico o tabla de balance de clases y conteo exacto de imágenes en `train`, `val` y `test`.

5. **Qué elementos del primer documento conservar:** El criterio metodológico de partición por video/sesión (Sección 3.3 y 3.4) para evitar fuga de datos.

### 5. Implementación del Modelo YOLO

1. **Qué debe escribirse:** Justificación de la arquitectura adoptada (uso de `yolo11n.pt`/`yolo11s.pt` preentrenado en COCO para detección vehicular general + modelo ajustado `helmet_yolo11n.pt` para detección de `helmet` y `no_helmet`), evitando el olvido catastrófico sobre vehículos de transporte.

2. **Qué información debemos obtener:** Especificaciones de la arquitectura YOLO11 (parámetros, GFLOPs, tamaño del archivo de pesos) y flujo de inferencia en Python.

3. **Qué evidencia debemos incorporar:** Fragmento clave del módulo `src/detection/yolo_detector.py` y diagrama del flujo de inferencia del detector.

4. **Qué resultados debemos mostrar:** Comparativa técnica entre las variantes Nano (`n`) y Small (`s`) en términos de velocidad de inferencia y consumo de memoria.

5. **Qué elementos del primer documento conservar:** Sección 4.1 (Arquitectura general, Figura 1) y Sección 4.2 (Modelo base).

### 6. Entrenamiento y Experimentación

1. **Qué debe escribirse:** Descripción del entorno de entrenamiento (Google Colab / Kaggle con GPU T4), configuración de hiperparámetros (`epochs`, `batch_size`, `imgsz`, `lr0`, optimizador `AdamW`, aumentación `mosaic`), y descripción de los experimentos ejecutados (Baseline 1 preentrenado vs. Modelo ajustado).

2. **Qué información debemos obtener:** Logs de entrenamiento generados automáticamente por Ultralytics en la carpeta `runs/detect/train/`.

3. **Qué evidencia debemos incorporar:** Gráficas reales generadas por YOLO (`results.png` con curvas de `box_loss`, `cls_loss`, `dfl_loss`, `Precision`, `Recall` y `mAP`), más los mosaicos `train_batch0.jpg` y `val_batch0_pred.jpg`.

4. **Qué resultados debemos mostrar:** Evolución de las pérdidas por época y tiempo total de entrenamiento.

5. **Qué elementos del primer documento conservar:** Sección 4.3 (Línea base) y Sección 4.7 (Plan experimental, Experimentos 1 y 2).

### 7. Integración del Tracking Multiobjeto

1. **Qué debe escribirse:** Implementación de [ByteTrack](https://docs.ultralytics.com/modes/track) sobre las detecciones de YOLO, explicación de la asociación en dos etapas para manejar oclusiones parciales y gestión del ciclo de vida de los identificadores (`track_id`) en memoria.

2. **Qué información debemos obtener:** Parámetros configurados en `bytetrack.yaml` (`track_high_thresh`, `track_low_thresh`, `track_buffer`, `match_thresh`).

3. **Qué evidencia debemos incorporar:** Secuencia de 3 fotogramas consecutivos de un video procesado donde se observe que los mismos vehículos conservan su `ID #` a medida que avanzan por la vía.

4. **Qué resultados debemos mostrar:** Estabilidad de los IDs a lo largo del video de prueba y reducción de duplicaciones frente a la detección cuadro a cuadro sin tracking.

5. **Qué elementos del primer documento conservar:** Justificación de ByteTrack como primera alternativa (Sección 4.2).

### 8. Conteo Vehicular mediante Línea Virtual

1. **Qué debe escribirse:** Formulación matemática e implementación del cruce de segmento mediante producto vectorial sobre el punto inferior central (*bottom-center*) del bounding box, detección del sentido de circulación y uso del conjunto `counted_ids` para impedir el doble conteo.

2. **Qué información debemos obtener:** Resultados de conteo automático arrojados por el módulo `src/rules/line_counter.py` sobre un video de prueba frente al conteo manual del mismo video.

3. **Qué evidencia debemos incorporar:** Captura del video procesado mostrando la línea virtual, el cambio de estado al cruzarla y el contador superpuesto desglosado por `car`, `motorcycle`, `bus` y `truck`.

4. **Qué resultados debemos mostrar:** Tabla comparativa *Conteo Manual vs. Conteo TrafficSense* por tipo de vehículo y cálculo del Error Absoluto y Error Relativo (%).

5. **Qué elementos del primer documento conservar:** Criterio de aceptación de `RF-04` (Sección 2.4) y meta de error relativo $\le 10\%$ (Sección 6.1).

### 9. Implementación de la Detección de Casco

1. **Qué debe escribirse:** Explicación detallada del algoritmo de 9 pasos implementado en `src/rules/helmet_rule.py`: asociación espacial Persona–Motocicleta mediante $\text{IoA} \ge 0.35$ con caja extendida (soportando conductor y acompañante), extracción del tercio superior craneal (*Head ROI*), asociación con `helmet`/`no_helmet` y confirmación mediante ventana deslizante de $K$ sobre $N$ fotogramas.

2. **Qué información debemos obtener:** Parámetros de umbral ($\text{IoA}$, $\text{conf}$, tamaño de ventana $N=8$, mínimo de confirmación $K=5$).

3. **Qué evidencia debemos incorporar:** **Reemplazo definitivo de las Figuras 2, 3 y 4 del primer informe** por un paso a paso visual con fotogramas reales de motociclistas con casco (caja verde) y sin casco (caja roja) procesados por el código del equipo.

4. **Qué resultados debemos mostrar:** Comportamiento de la ventana deslizante ante casos claros, casos con acompañante y casos con oclusión temporal.

5. **Qué elementos del primer documento conservar:** La lógica conceptual de la Sección 4.4 (Regla de decisión de la infracción) y la tabla de casos de la Sección 5.5.

### 10. Registro de Alertas y Evidencia Visual

1. **Qué debe escribirse:** Mecanismo de deduplicación de alertas (`alerted_moto_ids`), generación automática del recorte de imagen (`crop` JPG con margen de contexto), aplicación del filtro de difuminado de privacidad y estampado de metadatos.

2. **Qué información debemos obtener:** Estructura de nombres de archivos de evidencia (ej. `alert_sesion01_id007_20261102_143208.jpg`) y tiempos de escritura en disco.

3. **Qué evidencia debemos incorporar:** Muestras reales de los recortes de imagen guardados automáticamente en la carpeta `data/evidence/`.

4. **Qué resultados debemos mostrar:** Verificación de que una motocicleta infractora que permanece 60 fotogramas en escena genera **exactamente 1 alerta y 1 imagen de evidencia**, cumpliendo `RF-06` y `RF-07`.

5. **Qué elementos del primer documento conservar:** Criterios de `RF-06`, `RF-07` y lineamientos de privacidad de la Sección 2.5 y 3.5.

### 11. Base de Datos

1. **Qué debe escribirse:** Diseño físico y lógico de la base de datos en [SQLite](https://docs.python.org/3/library/sqlite3.html) (`sesiones_monitoreo`, `conteos_vehiculares`, `alertas_infraccion`), diccionario de datos y flujo de inserción/consulta desde Python.

2. **Qué información debemos obtener:** Esquema DDL SQL completo y consultas de agregación utilizadas por el panel.

3. **Qué evidencia debemos incorporar:** Diagrama Entidad-Relación de las 3 tablas y captura de pantalla de los registros almacenados en `trafficsense.db` (vista en DB Browser for SQLite o consulta desde terminal/Streamlit).

4. **Qué resultados debemos mostrar:** Persistencia correcta de fecha, hora, cámara, ID, tipo de vehículo, clasificación de casco, confianza, ruta de evidencia y estado de revisión (`Pendiente`, `Confirmada`, `Descartada`).

5. **Qué elementos del primer documento conservar:** Selección de SQLite para el prototipo (Sección 4.6).

### 12. Desarrollo del Panel de Monitoreo

1. **Qué debe escribirse:** Arquitectura de la interfaz web en [Streamlit](https://docs.streamlit.io/), conexión reactiva con SQLite y el motor de inferencia, diseño de las dos pestañas (*Monitoreo* y *Configuración e Historial*) y funcionalidad de exportación a CSV.

2. **Qué información debemos obtener:** Capturas de pantalla del panel en ejecución local procesando un video real y mostrando indicadores verdaderos.

3. **Qué evidencia debemos incorporar:** **Capturas reales de las Pantallas 1 y 2 en Streamlit** (sustituyendo los bocetos estáticos de las Figuras 5 y 6 del Informe 1) y captura de un archivo CSV exportado abierto en hoja de cálculo.

4. **Qué resultados debemos mostrar:** Funcionamiento de las tarjetas KPI, gráfico de flujo vehicular por hora, galería de alertas recientes, filtros de búsqueda, cambio de estado de revisión humana y descarga de CSV (`RF-08` y `RF-09`).

5. **Qué elementos del primer documento conservar:** La estructura funcional de las Secciones 7.1, 7.2 y 7.3 del Informe 1.

### 13. Pruebas Funcionales

1. **Qué debe escribirse:** Diseño y ejecución de casos de prueba de caja negra sobre los requerimientos funcionales (`RF-01` a `RF-09`).

2. **Qué información debemos obtener:** Resultado de cada caso de prueba (Entrada, Procedimiento, Resultado Esperado, Resultado Obtenido, Estado: Aprobado / En ajuste).

3. **Qué evidencia debemos incorporar:** Fichas o tabla consolidada de los 9 casos de prueba funcionales con referencias a las capturas de verificación.

4. **Qué resultados debemos mostrar:** Porcentaje de casos de prueba funcionales superados satisfactoriamente en el entorno de desarrollo.

5. **Qué elementos del primer documento conservar:** Los criterios de aceptación definidos en la tabla de la Sección 2.4 del Informe 1.

### 14. Métricas Preliminares

1. **Qué debe escribirse:** Definición matemática y reporte de las métricas obtenidas hasta la Semana 10: `Precision`, `Recall`, `F1-Score`, `mAP@0.5` y `mAP@0.5:0.95` en validación para el modelo YOLO; error relativo de conteo vehicular en video de prueba; y rendimiento computacional (`FPS` y latencia en ms por cuadro).

2. **Qué información debemos obtener:** Cifras exactas exportadas por `model.val()` de Ultralytics y por el medidor de tiempos del pipeline.

3. **Qué evidencia debemos incorporar:** Matriz de confusión normalizada (`confusion_matrix_normalized.png`), curva Precisión-Recall (`PR_curve.png`) y tabla de tiempos de inferencia en GPU vs. CPU.

4. **Qué resultados debemos mostrar:** Comparación directa entre las metas iniciales planteadas en la Unidad 1 y los valores preliminares reales obtenidos en la Semana 10 (sin inventar ni inflar ningún número).

5. **Qué elementos del primer documento conservar:** Tabla de métricas y metas iniciales de la Sección 6.1.

### 15. Resultados Obtenidos

1. **Qué debe escribirse:** Síntesis integrada de los logros experimentales y de ingeniería de software alcanzados en las Semanas 6 a 10, destacando la operatividad de extremo a extremo del prototipo.

2. **Qué información debemos obtener:** Resumen de un video de prueba completo procesado de principio a fin por TrafficSense.

3. **Qué evidencia debemos incorporar:** Secuencia visual completa (*Video de entrada* $\to$ *Tracking y Conteo* $\to$ *Detección de Infracción* $\to$ *Registro en SQLite* $\to$ *Visualización en Panel Streamlit*).

4. **Qué resultados debemos mostrar:** Estadísticas reales generadas durante la corrida demostrativa (total de vehículos contados por clase, motocicletas evaluadas, alertas emitidas y tasa de cumplimiento calculada).

5. **Qué elementos del primer documento conservar:** Vínculo directo con el objetivo general y los 5 objetivos específicos de la Sección 1.4.

### 16. Limitaciones Técnicas Actuales

1. **Qué debe escribirse:** Análisis honesto y riguroso de las limitaciones observadas en el prototipo de la Semana 10: sensibilidad a cabezas muy pequeñas/lejanas, oclusiones severas cuando el pasajero va totalmente cubierto por el conductor, falsos negativos en cascos oscuros bajo contraluz, y caída de FPS cuando se ejecutan dos modelos en CPU sin exportar a ONNX.

2. **Qué información debemos obtener:** Ejemplos reales de falsos positivos o falsos negativos detectados durante las pruebas de las semanas 8–10.

3. **Qué evidencia debemos incorporar:** 2 o 3 recortes reales donde el modelo haya tenido baja confianza o error de clasificación, explicando la causa técnica.

4. **Qué resultados debemos mostrar:** Qué medidas de mitigación se aplicarán en las semanas 11 y 12 (ajuste de ROI, reentrenamiento con muestras locales difíciles, exportación a ONNX).

5. **Qué elementos del primer documento conservar:** Tabla de riesgos y mitigaciones de la Sección 6.4.

### 17. Matriz de Avance del Proyecto (Justificación del >60 %)

1. **Qué debe escribirse:** Presentación de la metodología de evaluación ponderada y desglose del avance técnico alcanzado al cierre de la Semana 10.

2. **Qué información debemos obtener:** Porcentajes verificados de los 7 componentes del proyecto según las evidencias adjuntas en el propio informe.

3. **Qué evidencia debemos incorporar:** La **Matriz de Avance Ponderada (Entregable 4 de este documento)** debidamente actualizada con los enlaces o referencias cruzadas a las figuras y tablas del informe.

4. **Qué resultados debemos mostrar:** Demostración cuantitativa y auditable de que el proyecto supera el umbral mínimo del 60 % exigido para la Unidad 2 (ubicándose en el rango 62 %–68 %).

5. **Qué elementos del primer documento conservar:** Cronograma original de la Sección 6.5 como línea base de comparación.

### 18. Conclusiones Parciales (Segunda Unidad)

1. **Qué debe escribirse:** Una conclusión concreta por cada uno de los 5 objetivos específicos del proyecto, indicando qué se ha demostrado empíricamente hasta la Semana 10.

2. **Qué información debemos obtener:** Síntesis de las secciones 3 a 17 del informe.

3. **Qué evidencia debemos incorporar:** Referencia directa a las métricas preliminares y al prototipo funcional construido.

4. **Qué resultados debemos mostrar:** Viabilidad técnica comprobada del sistema TrafficSense y solidez de la arquitectura modular implementada.

5. **Qué elementos del primer documento conservar:** Estructura de los objetivos específicos de la Sección 1.4.

### 19. Actividades Pendientes para la Tercera Unidad (Semanas 11 a 15)

1. **Qué debe escribirse:** Plan de cierre detallado para las semanas 11, 12, 13, 14 y 15: culminación de detalles del panel y regla de infracción (Sem. 11), grabación y pruebas con videos propios de San Martín y análisis de fallos (Sem. 12), reentrenamiento final y comparativa formal con los baselines (Sem. 13), y prueba de usabilidad y presentación final (Sem. 14–15).

2. **Qué información debemos obtener:** Fechas exactas del calendario académico de la UNSM para la Unidad 3 y asignación de responsables por tarea.

3. **Qué evidencia debemos incorporar:** Cronograma actualizado de las Semanas 11 a 15 con entregables de cierre.

4. **Qué resultados debemos mostrar:** Hoja de ruta realista que garantiza llegar al 100 % en la entrega final.

5. **Qué elementos del primer documento conservar:** Bloques de las semanas 11 a 14 de la Sección 6.5 del Informe 1.

### 20. Referencias y Anexos

1. **Qué debe escribirse:** Bibliografía normalizada en formato IEEE/APA y anexos técnicos (código fuente principal, script DDL de SQLite, ficha de licencias de datasets y manual breve de instalación y ejecución).

2. **Qué información debemos obtener:** Metadatos completos de los papers de YOLOv8/YOLO11, ByteTrack (Zhang et al., ECCV 2022), DeepSORT (Wojke et al., ICIP 2017), Microsoft COCO (Lin et al., ECCV 2014) y enlaces oficiales.

3. **Qué evidencia debemos incorporar:** Enlaces al repositorio de GitHub del equipo, enlace al notebook de Google Colab/Kaggle y capturas adicionales de ejecución.

4. **Qué resultados debemos mostrar:** Trazabilidad académica y reproducibilidad del software.

5. **Qué elementos del primer documento conservar:** Las 11 fuentes listadas en la Sección 9 del Informe 1, pero ahora redactadas con rigor bibliográfico completo.

## ENTREGABLE 6. Lista de Programas, Herramientas, Tecnologías y Dependencias

### 6.1 Stack Tecnológico Seleccionado (Gratuito y de Bajo Costo Computacional)

| Categoría | Herramienta / Tecnología | Uso en TrafficSense | Enlace Oficial / Documentación | 
| ----- | ----- | ----- | ----- | 
| **Lenguaje Base** | Python 3.10 – 3.12 | Desarrollo integral del backend de visión artificial, reglas, base de datos y panel. | [docs.python.org](https://docs.python.org/3/) | 
| **Detección de Objetos** | Ultralytics (`ultralytics >= 8.3.0`) | Entrenamiento e inferencia con modelos `yolo11n.pt` / `yolo11s.pt` y `yolov8n.pt`. | [docs.ultralytics.com](https://docs.ultralytics.com/) | 
| **Framework Deep Learning** | PyTorch (`torch`, `torchvision`) | Motor tensorial subyacente para entrenamiento en GPU e inferencia. | [pytorch.org](https://pytorch.org/) | 
| **Tracking y Zonas** | ByteTrack (vía Ultralytics / `supervision`) | Seguimiento multiobjeto con IDs persistentes, `LineZone` y anotadores visuales. | [supervision.roboflow.com](https://supervision.roboflow.com/) | 
| **Procesamiento de Video** | OpenCV (`opencv-python >= 4.9.0`) | Lectura de video/RTSP, recortes de evidencia (`crops`), difuminado de privacidad y dibujo geométrico. | [docs.opencv.org](https://docs.opencv.org/4.9.0/) | 
| **Base de Datos** | SQLite 3 (`sqlite3` nativo) | Almacenamiento relacional local sin servidor para sesiones, conteos y alertas. | [docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html) | 
| **Panel de Monitoreo** | Streamlit (`streamlit >= 1.38.0`) | Construcción rápida del dashboard interactivo de 2 pantallas y descarga CSV. | [docs.streamlit.io](https://docs.streamlit.io/) | 
| **Análisis y Exportación** | Pandas (`pandas`) y NumPy (`numpy`) | Cálculos vectoriales IoU/IoA, agregación horaria de tráfico y generación de CSV. | [pandas.pydata.org](https://pandas.pydata.org/) | 
| **Anotación de Datos** | CVAT / Label Studio / Roboflow | Etiquetado de motocicletas, personas, `helmet` y `no_helmet` en formato YOLO. | [cvat.ai](https://www.cvat.ai/) / [labelstud.io](https://labelstud.io/) | 
| **Entrenamiento en Nube** | Google Colab / Kaggle Notebooks | Acceso gratuito a GPUs NVIDIA T4 (16 GB VRAM) para entrenar `helmet_yolo11n.pt`. | [colab.research.google.com](https://colab.research.google.com/) / [kaggle.com](https://www.kaggle.com/) | 
| **Asistente de Código IA** | Antigravity + Git / GitHub | Desarrollo modular asistido, ejecución de pruebas y control de versiones. | [github.com](https://github.com/) | 

### 6.2 Archivo `requirements.txt` Recomendado

```
ultralytics>=8.3.0
supervision>=0.22.0
opencv-python>=4.9.0.80
numpy>=1.26.0
pandas>=2.2.0
streamlit>=1.38.0
Pillow>=10.3.0
PyYAML>=6.0.1
matplotlib>=3.8.0
seaborn>=0.13.0
onnx>=1.16.0
onnxruntime>=1.18.0
pytest>=8.2.0

```

## ENTREGABLE 7. Arquitectura Técnica Recomendada y Estructura de Carpetas

### 7.1 Determinación sobre la Necesidad de Programar

**Sí, es indispensable desarrollar software funcional para la entrega de la Semana 10.** Presentar únicamente un segundo documento Word con capturas estáticas o un notebook suelto de Google Colab no cubrirá los bloques de las Semanas 8, 9 y 10 de su propio cronograma (tracking integrado, conteo por línea virtual, regla de infracción, base de datos SQLite y primera versión del panel). Sin embargo, gracias a que `ultralytics`, `supervision`, `sqlite3` y `streamlit` resuelven los algoritmos complejos de bajo nivel, **el código que debemos programar es ligero, modular y totalmente realizable en pocos días utilizando Antigravity**.

### 7.2 Estructura Modular de Carpetas del Proyecto (`trafficsense/`)

```
trafficsense/
├── README.md                          # Instrucciones de instalación, arquitectura y ejecución
├── requirements.txt                   # Dependencias de Python reproducibles
├── .gitignore                         # Exclusión de pesos pesados, videos crudos y __pycache__
│
├── configs/
│   ├── config.yaml                    # Parámetros globales: rutas de modelos, línea virtual, umbrales
│   ├── dataset_helmet.yaml            # Configuración YOLO para el entrenamiento de cascos
│   └── bytetrack.yaml                 # Hiperparámetros del tracker ByteTrack
│
├── data/
│   ├── raw_videos/                    # Videos de entrada (.mp4) de prueba y de San Martín
│   ├── processed/                     # Dataset dividido en train/ (70%), val/ (20%), test/ (10%)
│   ├── evidence/                      # Recortes JPG generados automáticamente por cada alerta
│   └── database/
│       └── trafficsense.db            # Base de datos relacional SQLite (autocreable)
│
├── models/
│   ├── yolo11n.pt                     # Pesos base COCO para vehículos y personas (descarga automática)
│   └── helmet_yolo11n.pt              # Pesos ajustados (fine-tuned) para helmet / no_helmet
│
├── notebooks/
│   └── 01_train_helmet_yolo11.ipynb   # Notebook reproducible para entrenar en Google Colab / Kaggle
│
├── scripts/
│   ├── convert_voc_to_yolo.py         # Convierte XML de Kaggle Helmet Detection a TXT formato YOLO
│   ├── split_dataset_by_video.py      # Divide 70/20/10 agrupando por prefijo de video/sesión
│   ├── verify_dataset.py              # Verifica integridad de cajas [0,1] y correspondencia img-txt
│   └── seed_demo_data.py              # Inserta datos de prueba marcados como es_dato_simulado=1
│
├── src/
│   ├── __init__.py
│   ├── config_loader.py               # Carga y validación de configs/config.yaml
│   ├── video/
│   │   └── video_stream.py            # Lectura de video/cámara con OpenCV, redimensionado y FPS
│   ├── detection/
│   │   └── yolo_detector.py           # Wrapper para detector de vehículos y detector de cascos
│   ├── tracking/
│   │   └── tracker_manager.py         # Gestión de ByteTrack e historial de trayectorias por track_id
│   ├── rules/
│   │   ├── geometry.py                # Cálculo de IoU, IoA (Intersection over Area) y cruce vectorial
│   │   ├── line_counter.py            # Conteo vehicular por línea virtual, sentido y deduplicación
│   │   └── helmet_rule.py             # Asociación moto-persona-cabeza, ventana de N cuadros y alerta
│   ├── database/
│   │   └── db_manager.py              # Creación de tablas SQLite, inserción, filtros y exportación CSV
│   ├── utils/
│   │   └── visualizer.py              # Dibujo de cajas por color, línea virtual, recorte y difuminado
│   └── pipeline.py                    # Orquestador principal que une las 7 etapas cuadro a cuadro
│
├── app/
│   └── streamlit_app.py               # Panel web con Pestaña 1 (Monitoreo) y Pestaña 2 (Config/Historial)
│
└── tests/
    ├── test_geometry_and_line.py      # Pruebas unitarias de cruce de línea virtual, IoU e IoA
    ├── test_helmet_rule.py            # Pruebas de ventana deslizante de N cuadros y deduplicación
    └── test_db_manager.py             # Pruebas de inserción, consulta y exportación CSV en SQLite

```

### 7.3 Qué Aprovechamos de Bibliotecas vs. Qué Programamos Nosotros

| Subsistema | Resuelto por Bibliotecas Existentes (No reinventar) | Programación Propia Requerida en Nuestro Proyecto | 
| ----- | ----- | ----- | 
| **Detección YOLO** | Red neuronal, NMS (*Non-Maximum Suppression*), carga de pesos `.pt`/`.onnx` y entrenamiento (`ultralytics`). | `yolo_detector.py`: Invocar detección de vehículos y detección de cascos; estructurar salidas limpias; manejar modo de respaldo si aún no existe `helmet_yolo11n.pt`. | 
| **Tracking Multiobjeto** | Filtro de Kalman, matriz de asociación IoU en dos etapas y asignación de `track_id` (`ultralytics` / `supervision`). | `tracker_manager.py`: Diccionario de estado por `track_id` en memoria, almacenamiento de los últimos centroides y purga de objetos inactivos. | 
| **Conteo Vehicular** | Dibujo de líneas en imagen (`cv2.line` / `sv.LineZone`). | `line_counter.py` y `geometry.py`: Verificación de cambio de signo por producto cruz sobre el punto inferior central, clasificación por tipo (`car`, `motorcycle`, `bus`, `truck`) y conjunto `counted_ids`. | 
| **Regla de Casco** | Inferencia de cajas `helmet` y `no_helmet`. | `helmet_rule.py`: **Núcleo algorítmico propio**: asociación espacial Persona–Moto ($\text{IoA} \ge 0.35$ con soporte para conductor y acompañante), recorte craneal, ventana deslizante de $K/N$ cuadros y conjunto `alerted_moto_ids`. | 
| **Base de Datos y Evidencias** | Motor SQL transaccional (`sqlite3`) y compresión JPEG (`cv2.imwrite`). | `db_manager.py` y `visualizer.py`: Esquema de 3 tablas, guardado de recortes con margen y difuminado de privacidad, actualización de estado (`Pendiente`/`Confirmada`/`Descartada`) y exportación CSV. | 
| **Panel de Monitoreo** | Componentes visuales web, tablas, barras y botones (`streamlit`). | `streamlit_app.py`: Maquetación de las 2 pestañas fiel al diseño de la Unidad 1, bucle de visualización de video en vivo/grabado y conexión reactiva con `db_manager.py`. | 

### 7.4 Cómo Ejecutar y Probar Cada Módulo

1. **Ejecutar pruebas unitarias automatizadas (sin necesidad de GPU ni video pesado):**

   ```
   pytest tests/ -v
   
   ```

2. **Verificar el dataset preparado:**

   ```
   python scripts/verify_dataset.py --data configs/dataset_helmet.yaml
   
   ```

3. **Probar el pipeline completo por línea de comandos sobre un video corto:**

   ```
   python -m src.pipeline --source data/raw_videos/muestra_trafico.mp4 --output data/output_annotated.mp4 --save-db
   
   ```

4. **Iniciar el Panel de Monitoreo en Streamlit:**

   ```
   streamlit run app/streamlit_app.py
   
   ```

## ENTREGABLE 8. Plan de Desarrollo por Fases (Con Prioridades)

Para asegurar el 60 %+ de avance sin dispersar esfuerzos en tareas que corresponden a las semanas 12 a 14, el trabajo se organiza en **7 fases secuenciales y priorizadas**:

### Fase 1: Requisitos Indispensables y Preparación de Datos para la Segunda Entrega (Prioridad: CRÍTICA)

* **Objetivo:** Consolidar el entorno de trabajo, la estructura modular del repositorio y el dataset `TrafficSense-v1.0` validado en formato YOLO con partición 70/20/10 por sesión.

* **Tareas:**

  1. Inicializar la estructura de carpetas `trafficsense/` y el entorno virtual con `requirements.txt`.

  2. Descargar [Kaggle Helmet Detection](https://www.kaggle.com/datasets/andrewmvd/helmet-detection) y un dataset complementario de [Roboflow Universe](https://universe.roboflow.com/search?q=class%3Ahelmet).

  3. Ejecutar `scripts/convert_voc_to_yolo.py` y `scripts/split_dataset_by_video.py`.

  4. Extraer 150–300 fotogramas de un video de tráfico local (a 1–2 FPS) y etiquetarlos en CVAT/Roboflow.

  5. Ejecutar `scripts/verify_dataset.py` para auditar las etiquetas.

* **Herramientas:** Python, CVAT / Roboflow, Kaggle API.

* **Resultado esperado:** Dataset limpio en `data/processed/` y archivo `configs/dataset_helmet.yaml`.

* **Evidencia que debemos generar:** Salida en consola de `verify_dataset.py` (0 errores), tabla de conteo de imágenes/instancias por clase y capturas del proceso de anotación.

* **Dependencias:** Ninguna (punto de partida).

* **Criterios de terminación (DoD):** El script verificador confirma 70 % `train`, 20 % `val`, 10 % `test` sin superposición de secuencias y con coordenadas normalizadas en $[0, 1]$.

### Fase 2: Implementación y Entrenamiento del Núcleo de Inteligencia Artificial (Prioridad: CRÍTICA)

* **Objetivo:** Evaluar el baseline preentrenado (`yolo11n.pt`) y entrenar la primera versión ajustada del detector de cascos (`helmet_yolo11n.pt`).

* **Tareas:**

  1. Configurar y ejecutar el notebook `notebooks/01_train_helmet_yolo11.ipynb` en Google Colab / Kaggle con GPU T4 durante 50 épocas (`imgsz=640`, `batch=16`).

  2. Ejecutar `model.val()` para obtener las métricas en el conjunto de validación (`Precision`, `Recall`, `mAP@0.5`, `mAP@0.5:0.95`).

  3. Descargar los pesos `best.pt` a `models/helmet_yolo11n.pt` (y exportar copia a `helmet_yolo11n.onnx`).

  4. Implementar `src/detection/yolo_detector.py` integrando el detector de vehículos COCO y el detector de cascos.

* **Herramientas:** Google Colab / Kaggle, Ultralytics YOLO11, PyTorch.

* **Resultado esperado:** Archivo `models/helmet_yolo11n.pt` funcional y módulo `yolo_detector.py` capaz de inferir sobre imágenes y cuadros de video.

* **Evidencia que debemos generar:** Curvas `results.png`, `confusion_matrix_normalized.png`, `PR_curve.png`, `val_batch0_pred.jpg` y tabla de métricas preliminares.

* **Dependencias:** Fase 1 completada.

* **Criterios de terminación (DoD):** El modelo `helmet_yolo11n.pt` carga sin errores en local y produce predicciones `helmet` y `no_helmet` con puntuaciones de confianza reales sobre imágenes de prueba.

### Fase 3: Integración del Tracking Multiobjeto y Conteo por Línea Virtual (Prioridad: ALTA)

* **Objetivo:** Lograr que el sistema siga vehículos con IDs persistentes mediante ByteTrack y los cuente por tipo y sentido al cruzar una línea virtual configurable.

* **Tareas:**

  1. Implementar `src/tracking/tracker_manager.py` conectando ByteTrack con las detecciones de vehículos (`car`, `motorcycle`, `bus`, `truck`) y personas (`person`).

  2. Implementar `src/rules/geometry.py` y `src/rules/line_counter.py` con el cálculo de cruce por producto vectorial, sentido de circulación y conjunto `counted_ids`.

  3. Ejecutar pruebas unitarias con `tests/test_geometry_and_line.py`.

* **Herramientas:** Ultralytics ByteTrack, Roboflow Supervision, OpenCV, NumPy, Pytest.

* **Resultado esperado:** Conteo vehicular exacto sin duplicados y seguimiento fluido entre fotogramas.

* **Evidencia que debemos generar:** Video procesado mostrando la línea virtual, las cajas con `ID #` persistente y el marcador de conteo actualizándose en pantalla; tabla comparativa *Conteo Manual vs. Conteo del Sistema* en un clip de 1–2 minutos.

* **Dependencias:** Fase 2 (módulo detector base).

* **Criterios de terminación (DoD):** Un mismo vehículo conserva su ID al cruzar la línea virtual, se contabiliza exactamente una vez en su categoría y pasa los tests unitarios.

### Fase 4: Regla de Infracción Multi-Cuadro, Alertas y Base de Datos SQLite (Prioridad: ALTA)

* **Objetivo:** Implementar la asociación espacial Persona–Motocicleta (conductor y acompañante), la confirmación temporal de ausencia de casco en $K$ de $N$ cuadros, el recorte de evidencia visual y la persistencia en SQLite.

* **Tareas:**

  1. Programar `src/rules/helmet_rule.py` con el cálculo de $\text{IoA} \ge 0.35$ sobre la caja extendida de la motocicleta, asociación con la región craneal (*Head ROI*), ventana deslizante `deque(maxlen=8)` y deduplicación en `alerted_moto_ids`.

  2. Programar el guardado del recorte JPEG en `data/evidence/` con difuminado opcional de privacidad en `src/utils/visualizer.py`.

  3. Implementar `src/database/db_manager.py` con las 3 tablas SQLite (`sesiones_monitoreo`, `conteos_vehiculares`, `alertas_infraccion`) y métodos CRUD + exportación CSV.

  4. Unificar todo el flujo en `src/pipeline.py`.

* **Herramientas:** Python `collections.deque`, OpenCV, `sqlite3`, Pandas.

* **Resultado esperado:** Pipeline de extremo a extremo que procesa un video, guarda recortes de infracción únicos y registra conteos y alertas en `data/database/trafficsense.db`.

* **Evidencia que debemos generar:** Captura de la base de datos SQLite poblada con registros reales, carpeta `data/evidence/` con recortes generados automáticamente y pruebas unitarias `test_helmet_rule.py` y `test_db_manager.py` aprobadas.

* **Dependencias:** Fases 2 y 3 completadas.

* **Criterios de terminación (DoD):** Cada motocicleta con ocupante sin casco confirmado en $\ge 5$ de $8$ cuadros genera exactamente una fila en `alertas_infraccion` y un archivo `.jpg` en `data/evidence/`.

### Fase 5: Desarrollo de la Primera Versión Funcional del Panel de Monitoreo (Prioridad: MEDIA-ALTA)

* **Objetivo:** Construir el dashboard web de 2 pestañas en Streamlit alimentado por el pipeline real y la base de datos SQLite.

* **Tareas:**

  1. Desarrollar la Pestaña 1 (*Monitoreo*) en `app/streamlit_app.py`: reproductor/procesador de video anotado, 4 tarjetas KPI, gráfico de barras de flujo por hora y lista de alertas recientes con miniaturas de evidencia.

  2. Desarrollar la Pestaña 2 (*Configuración e Historial*): ajuste de coordenadas de línea virtual y umbrales (`conf`, cuadros $K/N$), filtros por fecha/cámara/estado, selector para cambiar el estado de revisión (`Pendiente` $\to$ `Confirmada` / `Descartada`) y botón de exportación a CSV.

* **Herramientas:** Streamlit, Pandas, SQLite3, Pillow.

* **Resultado esperado:** Aplicación web interactiva ejecutable con `streamlit run app/streamlit_app.py`.

* **Evidencia que debemos generar:** Capturas en alta resolución de ambas pestañas operando con datos reales y archivo CSV exportado.

* **Dependencias:** Fase 4 completada.

* **Criterios de terminación (DoD):** El panel refleja los conteos y alertas reales almacenados en SQLite, permite actualizar el estado de una alerta y descarga correctamente el reporte CSV.

### Fase 6: Pruebas Funcionales y Recolección de Evidencias (Prioridad: ALTA)

* **Objetivo:** Ejecutar un protocolo de pruebas sobre los requerimientos `RF-01` a `RF-09`, medir FPS/latencia y recopilar todas las capturas, gráficas y tablas necesarias para la defensa del 60 %.

* **Tareas:**

  1. Procesar de principio a fin al menos 2 videos de tráfico diurno (de 30 a 90 segundos cada uno) donde aparezcan autos, buses/camiones y motocicletas con y sin casco.

  2. Realizar el conteo manual de esos clips para calcular el error relativo del conteo vehicular.

  3. Completar la matriz de casos de prueba `RF-01` a `RF-09` y capturar todas las pantallas numeradas.

* **Herramientas:** Pipeline TrafficSense, Streamlit, hoja de cálculo para conteo manual.

* **Resultado esperado:** Carpeta de evidencias lista para insertar en el informe y mostrar en la exposición.

* **Evidencia que debemos generar:** Video demostrativo renderizado (`output_demo.mp4`), tabla de error de conteo, tabla de métricas YOLO y capturas de los 9 requerimientos funcionales.

* **Dependencias:** Fases 1 a 5 completadas.

* **Criterios de terminación (DoD):** Todas las cifras que se van a escribir en el informe cuentan con su respaldo gráfico y experimental verificable.

### Fase 7: Elaboración y Cierre del Segundo Informe Académico (Prioridad: ALTA)

* **Objetivo:** Redactar el documento formal de la Unidad 2 siguiendo la estructura de 20 secciones del Entregable 5 e incorporando la Matriz de Avance Ponderada.

* **Tareas:**

  1. Reemplazar los bocetos y dibujos de patentes del primer informe por los resultados y capturas reales de las Fases 1 a 6.

  2. Redactar el análisis de limitaciones técnicas y el plan de trabajo para la Unidad 3 (Semanas 11 a 15).

  3. Completar las referencias bibliográficas en formato IEEE/APA y revisar la coherencia general del documento.

* **Herramientas:** Procesador de textos (Word / Google Docs), gestor bibliográfico.

* **Resultado esperado:** Segundo Informe Académico terminado y presentación lista para el docente.

* **Evidencia que debemos generar:** Documento final del Segundo Entregable y diapositivas/demostración en vivo.

* **Dependencias:** Fase 6 completada.

* **Criterios de terminación (DoD):** El informe no contiene campos *"Por definir"*, no inventa métricas, incluye evidencias reales de todos los componentes y justifica más del 60 % de avance.

## ENTREGABLE 9. Prompt Especializado, Independiente y Completo para Antigravity

Copia y pega el siguiente bloque **exactamente como está** en **Antigravity** para construir la base completa y funcional del software TrafficSense de manera incremental, segura y auditable:

````
# PROMPT DE INGENIERÍA DE SOFTWARE PARA ANTIGRAVITY: PROYECTO TRAFFICSENSE (HITO 2 - SEMANA 10)

## 1. CONTEXTO Y OBJETIVO DEL PROYECTO
Estás asistiendo al equipo de Ingeniería de Sistemas e Informática de la Universidad Nacional de San Martín (UNSM) en el desarrollo de **TrafficSense: Monitoreo de flujo vehicular y detección de motociclistas sin casco mediante YOLO y tracking multi-objeto**.
Necesitamos construir el prototipo funcional correspondiente a la **Semana 10 (Segundo Entregable, >60 % de avance)** en Python, respetando nuestra arquitectura de 7 etapas:
1. Captura de video (OpenCV: archivo `.mp4`/`.avi`, RTSP o webcam).
2. Preprocesamiento (redimensionado, ROI y control de FPS).
3. Detección con Ultralytics YOLO (`yolo11n.pt` / `yolov8n.pt`).
4. Seguimiento multiobjeto con ByteTrack (asignación de `track_id` persistente).
5. Reglas de negocio:
   - Conteo vehicular por cruce de línea virtual configurable (clasificando `car`, `motorcycle`, `bus`, `truck`, identificando el sentido de circulación y evitando doble conteo por `track_id`).
   - Detección de motociclistas sin casco: asociación espacial entre motocicleta (`motorcycle`) y sus ocupantes (`person`/`rider`, soportando conductor y acompañante), análisis de la región superior de la cabeza (`helmet` vs. `no_helmet`), confirmación mediante ventana deslizante de $K$ sobre $N$ fotogramas consecutivos y emisión de una única alerta por motocicleta seguida.
6. Almacenamiento persistente en SQLite (`sqlite3`) + guardado de recortes de imagen (`crops` JPG) como evidencia visual (con opción de difuminado de privacidad en el tercio facial/placa).
7. Panel de monitoreo web en Streamlit con dos pestañas: (1) Monitoreo de video, KPIs, flujo por hora y alertas recientes con evidencia; (2) Configuración de línea virtual/umbrales, historial de alertas con revisión humana (`Pendiente`, `Confirmada`, `Descartada`) y exportación a CSV.

## 2. REGLAS ESTRICTAS DE INTEGRIDAD Y CALIDAD (OBLIGATORIAS)
1. **Inspección previa obligatoria:** Antes de crear o modificar cualquier archivo, inspecciona todo el directorio de trabajo actual (`ls`, árbol de directorios, archivos `.py`, `.ipynb`, `.yaml`, `.db` o pesos `.pt` existentes).
2. **Prohibido sobrescribir o borrar trabajo previo sin justificación:** Si ya existen scripts, notebooks, modelos entrenados o configuraciones, intégralos y respétalos. Antes de reemplazar un archivo existente con lógica previa, explica qué encontraste y por qué se refactoriza.
3. **Prohibido inventar resultados de IA o simular detecciones falsas en el motor de inferencia:** El pipeline de video NO debe generar cajas aleatorias ni falsificar detecciones de cascos.
4. **Manejo transparente de la dependencia del modelo de cascos (`helmet_yolo11n.pt`):**
   - El sistema debe utilizar dos detectores o modos claramente definidos:
     a) **Detector de tráfico base (`models/yolo11n.pt` o descarga oficial de Ultralytics):** Detecta `person` (clase 0), `car` (clase 2), `motorcycle` (clase 3), `bus` (clase 5) y `truck` (clase 7) sobre COCO. Esto permite que el tracking ByteTrack, el conteo vehicular por línea virtual y la asociación Persona-Motocicleta funcionen al 100 % con pesos reales desde el primer momento.
     b) **Detector especializado de cascos (`models/helmet_yolo11n.pt`):** Busca este archivo de pesos entrenado para las clases `helmet` y `no_helmet`.
   - **Si `models/helmet_yolo11n.pt` AÚN NO EXISTE en el disco:** El sistema NO debe romperse ni debe inventar que detectó un casco. Debe mostrar una advertencia explícita en consola y en el panel de Streamlit (`"⚠️ Modo Base Activo: Pesos 'models/helmet_yolo11n.pt' no encontrados. El conteo vehicular, tracking ByteTrack y asociación Persona-Moto están operativos; la clasificación de casco queda en estado 'SIN_MODELO_CASCO' hasta colocar los pesos entrenados."`). Adicionalmente, incluye un modo opcional de prueba (`--demo-rule-test` o script de semilla claramente etiquetado como `es_dato_simulado = 1` en SQLite) EXCLUSIVAMENTE para probar la base de datos y la interfaz del panel cuando no se está corriendo un video con el modelo de cascos.

## 3. ARQUITECTURA DE CARPETAS Y ARCHIVOS A IMPLEMENTAR
Construye de forma incremental la siguiente estructura modular (adaptándola si ya existen carpetas equivalentes en el repositorio):

```text
trafficsense/
├── README.md
├── requirements.txt
├── configs/
│   ├── config.yaml
│   ├── dataset_helmet.yaml
│   └── bytetrack.yaml
├── data/
│   ├── raw_videos/
│   ├── processed/
│   ├── evidence/
│   └── database/
├── models/
├── scripts/
│   ├── convert_voc_to_yolo.py
│   ├── split_dataset_by_video.py
│   ├── verify_dataset.py
│   └── seed_demo_data.py
├── src/
│   ├── __init__.py
│   ├── config_loader.py
│   ├── video/
│   │   └── video_stream.py
│   ├── detection/
│   │   └── yolo_detector.py
│   ├── tracking/
│   │   └── tracker_manager.py
│   ├── rules/
│   │   ├── geometry.py
│   │   ├── line_counter.py
│   │   └── helmet_rule.py
│   ├── database/
│   │   └── db_manager.py
│   ├── utils/
│   │   └── visualizer.py
│   └── pipeline.py
├── app/
│   └── streamlit_app.py
└── tests/
    ├── test_geometry_and_line.py
    ├── test_helmet_rule.py
    └── test_db_manager.py

````

## 4. ESPECIFICACIONES TÉCNICAS PASO A PASO (DESARROLLO INCREMENTAL)

### PASO 1: Auditoría del Repositorio y Configuración Base

* Analiza el workspace actual y reporta qué archivos existen.

* Crea `requirements.txt` y `configs/config.yaml` con parámetros configurables:

  * `video_source`, `camera_name` (`"Cámara 01 - Av. Principal"`), `vehicle_model_path` (`"models/yolo11n.pt"`), `helmet_model_path` (`"models/helmet_yolo11n.pt"`).

  * `confidence_threshold: 0.50`, `iou_threshold: 0.45`.

  * `counting_line`: `p1: [100, 400]`, `p2: [1180, 400]`.

  * `helmet_rule`: `rider_moto_ioa_threshold: 0.35`, `moto_upper_expansion_ratio: 0.35`, `head_roi_ratio: 0.35`, `window_size_frames: 8`, `min_confirm_frames: 5`, `apply_privacy_blur: true`.

### PASO 2: Scripts de Preparación y Verificación de Dataset (`scripts/`)

* `scripts/convert_voc_to_yolo.py`: Convierte anotaciones XML (formato PASCAL VOC como el dataset Kaggle Helmet Detection de `andrewmvd`) a archivos `.txt` en formato YOLO normalizado (`class_id x_center y_center width height`), mapeando etiquetas equivalentes (`With Helmet`/`helmet` -> `0`, `Without Helmet`/`no_helmet` -> `1`).

* `scripts/split_dataset_by_video.py`: Divide un directorio de imágenes y etiquetas en `train` (70 %), `val` (20 %) y `test` (10 %) agrupando por prefijo de secuencia o video para evitar fuga de datos (*data leakage*).

* `scripts/verify_dataset.py`: Verifica que cada imagen tenga su `.txt`, que las coordenadas estén en `[0.0, 1.0]`, cuenta las instancias por clase e imprime un reporte de auditoría listo para pegar en el informe académico.

### PASO 3: Geometría, Tracking y Conteo Vehicular (`src/rules/geometry.py`, `src/tracking/tracker_manager.py`, `src/rules/line_counter.py`)

* En `geometry.py`:

  * Implementa `compute_iou(boxA, boxB)`.

  * Implementa `compute_ioa(inner_box, outer_box)` (área de intersección dividida entre el área de `inner_box`).

  * Implementa `expand_bbox_upwards(bbox, ratio=0.35, img_h=None)` para extender la caja de una motocicleta hacia arriba y cubrir a los ocupantes.

  * Implementa `check_segment_crossing(prev_pt, curr_pt, line_p1, line_p2)` usando producto vectorial 2D que devuelva `(crossed: bool, direction: Optional[str])` (`"Entrada"` o `"Salida"`).

* En `tracker_manager.py`:

  * Mantén el estado de cada `track_id` activo: historial de puntos inferiores centrales (*bottom-center*: `((x1+x2)/2, y2)`), clase vehicular estabilizada, ventana deslizante de casco (`deque`) y edad de inactividad.

* En `line_counter.py`:

  * Evalúa para cada vehículo rastreado (`car`, `motorcycle`, `bus`, `truck`) si su segmento `(prev_bottom_center, curr_bottom_center)` cruzó la línea virtual `(P1, P2)`.

  * Usa un conjunto `counted_ids: set[int]` para garantizar que ningún `track_id` se cuente dos veces.

  * Lleva contadores acumulados por clase vehicular y por sentido (`Entrada` / `Salida`).

### PASO 4: Regla de Detección de Motociclistas sin Casco (`src/rules/helmet_rule.py`)

Implementa una clase `HelmetInfractionRule` que ejecute en cada fotograma:

1. Recibe las motocicletas rastreadas (con su `track_id`), las personas detectadas en el cuadro y las detecciones de `helmet` / `no_helmet` (si el modelo de cascos está activo).

2. **Asociación Persona–Motocicleta (Conductor y Acompañante):**

   * Para cada motocicleta $M_i$, expande su caja un 35 % hacia arriba (`M_i_ext`).

   * Asocia a $M_i$ todas las personas $P_j$ cuyo `compute_ioa(P_j, M_i_ext) >= 0.35`. Esto permite detectar 1, 2 o más ocupantes sobre la misma moto.

3. **Región de Cabeza (*Head ROI*) y Asociación de Casco:**

   * Para cada ocupante $P_j$ asociado a $M_i$, calcula su tercio superior: `head_roi = [x1, y1, x2, y1 + 0.35 * (y2 - y1)]`.

   * Empareja las detecciones `helmet` y `no_helmet` (con `conf >= confidence_threshold`) cuyo centroide caiga dentro de `head_roi` (o tengan `IoU >= 0.25` con `head_roi`).

4. **Decisión del Cuadro y Ventana Deslizante (**$K$ **de** $N$ **cuadros):**

   * Si al menos un ocupante de $M_i$ tiene predicción `no_helmet` válida en el cuadro actual, agrega `"no_helmet"` (y su confianza) a la ventana deslizante `deque(maxlen=window_size_frames)` del `track_id` de la motocicleta.

   * Si todos los ocupantes detectados tienen `"helmet"`, agrega `"helmet"`.

   * Si en la ventana actual de longitud $N$ (ej. 8) existen al menos $K$ (ej. 5) votos `"no_helmet"`, marca la motocicleta como infractora confirmada.

   * Si se confirma el estado `"helmet"` en al menos $K$ cuadros y la moto no ha sido contabilizada en las métricas de cumplimiento, regístrala como `"con_casco"` para poder calcular el `% de Cumplimiento` real.

5. **Deduplicación de Alertas:**

   * Usa `alerted_moto_ids: set[int]` para que cada `track_id` infractor genere **una única alerta y un único recorte de imagen** durante todo su recorrido.

### PASO 5: Almacenamiento en SQLite y Evidencias (`src/database/db_manager.py` y `src/utils/visualizer.py`)

* En `db_manager.py`:

  * Crea automáticamente `data/database/trafficsense.db` con las tablas:

    1. `sesiones_monitoreo`

    2. `conteos_vehiculares`

    3. `alertas_infraccion` (campos: `alerta_id`, `sesion_id`, `fecha`, `hora`, `camara`, `track_id`, `tipo_vehiculo`, `clasificacion_casco`, `ocupantes_detectados`, `confianza`, `cuadros_confirmados`, `ruta_evidencia`, `estado_revision`, `es_dato_simulado`).

  * Incluye métodos para insertar sesiones, conteos y alertas, consultar KPIs globales, obtener flujo agrupado por hora, filtrar historial por fecha/cámara/estado/simulado, actualizar `estado_revision` (`'Pendiente'`, `'Confirmada'`, `'Descartada'`) y exportar a CSV.

* En `visualizer.py`:

  * Función `save_evidence_crop(frame, moto_ext_bbox, save_path, apply_privacy_blur=True)` que recorte la motocicleta y sus ocupantes con un margen de 15 píxeles y guarde el archivo `.jpg`.

  * Función `draw_annotations(...)` que dibuje la línea virtual y las cajas en colores semánticos: verde (`con_casco`), rojo (`sin_casco`), amarillo (`moto en evaluación / sin modelo de casco`) y azul (`car`, `bus`, `truck`).

* En `scripts/seed_demo_data.py`:

  * Crea un script que genere datos de prueba en SQLite e imágenes sintéticas de prueba en `data/evidence/` marcando explícitamente `es_dato_simulado = 1` y un sello visual `"DATO SIMULADO DE PRUEBA"` en la imagen, para que jamás se confundan con datos reales.

### PASO 6: Orquestador del Pipeline (`src/pipeline.py`) y Panel de Monitoreo (`app/streamlit_app.py`)

* En `src/pipeline.py`:

  * Implementa la clase `TrafficSensePipeline` que pueda ejecutarse tanto por CLI (`python -m src.pipeline --source ...`) como desde Streamlit mediante un generador (`yield frame_annotated, frame_stats`).

  * Incluye manejo robusto de excepciones (archivos de video inexistentes, fin de stream, ausencia de GPU haciendo fallback automático a CPU).

* En `app/streamlit_app.py`:

  * **Pestaña 1 ("📹 Monitoreo"):**

    * Selector de fuente de video (subir archivo `.mp4`/`.avi`, elegir de `data/raw_videos/` o usar webcam) y botón Iniciar/Detener procesamiento.

    * Visor de video anotado en vivo + barra inferior con `FPS`, `Latencia (ms)`, `Modelo Activo` y `Tracker`.

    * 4 tarjetas KPI (`Vehículos Totales`, `Motocicletas`, `Alertas Sin Casco`, `% Cumplimiento`).

    * Gráfico de barras de flujo vehicular por hora y sección de `Alertas Recientes (Evidencia)` mostrando las miniaturas `.jpg` reales.

  * **Pestaña 2 ("⚙️ Configuración e Historial"):**

    * Controles para ajustar las coordenadas de la línea virtual `(x1, y1) - (x2, y2)` con vista previa sobre un cuadro del video, umbral de confianza y cuadros de confirmación $K/N$.

    * Filtros por Fecha, Cámara, Estado (`Todos`, `Pendiente`, `Confirmada`, `Descartada`) y casilla para ocultar/mostrar registros con `es_dato_simulado = 1`.

    * Tabla de historial de infracciones, selector para cambiar el `estado_revision` de cualquier alerta en SQLite y botón de descarga `Exportar CSV`.

### PASO 7: Pruebas Automatizadas, Corrección de Errores y Documentación

* Escribe y ejecuta las pruebas unitarias en `tests/test_geometry_and_line.py`, `tests/test_helmet_rule.py` y `tests/test_db_manager.py` con `pytest`.

* Si alguna prueba falla, corrige el código hasta que el 100 % de los tests pasen.

* Redacta un `README.md` completo con:

  1. Requisitos e instalación paso a paso.

  2. Comandos para preparar el dataset, ejecutar tests, correr el pipeline por CLI y levantar el panel en Streamlit.

  3. Tabla clara de **Funcionalidades Implementadas vs. Dependencias Pendientes** (indicando dónde colocar `models/helmet_yolo11n.pt` tras entrenarlo en Colab).

```

---

## ENTREGABLE 10. Lista de Evidencias y Capturas que Debemos Conseguir para la Presentación

Para sustentar sin fisuras el avance mínimo del 60 % ante el docente en la Semana 10, debemos recolectar e incluir en el informe y en las diapositivas las siguientes **12 evidencias verificables**:

| N.º | Categoría | Evidencia o Captura Específica | Dónde se Obtiene | Qué Demuestra ante el Docente |
| :---: | :--- | :--- | :--- | :--- |
| **E-01** | **Repositorio y Arquitectura** | Captura del árbol de carpetas modular en el IDE (Antigravity/VS Code) y del historial de commits en GitHub. | Entorno local y GitHub | Que existe una arquitectura de software limpia y trabajo colaborativo real. |
| **E-02** | **Dataset y Etiquetado** | Captura de pantalla de [CVAT](https://www.cvat.ai/) o [Roboflow](https://universe.roboflow.com/) mostrando fotogramas con las cajas `motorcycle`, `rider`, `helmet` y `no_helmet`, junto con un archivo `.txt` YOLO abierto. | Herramienta de anotación | Cumplimiento del bloque Semanas 6–7 (preparación y anotación de datos). |
| **E-03** | **Auditoría del Dataset** | Captura de la salida de consola de `python scripts/verify_dataset.py` mostrando el conteo exacto de imágenes en `train` (70 %), `val` (20 %) y `test` (10 %) con 0 errores de formato. | Terminal de Python | Rigor metodológico en la partición de datos sin fuga de información (*data leakage*). |
| **E-04** | **Entrenamiento del Modelo YOLO** | Gráfica `results.png` generada por Ultralytics en Google Colab / Kaggle mostrando la caída de `box_loss`/`cls_loss` y el ascenso de `mAP@0.5` durante las épocas de entrenamiento. | Carpeta `runs/detect/train/` en Colab/Kaggle | Que el modelo fue efectivamente entrenado (*fine-tuned*) y no es una simulación. |
| **E-05** | **Métricas Preliminares de IA** | Imagen `confusion_matrix_normalized.png`, curva `PR_curve.png` y mosaico `val_batch0_pred.jpg` generados al validar el modelo. | Carpeta `runs/detect/val/` | Desempeño cuantitativo real del detector en las clases `helmet` y `no_helmet`. |
| **E-06** | **Tracking Multiobjeto (ByteTrack)** | Tira visual de 3 fotogramas consecutivos ($t, t+15, t+30$) de un video de tráfico donde se observe que una misma motocicleta y un mismo auto conservan exactamente el mismo `ID #`. | Video procesado por `src/pipeline.py` | Cumplimiento de `RF-02` y `RF-03` (seguimiento persistente entre cuadros). |
| **E-07** | **Conteo por Línea Virtual** | Captura del instante en que un vehículo cruza la línea virtual y el contador en pantalla se incrementa, acompañada de la tabla comparativa *Conteo Manual vs. Conteo Automático* de un clip de prueba. | Video procesado + conteo manual | Cumplimiento de `RF-04` y verificación de la meta de error de conteo. |
| **E-08** | **Regla de Casco y Multi-Ocupante** | Captura comparativa de una motocicleta con conductor con casco (caja verde) y otra con ocupante sin casco tras superar la ventana de $K$ de $N$ cuadros (caja roja de alerta). | Video procesado por `helmet_rule.py` | Cumplimiento de `RF-05` y `RF-06` (reemplazando las patentes simuladas del Informe 1). |
| **E-09** | **Recortes de Evidencia Visual** | Captura de la carpeta `data/evidence/` mostrando los recortes `.jpg` generados automáticamente para cada alerta única (con difuminado de privacidad aplicado). | Explorador de archivos local | Cumplimiento de `RF-07` y respeto a la [Ley N.º 29733](https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733). |
| **E-10** | **Persistencia en Base de Datos** | Captura de las tablas `conteos_vehiculares` y `alertas_infraccion` en `trafficsense.db` mostrando filas con fecha, hora, `track_id`, confianza, ruta de evidencia y estado `Pendiente`. | DB Browser for SQLite o consulta SQL | Que las alertas y conteos se almacenan de forma persistente y estructurada. |
| **E-11** | **Panel de Monitoreo Funcional** | Capturas reales de la **Pestaña 1 (Monitoreo)** y de la **Pestaña 2 (Configuración e Historial)** en Streamlit, más el archivo `.csv` exportado abierto en Excel/Sheets. | Navegador web (`localhost:8501`) | Cumplimiento de `RF-08` y `RF-09` (reemplazando los bocetos de las Figuras 5 y 6). |
| **E-12** | **Pruebas Unitarias y Video Demo** | Captura de `pytest tests/ -v` con todos los tests en verde (`PASSED`) y un video corto (`demo_semana10.mp4` de 30–60 s) listo para reproducir en vivo frente al docente. | Terminal + Reproductor de video | Calidad de ingeniería de software y demostración funcional en vivo. |

---

## ENTREGABLE 11. Lista de Actividades que Deben Quedar para la Tercera Unidad (Semanas 11 a 15)

Para proteger al equipo de la sobrecarga en la Semana 10 y mantener la coherencia con el cronograma original del proyecto, las siguientes actividades **deben declararse explícitamente en el informe como planificadas para la Tercera Unidad (Semanas 11 a 15)**:

| Semana | Actividad Programada para la Tercera Unidad | Por qué corresponde a la Unidad 3 y no a la Semana 10 |
| :---: | :--- | :--- |
| **Semana 11** | **Refinamiento de la regla de infracción, ajustes visuales del panel web y cierre del bloque Semanas 10–11.** | En el cronograma original (Sección 6.5), la regla de infracción, base de datos y panel abarcan las semanas 10 y 11; en la Semana 10 se entrega la versión funcional base (MVP) y en la 11 se pule la interfaz y el manejo de casos borde. |
| **Semana 12** | **Campaña de grabación y pruebas extensivas con videos propios de San Martín (mañana, mediodía y tarde) y análisis sistemático de errores.** | Planificado originalmente para la Semana 12. Incluye evaluar el comportamiento ante sombras, contraluz, mototaxis (trimóviles muy frecuentes en Tarapoto/San Martín), cascos oscuros y motocicletas con múltiples pasajeros. |
| **Semana 12–13** | **Segundo ciclo de ajuste fino (*Fine-Tuning v2*) re-entrenando el modelo con los casos difíciles locales (*Hard Negative Mining*).** | Requiere haber ejecutado primero el análisis de errores de la Semana 12 sobre los videos locales de San Martín. |
| **Semana 13** | **Evaluación experimental definitiva: comparativa formal entre Baseline 1 (COCO), Baseline 2 (Datos públicos) y Modelo Final (Datos públicos + propios), y comparación entre ByteTrack y BoT-SORT.** | Corresponde a los Experimentos 3, 4 y 5 del Plan Experimental (Sección 4.7) y a la Semana 13 del cronograma original. |
| **Semana 13–14** | **Cálculo de métricas avanzadas de seguimiento (`IDF1`, `MOTA`, `HOTA`, *ID Switches*) sobre secuencias anotadas de prueba.** | Requiere contar con secuencias de video de prueba completamente anotadas cuadro a cuadro para seguimiento. |
| **Semana 14–15** | **Prueba de usabilidad del panel con 3 a 5 usuarios finales, optimización final de inferencia (ONNX/OpenVINO), redacción del informe final y demostración de cierre del curso.** | Corresponde al cierre del proyecto (Hito Final) donde se consolida el 100 % de los requerimientos funcionales y no funcionales. |

---

## SECCIÓN DE VERIFICACIÓN: Datos Faltantes y Preguntas Concretas para el Equipo

Para pasar de este Plan Maestro a la redacción final de los resultados del **Segundo Informe Académico** sin inventar ningún dato, necesito que me confirmen los siguientes **5 puntos específicos que no aparecen en el documento de la Unidad 1**:

1. **Estado real de su código y repositorio hoy:** ¿Tienen ya algún script de Python, notebook de Google Colab o repositorio en GitHub iniciado entre las semanas 6 y 10, o empezarán a generar todo el código ahora mismo usando el Prompt de Antigravity del Entregable 9?
2. **Estado de los datos y videos locales de San Martín:** ¿Han logrado grabar ya algún video de tráfico en calles de San Martín (Tarapoto u otra localidad) o descargar algún dataset de Kaggle/Roboflow, o todavía no cuentan con videos locales grabados?
3. **Estado del entrenamiento del modelo de cascos:** ¿Tienen ya un modelo YOLO entrenado (`best.pt`) con sus gráficas `results.png` y matriz de confusión, o necesitan ejecutar primero el entrenamiento en Google Colab siguiendo la Fase 2?
4. **Hardware disponible en el equipo:** ¿En qué equipo ejecutarán la demostración frente al docente (laptop solo con CPU Intel/AMD, laptop con GPU NVIDIA dedicada, o ejecución desde Google Colab)?
5. **Datos administrativos del curso:** ¿Cuáles son los nombres completos de los integrantes del equipo, el nombre del docente del curso y la confirmación de si la tercera unidad cierra en la semana 14 o en la semana 15 según el sílabo oficial de la UNSM?

```