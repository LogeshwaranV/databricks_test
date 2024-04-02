from databricks.sdk import WorkspaceClient
from databricks.sdk.service.compute import DockerImage, DockerBasicAuth
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabricksCluster:
    def __init__(self, workspace_client):
        self.workspace_client = workspace_client

    def create_cluster(self, cluster_name, spark_version, docker_image, autotermination_minutes, num_workers):
        try:
            cluster = self.workspace_client.clusters.create_and_wait(
                cluster_name=cluster_name,
                spark_version=spark_version,
                docker_image=docker_image.as_dict(),
                autotermination_minutes=autotermination_minutes,
                num_workers=num_workers
            ).result()
            logger.info(f"Cluster '{cluster_name}' created successfully.")
            return cluster
        except Exception as e:
            logger.error(f"Error creating cluster '{cluster_name}': {e}")
            raise

    def start_cluster(self, cluster_id):
        try:
            result = self.workspace_client.clusters.start(cluster_id=cluster_id).result()
            logger.info(f"Cluster with ID '{cluster_id}' started successfully.")
            return result
        except Exception as e:
            logger.error(f"Error starting cluster with ID '{cluster_id}': {e}")
            raise