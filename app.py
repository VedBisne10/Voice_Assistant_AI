# Entry point — just boot up Nova and let her run.
from assistant.orchestrator import Orchestrator  # pull in the main brain that runs the whole assistant

nova = Orchestrator()  # create the orchestrator instance — this sets up the mic, speaker, LLM, memory, all of it
nova.run_forever()  # hand control over to the loop and never come back — runs until the user says goodbye
