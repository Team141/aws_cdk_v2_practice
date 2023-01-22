import aws_cdk
from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_ssm as ssm,
)

from constructs import Construct

class LambdaStack(Stack):
    def __init__(self,scope: Construct, id:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        lambda_function = _lambda.Function(self, 'helloworldfunction',
                                           runtime=_lambda.Runtime.PYTHON_3_8,
                                           code=_lambda.Code.from_asset("lambda"),
                                           handler='hello.handler'
                                           )
        api_gateway = apigw.LambdaRestApi(self, 'helloworld',
                                          handler=lambda_function,
                                          rest_api_name="mylambdaapi"
                                          )