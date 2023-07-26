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