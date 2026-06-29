# Entry point — just boot up Nova and let her run.
from assistant.orchestrator import Orchestrator

nova = Orchestrator()
nova.run_forever()
