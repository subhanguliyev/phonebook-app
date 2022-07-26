pipeline {
    agent { label 'slave1' }
    environment {
    	DOCKERHUB_CREDENTIALS = credentials('dockerhubcredentials')
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
		 dir('tests') {
		    script {
		    	sh "python -m pytest test_app.py"
		        echo 'Test Completed'
                	}
		    }
	         }
        }
	 stage('SonarQube analysis') {
             steps {
                 dir('tests') {
                    script {
                        sh """
				sonar-scanner.bat -D"sonar.projectKey=sonarqube-flask" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=f3d99ebef8b3767dd9e4b11f4b38446cf348811d"
			"""
                        echo 'Sonarqube tested'
                        }
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
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
				echo 'Login Completed'
			}
	}
        stage('Build phonebook-app docker image') {
            steps {
                sh "docker images"
                sh "ls -lh"
		sh "docker build -t 127.0.0.1:5000/phonebook-app:${BUILD_NUMBER} ."
		echo 'Build Image Completed'
            }
        }
        stage('Push to docker registry') {
            steps {
                sh "docker push 127.0.0.1:5000/phonebook-app:${BUILD_NUMBER}"
		echo 'Push Image Completed'
            }
        }
        stage('Update kubernetes deployment') {
            steps{
	    	dir('kubernetes'){
		   script {
		   	sh """
                    		sed -i -e "/^\\s*image:\\s.*/s/phonebook-app:.*/phonebook-app:${BUILD_NUMBER}/g" front/deployment.yaml
                	"""
                	sh "kubectl apply -f front/deployment.yaml"
			echo 'K8s updated'
			}
            	     }
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

