resource "digitalocean_app" "this" {
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

      routes {
        path = "/api"
      }

      github {
        repo   = "brotherko/chatgpt-playground"
        branch = "main"
      }
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

    database {
      name    = "db"
      engine  = "PG"
      db_name = "db"
      db_user = "user"
    }
  }
}
