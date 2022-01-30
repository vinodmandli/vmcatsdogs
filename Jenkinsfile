pipeline {

  environment {
    dockerimagename = "vinodmandli/vmcatsdogs"
	registryCredential = 'dockerHubCredentials'
    dockerImage = ""
  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git 'https://github.com/vinodmandli/vmcatsdogs.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerimagename
        }
      }
    }

    stage('Pushing Image') {
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        script {
          kubernetesDeploy(configs: "vmcatsdogs.yml", kubeconfigId: "kubernetes")
        }
      }
    }

  }

}
