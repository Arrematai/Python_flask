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
  
  for scheduler in schedulers:
    SchedulerClass  = dynamic_import(scheduler["path"], scheduler["class"]) 
    
    if SchedulerClass:
      instance = SchedulerClass(scheduler["nome"],schedulersLog,lotesRepository)  # Instancia a classe
      instance.exec()
      
      # ADD somente se não existe com esse nome
      if not schedulerBackground.get_job(scheduler["nome"]):
        job = schedulerBackground.add_job(
          func=instance.exec,
          trigger=CronTrigger(hour=int(scheduler["hora"]), minute=int(scheduler["minuto"])),
          replace_existing=True,
          # args=["receitafederal",schedulersLog,lotesRepository],
          id=scheduler["nome"]
        )

    print("JOB Agendado: ", job.id,job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"))
  
# Executar Scheduler
def init():

  try:
    print('INICIADO SCHEDULERS')
    schedulerBackground.start()
    Schedulers();

    # SERVE PARA MANTER O SCHEDULER ABERTO
    while True:
      print('SLEEP SCHEDULERS...')
      time.sleep(600) # 10 minutos

  except (KeyboardInterrupt, SystemExit):
    schedulerBackground.shutdown()
        
  