pipeline {
    agent any

    environment {
        AIBOM_REPO = "https://github.com/lavitha-p/AIBOM.git"
        MODEL_REPO = "https://github.com/karpathy/minGPT.git"
        MODEL_DIR = "minGPT"
    }
    

    stage('Clone Open Source Model') {
    steps {
        dir("${WORKSPACE}") {
            bat 'IF EXIST minGPT (rmdir /s /q minGPT)'
            bat 'git clone https://github.com/karpathy/minGPT.git minGPT'
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
        dir('minGPT') {
            bat 'C:\\Users\\HP\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe generate_aibom.py'
        }
    }
}

        stage('Check Reports') {
            steps {
                dir("${env.MODEL_DIR}\\reports") {
                    bat "dir"
                    bat "type aibom.json || echo aibom.json not found"
                    bat "type sbom.json || echo sbom.json not found"
                    bat "type vulnerability_report.json || echo vulnerability_report.json not found"
                }
            }
        }
    }

