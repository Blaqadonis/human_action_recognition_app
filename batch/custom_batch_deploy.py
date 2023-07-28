import sys
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from custom_batch import run

deployment = Deployment.build_from_flow(
    flow=run,
    name="human_action_recognition",
    parameters={"csv_file" : sys.argv[1],
        "run_id" : sys.argv[2],    #'MLflow Run ID',
        "block" : sys.argv[3],   #'update-me'
    "email" : sys.argv[4],   #'your-email-address'
    "password" : sys.argv[5]  #'your-app-password'
    },schedule=CronSchedule(cron=sys.argv[6], #you-cron-expression
    work_queue_name="big",))

deployment.apply()
