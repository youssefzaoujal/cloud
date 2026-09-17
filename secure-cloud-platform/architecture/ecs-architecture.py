from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, Fargate
from diagrams.aws.database import Elasticache, RDS
from diagrams.aws.devtools import Codebuild, Codedeploy, Codepipeline, XRay
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import CloudMap, ELB, NATGateway, Route53
from diagrams.aws.security import SecretsManager, WAF
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github


with Diagram(
    "Project 6 - ECS Fargate Microservices with Service Discovery",
    filename="ecs-architecture",
    show=False,
    direction="LR",
    graph_attr={"fontsize": "20", "bgcolor": "white", "pad": "0.6", "splines": "spline", "nodesep": "0.7", "ranksep": "1.0"},
    node_attr={"fontsize": "12"},
    edge_attr={"fontsize": "11"},
):
    users = Users("Clients")
    dns = Route53("Route 53\nalias record")
    waf = WAF("AWS WAF\nOWASP + rate limit")

    with Cluster("CI/CD Pipeline"):
        source = Github("GitHub\nsource")
        pipeline = Codepipeline("CodePipeline")
        build = Codebuild("CodeBuild\nDocker build")
        registry = ECR("Amazon ECR\nscan on push")
        deploy = Codedeploy("CodeDeploy\nblue / green")
        source >> pipeline >> build >> registry
        pipeline >> deploy

    with Cluster("VPC - 2 Availability Zones"):
        with Cluster("Public subnets"):
            alb = ELB("Application\nLoad Balancer")
            nat = NATGateway("NAT Gateway")

        with Cluster("Private subnets - ECS Fargate"):
            cloudmap = CloudMap("Cloud Map\ninternal service discovery")
            with Cluster("Microservices"):
                auth = Fargate("Auth service")
                orders = Fargate("Orders service")
                notifications = Fargate("Notifications service")

        with Cluster("Isolated data subnets"):
            cache = Elasticache("ElastiCache Redis\nsessions")
            database = RDS("RDS PostgreSQL\nMulti-AZ")

    secrets = SecretsManager("Secrets Manager\nauto rotation")
    topic = SNS("SNS\norder-events")

    with Cluster("Observability"):
        xray = XRay("AWS X-Ray\nservice map")
        cloudwatch = Cloudwatch("CloudWatch\nlogs and alarms")

    users >> Edge(label="HTTPS") >> dns >> waf >> alb
    alb >> Edge(label="path-based routing") >> [auth, orders, notifications]
    orders >> Edge(label="private DNS", style="dashed") >> cloudmap >> auth
    auth >> Edge(label="sessions") >> cache
    orders >> cache
    auth >> Edge(label="TLS 5432") >> database
    orders >> database
    orders >> Edge(label="publish event", style="dotted") >> topic >> notifications
    secrets >> Edge(label="runtime injection", color="darkgreen") >> [auth, orders, notifications]
    notifications >> Edge(label="egress", style="dotted", color="grey") >> nat
    registry >> Edge(label="image pull", color="darkorange") >> [auth, orders, notifications]
    deploy >> Edge(label="shift traffic", color="darkorange") >> alb
    for service in [auth, orders, notifications]:
        service >> Edge(style="dotted", color="grey") >> xray
        service >> Edge(style="dotted", color="grey") >> cloudwatch
    cloudwatch >> Edge(label="alarm -> rollback", color="red", style="dashed") >> deploy