from exceptions.bad_format_exception import BadFormatException
from unclassifiers.base_format import BaseFormat
from unclassifiers.config import Config

class NewFormat(BaseFormat):

    def unclassify(self, tf_state_file):
        print("Start unclassifying Terraform state in new format")

        ''' Checking if terraform state file has module '''
        if not 'resources' in tf_state_file:
            raise  BadFormatException("Could not find modules in terraform state file")

        ''' Iterating modules '''
        for resource in tf_state_file["resources"]:

            ''' Removing Data'''
            if "mode" in resource and resource["mode"] == "data":
                resource["instances"] = []

            if "type" in resource and resource["type"] in self.config.classified_types:
                ''' iterating instances '''
                for instance in resource["instances"]:
                    ''' means nothing '''
                    instance["private"] = "bnVsbA=="

                    ''' Removing all field except WHITE-LIST '''
                    instance["attributes"] = {k: v for (k, v) in instance["attributes"].items() if
                                                         k in self.legitimate_fields}
                    print("unclassified successfully. type={0}, arn={1}".format(resource["type"],
                                                                                instance["attributes"]["arn"]))

        return tf_state_file


