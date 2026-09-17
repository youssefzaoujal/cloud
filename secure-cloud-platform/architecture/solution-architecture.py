"""
AWS Secure Cloud Platform - Target Architecture (Projects 6 + 8).

Regenerate with:
	python -m pip install diagrams
	python architecture/solution-architecture.py

Graphviz must be installed and available on PATH. The script writes
solution-architecture.png next to this file.
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.management import Cloudtrail, Cloudwatch, Config
from diagrams.aws.network import (
	ALB,
	CloudFront,
	CloudMap,
	InternetGateway,
	NATGateway,
	Route53,
)
from diagrams.aws.security import (
	Guardduty,
	IAM,
	KMS,
	SecretsManager,
	SecurityHub,
	WAF,
)
from diagrams.onprem.client import Users


GRAPH_ATTR = {
	"splines": "spline",
	"nodesep": "0.55",
	"ranksep": "0.95",
	"fontsize": "16",
	"pad": "0.4",
	"compound": "true",
}

DASHED = {"style": "dashed", "color": "darkgreen"}


with Diagram(
	"AWS Secure Cloud Platform - Target Architecture (Projects 6 + 8)",
	filename=str(Path(__file__).with_name("solution-architecture")),
	show=False,
	direction="LR",
	graph_attr=GRAPH_ATTR,
):
	users = Users("Internet users")

	with Cluster("Edge layer (global)"):
		dns = Route53("Route 53\nalias + health checks")
		cdn = CloudFront("CloudFront\nTLS 1.2+ / ACM cert")
		waf = WAF("AWS WAF\nOWASP + rate limiting")

	with Cluster("VPC 10.0.0.0/16 - eu-west-1 - 2 Availability Zones"):
		igw = InternetGateway("Internet Gateway")

		with Cluster("Public subnets (AZ-a / AZ-b)"):
			alb = ALB("Application Load Balancer\nHTTP demo / HTTPS target")
			nat = NATGateway("NAT Gateway\n(1 per AZ)")

		with Cluster("Private app subnets (AZ-a / AZ-b)"):
			with Cluster("ECS Fargate cluster"):
				auth = ECS("auth-service")
				orders = ECS("orders-service")
				notifications = ECS("notifications-service")
			cloud_map = CloudMap("Cloud Map\nprivate DNS discovery")

		with Cluster("Private data subnets (AZ-a / AZ-b)"):
			postgres = RDS("RDS PostgreSQL\nMulti-AZ, SSE-KMS")
			redis = ElastiCache("ElastiCache Redis\nsessions, encrypted")

	with Cluster("Build and artifacts"):
		ecr = ECR("Amazon ECR\nscan on push")

	with Cluster("Data protection and identity"):
		kms = KMS("KMS CMKs")
		secrets = SecretsManager("Secrets Manager\nauto rotation")
		iam = IAM("IAM task roles\nleast privilege")

	with Cluster("Detection, audit and observability"):
		logs = Cloudwatch("CloudWatch\nlogs, metrics, alarms")
		audit = Cloudtrail("CloudTrail\nlog file validation")
		config = Config("AWS Config\ncompliance rules")
		detection = Guardduty("GuardDuty\nthreat detection")
		security_hub = SecurityHub("Security Hub\ncentral findings")

	users >> Edge(label="HTTPS") >> dns >> cdn
	cdn >> Edge(label="inspected by", style="dotted") >> waf
	cdn >> Edge(label="origin HTTPS") >> igw >> alb
	alb >> Edge(label="/auth/*") >> auth
	alb >> Edge(label="/orders/*") >> orders
	alb >> Edge(label="/notifications/*") >> notifications

	orders >> Edge(label="resolve", style="dotted") >> cloud_map
	cloud_map >> Edge(style="dotted") >> notifications
	auth >> Edge(label="TLS 5432") >> postgres
	orders >> Edge(label="TLS 5432") >> postgres
	notifications >> Edge(label="TLS 5432") >> postgres
	orders >> Edge(label="sessions") >> redis

	orders >> Edge(label="egress", style="dashed") >> nat >> igw

	ecr >> Edge(label="image pull", **DASHED) >> auth
	secrets >> Edge(label="runtime credentials", **DASHED) >> orders
	kms >> Edge(label="encrypts", **DASHED) >> secrets
	kms >> Edge(label="encrypts", **DASHED) >> postgres
	iam >> Edge(label="assumed by", **DASHED) >> notifications

	notifications >> Edge(label="app logs", **DASHED) >> logs
	audit >> Edge(label="API events", style="dotted") >> detection
	detection >> Edge(label="findings") >> security_hub
	config >> Edge(label="findings") >> security_hub
	logs >> Edge(label="alarms", style="dotted") >> security_hub
