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
            dockerImage.push(${env.BUILD_ID})
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        script {
          sh 'kubectl apply -f ./vmcatsdogs.yml'
		  sh 'kubectl set image statefulset/vmcatsdogs vmcatsdogsserver=vinodmandli/vmcatsdogs:${env.BUILD_ID}'
		  sh 'kubectl rollout status statefulset/vmcatsdogs'
        }
      }
    }

  }

}
