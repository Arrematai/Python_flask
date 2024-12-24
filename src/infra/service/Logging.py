import os
import logging
from typing import Text

class Log:
  hostname: Text
  level: Text
  path_log: Text = '/log/arrematai'

  def __init__(cls, ip):
    cls.ip = ip
    cls.logging = logging
    cls.createPathLog()
    # cls.hostname = hostname

  def register(cls, filename, level, formatter) -> None:
    cls.logging.basicConfig(handlers=[cls.logging.FileHandler(
      filename=cls.path_log+filename+'.log',
      mode='a', 
      encoding='utf-8', 
    )], level=level, format=formatter, datefmt='%d/%b/%y %H:%M:%S')
    
  def messageInfoHost(cls, message:Text) -> None:
    cls.register(
      filename='info', 
      level=cls.logging.INFO,
      formatter=f"[%(asctime)s] — %(levelname)s - v{__version__} - {cls.ip} — %(message)s"
    )
    cls.logging.info(str(message))

  def messageErrorHost(cls, message:Text) -> None:
    cls.register(
      filename='info', 
      level=cls.logging.ERROR,
      formatter=f"[%(asctime)s] — %(name)s — %(levelname)s - v{__version__} - {cls.ip} — %(message)s"
    )
    cls.logging.error(str(message))


  def messageDebug(cls, message:Text) -> None:
    cls.register(
      filename='info', 
      level=cls.logging.DEBUG,
      formatter=f"[%(asctime)s] — %(name)s — %(levelname)s - v{__version__} - {cls.ip} — %(message)s"
    )
    cls.logging.debug(str(message))

  def createPathLog(cls) -> None:
    os.makedirs(cls.path_log, exist_ok = True)
