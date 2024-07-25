import logging
import os
import subprocess
import azure.functions as func

app = func.FunctionApp()

# @app.timer_trigger(schedule="0 0 * * 0", arg_name="myTimer", run_on_startup=False, use_monitor=True)
@app.timer_trigger(schedule="*/10 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=True)

def timer_trigger1(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    try:
        # Change de répertoire vers le dossier contenant le projet Scrapy
        os.chdir("/home/site/wwwroot/formation")
        
        # Utiliser python -m scrapy pour exécuter le spider
        result = subprocess.run(["scrapy", "crawl", "formationspider"], capture_output=True, text=True, check=True)
        
        logging.info(result.stdout)
        logging.error(result.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")