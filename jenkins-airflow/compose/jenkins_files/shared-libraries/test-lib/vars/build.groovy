def runHadoopBuild(useSpan) {
  if (useSpan == true) {
    withNewSpan(label: 'build_span') {
      sh (label: 'sh-build1', script: 'echo build_step1')
      sh (label: 'sh-build2', script: 'echo build_step2')
      sh (label: 'sh-build3', script: 'echo build_step3')
    }
  } else {
    sh (label: 'sh-build1', script: 'echo build_step1')
    sh (label: 'sh-build2', script: 'echo build_step2')
    sh (label: 'sh-build3', script: 'echo build_step3')    
  }
}