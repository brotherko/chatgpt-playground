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

      routes {
        path = "/api"
      }

      github {
        repo_clone_url = "brotherko/chatgpt-playground"
        branch         = "main"
      }
    }

    static_site {
      name          = "client"
      build_command = "npm run build"
      output_dir    = "build"

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