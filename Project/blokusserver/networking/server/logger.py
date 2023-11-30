

import logging
from sys import stdout

##################################################
## Author: Luis Eckert / Kevin Wagner
##################################################

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
                    level = logging.DEBUG,
                    format= LOG_FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger:logging.Logger = logging.getLogger()
