resource "aws_s3_bucket" "app_bucket" {

  bucket = "rajnishaipractisetest2345671"

  tags = {
    Name = "ai-governance-bucket"
  }
}

# Intentionally missing encryption
# AI Agent and OPA should detect this later