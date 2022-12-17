variable "enabled" {
  type    = bool
  default = true
}

variable "openai_email" {
  type      = string
  sensitive = true
}

variable "openai_password" {
  type      = string
  sensitive = true
}
