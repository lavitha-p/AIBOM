pipeline {
    agent any

    environment {
        MODEL_REPO = "https://github.com/openai/gpt-2.git"
        AIBOM_REPO = "https://github.com/lavitha-p/aibom.git"
    }

    stages {
        stage('Build') {
            steps {
                echo "Starting build for model from ${env.MODEL_REPO}"
            }
        }

        stage('Deploy') {
            steps {
                echo "Cloning the model repository..."
                dir('model') {
                    git "${env.MODEL_REPO}"
                }
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python and dependencies...'
                bat '''
                    "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version
                    "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pip.exe" install -r https://raw.githubusercontent.com/lavitha-p/aibom/main/requirements.txt
                '''
            }
        }

        

        stage('Pull AIBOM Tool') {
    steps {
        dir('aibom-tool') {
            git url: 'https://github.com/lavitha-p/aibom.git', branch: 'main'
        }
    }
}


        stage('Generate AIBOM, SBOM, and Vulnerability Report') {
            steps {
                echo "Running AIBOM tool..."
                bat '''
                    cd aibom-tool
                    "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" generate_aibom.py --model_name "GenericModel" --model_version "1.0"

                '''
            }
        }

        stage('Analyze Vulnerabilities') {
            steps {
                echo "Displaying vulnerability summary..."
                bat '''
                    type aibom-tool\\reports\\vulnerability_report.json
                '''
            }
        }

        stage('Promote Release') {
            steps {
                echo 'Release stage completed!'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
