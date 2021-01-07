
[![N|Solid](logo.svg)](https://infralight.co)

# Teraform Unclassifier is an automatic solution for hiding classified data from state files

### Deploy Terraform Unclassifier to your AWS account
![N|Solid](architecture.png)]<br />
Unclassifier is now supported in N.Virginia (us-east-1), if you have any question, you can contact [Sefi Genis](mailto://sefi@infralight.co).

Follow these steps:
1.  Click
    [<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=infralight-terraform-unclassifier&templateURL=https://infralight-templates-public.s3.amazonaws.com/unclassifier/template.yml).
2.  In the **Select Template**, click **Next** (no need to make a
    selection)
3.  In the **Parameters** section input your existing S3 Bucket with .tfstate files, *InputS3Bucket*, then click **Next**
4.  In the **Options** page, click **Next** (no need to make any
    selections)
5.  In the **Review** page, select the options:
`I acknowledge that AWS CloudFormation might create IAM resources with custom names.`
6.  Click **Create Stack**

### Arguments
You can control terraform-unclassifier with these parameters:

| Parameter | Description | Optional/Mandatory |
| ------ | ------ | ----- |
| INPUT_BUCKET | Existing S3 Bucket contains sensitive terraform files | Mandatory |
| OUTPUT_BUCKET | terraform-unclassifier save unclassified state to this bucket | Mandatory |
| CLASSIFIED_TYPES | terraform resources to unclassify (multi resources split by , )<br />Default value is aws_acm_certificate | Optional |
| OUTPUT_DELIMITER | Controlling the output delimiter in Output S3 Bucket | Optional |
| TERRAFORM_STATE_SUFFIX | Controlling terraform state files sufix<br />Default value is .tfstate | Optional |
| INFRALIGHT_STATE_PATH | terraform-unclassifier saves internal state file<br />Default value is unclassifier.infl | Optional |
| HARD_REFRESH | unclassifing all .tfstate files no matter if they already unclassified<br />Default value is false | Optional |


## Supported Terraform Versions
- 0.11.X
- 0.12.X
- 0.13.X
- 0.14.X

License
----
Apache 2.0