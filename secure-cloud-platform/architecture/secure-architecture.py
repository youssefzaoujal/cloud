from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.integration import Eventbridge, SNS
from diagrams.aws.management import Cloudtrail, Cloudwatch, Config, Organizations, SystemsManager
from diagrams.aws.network import CloudFront, ELB, Endpoint, NATGateway, Route53
from diagrams.aws.security import Guardduty, IAM, Inspector, KMS, SecretsManager, SecurityHub, Shield, WAF
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users


with Diagram(
    "Project 8 - Secure Multi-Tier Architecture",
    filename=str(Path(__file__).with_name("secure-architecture")),
    show=False,
    direction="LR",
    graph_attr={"fontsize": "20", "bgcolor": "white", "pad": "0.6", "splines": "spline", "nodesep": "0.7", "ranksep": "1.1"},
    node_attr={"fontsize": "12"},
    edge_attr={"fontsize": "11"},
):
    users = Users("Users")

    with Cluster("Edge protection"):
        dns = Route53("Route 53")
        shield = Shield("Shield Standard\nL3/L4 DDoS")
        waf = WAF("AWS WAF\nmanaged rules")
        cdn = CloudFront("CloudFront")

    with Cluster("Identity and guardrails"):
        organization = Organizations("Organizations\nSCPs")
        iam = IAM("IAM roles\nleast privilege")

    with Cluster("VPC - 2 Availability Zones"):
        with Cluster("Public subnets"):
            alb = ELB("Application\nLoad Balancer")
            nat = NATGateway("NAT Gateway")

        with Cluster("Private subnets"):
            application = EC2("EC2 Auto Scaling\nIMDSv2")
            endpoints = Endpoint("VPC endpoints\nS3 / KMS / SSM")

        with Cluster("Isolated data subnets"):
            database = RDS("RDS Multi-AZ\nSSE-KMS")

    with Cluster("Data protection"):
        kms = KMS("KMS CMKs\ndata / logs / secrets")
        secrets = SecretsManager("Secrets Manager\nrotation")
        bucket = S3("S3\nSSE-KMS and versioning")

    with Cluster("Detection and audit"):
        trail = Cloudtrail("CloudTrail\nlog integrity")
        guardduty = Guardduty("GuardDuty\nthreat detection")
        config = Config("AWS Config\ncompliance rules")
        inspector = Inspector("Inspector\nvulnerability scanning")
        security_hub = SecurityHub("Security Hub\ncentral findings")

    with Cluster("Automated response"):
        eventbridge = Eventbridge("EventBridge\nhigh severity")
        remediation = Lambda("Lambda\nremediation")
        ssm = SystemsManager("SSM Automation")
        notifications = SNS("SNS\nsecurity alerts")

    logs = Cloudwatch("CloudWatch\nlogs and flow logs")

    users >> Edge(label="HTTPS") >> dns >> shield >> waf >> cdn
    cdn >> Edge(label="origin") >> alb >> Edge(label="ALB security group") >> application
    application >> Edge(label="TLS 5432") >> database
    application >> Edge(label="static assets") >> bucket
    application >> Edge(label="private AWS API calls", style="dashed", color="darkgreen") >> endpoints
    application >> Edge(label="egress", style="dotted", color="grey") >> nat
    kms >> Edge(label="encrypts", style="dashed", color="darkgreen") >> [database, bucket, application, secrets]
    secrets >> Edge(label="runtime credentials", style="dashed", color="darkgreen") >> application
    organization >> Edge(label="guardrails", style="dashed", color="purple") >> iam >> application
    trail >> Edge(label="API events", style="dotted") >> guardduty
    logs >> Edge(label="flow and DNS logs", style="dotted") >> guardduty
    [guardduty, config, inspector] >> Edge(label="findings", color="firebrick") >> security_hub
    security_hub >> Edge(color="firebrick") >> eventbridge
    eventbridge >> Edge(color="firebrick") >> [remediation, ssm, notifications]
    remediation >> Edge(label="quarantine and revoke", style="dashed", color="firebrick") >> application
    ssm >> Edge(label="auto-remediation", style="dashed", color="firebrick") >> config
    trail >> Edge(label="encrypted audit archive") >> bucket