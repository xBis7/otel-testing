// Script with all the predefined pipeline jobs.

pipelineJob('hadoop-test') {
  definition {
    cps {
      script(readFileFromWorkspace('/var/jenkins_home/Jenkinsfile.hadoop'))
      sandbox(true)
    }
  }
}

// For multiple pipelines.

// pipelineJob('PipelineJob2') {
//   definition {
//     cps {
//       script(readFileFromWorkspace('Jenkinsfile2'))
//       sandbox(true)
//     }
//   }
// }
