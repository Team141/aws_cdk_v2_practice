import aws_cdk as core
import aws_cdk.assertions as assertions

from sample_app_v2.sample_app_v2_stack import SampleAppV2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sample_app_v2/sample_app_v2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SampleAppV2Stack(app, "sample-app-v2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
