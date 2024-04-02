import logging
from databricks.sdk.service import jobs
from databricks.sdk.service.jobs import JobCluster
from databricks.sdk.service.compute import ClusterSpec
from databricks.sdk.service.jobs import Task, TaskDependency, NotebookTask, GitSource,GitProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabricksJobManager:
    def __init__(self, workspace_client):
        self.workspace_client = workspace_client

    def create_job(self, name, git_source, tasks):
        try:
            job = self.workspace_client.jobs.create(
                name=name,
                git_source = git_source,
                tasks=tasks
            )
            logger.info(f"Job '{name}' created successfully.")
            return job
        except Exception as e:
            logger.error(f"Error creating job '{name}': {e}")
            raise RuntimeError(f"Error creating job: {e}")

    def run_job_now(self, job_id):
        try:
            run_now_response = self.workspace_client.jobs.run_now(job_id=job_id)
            logger.info(f"Job with ID '{job_id}' ran successfully.")
            return run_now_response
        except Exception as e:
            logger.error(f"Error running job with ID '{job_id}': {e}")
            raise RuntimeError(f"Error running job now: {e}")

    def cancel_run(self, run_id):
        try:
            cancelled_run = self.workspace_client.jobs.cancel_run(run_id=run_id).result()
            logger.info(f"Run with ID '{run_id}' cancelled successfully.")
            return cancelled_run
        except Exception as e:
            logger.error(f"Error cancelling run with ID '{run_id}': {e}")
            raise RuntimeError(f"Error cancelling run: {e}")

    def delete_job(self, job_id):
        try:
            self.workspace_client.jobs.delete(job_id=job_id)
            logger.info(f"Job with ID '{job_id}' deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting job with ID '{job_id}': {e}")
            raise RuntimeError(f"Error deleting job: {e}")
    
    def create_job_cluster(self, cluster_name, node_type_id, num_workers, docker_image, policy_id, spark_version):
        
        # Define the ClusterSpec with the desired compute settings
        
        cluster_spec = ClusterSpec( 
            node_type_id= node_type_id,
            num_workers= num_workers,
            #docker_image = docker_image,
            policy_id = policy_id,
            spark_version = spark_version
            )
        
        # Initialize the JobCluster with a unique name and ClusterSpec
        job_cluster = JobCluster(job_cluster_key = cluster_name, new_cluster = cluster_spec)

        return job_cluster
    
    def create_task(task_key, description, job_cluster, notebook_task, compute_key=None, max_retries=None, depends_on=None):
        # Initialize the Task with the specified parameters
        task = Task(
            task_key=task_key,
            job_cluster_key = job_cluster.job_cluster_key,
            description=description,
            notebook_task = notebook_task,
            max_retries=max_retries,
            depends_on=depends_on

        )
        return task
    
    def create_notebook_task(notebook_path, source, base_parameters=None):

        notebook_source = jobs.Source(GIT = source)

        notebook_task = NotebookTask(notebook_path=notebook_path, base_parameters=base_parameters, source=notebook_source)
        return notebook_task
    
    def create_git_souce(git_url,git_provider,git_branch):
        
        provider = GitProvider(GIT_LAB = git_provider)
        git_source = GitSource(git_url,provider,git_branch)

        return git_source