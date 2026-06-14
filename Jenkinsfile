pipeline {
  agent any

  environment {
    TF_DIR     = 'tf-scripts'
    POLICY_DIR = 'policy'
    PLAN_FILE  = "${TF_DIR}/plan.tfplan"
    PLAN_JSON  = "${TF_DIR}/plan.json"
  }

  options {
    ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Terraform Init') {
      steps {
        dir(env.TF_DIR) {
          sh 'terraform init -input=false'
        }
      }
    }

    stage('Terraform Format') {
      steps {
        dir(env.TF_DIR) {
          sh 'terraform fmt -check -recursive'
        }
      }
    }

    stage('Terraform Validate') {
      steps {
        dir(env.TF_DIR) {
          sh 'terraform validate'
        }
      }
    }

    stage('Terraform Plan') {
      steps {
        dir(env.TF_DIR) {
          sh 'terraform plan -out=plan.tfplan'
        }
      }
    }

    stage('Export Plan JSON') {
      steps {
        dir(env.TF_DIR) {
          sh 'terraform show -json plan.tfplan > plan.json'
        }
      }
    }

    stage('OPA Policy Check') {
      steps {
        sh '''
          if ! command -v opa >/dev/null 2>&1; then
            echo "OPA binary not found. Install OPA or add it to PATH."
            exit 1
          fi

          opa eval --input "${PLAN_JSON}" --data "${POLICY_DIR}" --format json 'data.terraform.tags.deny' > opa-results.json

          python - <<'PY'
import json, sys
try:
    payload = json.load(sys.stdin)
    results = payload.get('result', [])
    value = []
    if results:
        expressions = results[0].get('expressions', [])
        if expressions:
            value = expressions[0].get('value', [])
except Exception as exc:
    print('Failed to parse OPA output:', exc)
    sys.exit(1)

if len(value) != 0:
    print('OPA policy violations found:')
    for item in value:
        print('  -', item)
    sys.exit(1)

print('OPA policy passed.')
PY
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: "${TF_DIR}/plan.json,${TF_DIR}/opa-results.json", allowEmptyArchive: true
    }
    failure {
      echo 'Build failed. Review Terraform and OPA output for policy violations.'
    }
  }
}
