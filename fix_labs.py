import json
import re

# Define los nuevos textos para cada lab
new_endings = {
    "lab-02-clusters.ipynb": """## Resumen del Laboratorio

### Competencias Adquiridas:

**Gestión de Recursos:**
- Evaluación de autoscaling con cargas de trabajo variables
- Análisis de métricas de performance en Spark UI

**Optimización de Costos:**
- Cálculo de costos de VMs Azure y DBUs de Databricks
- Comparación de escenarios: All-Purpose vs Jobs clusters
- Estrategias de ahorro con Spot instances

**Mejores Prácticas:**
- Dimensionamiento apropiado de clusters según workload
- Trade-offs entre performance y costo
- Configuración de auto-termination y autoscaling

### Próximos Pasos:
- **Lab 03**: Notebooks avanzados con widgets y magic commands
- **Lab 04**: Arquitectura de datos Medallion
- **Lab 05**: Orquestación de workflows multi-task""",

    "lab-03-notebooks.ipynb": """## Resumen del Laboratorio

### Competencias Adquiridas:

**Magic Commands:**
- Uso de %md, %%sql, %sh, %fs para operaciones especializadas
- Integración de múltiples lenguajes en un mismo notebook

**Parametrización:**
- Implementación de widgets (text, dropdown, combobox, multiselect)
- Diseño de notebooks reutilizables con parámetros dinámicos

**Debugging y Optimización:**
- Decorators para medición de tiempo de ejecución
- Análisis de planes de ejecución con explain()
- Detección de valores nulos y validación de calidad de datos

**Persistencia:**
- Escritura de DataFrames particionados en formato Delta

### Próximos Pasos:
- **Lab 04**: Arquitectura Medallion completa (Bronze/Silver/Gold)
- **Lab 05**: Workflows de producción con error handling
- **Lab 06**: Integración de múltiples fuentes de datos""",

    "lab-04-transformacion.ipynb": """## Resumen del Laboratorio

### Competencias Adquiridas:

**Arquitectura Medallion:**
- **Bronze**: Ingesta raw con metadata de auditoría (_ingested_at, _source, _batch_id)
- **Silver**: Deduplicación con Window functions, limpieza y validación de calidad
- **Gold**: Agregaciones de negocio para analytics y reporting

**Data Quality:**
- Implementación de validaciones de integridad de datos
- Segregación de registros válidos e inválidos
- Tracking de issues de calidad por registro

**Delta Lake Operations:**
- MERGE (upserts), OPTIMIZE (compactación), Z-ORDER (indexación)
- Time Travel para consultas de versiones históricas
- DESCRIBE HISTORY para auditoría de cambios

**Window Functions:**
- Deduplicación basada en particiones y ordenamiento
- row_number() para identificación de registros únicos

### Próximos Pasos:
- **Lab 05**: Orquestación de workflows multi-notebook
- **Lab 06**: Integración de fuentes de datos heterogéneas""",

    "lab-05-jobs.ipynb": """## Resumen del Laboratorio

### Competencias Adquiridas:

**Parametrización de Notebooks:**
- Uso de dbutils.widgets para recibir parámetros de runtime
- Diseño de notebooks reutilizables para diferentes ambientes (dev/staging/prod)

**Error Handling:**
- Implementación de try-catch con logging detallado
- Retorno de resultados estructurados (JSON) con dbutils.notebook.exit()
- Estrategias de recuperación ante fallos

**Workflows Multi-Task:**
- Orquestación de pipelines con dependencias entre tareas
- Propagación de outputs entre notebooks (Task 1 → Task 2 → Task 3)
- Simulación de workflows de producción (Ingest → Transform → Aggregate)

**Mejores Prácticas:**
- Paths dinámicos por ambiente y fecha para facilitar testing y recovery
- Métricas y timestamps para observabilidad
- Estados de ejecución (SUCCESS/FAILED) para monitoreo

### Próximos Pasos:
- **Lab 06**: Integración y streaming de datos
- Implementación real de Databricks Workflows en la UI
- Configuración de schedules y alertas""",

    "lab-06-integracion.ipynb": """## Resumen del Laboratorio

### Competencias Adquiridas:

**Integración Multi-Formato:**
- Lectura y escritura de CSV, JSON y Parquet
- Configuración de opciones específicas por formato (header, delimiter, schema inference)
- Comparación de performance y casos de uso por formato

**Transformaciones de Datos:**
- JOINs complejos (left, inner) para enriquecimiento de datos
- Integración de datos transaccionales con dimensiones de referencia
- Cálculos derivados (total_amount = quantity × price)

**Optimización:**
- Particionamiento de datos por columnas clave (region, date)
- Estrategias de escritura eficiente para grandes volúmenes

**Streaming (Auto Loader):**
- Configuración de streaming ingestion con checkpoints
- Procesamiento incremental de datos
- Manejo de schema evolution

### Próximos Pasos:
- Implementar integración con Azure Storage Account (ADLS Gen2)
- Configurar Unity Catalog para governance de datos
- Explorar Apache Kafka para streaming en tiempo real
- Implementar pipelines de CI/CD con Databricks Repos"""
}

# Procesar cada notebook
for filename, new_text in new_endings.items():
    filepath = f"notebooks/{filename}"
    print(f"Procesando {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Buscar la última celda markdown que contiene "Lab Completado"
    for i in range(len(nb['cells']) - 1, -1, -1):
        cell = nb['cells'][i]
        if cell['cell_type'] == 'markdown':
            source_text = ''.join(cell['source'])
            if 'Lab Completado' in source_text or 'Has aprendido' in source_text or 'Has implementado' in source_text:
                # Reemplazar con el nuevo texto
                nb['cells'][i]['source'] = [line + '\n' for line in new_text.split('\n')]
                print(f"  ✓ Celda actualizada en {filename}")
                break
    
    # Guardar el notebook actualizado
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

print("\n✅ Todos los notebooks actualizados")
