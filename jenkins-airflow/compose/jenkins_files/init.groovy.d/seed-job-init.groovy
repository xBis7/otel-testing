import javaposse.jobdsl.plugin.ExecuteDslScripts
import jenkins.model.Jenkins

// Get the Jenkins instance
def jenkinsInstance = Jenkins.instance

// Define the Seed Job name
def seedJobName = 'SeedJob'

// Check if the SeedJob already exists
def seedJob = jenkinsInstance.getItem(seedJobName)

if (seedJob == null) {
    // Create the SeedJob as a freestyle project
    def seedProject = jenkinsInstance.createProject(hudson.model.FreeStyleProject, seedJobName)

    // Define the build step to copy the DSL script into the workspace
    def copyScript = '''
        cp /var/jenkins_home/pipelines/pipeline_jobs.groovy ${WORKSPACE}/pipeline_jobs.groovy
    '''

    seedProject.buildersList.add(new hudson.tasks.Shell(copyScript))

    // Configure the job to execute DSL scripts after copying the file
    def executeDsl = new ExecuteDslScripts()
    executeDsl.targets = 'pipeline_jobs.groovy'  // Path relative to the workspace
    seedProject.buildersList.add(executeDsl)

    // Save the Seed Job
    seedProject.save()

    println("Created SeedJob with DSL script execution.")
} else {
    println("SeedJob already exists.")
}
