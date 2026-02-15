from typing import List, Dict, Tuple
from .cleaner import LineError, LineOrchestrator, ErrorTypes

config = {
        "use_null": True,
        "use_type": True,
        "use_duplicate": False
    }

orchestrator = LineOrchestrator(config)

fila_sucia: List[str] = ["101", "35", "dato_invalido"]
    
    # Aquí simulamos que el detector ya encontró un NULL en la col 1
errores_detectados: LineError = {1: ErrorTypes.NULL}
# 4. Ejecutar el proceso
fila_final, errores = orchestrator.process(fila_sucia, errores_detectados)

# 5. Ver el resultado
print(f"Entrada: {fila_sucia}")
print(f"Errores reportados: {errores}")
print(f"Salida final: {fila_final}")

if not fila_final:
    print("Estado: La fila fue ELIMINADA por el orquestador.")
else:
    print("Estado: La fila es VÁLIDA.")