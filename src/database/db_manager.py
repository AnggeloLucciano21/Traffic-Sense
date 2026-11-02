"""
Módulo de persistencia relacional con SQLite 3 para TrafficSense.
Gestiona el esquema de base de datos para sesiones de monitoreo, aforo vehicular
y registro de alertas de infracción con auditoría y revisión humana.
"""

from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd


class DatabaseManager:
    """
    Administrador transaccional de SQLite para TrafficSense.
    """

    def __init__(self, db_path: str | Path = "data/database/trafficsense.db", auto_create: bool = True):
        self.db_path = Path(db_path)
        if str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn: Optional[sqlite3.Connection] = None
        if auto_create:
            self.create_tables()

    def get_connection(self) -> sqlite3.Connection:
        """Retorna una conexión a SQLite configurada con row_factory como sqlite3.Row."""
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self) -> None:
        """Crea el esquema relacional de 3 tablas si no existe."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. Sesiones de monitoreo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesiones_monitoreo (
                sesion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_fuente TEXT NOT NULL,
                camara TEXT NOT NULL DEFAULT 'CAM-01-TARAPOTO',
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                modelo_usado TEXT NOT NULL,
                tracker_usado TEXT NOT NULL DEFAULT 'ByteTrack',
                fps_promedio REAL DEFAULT 0.0,
                total_vehiculos INTEGER DEFAULT 0,
                total_motos INTEGER DEFAULT 0,
                total_alertas INTEGER DEFAULT 0
            )
        """)

        # 2. Conteos vehiculares por línea virtual
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conteos_vehiculares (
                conteo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                hora_franja TEXT NOT NULL,
                camara TEXT NOT NULL,
                track_id INTEGER NOT NULL,
                tipo_vehiculo TEXT NOT NULL,
                sentido TEXT NOT NULL,
                confianza REAL NOT NULL,
                FOREIGN KEY (sesion_id) REFERENCES sesiones_monitoreo(sesion_id)
            )
        """)

        # 3. Alertas de infracción y cumplimiento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas_infraccion (
                alerta_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                camara TEXT NOT NULL,
                track_id INTEGER NOT NULL,
                tipo_vehiculo TEXT NOT NULL DEFAULT 'motorcycle',
                clasificacion_casco TEXT NOT NULL,
                ocupantes_detectados INTEGER DEFAULT 1,
                confianza REAL NOT NULL,
                cuadros_confirmados INTEGER NOT NULL,
                ruta_evidencia TEXT,
                estado_revision TEXT NOT NULL DEFAULT 'Pendiente',
                es_dato_simulado INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (sesion_id) REFERENCES sesiones_monitoreo(sesion_id)
            )
        """)

        conn.commit()
        conn.close()

    def start_session(
        self,
        nombre_fuente: str,
        camara: str = "CAM-01-TARAPOTO",
        modelo_usado: str = "yolo11n.pt",
        tracker_usado: str = "ByteTrack"
    ) -> int:
        """Registra el inicio de una sesión de procesamiento de video."""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO sesiones_monitoreo (nombre_fuente, camara, fecha_inicio, modelo_usado, tracker_usado)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre_fuente, camara, now, modelo_usado, tracker_usado))

        sesion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return sesion_id

    def end_session(
        self,
        sesion_id: int,
        total_vehiculos: int,
        total_motos: int,
        total_alertas: int,
        fps_promedio: float = 0.0
    ) -> None:
        """Actualiza la sesión con los totales acumulados y fecha de cierre."""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            UPDATE sesiones_monitoreo
            SET fecha_fin = ?, total_vehiculos = ?, total_motos = ?, total_alertas = ?, fps_promedio = ?
            WHERE sesion_id = ?
        """, (now, total_vehiculos, total_motos, total_alertas, fps_promedio, sesion_id))

        conn.commit()
        conn.close()

    def insert_conteo(self, conteo: Dict[str, Any]) -> int:
        """Inserta un registro individual de cruce de línea."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conteos_vehiculares (
                sesion_id, fecha, hora, hora_franja, camara, track_id, tipo_vehiculo, sentido, confianza
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conteo.get("sesion_id"),
            conteo.get("fecha", datetime.now().strftime("%Y-%m-%d")),
            conteo.get("hora", datetime.now().strftime("%H:%M:%S")),
            conteo.get("hora_franja", datetime.now().strftime("%H:00")),
            conteo.get("camara", "CAM-01-TARAPOTO"),
            conteo.get("track_id"),
            conteo.get("tipo_vehiculo", "car"),
            conteo.get("sentido", "Entrada"),
            conteo.get("confianza", 1.0)
        ))

        conteo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conteo_id

    def insert_alerta(self, alerta: Dict[str, Any]) -> int:
        """Inserta un registro de alerta de casco."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alertas_infraccion (
                sesion_id, fecha, hora, camara, track_id, tipo_vehiculo,
                clasificacion_casco, ocupantes_detectados, confianza,
                cuadros_confirmados, ruta_evidencia, estado_revision, es_dato_simulado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alerta.get("sesion_id"),
            alerta.get("fecha", datetime.now().strftime("%Y-%m-%d")),
            alerta.get("hora", datetime.now().strftime("%H:%M:%S")),
            alerta.get("camara", "CAM-01-TARAPOTO"),
            alerta.get("track_id"),
            alerta.get("tipo_vehiculo", "motorcycle"),
            alerta.get("clasificacion_casco", "sin_casco"),
            alerta.get("ocupantes_detectados", 1),
            alerta.get("confianza", 0.0),
            alerta.get("cuadros_confirmados", 1),
            alerta.get("ruta_evidencia", ""),
            alerta.get("estado_revision", "Pendiente"),
            alerta.get("es_dato_simulado", 0)
        ))

        alerta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return alerta_id

    def update_alerta_revision(self, alerta_id: int, nuevo_estado: str) -> bool:
        """Permite la revisión humana de una alerta ('Pendiente' -> 'Confirmada' / 'Descartada')."""
        if nuevo_estado not in ("Pendiente", "Confirmada", "Descartada"):
            raise ValueError(f"Estado de revisión no válido: {nuevo_estado}")

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alertas_infraccion SET estado_revision = ? WHERE alerta_id = ?
        """, (nuevo_estado, alerta_id))
        modified = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return modified

    def get_kpis(self, sesion_id: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene métricas agregadas globales o por sesión."""
        conn = self.get_connection()
        cursor = conn.cursor()

        filtro = "WHERE sesion_id = ?" if sesion_id is not None else ""
        params = (sesion_id,) if sesion_id is not None else ()

        # Total vehículos y motos
        cursor.execute(f"SELECT COUNT(*) FROM conteos_vehiculares {filtro}", params)
        total_vehiculos = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM conteos_vehiculares {filtro} {'AND' if filtro else 'WHERE'} tipo_vehiculo = 'motorcycle'", params)
        total_motos = cursor.fetchone()[0]

        # Total alertas sin casco y con casco
        cursor.execute(f"SELECT COUNT(*) FROM alertas_infraccion {filtro} {'AND' if filtro else 'WHERE'} clasificacion_casco = 'sin_casco'", params)
        total_sin_casco = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM alertas_infraccion {filtro} {'AND' if filtro else 'WHERE'} clasificacion_casco = 'con_casco'", params)
        total_con_casco = cursor.fetchone()[0]

        conn.close()

        total_motos_evaluadas = total_sin_casco + total_con_casco
        cumplimiento_pct = (float(total_con_casco) / total_motos_evaluadas * 100.0) if total_motos_evaluadas > 0 else 0.0

        return {
            "total_vehiculos": total_vehiculos,
            "total_motos": total_motos,
            "total_sin_casco": total_sin_casco,
            "total_con_casco": total_con_casco,
            "motos_evaluadas": total_motos_evaluadas,
            "cumplimiento_pct": round(cumplimiento_pct, 1)
        }

    def get_hourly_counts(self, sesion_id: Optional[int] = None) -> pd.DataFrame:
        """Devuelve un DataFrame de conteos agrupados por franja horaria y tipo de vehículo."""
        conn = self.get_connection()
        query = """
            SELECT hora_franja, tipo_vehiculo, COUNT(*) as cantidad
            FROM conteos_vehiculares
        """
        if sesion_id is not None:
            query += f" WHERE sesion_id = {sesion_id}"
        query += " GROUP BY hora_franja, tipo_vehiculo ORDER BY hora_franja ASC"

        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_alertas(
        self,
        limit: int = 50,
        estado: Optional[str] = None,
        incluir_simulados: bool = True
    ) -> List[Dict[str, Any]]:
        """Recupera la lista de alertas recientes con filtros."""
        conn = self.get_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        if estado and estado != "Todos":
            conditions.append("estado_revision = ?")
            params.append(estado)

        if not incluir_simulados:
            conditions.append("es_dato_simulado = 0")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"""
            SELECT * FROM alertas_infraccion
            {where_clause}
            ORDER BY alerta_id DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        conn.close()
        return result

    def export_csv(self, tabla: str, output_path: str | Path) -> bool:
        """Exporta una tabla de la base de datos a formato CSV (RF-09)."""
        if tabla not in ("conteos_vehiculares", "alertas_infraccion", "sesiones_monitoreo"):
            raise ValueError(f"Tabla no autorizada para exportación: {tabla}")

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        conn = self.get_connection()
        df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
        conn.close()

        df.to_csv(str(path), index=False, encoding="utf-8")
        return path.is_file()
