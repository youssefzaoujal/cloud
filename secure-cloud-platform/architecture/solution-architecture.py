from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.management import Cloudwatch, Cloudtrail
from diagrams.aws.network import ALB, CloudFront, CloudMap, Route53
from diagrams.aws.security import Guardduty, KMS, SecretsManager, SecurityHub, WAF
from diagrams.onprem.client import Users


with Diagram(
	"AWS Secure Cloud Platform - Target Architecture",
	filename=str(Path(__file__).with_name("solution-architecture")),
	show=False,
	direction="LR",
	graph_attr={"splines": "ortho", "nodesep": "0.65", "ranksep": "1.0"},
):
	users = Users("Internet users")
	dns = Route53("Route 53")
	edge = CloudFront("CloudFront")
	waf = WAF("AWS WAF")
	alb = ALB("Application Load Balancer")

	with Cluster("AWS VPC"):
		with Cluster("Private subnets"):
			with Cluster("ECS Fargate services"):
				auth = ECS("auth-service")
				orders = ECS("orders-service")
				notifications = ECS("notifications-service")
				cloud_map = CloudMap("Cloud Map\nservice discovery")

			postgres = RDS("RDS PostgreSQL")
			redis = ElastiCache("ElastiCache Redis")


	secrets = SecretsManager("Secrets Manager")
	kms = KMS("KMS")
	logs = Cloudwatch("CloudWatch Logs")
	audit = Cloudtrail("CloudTrail")
	detection = Guardduty("GuardDuty")
	security_hub = SecurityHub("Security Hub")

	users >> Edge(label="DNS") >> dns >> edge >> Edge(label="HTTPS") >> waf >> alb
	alb >> Edge(label="HTTP") >> [auth, orders, notifications]
	orders >> Edge(label="service call") >> cloud_map >> notifications
	auth >> Edge(label="SQL") >> postgres
	orders >> Edge(label="SQL") >> postgres
	orders >> Edge(label="cache") >> redis
	notifications >> Edge(label="SQL") >> postgres

	secrets >> Edge(style="dashed", label="credentials") >> [auth, orders, notifications]
	kms >> Edge(style="dashed", label="encryption") >> [secrets, postgres, redis]
	[auth, orders, notifications] >> Edge(style="dashed", label="application logs") >> logs
	audit >> Edge(style="dashed", label="audit events") >> security_hub
	detection >> Edge(style="dashed", label="findings") >> security_hub
