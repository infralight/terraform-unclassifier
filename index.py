import json
import os

from exceptions.missing_argument_exception import MissingArgumentException
from connectors.s3_connector import S3Connector
from exceptions.not_supported_exception import NotSupportedException
from unclassifiers.new_format import NewFormat
from unclassifiers.old_format import OldFormat
from utils.terraform_version import TerraformVersion
from unclassifiers.config import Config

s3_client = S3Connector()

def lambda_handler(event, context):

    if get_env_or_default("INPUT_BUCKET", "") == "":
        raise MissingArgumentException("INPUT_BUCKET is a mandatory argument")

    if get_env_or_default("OUTPUT_BUCKET", "") == "":
        raise MissingArgumentException("OUTPUT_BUCKET is a mandatory argument")

    INPUT_BUCKET = get_env_or_default("INPUT_BUCKET", None)
    OUTPUT_BUCKET = get_env_or_default("OUTPUT_BUCKET", None)
    OUTPUT_DELIMITER = get_env_or_default("OUTPUT_DELIMITER", "output")
    CLASSIFIED_TYPES = [k.strip() for k in get_env_or_default("CLASSIFIED_TYPES", "aws_acm_certificate").split(",")]
    TERRAFORM_STATE_FILE_SUFFIX =  get_env_or_default("TERRAFORM_STATE_SUFFIX", ".tfstate")
    INFRALIGHT_OUTPUT_STATE_PATH = get_env_or_default("INFRALIGHT_STATE_PATH", "unclassifier.infl")
    HARD_REFRESH =  get_env_or_default("HARD_REFRESH", False)

    ''' .tfstate files in S3 Bucket '''
    input_keys = s3_client.get_all_s3_keys(INPUT_BUCKET, TERRAFORM_STATE_FILE_SUFFIX)

    ''' InfraLight unclassifier latest state '''
    current_state_input_keys = s3_client.get_json_object_or_default(OUTPUT_BUCKET, INFRALIGHT_OUTPUT_STATE_PATH, [])

    ''' state files to classify '''
    if bool(HARD_REFRESH):
        diff_keys = current_state_input_keys
    else:
        diff_keys = [k for k in input_keys if k not in current_state_input_keys]
    if len(diff_keys) == 0:
        return "No Diff"

    for key in diff_keys:
        try:
            ''' Unclassifying state file'''
            unclassified_state = handle_terraform_state(key['Key'], Config(classified_types=CLASSIFIED_TYPES))
            ''' Saving unclassified state in OUTPUT s3 bucket '''
            output_key = os.path.join(OUTPUT_DELIMITER, os.path.splitext(key["Key"])[0] + "_unclassified.tfstate")
            s3_client.put_object(OUTPUT_BUCKET, output_key, json.dumps(unclassified_state))
            ''' Updating InfraLight unclassifier state '''
            current_state_input_keys.append(key)
        except Exception as ex:
            print("An error occurred while trying to unclassify terraform state. error={0}".format(ex))

    ''' Saving InfraLight unclassifier state file '''
    s3_client.put_object(OUTPUT_BUCKET, INFRALIGHT_OUTPUT_STATE_PATH, json.dumps(input_keys))

    return "Done"

def handle_terraform_state(s3_key: str, config: Config):
    tf_state = s3_client.get_json_object_or_default(get_env_or_default("INPUT_BUCKET", None), s3_key, None)
    unclassifier = None

    version = TerraformVersion.parse(tf_state['terraform_version'])

    if version.greaterThanEqual("0.12") or "resources" in tf_state:
        unclassifier = NewFormat(config)
    elif version.greaterThanEqual("0.11.0") or "modules" in tf_state:
        unclassifier = OldFormat(config)
    else:
        raise NotSupportedException("Terraform version is not supported")

    return unclassifier.unclassify(tf_state)


def get_env_or_default(key: str, default_value):
    return default_value if os.environ.get(key) is None else os.environ.get(key)

if __name__ == '__main__':
    os.environ["INPUT_BUCKET"] = "silverfort-mvp"
    os.environ["OUTPUT_BUCKET"] = "infralight-tests"
    lambda_handler({}, None)