import aws_cdk
from aws_cdk import (
    aws_cloudfront as cdn,
    Stack,
    aws_s3 as s3,
    aws_ssm as ssm,
)
from constructs import Construct


class CDNStack(Stack):

    def __init__(self, scope: Construct, id: str, s3bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        bucketName = s3.Bucket.from_bucket_name(self, 's3bucket',s3bucket)

        cdn_id = cdn.CloudFrontWebDistribution(
            self, 'webhosting-cdn',
            origin_configs=[cdn.SourceConfiguration(
                behaviors=[
                    cdn.Behavior(is_default_behavior=True)
                ],
                s3_origin_source=cdn.S3OriginConfig(
                    s3_bucket_source=bucketName,
                    origin_path="/build",
                    origin_access_identity=cdn.OriginAccessIdentity(
                        self, 'webhosting-origin'
                    )
                )
            )],
            error_configurations=[
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=400,
                    response_code=200,
                    response_page_path="/",
                ),
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=403,
                    response_code=200,
                    response_page_path='/',
                ),
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=200,
                    response_page_path="/",
                )
            ]

        )

        #SSM Parameters
        ssm.StringParameter(self, "cdn-dist-id",
                            parameter_name='/'+env_name+'/app-distribution-id',
                            string_value=cdn_id.distribution_id
                            )

        ssm.StringParameter(self, "cdn-url",
                            parameter_name='/' + env_name + '/app-cdn-url',
                            string_value='https://'+cdn_id.distribution_domain_name
                            )