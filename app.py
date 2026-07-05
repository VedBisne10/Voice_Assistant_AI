# start the assistant
from assistant.orchestrator import Orchestrator  # the main class that runs everything

nova = Orchestrator()  # create nova - this sets up mic, speaker, AI, memory
nova.run_forever()  # start listening and never stop until user says bye
