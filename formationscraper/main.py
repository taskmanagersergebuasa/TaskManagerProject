import logging
import os
import subprocess


logging.info('Python timer trigger function executed.')
try:
    # Change de répertoire vers le dossier contenant le projet Scrapy
    os.chdir("/home/site/wwwroot/formation")
    
    # Utiliser python -m scrapy pour exécuter le spider
    logging.info('Spider executed.')
    spider_result = subprocess.run(["scrapy", "crawl", "formationspider"], capture_output=True, text=True, check=True)
    logging.info(f"Spider Output: {spider_result.stdout}")

except subprocess.CalledProcessError as e:
    logging.error(f"Error executing command: {e.stdout}")
    logging.error(f"Error executing command: {e.stderr}")
except Exception as e:
    logging.error(f"Unexpected error: {str(e)}")