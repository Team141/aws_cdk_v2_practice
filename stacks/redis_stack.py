from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_elasticache as redis,
)
from constructs import Construct

class RedisStack(Stack):
    def __init__(self, scope: Construct, id:str, vpc, redissg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        #low level api calls using 'Cfnxxxxx' properties
        subnet_group = redis.CfnSubnetGroup(self, 'redis-subnet-group',
                                            subnet_ids=subnets,
                                            description="subnet group for redis"
                                            )

        redis_cluster = redis.CfnCacheCluster(self, 'redis',
                                              cache_node_type='cache.t2.small',
                                              engine='redis',
                                              num_cache_nodes=1,
                                              cluster_name=prj_name+'-redis-'+env_name,
                                              cache_subnet_group_name=subnet_group.ref, #exciplit referenced to sunbnets_group using 'Ref'
                                              vpc_security_group_ids=[redissg],
                                              auto_minor_version_upgrade=True
                                              )
        redis_cluster.add_depends_on(subnet_group) # exciplit depends on subnet_group

        #SSM parameters
        ssm.StringParameter(self, 'redis-endpoint',
                            string_value=redis_cluster.attr_redis_endpoint_address,
                            parameter_name='/'+env_name+'/redis-endpoint'
                            )
        ssm.StringParameter(self, 'redis-port',
                            string_value=redis_cluster.attr_redis_endpoint_port,
                            parameter_name='/'+env_name+'/redis-port'
                            )