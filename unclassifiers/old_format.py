from unclassifiers.base_format import BaseFormat
from unclassifiers.config import Config
from exceptions.bad_format_exception import BadFormatException

class OldFormat(BaseFormat):

    def unclassify(self, tf_state_file):
        print("Start unclassifying Terraform state in old format")

        ''' Checking if terraform state file has module '''
        if not 'modules' in tf_state_file:
            raise  BadFormatException("Could not find modules in terraform state file")

        ''' Iterating modules '''
        for module in tf_state_file["modules"]:

            ''' Removing data '''
            if "outputs" in module:
                module["outputs"] = {}

            if not "resources" in module:
                continue


            ''' Iterating all resources in module'''
            for resource_id in module["resources"]:
                resource = module["resources"][resource_id]

                if "type" in resource and resource["type"] in self.config.classified_types:
                    if "primary" in resource and "attributes" in resource["primary"]:

                        ''' Removing all field except WHITE-LIST '''
                        resource["primary"]["attributes"] = {k:v for (k,v) in resource["primary"]["attributes"].items() if k in self.legitimate_fields}
                        print("unclassified successfully. type={0}, arn={1}".format(resource["type"], resource["primary"]["attributes"]["arn"]))

        return tf_state_file


