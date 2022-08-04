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
	stage('Initialize Python'){
            steps {
                script{
                        def pythonHome = tool 'MyPython'
                        env.PATH = "${pythonHome}/bin:${env.PATH}"
			echo 'Python initialized'
                        }

                }
        }
	 stage('Testing app') {
            steps {
		script {
			sh "python -m pytest test_app.py"
		        echo 'Test Completed'
                	}
	        }
        }
	stage('Initialize Docker'){
            steps {
		script{
			def dockerHome = tool 'MyDocker'
                        env.PATH = "${dockerHome}/bin:${env.PATH}"
			echo 'Docker init'
			}
			 
		}
	}
        stage('Login to DockerHub') {
			steps {
				echo "PATH is: ${env.PATH}"
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
            steps{
                sh "kubectl apply -f jenkins/workspace/phonebook/kubernetes/front/deployment.yaml"
		echo 'K8s updated'
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

