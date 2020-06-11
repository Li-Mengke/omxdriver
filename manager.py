from error_manager import Error_Handler

handler = Error_Handler()
logger = handler.get_logger()

logger.warning('something')