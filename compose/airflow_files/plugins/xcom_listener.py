from airflow.listeners import hookimpl
from airflow.models.baseoperator import BaseOperator
from airflow.plugins_manager import AirflowPlugin

class XComPushListener:
  @hookimpl
  def on_task_success(self, operator: BaseOperator, **kwargs):
    # Pushing a custom message to XCom on task success
    ti = kwargs['task_instance']
    ti.xcom_push(key='custom_key', value='Task succeeded!')

class XComPushPlugin(AirflowPlugin):
  name = "xcom_push_plugin"
  listeners = [XComPushListener()]