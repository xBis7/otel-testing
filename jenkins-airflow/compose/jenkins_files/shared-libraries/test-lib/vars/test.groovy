def runMvnTest(directory, testClass) {
  dir(directory) {
    withMaven(maven: 'M3') {
      sh (label: "sh-test ${testClass}", script: "mvn test -Dtest=${testClass}")
    }
  }
}

def runHadoopTests(useSpan) {
  if (useSpan == true) {
    withNewSpan(label: 'test_span') {
      // runMvnTest('hadoop-common-project/hadoop-common', 'TestConfigurationDeprecation')
      // runMvnTest('hadoop-common-project/hadoop-common', 'TestCommonConfigurationFields')
      // runMvnTest('hadoop-hdfs-project/hadoop-hdfs', 'TestLeaseManager')
      // runMvnTest('hadoop-hdfs-project/hadoop-hdfs', 'TestHdfsServerConstants')
      sh (label: 'sh-test1', script: 'echo test_step1')
      sh (label: 'sh-test2', script: 'echo test_step2')
      sh (label: 'sh-test3', script: 'echo test_step3')
    }
  } else {
    // runMvnTest('hadoop-common-project/hadoop-common', 'TestConfigurationDeprecation')
    // runMvnTest('hadoop-common-project/hadoop-common', 'TestCommonConfigurationFields')
    // runMvnTest('hadoop-hdfs-project/hadoop-hdfs', 'TestLeaseManager')
    // runMvnTest('hadoop-hdfs-project/hadoop-hdfs', 'TestHdfsServerConstants')
    sh (label: 'sh-test1', script: 'echo test_step1')
    sh (label: 'sh-test2', script: 'echo test_step2')
    sh (label: 'sh-test3', script: 'echo test_step3')
  }
}
