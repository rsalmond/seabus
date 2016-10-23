provider "aws" {
    region  = "us-east-1"
    profile = "seabus"
}

resource "aws_route53_record" "www" {
    zone_id     = "Z38AGVFAO0JEIN"
    name        = "seab.us"
    type        = "A"
    ttl         = "300"
    records     = ["107.161.27.162"]
}

resource "aws_route53_record" "api" {
    zone_id     = "Z38AGVFAO0JEIN"
    name        = "api.seab.us"
    type        = "A"
    ttl         = "300"
    records     = ["107.161.27.162"]
}
