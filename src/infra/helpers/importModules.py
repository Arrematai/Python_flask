import importlib

"""
Importa dinamicamente um módulo e retorna a classe especificada.
"""
def dynamic_import(module_path, class_name):
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Erro ao importar modulo: {module_path}.{class_name}: {e}")
        return None
