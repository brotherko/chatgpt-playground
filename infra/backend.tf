terraform {
  backend "remote" {
    organization = "brotherko"

    workspaces {
      name = "gptpg-prod"
    }
  }
}
