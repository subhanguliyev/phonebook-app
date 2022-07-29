pipeline {
    agent { label 'slave1' }
    environment {
    	PATH = "C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\bin;${env.PATH}"
        DOCKERHUB_CREDENTIALS= credentials('dockerhubcredentials')
	if (isUnix()) --> sh "command"
	else --> bat "command"
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
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
				echo 'Login Completed'
			}
		}
        stage('Build phonebook-app docker image') {
            steps {
                sh "docker images"
                sh "ls -lh"
		sh "docker build -t 127.0.0.1:5000/phonebook-app ."
		echo 'Build Image Completed'
            }
        }
        stage('Push to docker registry') {
            steps {
                sh "docker push 127.0.0.1:5000/phonebook-app:latest"
		echo 'Push Image Completed'
            }
        }
        stage('Update kubernetes deployment') {
            steps {
                sh "kubectl apply -f phonebook/kubernetes/front/deployment.yaml"
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

