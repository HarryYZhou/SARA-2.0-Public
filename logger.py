import logging

class Logger:
    log_filename = 'log.txt'

    def __init__(self, frequency) -> None:
        self.frequency = frequency
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(self.log_filename),
                logging.StreamHandler()
            ],
            level=logging.INFO
        )

    def begin(self) -> None:
        logging.info(f'==== Begin running {self.frequency} ====')

    def success(self, name: str) -> None:
        logging.info(f'Email to {name : >10} succeeded')

    def failure(self, name: str) -> None:
        logging.error(f'Email to {name : >10} failed')

    def end(self) -> None:
        logging.info(f'==== Completed emailing ====\n')

    def error(self, name: str) -> None:
        logging.error(f'Error: {name : >10}')

    def passed(self, name: str) -> None:
        logging.info(f"Sensitivity for {name : >10} wasn't triggered ---- Continuing Iteration")