from datetime import datetime
import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient


mlflow.set_tracking_uri("http://127.0.0.1:5000")


client = MlflowClient()
experiment = client.get_experiment_by_name("Blaqs_har_classifier")
best_run = client.search_runs(
experiment_ids=experiment.experiment_id,
run_view_type=ViewType.ACTIVE_ONLY,
max_results=1
)[0]
run_id = best_run.info.run_id
model_uri = f"runs:/{run_id}/model"
MODEL_NAME = "best_tensorflow_pretrained_model"
mlflow.register_model(model_uri, MODEL_NAME)


VERSION = client.get_latest_versions(name=MODEL_NAME)[0].version
NEW_STAGE = 'Production'

def transition_model_to_staging(name: str, version: int, stage: str):
    '''Transition model to production stage'''
    client.transition_model_version_stage(name=name, version=version,
        stage=stage, archive_existing_versions=False )
    return print("Model transitioned to production stage")





if __name__ == "__main__":
    transition_model_to_staging(MODEL_NAME, VERSION, NEW_STAGE)
    date = datetime.today().date()
    client.update_model_version(name=MODEL_NAME, version = VERSION,
    description=f"The model version {VERSION} was transitioned to {NEW_STAGE} on {date}")
    