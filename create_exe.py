import os
import subprocess

venv_python = os.path.join(".venv", "Scripts", "python")
name_of_py = "main"
name_of_exe = "BookCreator"
upx_dir = r"D:\upx-4.2.4"

command = [
    venv_python,
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    f"--name={name_of_exe}",
    "--clean",
    "--noconsole",
    "--optimize=0",
    f"--distpath=output",
    f"--workpath={name_of_py}.build",
    f"--specpath={name_of_py}.build",
    f"{name_of_py}.py"
]

if os.path.isdir(upx_dir):
    command.append(f"--upx-dir={upx_dir}")
else:
    print(f"UPX не найден: {upx_dir}. Собираем exe без сжатия.")

try:
    subprocess.run(command, check=True)
    print("EXE создано!")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при билде: {e}")
