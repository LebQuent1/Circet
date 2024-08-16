import os
import subprocess
import fonction_python.all_csvpython as dl_new_inter
from datetime import datetime

def run_all_csvpython(full_path_tempo):
    try:
        print("Running all_csvpython.main()")
        dl_new_inter.main(full_path_tempo)
    except Exception as e:
        print(f"An error occurred while running all_csvpython: {e}")

def run_scrap_images():
    try:
        script_path = os.path.join("fonction_python", "scrap_images.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_scrap_nom():
    try:
        script_path = os.path.join("fonction_python", "scrap_nom.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_rename():
    try:
        script_path = os.path.join("fonction_python", "rename.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_scriptJsonFormat():
    try:
        script_path = os.path.join("fonction_python", "scriptJsonFormat.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_testrequeteINTER():
    try:
        script_path = os.path.join("fonction_python", "testrequeteINTER.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_testrequeteDonnePhoto():
    try:
        script_path = os.path.join("fonction_python", "testRequeteDonnePhoto.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def run_testrequetePHOTO():
    try:
        script_path = os.path.join("fonction_python", "testrequetePHOTO.py")
        print(f"Running script: {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"Script {script_path} finished with return code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        print(e.stdout)
        print(e.stderr)

def main():
    # Capture the start time
    start_time = datetime.now()
    print(f"Script started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")

    folder_name_tempo = "tempo"
    full_path_tempo = os.path.join(current_directory, folder_name_tempo)
    print(f"Full path to tempo: {full_path_tempo}")

    run_all_csvpython(full_path_tempo)
    run_scrap_images()
    run_scrap_nom()
    run_rename()
    run_scriptJsonFormat()
    run_testrequeteINTER()
    run_testrequeteDonnePhoto()
    run_testrequetePHOTO()

    # Capture the end time
    end_time = datetime.now()
    print(f"Script finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {end_time - start_time}")

if __name__ == "__main__":
    main()
