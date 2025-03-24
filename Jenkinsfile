pipeline {
    agent any

    environment {
        AIBOM_REPO = "https://github.com/lavitha-p/AIBOM.git"
        MODEL_REPO = "https://github.com/karpathy/minGPT.git"
        MODEL_DIR = "minGPT"
        PYTHON_PATH = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {
        stage('Clone Open Source Model') {
            steps {
                dir("${WORKSPACE}") {
                    bat 'IF EXIST minGPT (rmdir /s /q minGPT)'
                    bat 'git clone %MODEL_REPO% %MODEL_DIR%'
                }
            }
        }

        stage('Inject AIBOM Generator Tools') {
            steps {
                dir("${env.MODEL_DIR}") {
                    bat "git clone %AIBOM_REPO% aibom-temp"
                    bat "copy aibom-temp\\*.py ."
                    bat "copy aibom-temp\\*.json ."
                    bat "rmdir /s /q aibom-temp"
                }
            }
        }

        stage('Run AIBOM Tool') {
            steps {
                dir("${env.MODEL_DIR}") {
                    bat 'python -m pip install -r requirements.txt'
bat 'python generate_aibom.py'
bat 'syft . -o json > reports/sbom.json'
bat 'trivy fs . --format json --output reports/vulnerability_report.json'

                    bat "\"${PYTHON_PATH}\" generate_aibom.py"

                }
            }
        }

        stage('Check Reports') {
            steps {
                dir("${env.MODEL_DIR}\\reports") {
                    bat "dir"
                    bat "type aibom.json || echo ❌ aibom.json not found"
                    bat "type sbom.json || echo ❌ sbom.json not found"
                    bat "type vulnerability_report.json || echo ❌ vulnerability_report.json not found"
                }
            }
        }
    }

    post {
        always {
            dir("${WORKSPACE}") {
                bat 'IF EXIST minGPT (rmdir /s /q minGPT)'
            }
        }
    }
}
