from cx_Freeze import setup, Executable

# Lista de scripts que você deseja incluir no executável
scripts = ["gvg.py"]

# Lista de módulos que você deseja incluir
includes = ["pyautogui", "time", "cv2", "logging", "keyboard"]

# Lista de imagens que você deseja incluir
include_files = [("img", "img"), ("log", "log")]

# Configurações para o executável
options = {
    "build_exe": {
        "includes": includes,
        "include_files": include_files,
    }
}

setup(
    name="gvg",
    version="1.0",
    description="bot - gvg",
    executables=[Executable(script) for script in scripts],
    options=options,
)