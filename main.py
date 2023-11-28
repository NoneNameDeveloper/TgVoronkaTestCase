from loader import app

from app import handlers

from loguru import logger


async def main():
    logger.info("Client started!")


app.run()

