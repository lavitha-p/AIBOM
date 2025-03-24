pipeline {
    agent any

    parameters {
        string(name: 'MODEL_REPO', defaultValue: 'https://github.com/openai/gpt-2.git', description: 'GitHub link to the model repo')
    }

    environment {
        AIBOM_REPO = 'https://github.com/lavitha-p/aibom.git'
        AIBOM_SCRIPT = 'generate_aibom.py'
        PYTHON = 'python3'  // Adjust if needed (like py or python3)
    }

    stages {

        stage('Build') {
            steps {
                echo "Starting build for model from ${params.MODEL_REPO}"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Cloning the model repository...'
                dir('model') {
                    git url: "${params.MODEL_REPO}"
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running preliminary checks...'
            }
        }

        stage('Promote Release') {
            steps {
                echo 'Promoting model for further processing...'
            }
        }

        stage('Check Required Files') {
            steps {
                echo 'Checking for required files in model repo...'
                dir('model') {
                    bat '''
                        if not exist requirements.txt (
                            echo "requirements.txt not found!" && exit 1
                        )
                    '''
                }
            }
        }

        stage('Pull AIBOM Tool') {
            steps {
                echo 'Cloning AIBOM generator tool...'
                dir('model') {
                    bat "git clone ${env.AIBOM_REPO}"
                }
            }
        }

        stage('Generate AIBOM, SBOM, and Vulnerability Report') {
            steps {
                echo 'Running AIBOM tool on model...'
                dir('model') {
                    bat '''
                        cd aibom-generator
                        call ..\\venv\\Scripts\\activate
                        python generate_aibom.py --model_name "GenericModel" --model_version "1.0"
                    '''
                }
            }
        }

        stage('Analyze Vulnerabilities') {
            steps {
                echo 'Checking generated vulnerability report...'
                dir('model/aibom-generator/reports') {
                    bat '''
                        if exist vulnerability_report.json (
                            echo "Vulnerability report found. Analyzing..."
                        ) else (
                            echo "vulnerability_report.json not found!" && exit 1
                        )
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
