# Sistema de Monitorización IoT: InfluxDB + Grafana + Python

Este proyecto implementa una arquitectura completa de **Series Temporales** para la ingesta, procesamiento (Downsampling) y visualización de métricas de sensores en tiempo real.

## 📂 Estructura del Proyecto
* `docker-compose.yml`: Define la infraestructura (InfluxDB y Grafana).
* `simulador.py`: Script en Python que actúa como productor de datos.
* `venv/`: Entorno virtual de Python (aislamiento de librerías).
* `README.md`: Guía de uso.

---

## 🛠️ Requisitos Previos
1. **Docker Desktop** instalado.
2. **Python 3.10** o superior.

---

## 🚀 Paso 1: Levantar la Infraestructura (Docker)

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta el siguiente comando para descargar las imágenes y arrancar los servicios en segundo plano:
   ```
   docker-compose up -d
   ```
3. Verifica que los contenedores están corriendo:
   * **InfluxDB:** `http://localhost:8086`
   * **Grafana:** `http://localhost:3000`

---

## 🐍 Paso 2: Configurar el Entorno de Python

Para asegurar que el simulador tenga las librerías necesarias sin afectar a tu sistema global:

1. **Crear el entorno virtual:**
   ```
   python -m venv venv
   ```
2. **Activar el entorno:**
   * En Windows: `.\venv\Scripts\activate`
   * En Linux/Mac: `source venv/bin/activate`
3. **Instalar la librería cliente de InfluxDB:**
   ```
   pip install influxdb-client
   ```

---

## 🛢️ Paso 3: Configuración Inicial de InfluxDB

1. Entra en `http://localhost:8086`.
2. Sigue el asistente inicial:
   * **Username:** `usuario1` (o el que prefieras).
   * **Organization:** `Universidad de Sevilla`.
   * **Bucket Inicial:** `sensores_raw`. (luego se puede editar este bucket. Al editarlo, poner en "older than" la cifra que quieres que esten guardados los datos antes de ser borrados. MIN: 1hora)
   * **Se generará acontinuación un token, muy importante copiarlo. Si no se genera, mas adelante se ve como conseguirlo**
3. **Crear el segundo Bucket:**
   * Ve a **Load Data (en el menú de la izquierda)** > **Buckets**.
   * Crea un nuevo bucket llamado `sensores_resumen` (aquí se guardarán los promedios).
4. **Obtener el Token:**
   * Ve a **Load Data** > **API Tokens**.
   * Haz clic en **Generate API Token** > **All Access Token**.
   * **Cópialo y guárdalo**, lo necesitarás para el script y para Grafana.

---

## 🧠 Paso 4: Configurar la Tarea de Procesamiento (Downsampling)

Para optimizar el almacenamiento, crearemos una tarea que resuma los datos cada 5 minutos:

1. En InfluxDB, ve a **Tasks** > **Create Task**.
2. Rellena los campos: **Name:** `Resumen_5min`, **Every:** `5m`.
3. Pega el siguiente código **Flux**:
   ```flux
   from(bucket: "sensores_raw")
       |> range(start: -5m)
       |> filter(fn: (r) => r._measurement == "lectura_clima")
       |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
       |> to(bucket: "sensores_resumen")
   ```
4. Guarda la tarea. Ahora, InfluxDB calculará promedios automáticamente cada 5 minutos.



---

## 📈 Paso 5: Configuración de Grafana

1. Entra en `http://localhost:3000` (User: `admin` | Pass: `admin`). Pedirá cambiar la contraseña, pero se puede saltar si asi se desea
2. Ve a **Connections** > **Data Sources** > **Add Data Source**.
3. Selecciona **InfluxDB**.
4. **Configuración clave:**
   * **Query Language:** `Flux`.
   * **URL:** `http://influxdb:8086`.
   * **Basic Auth:** Desactivado.
   * **InfluxDB Details:** Pega tu Organización, Token y el Bucket por defecto (`sensores_raw`).
5. Haz clic en **Save & Test**.
6. **Crear Dashboard:**
   * Crea un nuevo Dashboard y añade un panel desde el menú de la derecha.
   * En el panel, **configure visualization**, en rango de tiempo seleccionar **last 5 minutes** y en refresh 5s.
   * Introduce este código Flux en **queries** para ver la temperatura en tiempo real:
     ```flux
     from(bucket: "sensores_raw")
       |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
       |> filter(fn: (r) => r["_measurement"] == "lectura_clima")
       |> filter(fn: (r) => r["_field"] == "temperatura")
     ```
   
   * Crea otro nuevo panel.
   * En el panel, de nuevo, **configure visualization**, en rango de tiempo seleccionar **last 5 minutes** y en refresh 5s.
   * Introduce este código Flux en **queries** para ver el resumen de la temperatura cada 5 minutos:
     ```flux
     from(bucket: "sensores_resumen")
       |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
       |> filter(fn: (r) => r["_measurement"] == "lectura_clima")
     ```



---

## Paso 6: Ejecutar el Simulador

1. Abre `simulador.py` y asegúrate de pegar tu **Token**, **Org** y **Bucket** en las variables correspondientes.
2. Con el entorno virtual activado, ejecuta:
   ```bash
   python simulador.py
   ```
3. Verás mensajes en la consola confirmando el envío de datos. Vuelve a Grafana y verás cómo las gráficas cobran vida.

---

## Solución de Problemas Comunes

* **Error `exec format error` en Docker:** Esto ocurre por un conflicto de arquitectura (Intel vs ARM). Asegúrate de que el archivo `docker-compose.yml` incluya la línea `platform: linux/amd64` en cada servicio.
* **Grafana no conecta a InfluxDB:** Asegúrate de usar la URL `http://influxdb:8086` (nombre del servicio en Docker) y NO `localhost`.
* **No aparecen datos en las gráficas:** Comprueba que el rango de tiempo en Grafana esté configurado en "Last 5 minutes" y que el refresco automático esté en "5s".
---

### Conceptos Técnicos Aplicados
* **TSM (Time-Structured Merge Tree):** Motor de almacenamiento de InfluxDB optimizado para series temporales.
* **Line Protocol:** Formato de ingesta de datos de alta eficiencia.
* **Downsampling:** Estrategia de reducción de resolución de datos para eficiencia de almacenamiento.
* **Contenerización:** Despliegue de microservicios aislados mediante Docker.

