terraform {
  backend "s3" {
    bucket         = "bmi-health-check-tfstate-319029038820"
    key            = "bmi-health-check/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "bmi-health-check-tf-locks"
    encrypt        = true
  }
}
