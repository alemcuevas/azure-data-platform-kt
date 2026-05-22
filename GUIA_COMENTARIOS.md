# 📝 Guía: Cómo Agregar Comentarios a los Notebooks

Esta guía muestra cómo agregar documentación inline directamente en los notebooks de Databricks.

---

## 📋 Tabla de Contenidos

1. [Estructura General](#estructura-general)
2. [Comentarios en Código Python](#comentarios-en-código-python)
3. [Celdas de Markdown](#celdas-de-markdown)
4. [Docstrings de Funciones](#docstrings-de-funciones)
5. [Ejemplos Completos](#ejemplos-completos)

---

## 📐 Estructura General

### Patrón Recomendado para Cada Celda de Código

```python
# =============================================================================
# TÍTULO DE LA SECCIÓN
# =============================================================================
# Descripción breve de lo que hace esta sección (2-3 líneas)
# Incluye el propósito y contexto necesario

# Paso 1: Descripción del primer paso
variable1 = algo()  # Comentario inline: qué hace esta línea específica

# Paso 2: Descripción del segundo paso
# Si la operación es compleja, explica ANTES de la línea de código
variable2 = operacion_compleja(  
    parametro1="valor",     # Qué representa este parámetro
    parametro2=123          # Por qué este valor específico
)

# Nota importante o advertencia
# ⚠️ PRECAUCIÓN: Explica cualquier gotcha o limitación

# Resultado esperado
print(f"✅ Acción completada: {variable2}")
```

---

## 🐍 Comentarios en Código Python

### 1. Comentarios de Cabecera de Sección

Usa separadores visuales para organizar el código:

```python
# =============================================================================
# IMPORTACIONES
# =============================================================================
# Importar funciones esenciales de PySpark para transformaciones de datos
from pyspark.sql.functions import col, upper, when, current_timestamp
from pyspark.sql.types import *

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
# Definir parámetros globales del notebook
BATCH_SIZE = 1000
OUTPUT_PATH = "/tmp/lab01/output"
```

**Ventajas:**
- Separa visualmente secciones
- Fácil de encontrar con Ctrl+F
- Mejora navegación en notebooks largos

---

### 2. Comentarios Inline (Misma Línea)

```python
# ✅ BUENO: Comenta la intención, no lo obvio
df.withColumn("age_category",           # Categorizar edad para análisis demográfico
              when(col("age") < 18, "menor")
              .when(col("age") < 65, "adulto")
              .otherwise("senior"))

# ❌ MALO: No comentes lo obvio
x = 5  # Asignar 5 a x

# ✅ BUENO: Comenta el POR QUÉ
x = 5  # Máximo de reintentos antes de fallar
```

**Regla de oro:** Los comentarios deben explicar el **POR QUÉ**, no el **QUÉ** (el código ya muestra el qué).

---

### 3. Comentarios Multi-línea para Explicaciones Complejas

```python
# =============================================================================
# DEDUPLICACIÓN CON WINDOW FUNCTIONS
# =============================================================================
# Problema: Tenemos registros duplicados con diferentes timestamps
# Solución: Usar window function para mantener solo el más reciente
# 
# Estrategia:
#   1. Particionar por transaction_id (agrupa duplicados)
#   2. Ordenar por _ingested_at DESC (más reciente primero)
#   3. Usar row_number() para numerar dentro de cada grupo
#   4. Filtrar solo row_num = 1 (el más reciente)
#
# Alternativa considerada: dropDuplicates() - Descartada porque no permite
# control sobre cuál duplicado mantener

from pyspark.sql.window import Window

window_spec = Window.partitionBy("transaction_id").orderBy(col("_ingested_at").desc())

df_dedup = df_bronze \
    .withColumn("row_num", row_number().over(window_spec)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")
```

---

### 4. Comentarios de Advertencia

```python
# ⚠️ PRECAUCIÓN: collect() trae TODOS los datos al driver
# Solo usar con datasets pequeños (< 1MB)
# Para datasets grandes, usar .take(n) o .limit(n)
results = df.collect()

# 💡 TIP: Para mejor performance, cachear DataFrames reutilizados
df_large.cache()  # Materializar en memoria
df_large.count()  # Disparar acción para cachear

# 🔒 SEGURIDAD: Nunca hardcodear credenciales
# ❌ password = "mypass123"  
# ✅ password = dbutils.secrets.get(scope="vault", key="db-password")
```

**Emojis útiles:**
- ⚠️ Advertencia/Precaución
- 💡 Tip/Sugerencia
- 🔒 Seguridad
- ❌ Mal ejemplo
- ✅ Buen ejemplo
- 📊 Resultado/Métrica
- 🔧 Configuración

---

### 5. TODOs y FIXMEs

```python
# TODO: Implementar retry logic para failures transitorios
# FIXME: Este filtro excluye nulls inadvertidamente - corregir en próxima versión
# HACK: Workaround temporal hasta que se arregle el bug en Spark 3.5
# NOTE: Este código asume que 'date' siempre está presente
```

---

## 📝 Celdas de Markdown

### 1. Título de Sección

```markdown
# Lab 01 - Configuración Inicial y Workspace

**Objetivos:**
- Familiarizarse con notebooks de Databricks
- Crear DataFrames básicos
- Ejecutar transformaciones simples
- Trabajar con diferentes lenguajes

**Duración estimada:** 30 minutos

**Prerequisitos:**
- Cluster activo
- Acceso a DBFS
```

---

### 2. Subsecciones con Contexto

```markdown
## Parte 1: Crear DataFrame Simple

En esta sección aprenderás a:
1. Crear un DataFrame desde una lista de tuplas
2. Especificar nombres de columnas explícitamente
3. Visualizar el DataFrame con `display()`

**Concepto clave:** Los DataFrames son inmutables - cada transformación crea un nuevo DataFrame.

**Patrón común:** Crear datos sintéticos para testing sin depender de fuentes externas.
```

---

### 3. Explicaciones con Ejemplos

```markdown
## Transformaciones vs Acciones

### Transformaciones (Lazy - No ejecutan)
- `select()`, `filter()`, `withColumn()`
- Se definen pero no se ejecutan
- Spark construye un plan de ejecución (DAG)

```python
# Esto NO ejecuta nada todavía
df_filtered = df.filter(col("age") > 18)
df_result = df_filtered.select("name", "age")
```

### Acciones (Eager - Ejecutan inmediatamente)
- `count()`, `collect()`, `show()`, `write()`
- Disparan la ejecución del plan completo

```python
# ESTO dispara la ejecución
count = df_result.count()  # ← Aquí se ejecuta TODO
```

**Ventaja de Lazy Evaluation:**
Spark puede optimizar el plan completo antes de ejecutar (ej: pushdown de filtros).
```

---

### 4. Diagramas y Tablas

```markdown
## Arquitectura Medallion

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BRONZE    │───▶│   SILVER    │───▶│    GOLD     │
│   (Raw)     │    │  (Cleaned)  │    │  (Curated)  │
└─────────────┘    └─────────────┘    └─────────────┘
     ↓                    ↓                    ↓
  As-is          Deduplicated         Aggregated
  + Metadata     + Validated          + Optimized
```

### Comparación de Capas

| Capa | Propósito | Formato | Ejemplo |
|------|-----------|---------|---------|
| Bronze | Preservar datos originales | Delta/Parquet | Logs raw, eventos |
| Silver | Datos limpios y confiables | Delta | Transacciones validadas |
| Gold | Optimizados para consumo | Delta | Métricas diarias, features ML |
```

---

### 5. Alertas y Callouts

```markdown
> ⚠️ **IMPORTANTE:** Nunca ejecutes `.collect()` en DataFrames grandes (>1GB). 
> Puede causar OutOfMemoryError en el driver.

> 💡 **TIP:** Para ver el plan de ejecución antes de ejecutar, usa `.explain()` o `.explain(mode="formatted")`.

> 🔒 **SEGURIDAD:** Usa Azure Key Vault para credenciales. 
> Accede con `dbutils.secrets.get(scope, key)`.

> 📚 **REFERENCIA:** 
> - [PySpark API Docs](https://spark.apache.org/docs/latest/api/python/)
> - [Delta Lake Guide](https://docs.delta.io/)
```

---

## 📜 Docstrings de Funciones

### Formato Google Style (Recomendado)

```python
def calcular_costo_cluster(vm_type, num_workers, horas_mes, tipo_cluster="all_purpose", usar_spot=False):
    """
    Calcula el costo mensual de un cluster de Databricks.
    
    Esta función considera tanto el costo de las VMs de Azure como los DBUs
    (Databricks Units) para proporcionar una estimación completa del costo.
    
    Args:
        vm_type (str): Tipo de VM Azure (ej: "Standard_DS3_v2", "Standard_E4s_v3")
        num_workers (int): Número de workers en el cluster (mínimo 1)
        horas_mes (int): Horas de ejecución estimadas por mes (0-744)
        tipo_cluster (str, optional): Tipo de cluster. Opciones:
            - "all_purpose": Clusters interactivos ($0.55/DBU)
            - "jobs": Clusters automatizados ($0.22/DBU)
            Defaults to "all_purpose".
        usar_spot (bool, optional): Si True, aplica descuento de Spot VMs (~40%).
            Nota: Spot VMs pueden ser interrumpidas sin previo aviso.
            Defaults to False.
    
    Returns:
        dict: Diccionario con desglose de costos:
            {
                "vm_type": str,
                "workers": int,
                "cores_total": int,
                "ram_total_gb": int,
                "dbus_hora": float,
                "costo_vm_hora": float,
                "costo_dbu_hora": float,
                "costo_total_hora": float,
                "horas_mes": int,
                "costo_mensual": float,
                "costo_anual": float,
                "tipo_cluster": str,
                "usa_spot": bool
            }
    
    Raises:
        ValueError: Si num_workers < 1 o horas_mes < 0 o horas_mes > 744
        KeyError: Si vm_type no existe en el catálogo de VMs
    
    Example:
        >>> # Calcular costo de un cluster de Jobs con Spot VMs
        >>> resultado = calcular_costo_cluster(
        ...     vm_type="Standard_DS3_v2",
        ...     num_workers=3,
        ...     horas_mes=160,
        ...     tipo_cluster="jobs",
        ...     usar_spot=True
        ... )
        >>> print(f"Costo mensual: ${resultado['costo_mensual']:.2f}")
        Costo mensual: $372.80
        
        >>> # Comparar All-Purpose vs Jobs
        >>> costo_dev = calcular_costo_cluster("Standard_DS3_v2", 2, 160, "all_purpose")
        >>> costo_prod = calcular_costo_cluster("Standard_DS3_v2", 2, 160, "jobs")
        >>> ahorro = costo_dev['costo_mensual'] - costo_prod['costo_mensual']
        >>> print(f"Ahorro usando Jobs cluster: ${ahorro:.2f}/mes")
    
    Note:
        - Precios basados en región East US (Enero 2026)
        - DBUs calculados con fórmula: cores × 0.75 × num_workers
        - Spot VMs: Descuento promedio de 40% (puede variar)
        - No incluye costos de storage (DBFS, ADLS)
    
    See Also:
        - optimizar_costo_cluster(): Recomendaciones de optimización
        - calcular_ahorro_spot(): Análisis de ahorro con Spot VMs
    
    References:
        - Azure Databricks Pricing: https://azure.microsoft.com/pricing/details/databricks/
        - VM Pricing: https://azure.microsoft.com/pricing/details/virtual-machines/
    """
    # Validaciones
    if num_workers < 1:
        raise ValueError("num_workers debe ser al menos 1")
    if horas_mes < 0 or horas_mes > 744:
        raise ValueError("horas_mes debe estar entre 0 y 744 (31 días × 24 horas)")
    
    # Configuración de precios...
    # (Resto de la implementación)
```

---

### Formato NumPy Style (Alternativa)

```python
def validate_data_quality(df):
    """
    Valida calidad de datos y marca registros inválidos.
    
    Esta función aplica un conjunto de reglas de validación comunes
    y agrega dos columnas al DataFrame: una lista de problemas encontrados
    y un flag booleano indicando si el registro es válido.
    
    Parameters
    ----------
    df : pyspark.sql.DataFrame
        DataFrame a validar. Debe contener las columnas:
        - transaction_id (string, no null)
        - amount (numeric, > 0)
        - quantity (int, > 0)
        - status (string, valores válidos: "completed", "pending", "cancelled")
    
    Returns
    -------
    pyspark.sql.DataFrame
        DataFrame original con dos columnas adicionales:
        - quality_issues : array<string>
            Lista de códigos de problemas detectados. Vacío si es válido.
        - is_valid : boolean
            True si pasa todas las validaciones, False en caso contrario.
    
    Examples
    --------
    >>> # Validar datos de transacciones
    >>> df_validated = validate_data_quality(df_transactions)
    >>> 
    >>> # Separar válidos e inválidos
    >>> df_valid = df_validated.filter(col("is_valid"))
    >>> df_errors = df_validated.filter(~col("is_valid"))
    >>> 
    >>> # Ver tipos de errores
    >>> df_errors.groupBy("quality_issues").count().show()
    
    Notes
    -----
    - Registros inválidos deben guardarse en tabla de errores para investigación
    - Los códigos de error son:
        * missing_transaction_id
        * invalid_amount
        * invalid_quantity
        * invalid_status
    - La función NO elimina registros, solo los marca
    
    See Also
    --------
    clean_data : Limpia y estandariza datos después de validación
    write_error_log : Guarda registros inválidos en tabla de errores
    """
    # Implementación...
```

---

## 💼 Ejemplos Completos

### Ejemplo 1: Celda Completa con Documentación Inline

```python
# =============================================================================
# GENERACIÓN DE DATOS SINTÉTICOS PARA TESTING
# =============================================================================
# Propósito: Crear dataset de prueba sin depender de fuentes externas
# Beneficios:
#   - Reproducible: Mismos datos en cada ejecución
#   - Rápido: No requiere I/O de red/disco
#   - Aislado: No afecta ni depende de sistemas productivos

from pyspark.sql.functions import *
from datetime import datetime, timedelta
import random

def generate_sales_data(num_records=1000, batch_id="BATCH_001"):
    """
    Genera datos sintéticos de ventas con distribución realista.
    
    Args:
        num_records (int): Cantidad de registros a generar
        batch_id (str): Identificador del lote para tracking
    
    Returns:
        DataFrame: Datos con metadata de ingesta (columnas con prefijo _)
    
    Example:
        >>> df = generate_sales_data(500, "TEST_001")
        >>> df.printSchema()
        >>> df.groupBy("region").count().show()
    """
    # Configurar listas de valores posibles
    dates = [(datetime.now() - timedelta(days=x)) for x in range(30)]  # Últimos 30 días
    products = ["LAPTOP", "MOUSE", "KEYBOARD", "MONITOR", "WEBCAM"]
    regions = ["NORTH", "SOUTH", "EAST", "WEST"]
    
    # Generar registros usando list comprehension (eficiente en Python)
    data = []
    for i in range(num_records):
        data.append({
            "transaction_id": f"TXN{i:06d}",  # Zero-padding: TXN000001, TXN000002...
            "date": dates[random.randint(0, len(dates)-1)].strftime("%Y-%m-%d"),
            "product_code": f"P{random.randint(100, 999)}",  # P100 a P999
            "product_name": random.choice(products),
            "region": random.choice(regions),
            "amount": round(random.uniform(50, 1000), 2),  # $50 a $1000
            "quantity": random.randint(1, 10),
            "customer_id": f"CUST{random.randint(1000, 9999)}",
            "status": random.choice(["completed", "pending", "cancelled"])
        })
    
    # Crear DataFrame desde lista de diccionarios
    # Spark infiere el schema automáticamente
    df = spark.createDataFrame(data)
    
    # Agregar metadata de ingesta (patrón Bronze en Medallion Architecture)
    # Prefijo '_': Indica columnas técnicas vs. datos de negocio
    df_bronze = df \
        .withColumn("_ingested_at", current_timestamp()) \    # Cuándo se ingirió
        .withColumn("_source", lit("sales_system")) \          # De dónde vino
        .withColumn("_batch_id", lit(batch_id))               # Qué lote es
    
    return df_bronze

# Generar primer lote de datos
# Nota: Usar 500 registros para lab (rápido). En producción podrían ser millones.
df_batch1 = generate_sales_data(500, "BATCH_001")

# Verificar resultado
print(f"✅ Batch 1 generado: {df_batch1.count()} registros")
print(f"📊 Columnas: {', '.join(df_batch1.columns)}")

# Mostrar muestra para validación visual
display(df_batch1.limit(10))
```

---

### Ejemplo 2: Documentación de Operación Delta

```python
# =============================================================================
# DELTA LAKE: MERGE (UPSERT)
# =============================================================================
# Caso de uso: Actualizar registros existentes e insertar nuevos en una sola operación
# 
# Contexto: Recibimos datos incrementales que pueden contener:
#   - Registros nuevos (deben insertarse)
#   - Actualizaciones a registros existentes (deben actualizarse)
# 
# Solución: MERGE implementa lógica UPSERT de forma atómica y eficiente
#
# Alternativas consideradas:
#   ❌ Overwrite completo: Perdemos datos históricos
#   ❌ Append + dedup posterior: Ineficiente, requiere reescribir toda la tabla
#   ✅ MERGE: Operación atómica, solo modifica registros afectados

from delta.tables import DeltaTable

# =============================================================================
# PASO 1: PREPARAR DATOS NUEVOS/ACTUALIZADOS
# =============================================================================
# Simular datos incrementales (en producción vendrían de API/streaming)
df_updates = generate_sales_data(50, "BATCH_003").select(
    "transaction_id",  # Clave de join
    "date", "product_code", "product_name", "region",
    "amount", "quantity", "customer_id", "status"
)

print(f"📦 Datos a mergear: {df_updates.count()} registros")

# =============================================================================
# PASO 2: CARGAR TABLA DELTA DESTINO
# =============================================================================
# DeltaTable.forPath(): Crea referencia a tabla Delta existente
# No carga datos en memoria, solo metadata
delta_table = DeltaTable.forPath(spark, silver_path)

print(f"🎯 Tabla destino: {silver_path}")

# =============================================================================
# PASO 3: EJECUTAR MERGE
# =============================================================================
# Sintaxis: target.merge(source, condition).when*().execute()

merge_result = delta_table.alias("target").merge(
    df_updates.alias("source"),
    "target.transaction_id = source.transaction_id"  # ← Condición de match
).whenMatchedUpdateAll() \  # Si hay match: actualizar TODAS las columnas
 .whenNotMatchedInsertAll() \  # Si NO hay match: insertar TODAS las columnas
 .execute()

# Alternativas más granulares:
# .whenMatchedUpdate(set={"amount": "source.amount", "updated_at": "current_timestamp()"})
# .whenMatchedDelete(condition="source.status = 'deleted'")
# .whenNotMatchedInsert(values={"transaction_id": "source.transaction_id", ...})

print("✅ MERGE completado")

# =============================================================================
# PASO 4: VERIFICAR RESULTADO
# =============================================================================
# Leer tabla actualizada
df_after = spark.read.format("delta").load(silver_path)
print(f"📊 Total registros post-merge: {df_after.count()}")

# Ver métricas del merge en el historial
history = spark.sql(f"DESCRIBE HISTORY delta.`{silver_path}` LIMIT 1")
display(history.select("version", "operation", "operationMetrics"))

# operationMetrics incluye:
#   - numTargetRowsInserted: Nuevos registros
#   - numTargetRowsUpdated: Registros actualizados
#   - numTargetRowsDeleted: Registros eliminados
#   - numOutputRows: Total de filas afectadas
```

---

### Ejemplo 3: Documentación de Streaming

```python
# =============================================================================
# STRUCTURED STREAMING CON AUTO LOADER
# =============================================================================
# Objetivo: Procesar archivos nuevos automáticamente al llegar al directorio
#
# Auto Loader (cloudFiles) proporciona:
#   ✅ Detección automática de archivos nuevos
#   ✅ Schema evolution (detecta cambios en estructura)
#   ✅ Exactly-once semantics (con checkpointing)
#   ✅ Escalabilidad (miles de archivos sin degradación)
#
# Casos de uso:
#   - Ingesta continua desde storage (ADLS, S3)
#   - Procesamiento de logs en tiempo real
#   - ETL incremental

# =============================================================================
# CONFIGURACIÓN DE RUTAS
# =============================================================================
streaming_input = "/tmp/lab06/streaming/input"           # ← Archivos nuevos llegan aquí
streaming_checkpoint = "/tmp/lab06/streaming/checkpoint" # ← Estado del stream
streaming_output = "/tmp/lab06/streaming/output"         # ← Resultados procesados

# Checkpoint: Almacena offsets de archivos procesados
# Permite recovery: Si el stream falla, continúa desde el último checkpoint
# ⚠️ IMPORTANTE: No cambiar checkpoint location sin razón
#    Cambiarlo causará reprocesamiento de TODOS los archivos

# =============================================================================
# PASO 1: CONFIGURAR STREAM DE LECTURA
# =============================================================================
df_stream = spark.readStream \
    .format("cloudFiles") \                              # ← Auto Loader
    .option("cloudFiles.format", "json") \               # Formato de archivos entrantes
    .option("cloudFiles.schemaLocation", streaming_checkpoint) \  # Dónde guardar schema inferido
    .option("cloudFiles.schemaEvolution", "addNewColumns") \  # Cómo manejar nuevas columnas
    .load(streaming_input)

# Opciones adicionales útiles:
# .option("cloudFiles.useNotifications", "true")  # Usar eventos de storage (más eficiente)
# .option("cloudFiles.maxFilesPerTrigger", 1000)  # Limitar archivos por micro-batch
# .option("cloudFiles.validateOptions", "true")   # Validar opciones al inicio

print("✅ Stream de lectura configurado")
print(f"   Input: {streaming_input}")
print(f"   Checkpoint: {streaming_checkpoint}")

# =============================================================================
# PASO 2: TRANSFORMACIONES (OPCIONAL)
# =============================================================================
# Las transformaciones en streaming son IGUALES a batch
# Spark las aplica a cada micro-batch automáticamente

df_stream_processed = df_stream \
    .withColumn("processed_at", current_timestamp()) \  # Timestamp de procesamiento
    .withColumn("value_category",                      # Categorización
                when(col("value") < 250, "Low")
                .when(col("value") < 750, "Medium")
                .otherwise("High"))

# 💡 TIP: Evita operaciones costosas (joins complejos, shuffles grandes)
# En streaming, cada micro-batch repite la operación

# =============================================================================
# PASO 3: CONFIGURAR STREAM DE ESCRITURA
# =============================================================================
query = df_stream_processed.writeStream \
    .format("delta") \                                  # Escribir a Delta Lake
    .option("checkpointLocation", streaming_checkpoint) \  # ← CRÍTICO: Habilita exactly-once
    .outputMode("append") \                             # Mode: append, update, complete
    .trigger(processingTime="5 seconds") \              # Micro-batch cada 5 segundos
    .start(streaming_output)

# Output Modes:
#   - append: Solo nuevas filas (default, más común)
#   - complete: Toda la tabla agregada (requiere agregaciones)
#   - update: Solo filas actualizadas (para agregaciones streaming)

print("🔄 Stream iniciado")
print(f"   Query ID: {query.id}")
print(f"   Status: {query.status}")
print(f"   Output: {streaming_output}")

# =============================================================================
# PASO 4: MONITORING
# =============================================================================
# Ver progreso reciente (últimos micro-batches)
for progress in query.recentProgress:
    print(f"📊 Batch: {progress['batchId']}")
    print(f"   Registros procesados: {progress['numInputRows']}")
    print(f"   Duración: {progress['durationMs']['batchDuration']}ms")

# Status actual
print(f"\n📍 Status: {query.status}")
print(f"   Activo: {query.isActive}")

# =============================================================================
# PASO 5: DETENER STREAM
# =============================================================================
# En notebooks, el stream corre indefinidamente
# Para detenerlo (después de testing):

# query.stop()  # Detiene el stream
# print("⏹️  Stream detenido")

# Para esperar a que termine (bloqueante):
# query.awaitTermination()  # Espera indefinidamente
# query.awaitTermination(timeout=60)  # Espera máximo 60 segundos
```

---

## 🎯 Resumen de Mejores Prácticas

### ✅ DO (Hacer)

1. **Explica el POR QUÉ, no solo el QUÉ**
   ```python
   # ✅ BUENO
   df.repartition(8)  # Incrementar paralelismo para usar todos los cores del cluster
   
   # ❌ MALO
   df.repartition(8)  # Reparticionar a 8
   ```

2. **Usa separadores visuales para secciones**
   ```python
   # =============================================================================
   # TÍTULO DE LA SECCIÓN
   # =============================================================================
   ```

3. **Documenta funciones con docstrings completos**
   - Descripción, Args, Returns, Examples, Notes

4. **Agrega warnings para gotchas comunes**
   ```python
   # ⚠️ PRECAUCIÓN: collect() trae todos los datos al driver
   ```

5. **Incluye ejemplos de uso**
   ```python
   # Ejemplo:
   #   df_result = mi_funcion(df, "columna")
   #   df_result.count()  # → 1000
   ```

---

### ❌ DON'T (No Hacer)

1. **No comentes lo obvio**
   ```python
   # ❌ MALO
   x = x + 1  # Incrementar x en 1
   ```

2. **No uses comentarios para código "comentado"**
   ```python
   # ❌ MALO: Usar Git para historial, no comentarios
   # df = df.filter(col("age") > 18)  # Antigua implementación
   # df = df.select("name", "age")    # Ya no lo usamos
   ```

3. **No escribas comentarios ambiguos**
   ```python
   # ❌ MALO
   df.cache()  # Optimización de performance
   
   # ✅ BUENO
   df.cache()  # Cachear porque se usa en 3 agregaciones siguientes
   ```

4. **No uses jerga sin explicar**
   ```python
   # ❌ MALO
   df.repartition(200)  # Mitigar skew
   
   # ✅ BUENO
   df.repartition(200)  # Mitigar skew (particiones desbalanceadas) redistribuyendo datos uniformemente
   ```

---

## 🚀 Cómo Aplicar a los Notebooks Existentes

### Opción 1: Editar Directamente en Databricks

1. Abre el notebook en Databricks Workspace
2. Para cada celda de código:
   - Agrega comentarios de cabecera con `# =====`
   - Inserta comentarios inline explicando lógica compleja
   - Documenta funciones con docstrings
3. Agrega celdas de Markdown antes de cada sección

### Opción 2: Descargar, Editar, Re-subir

1. Descarga el notebook (.ipynb) desde Databricks
2. Abre en VS Code o Jupyter
3. Edita agregando comentarios
4. Re-sube a Databricks

### Opción 3: Crear Versión Documentada Paralela

1. Crea copia del notebook: `lab-01-workspace-documented.ipynb`
2. Agrega toda la documentación inline
3. Mantén ambas versiones:
   - Original: Código limpio para ejecución
   - Documented: Con comentarios extensivos para aprendizaje

---

## 📚 Referencias

- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)

---

**Última actualización:** Mayo 2026
