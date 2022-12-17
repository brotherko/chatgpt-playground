resource "digitalocean_app" "this" {
  count = var.enabled ? 1 : 0

  spec {
    name   = "gptpg"
    region = "sgp"

    service {
      name               = "server"
      instance_count     = 1
      instance_size_slug = "basic-xxs"
      source_dir         = "/server"
      dockerfile_path    = "/server/Dockerfile"

      http_port = 80

      github {
        repo   = "brotherko/chatgpt-playground"
        branch = "main"
      }

      routes {
        path = "/api"
      }

      env {
        key   = "OPENAI_EMAIL"
        value = var.openai_email
        type  = "SECRET"
      }

      env {
        key   = "OPENAI_PASSWORD"
        value = var.openai_password
        type  = "SECRET"
      }

      #health_check {
      #  http_path             = "/health"
      #  initial_delay_seconds = 60
      #  period_seconds        = 3600
      #  timeout_seconds       = 60
      #  failure_threshold     = 1
      #}
    }

    static_site {
      name          = "client"
      build_command = "npm run build"
      output_dir    = "build"
      source_dir    = "/client"

      github {
        branch = "main"
        repo   = "brotherko/chatgpt-playground"
      }

      routes {
        path = "/"
      }
    }
  }
}

resource "digitalocean_project" "this" {
  name        = "gptpg"
  description = "ChatGPT Playground"
  purpose     = "Web Application"
  environment = "Production"
}

resource "digitalocean_project_resources" "this" {
  count = var.enabled ? 1 : 0

  project = digitalocean_project.this.id
  resources = [
    digitalocean_app.this[0].urn
  ]
}
