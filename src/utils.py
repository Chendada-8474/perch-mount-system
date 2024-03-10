import pathlib


def getPathExtension(path: str):
    return pathlib.Path(path).suffix
