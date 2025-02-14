import os
import logging
from typing import Text
from dotenv import load_dotenv
load_dotenv()

current_dir = os.getcwd()
EXECUTION_LEVEL = 25  # Escolha um valor entre os níveis existentes (10 DEBUG, 20 INFO)
CHECKSITEONLINE_LEVEL = 30  # Escolha um valor entre os níveis existentes (10 DEBUG, 20 INFO)
MONITORAMENTO_LEVEL = 31  # Escolha um valor entre os níveis existentes (10 DEBUG, 20 INFO)

def createdExecution(self, message, *args, **kwargs):
  if self.isEnabledFor(EXECUTION_LEVEL):
      self._log(EXECUTION_LEVEL, message, args, **kwargs)
      
def createdCheckSiteOnline(self, message, *args, **kwargs):
  if self.isEnabledFor(CHECKSITEONLINE_LEVEL):
      self._log(CHECKSITEONLINE_LEVEL, message, args, **kwargs)

def monitoramento(self, message, *args, **kwargs):
  if self.isEnabledFor(MONITORAMENTO_LEVEL):
      self._log(MONITORAMENTO_LEVEL, message, args, **kwargs)


class Log:
  hostname: Text
  level: Text
  path_log: Text

  def __init__(cls, ip):
    cls.ip = ip
    cls.version = os.getenv("VERSION")
    cls.logging = logging
    cls.path_log = os.path.join(current_dir, "log")
    cls.createPathLog()
    cls.createdLoggerCustom()

  def createdLoggerCustom(cls):
    cls.logging.addLevelName(EXECUTION_LEVEL, "EXECUTION")
    cls.logging.addLevelName(CHECKSITEONLINE_LEVEL, "CHECKSITE")
    cls.logging.addLevelName(MONITORAMENTO_LEVEL, "MONITORAMENTO")
    cls.logging.Logger.execution = createdExecution
    cls.logging.Logger.checkonline = createdCheckSiteOnline
    cls.logging.Logger.monitoramento = monitoramento
    cls.logger = cls.logging.getLogger("arrematei_logger")
    
  def register(cls, filename, level, formatter) -> None:
    cls.logging.basicConfig(handlers=[cls.logging.FileHandler(
      filename=os.path.join(cls.path_log, f'{filename}.log'),
      mode='a', 
      encoding='utf-8', 
    )], level=level, format=formatter, datefmt='%d/%b/%y %H:%M:%S')
  
  
  def executionTime(cls, start, end, api, query) -> None:
    execution_time = end - start
    cls.register(
      filename='execution', 
      level=EXECUTION_LEVEL,
      formatter=f"[%(asctime)s] — [{cls.version}] - %(levelname)s — %(message)s"
    )
    cls.logger.execution(f"API: {api}, Tempo de execução da: {execution_time:.6f} segundos, query: {query}")
    
  def checkOnlineSite(cls, start, end, site, status) -> None:
    execution_time = end - start
    cls.register(
      filename='check_online', 
      level=CHECKSITEONLINE_LEVEL,
      formatter=f"[%(asctime)s] — [{cls.version}] - %(levelname)s — %(message)s"
    )
    cls.logger.checkonline(f"SITE: {site}, Tempo de checagem da: {execution_time:.6f} segundos, status code: {status}")

  def monitoramento(cls, message) -> None:
    cls.register(
      filename='monitoramento', 
      level=MONITORAMENTO_LEVEL,
      formatter=f"[%(asctime)s] — [{cls.version}] - %(levelname)s — %(message)s"
    )
    cls.logger.monitoramento(message)
  
  
  def messageInfo(cls, message:Text) -> None:
    cls.register(
      filename='info', 
      level=cls.logging.INFO,
      formatter=f"[%(asctime)s] - [{cls.version}] — %(levelname)s — %(message)s"
    )
    cls.logging.info(str(message))

  def messageError(cls, message:Text) -> None:
    cls.register(
      filename='error', 
      level=cls.logging.ERROR,
      formatter=f"[%(asctime)s] — [{cls.version}] - %(name)s — %(levelname)s — %(message)s"
    )
    cls.logging.error(str(message))


  def messageDebug(cls, message:Text) -> None:
    cls.register(
      filename='debug', 
      level=cls.logging.DEBUG,
      formatter=f"[%(asctime)s] — [{cls.version}] - %(name)s — %(levelname)s — %(message)s"
    )
    cls.logging.debug(str(message))

  def createPathLog(cls) -> None:
    os.makedirs(cls.path_log, exist_ok = True)
