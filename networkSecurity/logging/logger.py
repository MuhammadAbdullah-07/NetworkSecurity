import logging
import os
from datetime import datetime


## Format of the Log File
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) ## Create paths and  folder "logs"
os.makedirs(logs_path,exist_ok=True) ## Create folder

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE) ### joing the folder and format of the log 

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("networkSecurity")