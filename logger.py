import logging

logging.basicConfig(
    filename="sms.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
