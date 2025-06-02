resource "aws_db_instance" "db" {
  identifier           = var.db_name
  engine               = var.engine
  instance_class       = var.instance_class
  allocated_storage    = var.storage
  username             = var.username
  password             = var.password
  skip_final_snapshot  = true
}