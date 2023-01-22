import aws_cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
)

from constructs import Construct

class SecuirtyStack(Stack):
    def __init__(self,scope: Construct, id:str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        self.lambda_sg = ec2.SecurityGroup(self, "lambdasg",
                                      security_group_name="lambda-sg",
                                      vpc=vpc,
                                      description="SG for lambda Functions",
                                      allow_all_outbound=True,
                                      )

        self.bastion_sg = ec2.SecurityGroup(self, "bastionsg",
                                       security_group_name="bastion-sg",
                                       vpc=vpc,
                                       description="SG for Bastion host",
                                       allow_all_outbound=True,
                                       )
        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(22),"SSH Access")

        redis_sg = ec2.SecurityGroup(self, "redissg",
                                           security_group_name="redis-sg",
                                           vpc=vpc,
                                           description="SG for Redis Cluster",
                                           allow_all_outbound=True,
                                           )
        redis_sg.add_ingress_rule(self.lambda_sg, ec2.Port.tcp(6379), "Access from Lambda functions")

        lambda_role = iam.Role(self, "lambdarole",
                               assumed_by=iam.ServicePrincipal(service="lambda.amazonaws.com"),
                               role_name="lambda-role",
                               managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                   managed_policy_name="service-role/AWSLambdaVPCAccessExecutionRole"
                               )]
                               )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*']
            )
        )

        #explicit export for redis-sg using 'CfnOutput'
        aws_cdk.CfnOutput(self, "redis-export",
                          export_name="redis-sg-export",
                          value=redis_sg.security_group_id
                          )

        #SSM Parameters
        ssm.StringParameter(self,"lambdasg-param",
                            parameter_name='/'+env_name+'/lambda-sg',
                            string_value=self.lambda_sg.security_group_id
                            )

        ssm.StringParameter(self, "lambdarole-param-arn",
                            parameter_name='/'+env_name+'lambda-role-arn',
                            string_value=lambda_role.role_arn,
                            )

        ssm.StringParameter(self, "lambdarole-param-name",
                            parameter_name='/'+env_name+'lambda-role-name',
                            string_value=lambda_role.role_name
                            )
