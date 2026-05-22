import json

# Arreglar Lab 02 - comentarios mezclados
filepath = "notebooks/lab-02-clusters.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Buscar la celda con el error (contiene "rand() * 1000# - Jobs")
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_text = ''.join(cell['source'])
        if 'rand() * 1000# - Jobs' in source_text:
            # Reemplazar con el código correcto
            new_code = '''# =============================================================================
# TEST DE AUTOSCALING - CARGA LIGERA
# =============================================================================
# Objetivo: Verificar que el cluster NO escala para cargas pequeñas
# Con 1 millón de registros, el cluster debería mantener workers mínimos

# Importaciones
from pyspark.sql.functions import rand  # Genera números aleatorios
import time                              # Para medir tiempo de ejecución

print("🔹 Carga Ligera: Procesando 1 millón de registros")
start = time.time()  # Timestamp de inicio

# Crear DataFrame sintético de 1 millón de filas
# spark.range(start, end): Genera DataFrame con columna 'id' (números secuenciales)
df_light = spark.range(0, 1_000_000) \\
    .withColumn(
        "value",                    # Nueva columna con valores aleatorios
        rand() * 1000               # rand(): número random entre 0-1, multiplicado por 1000
    ) \\
    .withColumn(
        "category",                 # Nueva columna con categorías (0-9)
        (rand() * 10).cast("int")  # cast("int"): convierte a entero (trunca decimales)
    )

# 💡 NOTA: spark.range() es muy eficiente porque no carga datos en memoria
# Se usa comúnmente para testing y generación de datos sintéticos

# Realizar agregación simple: contar registros por categoría
# collect(): ACCIÓN que trae TODOS los resultados al driver
# ⚠️ Solo usar collect() con resultados pequeños (aquí son ~10 filas)
result = df_light.groupBy("category").count().collect()

end = time.time()  # Timestamp de fin
print(f"✅ Completado en {end - start:.2f} segundos")
print(f"📊 Resultados: {len(result)} categorías")

# 📈 QUÉ OBSERVAR EN SPARK UI:
# - Cluster → Metrics: Número de workers activos (debería mantenerse en mínimo)
# - Jobs: Tiempo de ejecución y número de tasks
# - No debería activarse autoscaling porque la carga es ligera
'''
            cell['source'] = [line + '\n' for line in new_code.split('\n')]
            print("✓ Celda del Lab 02 corregida")
            break

# Guardar
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("✅ Lab 02 corregido")
