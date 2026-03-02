/*
 * Jenkinsfile - Declarative Pipeline for Selenium Test Automation (Step 7)
 * ========================================================================
 * Case Study Requirement: "Integrate Selenium tests with continuous
 * integration tools like Jenkins for seamless test automation."
 *
 * This pipeline:
 * 1. Checks out the source code from SCM
 * 2. Sets up a Python virtual environment
 * 3. Installs all dependencies from requirements.txt
 * 4. Runs the Pytest suite with HTML report generation
 * 5. Archives test reports for viewing in the Jenkins dashboard
 */

pipeline {
    agent any

    environment {
        // Python virtual environment directory
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {

        // ---------------------------------------------------------------
        // STAGE 1: CHECKOUT — Pull latest code from SCM
        // ---------------------------------------------------------------
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from source control...'
                checkout scm
            }
        }

        // ---------------------------------------------------------------
        // STAGE 2: SETUP ENVIRONMENT — Create venv & install dependencies
        // ---------------------------------------------------------------
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // ---------------------------------------------------------------
        // STAGE 3: RUN TESTS — Execute the Pytest suite
        // ---------------------------------------------------------------
        stage('Run Tests') {
            steps {
                echo 'Executing Selenium test suite with Pytest...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest tests/ \
                        --html=reports/report.html \
                        --self-contained-html \
                        -v \
                        --tb=short \
                        --junitxml=reports/junit-results.xml
                '''
            }
        }
    }

    // -------------------------------------------------------------------
    // POST-ACTIONS: Archive reports & notify on build status
    // -------------------------------------------------------------------
    post {
        always {
            echo 'Archiving test reports...'

            // Archive the pytest-html report for viewing in Jenkins
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Selenium Test Report'
            ])

            // Archive JUnit XML results for Jenkins test trend tracking
            junit allowEmptyResults: true, testResults: 'reports/junit-results.xml'

            // Archive screenshots captured on failure
            archiveArtifacts artifacts: 'reports/screenshots/**/*.png', allowEmptyArchive: true
        }

        success {
            echo ' All Selenium tests passed successfully!'
        }

        failure {
            echo ' Some tests failed. Check the Selenium Test Report for details.'
        }

        cleanup {
            // Clean up the virtual environment
            sh 'rm -rf ${VENV_DIR}'
        }
    }
}
