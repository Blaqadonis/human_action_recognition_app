from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from batch import run

deployment = Deployment.build_from_flow(
    flow=run,
    name="human_action_recognition",
    parameters={
        "csv_file": "Testing_set.csv",
        "run_id": "d347fb6459524bb8b28cf4254ae52850",
    },
    schedule=CronSchedule(cron="0 0 1 * *"), #first of every month
    work_queue_name="ml",
)

deployment.apply()
