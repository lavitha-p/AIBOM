pipeline {
    agent any

    stages {
        stage('Check Required Files') {
            steps {
                script {
                    if (!fileExists('dataset.json') || !fileExists('modelinfo.json')) {
                        error(" Required files missing: dataset.json or modelinfo.json")
                    }
                }
            }
        }

        stage('Pull AIBOM Tool') {
            steps {
                echo " Repo already cloned — skipping separate pull step."
            }
        }

        stage('Generate AIBOM, SBOM, and Vulnerability Report') {
    steps {
        bat '"C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" generate_aibom.py'
    }
}


        stage('Analyze Vulnerabilities') {
            steps {
                script {
                    def report = readJSON file: 'reports/vulnerability_report.json'
                    if (report.vulnerabilities && report.vulnerabilities.size() > 0) {
                        echo " Vulnerabilities found!"
                    } else {
                        echo " No vulnerabilities detected."
                    }
                }
            }
        }
    }
}
