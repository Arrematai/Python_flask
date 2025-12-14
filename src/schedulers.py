import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time


from src.infra.database.mysql import DataBase
from src.domain.lotes.repository import LotesRepository
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.domain.schedulers.repository.schedulersRepository import SchedulersRepository

## SCHEDULERS
from src.infra.helpers.importModules import dynamic_import


schedulerBackground = BackgroundScheduler()

def Schedulers():

  database = DataBase(dictionary=True)
  schedulersLog = SchedulersLogRepository(database)
  lotesRepository = LotesRepository(database)
  schedulersRepository = SchedulersRepository(database) 
  
  schedulers = schedulersRepository.getSchedulers()
  
  # print(schedulers)
  # exit(0)
  
  for scheduler in schedulers:
    SchedulerClass  = dynamic_import(scheduler["path"], scheduler["class"]) 
    
    if SchedulerClass:
      instance = SchedulerClass(scheduler["nome"],schedulersLog,lotesRepository)  # Instancia a classe
      instance.exec()
      
      nomeJob = f"{scheduler["nome"]}_{scheduler["hora"]}_{scheduler["minuto"]}"
      
      # ADD somente se não existe com esse nome
      if not schedulerBackground.get_job(nomeJob):
        job = schedulerBackground.add_job(
          func=instance.exec,
          trigger=CronTrigger(hour=int(scheduler["hora"]), minute=int(scheduler["minuto"])),
          replace_existing=True,
          # args=["receitafederal",schedulersLog,lotesRepository],
          id=nomeJob
        )

  print("JOB Agendado: ", job.id,job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"))
  if os.getenv("MODE") == "DEV":
    exit(0)
  
def init():
    try:
        print('INICIADO SCHEDULERS')
        schedulerBackground.start()
        Schedulers()

        # Mantém o programa vivo sem ocupar CPU
        schedulerBackground._event.wait()

    except (KeyboardInterrupt, SystemExit):
        schedulerBackground.shutdown()
        
  