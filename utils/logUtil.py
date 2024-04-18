import logging

class LogHelper():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.ERROR)  # 에러 레벨 이상의 로그만 기록
        format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(filename)s (%(funcName)s line : %(lineno)s) -> %(message)s")
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(format)

        self.logger.addHandler(streamHandler)
