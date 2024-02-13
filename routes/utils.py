import enum

class RouteVarTypes(enum.StrEnum):
    INT = "int"
    STRING = "string"
    FLOAT = "float"
    PATH = "path"
    UUID = "uuid"

def route_var(var_type: str, var: str) -> str:
    return f"<{var_type}:{var}>"