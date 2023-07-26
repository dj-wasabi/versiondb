from flask_restx import Namespace
from healthcheck import HealthCheck, EnvironmentDump

nsHealth = Namespace(
  "/api/v1/health",
  path="/api/v1/health",
  version="1.0",
  description="Health endpoints."
)

health = HealthCheck()
envdump = EnvironmentDump()
