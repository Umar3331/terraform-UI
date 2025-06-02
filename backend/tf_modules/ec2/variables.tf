# variable "ami" {
#   description = "AMI to use for the instance"
#   type        = string
#   default     = data.aws_ami.ubuntu.id
# }

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t2.micro"
}

variable "name" {
  description = "Name of the instance"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}