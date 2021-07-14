provider "aws" {
  region                  = "sa-east-1" // 남아메리카 상파울로
  shared_credentials_file = local.aws_credentials_path
  profile                 = local.aws_profile

  default_tags {
    tags = {
      Phase     = "Test"
      Owner     = "Donghyung Ko"
      Workspace = "BlueWhale/onboarding-projects/project-B"
    }
  }
}