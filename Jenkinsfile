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
		    url: 'https://github.com/subhanguliyev/phonebook-app'
		checkout([$class: 'GitSCM',
                          branches: [[name: '*/master']],
                          extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'phonebook-app']],
                          userRemoteConfigs: [[credentialsId: 'github', url: 'https://github.com/subhanguliyev/phonebook-app']]
                          ])

		echo 'Git Checkout Completed'
            }
        }
	
        stage('Login to DockerHub') {
			steps {
				'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
				echo 'Login Completed'
			}
		}
        stage('Build phonebook-app docker image') {
            steps {
                bat "docker images"
                bat "ls -lh"
		bat "docker build -t 127.0.0.1:5000/phonebook-app ."
		echo 'Build Image Completed'
            }
        }
        stage('Push to docker registry') {
            steps {
                bat "docker push 127.0.0.1:5000/phonebook-app:latest"
		echo 'Push Image Completed'
            }
        }
        stage('Update kubernetes deployment') {
            steps {
                bat "kubectl apply -f phonebook/kubernetes/front/deployment.yaml"
            }
        }

    }
    post {
        always {
            bat(label: "Cleanup", script: """#!/bin/bash
                docker logout
            """)
        }
    }
}

