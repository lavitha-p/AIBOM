pipeline {
    agent any

    environment {
        MODEL_REPO = "https://github.com/salesforce/xgen.git"
        MODEL_BRANCH = 'main'
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
                    git branch: "${env.MODEL_BRANCH}", url: "${env.MODEL_REPO}"
                }
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python and dependencies...'
                script {
                    def modelReq = fileExists('model/requirements.txt')
                    def reqFile = modelReq ? 'model/requirements.txt' : 'aibom-tool/requirements.txt'
                    echo "Using requirements file: ${reqFile}"

        bat '''
            "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" -m pip install --upgrade pip setuptools wheel
            if exist model\\requirements.txt (
                "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pip.exe" install -r model\\requirements.txt
            ) else (
                "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pip.exe" install -r aibom-tool\\requirements.txt
            )
        '''
                }
            }
        }

        stage('Pull AIBOM Tool') {
            steps {
                dir('aibom-tool') {
                    git url: "${env.AIBOM_REPO}", branch: 'main'
                }
            }
        }

        stage('Validate Files') {
            steps {
                script {
                    def datasetInModel = fileExists('model/dataset.json')
                    def modelinfoInModel = fileExists('model/modelinfo.json') || fileExists('model/modelcard.json')

                    if (!datasetInModel) {
                        echo "Copying dataset.json from AIBOM tool to model folder..."
                        bat 'copy aibom-tool\\dataset.json model\\dataset.json'
                    } else {
                        echo "Using dataset.json from model repo"
                    }

                    if (!modelinfoInModel) {
                        echo "Copying modelinfo.json from AIBOM tool to model folder..."
                        bat 'copy aibom-tool\\modelinfo.json model\\modelinfo.json'
                    } else {
                        echo "Using modelinfo.json or modelcard.json from model repo"
                    }
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
        dir('aibom-tool') {
            bat '''
                if not exist ..\\reports (
                    mkdir ..\\reports
                )
                "C:\\Users\\HP\\scoop\\shims\\trivy.exe" fs --severity CRITICAL,HIGH,MEDIUM,LOW --format json -o ..\\reports\\vulnerability_report.json .
            '''
        }
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
