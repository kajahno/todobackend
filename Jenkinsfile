pipeline {
    
    agent any

    options {
        ansiColor('xterm')
    }

    stages {
        try {
            stage('Run unit/integration tests'){
                steps {
                    sh 'make test'                
                }
            }

            stage('Build application artifacts'){
                steps {
                    sh 'make build'
                }
            }

            stage('Create release environment and run acceptance tests'){
                steps {
                    sh 'make release'
                }        
            }
        
            stage('Tag and publish release image'){
                steps {
                    sh "make tag latest \$(git rev-parse --short HEAD) \$(git tag --points-at HEAD)"
                    sh "make buildtag master \$(git tag --points-at HEAD)"
                    
                    withEnv(["DOCKER_USER=${DOCKER_USER}",
                            "DOCKER_PASSWORD=${DOCKER_PASSWORD}"]){
                        sh 'make login'         
                    }
                    
                    sh 'make publish'
                }
            }
        }
        finally {
            stage('Collect test reports'){
                steps {
                    junit '**/reports/*.xml'
                }
            }

            stage('Clean up'){
                steps {
                    sh 'make clean'
                    sh 'make logout'
                }
            }
        }        

    }

}
