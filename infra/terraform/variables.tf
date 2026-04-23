variable "project_name" {
  type    = string
  default = "beacon"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "root_domain_name" {
  type = string
}

variable "frontend_subdomain" {
  type    = string
  default = "beacon"
}

variable "api_subdomain" {
  type    = string
  default = "api.beacon"
}

variable "vpc_cidr" {
  type    = string
  default = "10.42.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.42.0.0/24", "10.42.1.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.42.10.0/24", "10.42.11.0/24"]
}

variable "api_image_tag" {
  type    = string
  default = "latest"
}

variable "api_container_cpu" {
  type    = number
  default = 512
}

variable "api_container_memory" {
  type    = number
  default = 1024
}

variable "api_desired_count" {
  type    = number
  default = 1
}
