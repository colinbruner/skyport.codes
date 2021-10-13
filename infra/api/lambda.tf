data "archive_file" "app" {
  type             = "zip"
  source_file      = "${path.module}/../../src/app/app.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/files/app.zip"
}


resource "aws_lambda_function" "api" {
  function_name = "iata_api"
  role          = aws_iam_role.lambda.arn
  handler       = "app.handle"

  filename         = data.archive_file.app.output_path
  source_code_hash = data.archive_file.app.output_base64sha256

  runtime = "python3.9"
}
