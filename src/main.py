# from databricks.sdk.service.compute import DockerImage, DockerBasicAuth
from utils import create_workspace_client
import logging
from cluster import DatabricksCluster
from job import DatabricksJobManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# docker_basic_auth = DockerBasicAuth(username='<your-username>', password='<your-password>')
# docker_image = DockerImage(url='<your-docker-image-url>', basic_auth=docker_basic_auth)

def main():
    # Initialize your DatabricksJobManager with the appropriate workspace client
    workspace_client = create_workspace_client()  # Initialize your workspace client here
    job_manager = DatabricksJobManager(workspace_client)

    # Define job parameters
    job_name = "Your Job Name"
    git_url = "https://github.com/yourusername/yourrepo.git"
    git_provider = "gitlab"  # Specify your Git provider (e.g., gitlab, github)
    git_branch = "main"
    notebook_path = "/path/to/your/notebook"
    source = "https://github.com/yourusername/yourrepo.git"
    base_parameters = {"param1": "value1", "param2": "value2"}

    # Create Git Source and Notebook Task
    git_source = job_manager.create_git_source(git_url, git_provider, git_branch)
    notebook_task = job_manager.create_notebook_task(notebook_path, source, base_parameters)

    # Create job cluster
    cluster_name = "Your Cluster Name"
    node_type_id = "Your Node Type ID"
    num_workers = 2  # Specify the number of workers
    docker_image = "Your Docker Image"
    policy_id = "Your Policy ID"
    spark_version = "Your Spark Version"
    job_cluster = job_manager.create_job_cluster(cluster_name, node_type_id, num_workers, docker_image, policy_id, spark_version)

    # Create task and job
    task_key = "Your Task Key"
    description = "Your Task Description"
    task = job_manager.create_task(task_key, description, job_cluster, notebook_task)

    # Create the job
    job = job_manager.create_job(job_name, git_source, [task])

    # Run the job now
    job_id = job.job_id
    run_response = job_manager.run_job_now(job_id)

    # Print the run response
    print("Job Run ID:", run_response.run_id)

if __name__ == "__main__":
    main()
