pipeline {
  agent {
    label 'master'
  }
  options {
    skipStagesAfterUnstable()
    timeout(time: 1, unit: 'HOURS') 
  }
  stages {
    stage('示例') {
      steps {
        cat run.sh
      }
    }
  }
}


def getServer() {
    def remote = [:]
    remote.name = "server"
    remote.host = "ssh.chdxia.com"
    remote.port = "22"
    remote.allowAnyHosts = true

    withCredentials([usernamePassword(
        credentialsId: 'a477bfd8-880b-4d82-ae37-eecaa6e0133d',
        usernameVariable: 'userName',
        passwordVariable: 'password'
    )]) {
        remote.user = "${userName}"
        remote.password = "${password}"
    }
    return remote
}
