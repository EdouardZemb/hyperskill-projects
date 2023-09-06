import logging


def initialize_logger():
    logging.basicConfig(filename='hyperskill.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')


class LoggingSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggingSingleton, cls).__new__(cls)
            cls._instance.initialize_logger()
        return cls._instance

    @staticmethod
    def initialize_logger():
        logging.basicConfig(filename='hyperskill.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
