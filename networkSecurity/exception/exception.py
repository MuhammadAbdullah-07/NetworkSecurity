## What does exception.py do?
## Gives you detailed error messages when something goes wrong ,which file the error occured, in which line number
import sys ## Gives Error Details
from networkSecurity.logging.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error Occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name,self.lineno,str(self.error_message))  

## To run this file

if __name__=="__main__":
    try:
        a=1/0
        logger.info("We are in the Try block")
    except Exception as e:
        logger.error("Error occurred", exc_info=True)
        raise NetworkSecurityException(e,sys)        