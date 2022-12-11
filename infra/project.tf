resource "digitalocean_project" "this" {
  name        = "gptpg"
  description = "ChatGPT Playground"
  purpose     = "Web Application"
  environment = "Production"
}

resource "digitalocean_project_resources" "this" {
  project = digitalocean_project.this.id
  resources = [
    digitalocean_app.this.urn
  ]
}
