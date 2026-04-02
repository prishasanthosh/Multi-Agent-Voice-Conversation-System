- A framework simplifies the orchestration, automation and optimization of a complex LLM workflow.
- It maximizes the performance of LLM models and overcomes its weakness.

## AGENTS:

- AutoGen abstracts and implements conversable agents designed to solve tasks through inter-agent conversations.
- **Conversable**: Agents in AutoGen are conversable, which means that any agent can send and receive messages from other agents to initiate or continue a conversation.
- **Customizable**: Agents in AutoGen can be customized to integrate LLMs, humans, tools, or a combination of them.

![AutoGen Agents](https://microsoft.github.io/autogen/0.2/assets/images/autogen_agents-b80434bcb15d46da0c6cbeed28115f38.png)

- A generic `ConversableAgent` class for Agents that are capable of conversing with each other through the exchange of messages to jointly finish a task.
- Two representative subclasses are `AssistantAgent` and `UserProxyAgent`:
  - The `AssistantAgent` is designed to act as an AI assistant, using LLMs by default but not requiring human input or code execution. It could write Python code (in a Python coding block) for a user to execute when a message (typically a description of a task that needs to be solved) is received.
  - The `UserProxyAgent` is conceptually a proxy agent for humans, soliciting human input as the agent's reply at each interaction turn by default and also having the capability to execute code and call functions or tools. Triggers code execution automatically when it detects an executable code block in the received message and no human user input is provided.

- The auto-reply capability of `ConversableAgent` allows for more autonomous multi-agent communication while retaining the possibility of human intervention. One can also easily extend it by registering reply functions with the `register_reply()` method.

![Agent Example](https://microsoft.github.io/autogen/0.2/assets/images/agent_example-a965f253ce7d8e1548ff819e19edc5e4.png)

## Supporting Diverse Conversation Patterns

- Conversations with different levels of autonomy and human-involvement patterns:
  - One can achieve fully autonomous conversations after an initialization step.
  - AutoGen can be used to implement human-in-the-loop problem-solving by configuring human involvement levels and patterns as human involvement is expected and/or desired in many applications.

## Static and Dynamic Conversation

- This dynamic nature allows the agent topology to adapt based on the actual conversation flow under varying input problem scenarios.
- Static conversations adhere to a predefined topology.
- Dynamic conversations are particularly beneficial in complex settings where interaction patterns cannot be predetermined.

## Registered Auto-Reply

- With the pluggable auto-reply function, one can choose to invoke conversations with other agents depending on the content of the current message and context.

## LLM-Based Function Call

- LLM decides if a specific function should be invoked based on the conversation's status during each inference.
- This approach enables dynamic multi-agent conversations, as seen in scenarios like multi-user math problem solving scenario, where a student assistant automatically seeks expertise via function calls.

## Diverse Applications Implemented with AutoGen

![Applications](https://microsoft.github.io/autogen/0.2/assets/images/app-c414cd164ef912e5e8b40f61042143ad.png)  
