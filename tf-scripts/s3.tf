resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = "terraform-agentic-ai-agent-demo-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "ai-governance-bucket"
    Environment = "dev"
    Owner       = "devops"
  }
}

# Intentionally missing encryption
# AI Agent and OPA should detect this later