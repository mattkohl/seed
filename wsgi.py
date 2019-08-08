from seed import application
import logging


@application.before_first_request
def setup_logging():
    if not application.debug:
        application.logger.addHandler(logging.StreamHandler())
        application.logger.setLevel(logging.INFO)


if __name__ == "__main__":
    application.run()
