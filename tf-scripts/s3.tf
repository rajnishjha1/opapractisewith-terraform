resource "aws_s3_bucket" "app_bucket" {

  bucket = "Terraform_agentic_ai_agent_demo098712"

  tags = {
    Name = "ai-governance-bucket"
  }
}

# Intentionally missing encryption
# AI Agent and OPA should detect this later