resource "aws_s3_bucket" "app_bucket" {

  bucket = "replace-with-unique-bucket-name"

  tags = {
    Name = "ai-governance-bucket"
  }
}

# Intentionally missing encryption
# AI Agent and OPA should detect this later