import logging

def setup_logger(name=__name__, level=logging.INFO):
    """
    Thiết lập logger chuẩn cho hệ thống.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.setLevel(level)

    return logger
