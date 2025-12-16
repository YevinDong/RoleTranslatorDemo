This repo uses uv as pakcage manager. Don't forget calling uv when running python scripts or unittests.

This is an AI project:
- aimed at addressing the issues raised in `./QUESTION.md`.
- The solution adopts `./SOLUTION.md`. 
- The current to-do items can be recorded in `TODO.MD`.

The project will be built with LangChain and LangGraph together, using versions ≥1.0.0.

The code must follow industry conventions (project structure and naming); for example, agent's state should inherit from langgraph’s AgentState


Agent internal files/modules explained:  When encountering functions/variables with identical names, define them inside the corresponding file; create the file if necessary.  

- `./src/agent/graph.py`: Entry-point module  
- `./src/agent/prompt.py`: Prompt module—exports/defines prompts  
- `./src/agent/state.py`: Defines the agent state  
- `./src/agent/tools/**.py`: Tools required by the LangChain agent  
- `./src/agent/utils/**.py`: Utility functions for the project, including logger, LLM export, env loading, etc.
- `./src/agent/graph_componentes/**.py`: Graph node components