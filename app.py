#!/usr/bin/env python3

import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecuirtyStack
from  stacks.bastion_stack import BastionStack
from stacks.kms_stack import KMSStack
from stacks.s3_stack import S3Stack
from stacks.rds_stack import RDSStack
from stacks.redis_stack import RedisStack
from stacks.cognito_stack import CogintoStack
from stacks.apigw_stack import APIStack
from stacks.lambda_stack import LambdaStack
from stacks.codepipeline_backned import CodePipelineBackendStack
from stacks.notifications import NotificationStack
from stacks.cdn_stack import CDNStack
from stacks.codepipeline_frontend import CodePipelineFrontendStack

app = cdk.App()

vpc_stack=VPCStack(app,"vpc")
security_stack=SecuirtyStack(app,"security-stack",vpc=vpc_stack.vpc)
bastion_stack=BastionStack(app,"bastion",vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack=KMSStack(app,"kms")
s3_stack=S3Stack(app, "s3buckets")
rds_stack=RDSStack(app, "rds", vpc=vpc_stack.vpc, lambdasg=security_stack.lambda_sg, bastionsg=security_stack.bastion_sg,
                   kmskey=kms_stack.kms_rds)
redis_stack=RedisStack(app, 'redis', vpc=vpc_stack.vpc, redissg=cdk.Fn.import_value('redis-sg-export')) #explicit import redis using 'Fn' class
cognito_stack=CogintoStack(app, 'cognito')
api_stack=APIStack(app, 'apigw')
lambdastack=LambdaStack(app, 'lambda')
cp_backend=CodePipelineBackendStack(app, 'cp-backend', artifactbucket=cdk.Fn.import_value('build-artifacts-bucket'))
notification=NotificationStack(app, 'notification')

cdn_stack=CDNStack(app,'cdn',s3bucket=cdk.Fn.import_value('frontend-bucket'))
cp_frontend=CodePipelineFrontendStack(app, 'cp-frontend', webhostingbucket=cdk.Fn.import_value('frontend-bucket'))

app.synth()
