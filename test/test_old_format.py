from unclassifiers.config import Config
from unclassifiers.old_format import OldFormat
import json
import unittest


class TestStringMethods(unittest.TestCase):

    def test_subnet_object(self):
        test_obj = json.loads(
            "{\"version\":3,\"terraform_version\":\"0.11.11\",\"serial\":1,\"lineage\":\"11111111-1111-1111-1111-111111111111\",\"modules\":[{\"path\":[\"root\"],\"outputs\":{\"aws_subnet_infralight-0000_id\":{\"sensitive\":false,\"type\":\"string\",\"value\":\"subnet-00000000\"}},\"resources\":{\"aws_subnet.infralight-1111\":{\"type\":\"aws_subnet\",\"depends_on\":[],\"primary\":{\"id\":\"subnet-11111111\",\"attributes\":{\"arn\":\"arn:aws:ec2:us-east-1:123456789012:subnet/subnet-11111111\",\"assign_ipv6_address_on_creation\":\"false\",\"availability_zone\":\"us-east-1b\",\"availability_zone_id\":\"use1-az2\",\"cidr_block\":\"192.168.0.0/24\",\"id\":\"subnet-11111111\",\"ipv6_cidr_block\":\"\",\"ipv6_cidr_block_association_id\":\"\",\"map_public_ip_on_launch\":\"true\",\"outpost_arn\":\"\",\"owner_id\":\"123456789012\",\"tags.%\":\"0\",\"vpc_id\":\"vpc-1111111111\"},\"meta\":{\"schema_version\":1},\"tainted\":false},\"deposed\":[],\"provider\":\"provider.aws\"}},\"depends_on\":[]}]}")
        unclassifier = OldFormat(Config(["aws_subnet"]))

        actual_result = json.dumps(unclassifier.unclassify(test_obj), separators=(',', ':'))
        excpected_result = '{"version":3,"terraform_version":"0.11.11","serial":1,"lineage":"11111111-1111-1111-1111-111111111111","modules":[{"path":["root"],"outputs":{},"resources":{"aws_subnet.infralight-1111":{"type":"aws_subnet","depends_on":[],"primary":{"id":"subnet-11111111","attributes":{"arn":"arn:aws:ec2:us-east-1:123456789012:subnet/subnet-11111111","id":"subnet-11111111","owner_id":"123456789012","vpc_id":"vpc-1111111111"},"meta":{"schema_version":1},"tainted":false},"deposed":[],"provider":"provider.aws"}},"depends_on":[]}]}'

        self.assertEqual(actual_result, excpected_result)

if __name__ == '__main__':
    unittest.main()