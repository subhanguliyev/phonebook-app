pipeline {
    agent { label 'slave1' }
    environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhub')
    }
    stages {
        stage("Git checkout") {
            steps {
                deleteDir()
                git branch: 'master',
                    url   : 'https://github.com/subhanguliyev/phonebook-app'
            }
        }
	
        stage('Login to DockerHub') {
			steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			}
		}
        stage('Build phonebook-app docker image') {
            steps {
                sh "ls -lh"
                sh "docker build -t localhost:5000/phonebook-app:${BUILD_NUMBER} ."
            }
        }
        stage('Push to docker registry') {
            steps {
                sh "docker push localhost:5006/phonebook-app:${BUILD_NUMBER}"
            }
        }
        stage('Update k8s deployment') {
            steps {
                sh """
                    sed -i -e "/^\\s*image:\\s.*/s/phonebook-app:.*/phonebook-app:${BUILD_NUMBER}/g" phonebook-app/k8s/front/deployment.yaml
                """
                sh "kubectl apply -f phonebook-app/k8s/front/"
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

