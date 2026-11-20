pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/var/jenkins_home/deploy/flask-app'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    if [ -f "$DEPLOY_DIR/app.pid" ]; then kill $(cat "$DEPLOY_DIR/app.pid") || true; fi
                    rm -rf "$DEPLOY_DIR"
                    mkdir -p "$DEPLOY_DIR"
                    cp app.py requirements.txt "$DEPLOY_DIR/"
                    python3 -m venv "$DEPLOY_DIR/venv"
                    "$DEPLOY_DIR/venv/bin/pip" install -r "$DEPLOY_DIR/requirements.txt"
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                    cd "$DEPLOY_DIR"
                    JENKINS_NODE_COOKIE=dontKillMe nohup ./venv/bin/python app.py > app.log 2>&1 &
                    echo $! > app.pid
                    sleep 3
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if python3 -c "import urllib.request,sys; r=urllib.request.urlopen('http://localhost:5000/'); sys.exit(0 if r.status==200 and r.read().decode()=='Hello, CI/CD!' else 1)"; then
                            echo "Post-deployment test PASSED"
                            exit 0
                        fi
                        sleep 1
                    done
                    echo "Post-deployment test FAILED"
                    cat "$DEPLOY_DIR/app.log"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'PIPELINE SUCCESS: application built, tested, deployed and verified.'
        }
        failure {
            echo 'PIPELINE FAILURE: see the failed stage in the console log above.'
        }
    }
}