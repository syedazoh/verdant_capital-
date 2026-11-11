pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python -m pip install -r requirements.txt'
                sh 'python -m pytest -q'
                sh 'python -m compileall -q agents challenge data orchestrator app.py'
            }
        }
    }
}
