import importlib
import platform
import sys

print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())
for package in ["pandas", "sqlalchemy", "pyodbc", "dotenv", "pytest"]:
    try:
        importlib.import_module(package)
        print(f"PASS: {package}")
    except Exception as exc:
        print(f"FAIL: {package} — {exc}")
