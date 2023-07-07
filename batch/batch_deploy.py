import sys
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from batch import run

deployment = Deployment.build_from_flow(
    flow=run,
    name="human_action_recognition",
    parameters={
        "csv_file": sys.argv[1],
        "run_id": sys.argv[2],
    },
    schedule=CronSchedule(cron="0 0 1 * *"), #first of every month
    work_queue_name="big",
)

deployment.apply()
