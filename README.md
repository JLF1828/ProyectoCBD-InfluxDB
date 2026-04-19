# Monitorización de Datos IoT con InfluxDB y Grafana
### Asignatura: Complemento de Base de Datos

Este proyecto implementa una solución completa para el almacenamiento, procesamiento y visualización de **Series Temporales (Time Series)** utilizando el ecosistema NoSQL de **InfluxDB**.

## 🚀 Arquitectura del Proyecto
El sistema se compone de tres capas principales:
1.  **Ingesta:** Script en Python que simula sensores enviando datos de temperatura y humedad en tiempo real.
2.  **Almacenamiento y Procesamiento:** **InfluxDB** actuando como base de datos de alto rendimiento, realizando *Downsampling* (resumen de datos) mediante tareas programadas en lenguaje **Flux**.
3.  **Visualización:** **Grafana** para la creación de dashboards dinámicos y alertas.



---

## 🛠️ Requisitos Previos
* **Docker Desktop** instalado y funcionando.
* **Python 3.x** instalado en el sistema.
* Librería de InfluxDB para Python: `pip install influxdb-client`.

---

## 📦 Instalación y Despliegue

### 1. Levantar la infraestructura
Desde la terminal, en la carpeta del proyecto, ejecuta:
```bash
docker-compose up -d
```
Esto levantará:
* **InfluxDB:** `http://localhost:8086`
* **Grafana:** `http://localhost:3000`

### 2. Configuración inicial de InfluxDB
1. Accede a `http://localhost:8086` y crea tu usuario.
2. Crea una organización llamada `MiUniversidad`.
3. Crea dos **Buckets**:
   * `sensores_raw`: Para los datos en tiempo real (alta resolución).
   * `sensores_resumen`: Para los promedios calculados (baja resolución).
4. Genera un **API Token** (All Access) y cópialo.

### 3. Configuración de la Tarea (Downsampling)
En el apartado **Tasks** de InfluxDB, crea una nueva tarea con el siguiente script para promediar datos cada 5 minutos:
```flux
from(bucket: "sensores_raw")
    |> range(start: -5m)
    |> filter(fn: (r) => r._measurement == "lectura_clima")
    |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
    |> to(bucket: "sensores_resumen")
```

---

## 🏃 Ejecución del Simulador
1. Abre el archivo `simulador.py`.
2. Sustituye la variable `token` por el token generado en el paso anterior.
3. Ejecuta el script:
```bash
python simulador.py
```
*Deberías empezar a ver en la terminal los mensajes de datos enviados.*

---

## 📊 Visualización en Grafana
1. Accede a `http://localhost:3000` (user: `admin` | pass: `admin`).
2. Añade un **Data Source** de tipo **InfluxDB**:
   * **Query Language:** Flux.
   * **URL:** `http://influxdb:8086`.
   * **Token:** Tu token de InfluxDB.
3. Importa o crea un **Dashboard** utilizando consultas Flux para visualizar la temperatura y humedad en tiempo real.



---

## 🎓 Conceptos Clave Demostrados
* **TSM Engine:** Uso de un motor de almacenamiento optimizado para timestamps.
* **Line Protocol:** Ingesta eficiente de datos sin necesidad de esquemas fijos.
* **Downsampling:** Optimización del almacenamiento reduciendo la resolución de datos históricos.
* **Escalabilidad:** Separación de capas mediante contenedores Docker.

