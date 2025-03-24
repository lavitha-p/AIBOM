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
            echo "📄 Displaying vulnerability report contents..."
            sh 'cat reports/vulnerability_report.json'

            def vulnReport = readJSON file: 'reports/vulnerability_report.json'
            def vulnList = vulnReport?.vulnerabilities ?: []

            if (vulnList && vulnList.size() > 0) {
                echo "⚠️ WARNING: Model not ready for production due to vulnerabilities:"
                vulnList.each { vuln ->
                    echo "-> ${vuln}"
                }
            } else {
                echo "✅ No vulnerabilities found. Model is ready for production!"
            }
        }
    }
 }
}
}
