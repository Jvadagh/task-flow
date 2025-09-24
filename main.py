import subprocess

if __name__ == "__main__":
    subprocess.run(["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"])
