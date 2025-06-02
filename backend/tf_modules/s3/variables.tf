variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "acl" {
  description = "Canned ACL to apply"
  type        = string
  default     = "private"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}