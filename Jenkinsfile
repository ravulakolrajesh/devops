pipeline {
    agent any
    environment {
        IMAGE_NAME = 'ravuladockerhub/my-app'
        IMAGE_TAG = "${BUILD_NUMBER ?: 'latest'}"
    }
    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/ravulakolrajesh/pythonaiproj.git'
            }
        }
        
        stage('SCA Scan') {
            steps {
        	script {
        	def status = sh(
        	script: '''
        	docker run --rm -v $PWD:/app python:3.9 \
        	  sh -c "pip install safety && safety check"
        	''',
        	returnStatus: true
        	)
        	
        	if(status !=0){
        	    currentBuild.result = 'UNSTABLE'
        	    echo "Vulnerabilities found! Marking build as UNSTABLE"
        	}
        	}
            }
        }

          stage('Build Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
        	script {
            def status = sh(
                script: '''
                docker run --rm \
                -v /var/run/docker.sock:/var/run/docker.sock \
                aquasec/trivy \
                --severity HIGH,CRITICAL image ravuladockerhub/my-app:${BUILD_NUMBER}
                ''',
                returnStatus: true
            )

            if (status != 0) {
                currentBuild.result = 'UNSTABLE'
                echo "Image vulnerabilities detected"
            }
        }
        }
        }
        
        stage('Run Container') {
            steps {
                sh '''
                docker stop my-app || true
                docker rm my-app || true
                docker run -d --name my-app -p 8081:80 my-app:latest
                '''
            }
        }

        stage('Sonar Scan') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=demo \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                        """
                    }
                }
            }
        }
        
        stage('OWASP ZAP Scan') {
        steps {
            script {
            def status = sh(
            script: '''
            docker run --rm -t \
              -v /var/jenkins_home/workspace/demopipeline:/zap/wrk:rw \
              --user $(id -u):$(id -g) \
              ghcr.io/zaproxy/zaproxy:stable \
              zap-baseline.py \
              -t http://host.docker.internal:8081 \
              -r zap-report.html
            ''',
            returnStatus: true
            )
            
            if (status != 0) {
                currentBuild.result = 'SUCCESS'
                echo "SUCCESS WITH Image vulnerabilities detected"
            }
        }
        }
    }    
    }
     post {
            always {
            archiveArtifacts artifacts: '*.html', allowEmptyArchive: true
          }
    }
}