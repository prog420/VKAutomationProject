def python_env = "python3.10"
def docker_compose_path = "/home/dmitry/Desktop/PythonProjects/VKAutomationProject/app/docker-compose.yml"
def tests_path = "/home/dmitry/Desktop/PythonProjects/VKAutomationProject/tests"
def requirements_path = "/home/dmitry/Desktop/PythonProjects/VKAutomationProject/requirements.txt"

def pytest_processes = 3 //number of processes in parallel for pytest-xdist 
def pytest_mark = "API"

pipeline {
    agent any

    stages {
        stage("Build") {
            steps {
                echo("Building...")
                sh "docker compose -f ${docker_compose_path} build"
            }
        }
        stage("Docker-Compose Up") {
            steps {
                echo "Starting containers..."
                sh "docker compose -f ${docker_compose_path} up -d"
            }
        }
        stage("Tests") {
            steps {
                echo "Starting tests..."
                script {
                    withPythonEnv(python_env) {
                        sh "rm -rf ${WORKSPACE}/allure-results"
                        sh "pip install -r ${requirements_path} --quiet"
                        sh "pytest -n ${pytest_processes} -s ${tests_path} --selenoid "
                        + "--alluredir=${WORKSPACE}/allure-results --log_dir=${WORKSPACE}/allure-results"
                    }
                }
            }
        }
    }

    post { 
        always { 
            echo "Docker-Compose Down"
            sh "docker compose -f ${docker_compose_path} down"

            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: "${WORKSPACE}/allure-results"]]
    	   ])
        }
    }
}