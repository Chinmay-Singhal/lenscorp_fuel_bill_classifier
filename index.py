import subprocess

try:
  subprocess.run(["fastapi", "run"])
except Exception as e:
  print(f"Error: {e}")
  subprocess.run(["fastapi", "run"])
