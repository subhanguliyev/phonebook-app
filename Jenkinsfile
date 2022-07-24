pipeline {
    agent { label 'slave1' }
    environment {
        DOCKERHUB_CREDENTIALS= credentials('dockerhubcredentials')
	}
    stages {
        stage("Git checkout") {
            steps {
                deleteDir()
                git branch: 'master',
		git credentialsId: 'github', url: 'https://github.com/subhanguliyev/phonebook-app'
		echo 'Git Checkout Completed'
            }
        }
	
        stage('Login to DockerHub') {
			steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
				echo 'Login Completed'
			}
		}
        stage('Build phonebook-app docker image') {
            steps {
                sh "ls -lh"
                sh "sudo docker build -t localhost:5000/phonebook-app:${BUILD_NUMBER} ."
		echo 'Build Image Completed'
            }
        }
        stage('Push to docker registry') {
            steps {
                sh "sudo docker push localhost:5000/phonebook-app:${BUILD_NUMBER}"
		echo 'Push Image Completed'
            }
        }
        stage('Update k8s deployment') {
            steps {
                sh """
                    sed -i -e "/^\\s*image:\\s.*/s/phonebook-app:.*/phonebook-app:${BUILD_NUMBER}/g" phonebook-app/k8s/front/deployment.yaml
                """
                sh "kubectl apply -f phonebook-app/kubernetes/front/"
            }
        }

    }
    post {
        always {
            sh(label: "Cleanup", script: """#!/bin/bash
                docker logout
            """)
        }
    }
}

