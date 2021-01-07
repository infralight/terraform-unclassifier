import boto3
import os
import json
from botocore.exceptions import ClientError


class S3Connector:

    def __init__(self, access_key_id="", secret_access_key="", session_token=""):

        if access_key_id == "":
            access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")

        if secret_access_key == "":
            secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        if session_token == "":
            session_token = os.environ.get("AWS_SESSION_TOKEN")

        if os.environ.get("AWS_DEFAULT_REGION") != None:
            region = os.environ.get("AWS_DEFAULT_REGION")
        else:
            region = "aws-global"

        self.client = boto3.client('s3',
                                   aws_access_key_id=access_key_id,
                                   aws_secret_access_key=secret_access_key,
                                   aws_session_token=session_token)
        self.region = region

    def get_all_s3_keys(self, bucket: str, suffix: str = None):
        """Get a list of all keys in an S3 bucket."""
        keys = []

        kwargs = {'Bucket': bucket}
        while True:
            resp = self.client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:

                keys.append({'Key': obj['Key'],
                             'LastModified': obj['LastModified'].timestamp(),
                             'Size': obj['Size']})

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

        if suffix == None:
            return keys

        return  [k for k in keys if k["Key"].endswith(suffix) and k["Size"] > 0]

    def get_json_object_or_default(self, bucket: str, key: str, default_value):
        """ Downloading object from S3 """
        try:
            obj = self.client.get_object(Bucket=bucket, Key=key)

            if obj['ContentLength'] == 0:
                return default_value

        except ClientError as ex:
            ''' File does not exist '''
            if ex.response['Error']['Code'] == "NoSuchKey":
                return default_value

        """ Parsing as JSON """
        try:
            text_format = obj['Body'].read().decode('utf-8')
            json_format = json.loads(text_format)
            return json_format
        except Exception as ex:
            print("File is in bad format. error={0}".format(ex))
            return default_value


    def put_object(self, bucket: str, key, body):
        self.client.put_object(Bucket=bucket, Key=key, Body=body)