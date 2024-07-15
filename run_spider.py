import os
import subprocess

# Change de répertoire vers le dossier contenant le projet Scrapy
os.chdir("/home/laetitia/Documents/TaskManagerProject/formationscraper") 

try:
    result = subprocess.run(
        ["scrapy", "crawl", "moncompteformationspider"],
        capture_output=True, text=True, check=True
    )

    # Extraire la sortie imprimée par le spider
    for line in result.stdout.splitlines():
        if "Date de mise à jour" not in line:
            print(f"La DATE de MISE À JOUR EST : {line}")
            break

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")
