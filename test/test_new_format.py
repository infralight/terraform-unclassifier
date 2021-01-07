from unclassifiers.config import Config
from unclassifiers.new_format import NewFormat
import json
import unittest


class TestStringMethods(unittest.TestCase):

    def test_new_state(self):
        with open('terraform14.tfstate', 'r') as tfstate:
            data =json.load(tfstate)

        unclassifier = NewFormat(Config(["aws_subnet"]))
        actual_result = json.dumps(unclassifier.unclassify(data), separators=(',', ':'))

        expected_result = "{\"version\":4,\"terraform_version\":\"0.14.0\",\"serial\":658,\"lineage\":\"a71712f3-a87b-fde1-76fa-a7a956ab0d33\",\"outputs\":{},\"resources\":[{\"module\":\"module.backend\",\"mode\":\"data\",\"type\":\"aws_ami\",\"name\":\"ubuntu\",\"provider\":\"provider[\\\"registry.terraform.io/hashicorp/aws\\\"]\",\"instances\":[]},{\"module\":\"module.infra\",\"mode\":\"managed\",\"type\":\"aws_subnet\",\"name\":\"subnet2\",\"provider\":\"provider[\\\"registry.terraform.io/hashicorp/aws\\\"]\",\"instances\":[{\"schema_version\":1,\"attributes\":{\"arn\":\"arn:aws:ec2:us-west-2:123456789012:subnet/subnet-11111111\",\"id\":\"subnet-11111111\",\"owner_id\":\"123456789012\",\"vpc_id\":\"vpc-22222222\"},\"sensitive_attributes\":[],\"private\":\"bnVsbA==\",\"dependencies\":[\"module.infra.aws_vpc.main\"]}]}]}"
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()