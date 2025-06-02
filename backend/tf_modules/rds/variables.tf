variable "db_name" {
  description = "The name of the DB instance"
  type        = string
}

variable "engine" {
  description = "The database engine to use"
  type        = string
  default     = "mysql"
}

variable "instance_class" {
  description = "The instance type of the RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "storage" {
  description = "Allocated storage in GBs"
  type        = number
  default     = 20
}

variable "username" {
  description = "Master DB username"
  type        = string
}

variable "password" {
  description = "Master DB password"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}