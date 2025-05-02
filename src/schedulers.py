from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time


from src.infra.database.mysql import DataBase
from src.infra.schedulers.receitaFederal import SchedulerReceitaFederal
from src.domain.lotes.repository import LotesRepository
from src.infra.schedulers.schedulersLogRepository import SchedulersLogRepository


scheduler = BackgroundScheduler()

def Schedulers():

  database = DataBase(dictionary=True)
  schedulersLog = SchedulersLogRepository(database)
  lotesRepository = LotesRepository(database)
  
  instance = SchedulerReceitaFederal("receitafederal",schedulersLog,lotesRepository)
  # instance.exec()

  # ADD somente se não existe com esse nome
  if not scheduler.get_job('receitafederal'):
    job = scheduler.add_job(
      func=instance.exec,
      trigger=CronTrigger(hour=9, minute=30),
      replace_existing=True,
      # args=["receitafederal",schedulersLog,lotesRepository],
      id='receitafederal'
    )

    print("JOB Agendado: ", job.id,job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"))


# Executar Scheduler
def init():

  try:
    print('INICIADO SCHEDULERS')
    scheduler.start()
    Schedulers();

    # SERVE PARA MANTER O SCHEDULER ABERTO
    while True:
      print('SLEEP SCHEDULERS...')
      time.sleep(60) # 10 minutos

  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
        
  