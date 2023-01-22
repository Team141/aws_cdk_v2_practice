import aws_cdk
from aws_cdk import (
    Aws,
    Stack,
    aws_s3 as s3,
    aws_ssm as ssm,
)
from constructs import Construct


class S3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        account_id = Aws.ACCOUNT_ID

        lambda_bucket = s3.Bucket(self, 'lambda-s3-bucket',
                                  bucket_name=account_id+'-'+env_name+'-lambda-deploy-packages',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  removal_policy=aws_cdk.RemovalPolicy.RETAIN,
                                  )

        #SSM Parameter
        ssm.StringParameter(self, 'ssm-lambda-bucket',
                            string_value=lambda_bucket.bucket_name,
                            parameter_name='/'+env_name+'/lambda-s3-bucket'
                            )

        # To Store Build Artifacts

        artifacts_bucket = s3.Bucket(self, 'build-artifacts',
                                  bucket_name=account_id + '-' + env_name + '-build-artifacts',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                                  )

        aws_cdk.CfnOutput(self, 's3-build-artifacts-export',
                          value=artifacts_bucket.bucket_name,
                          export_name='build-artifacts-bucket'
                          )

        # To Store Frontend App
        frontend_bucket = s3.Bucket(self, 'frontend',
                                     bucket_name=account_id + '-' + env_name + '-frontend',
                                     access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                     block_public_access=s3.BlockPublicAccess(
                                         block_public_acls=True,
                                         block_public_policy=True,
                                         ignore_public_acls=True,
                                         restrict_public_buckets=True
                                     ),
                                     encryption=s3.BucketEncryption.S3_MANAGED,
                                     removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                                     )

        aws_cdk.CfnOutput(self, 's3-frontend-export',
                          value=frontend_bucket.bucket_name,
                          export_name='frontend-bucket'
                          )