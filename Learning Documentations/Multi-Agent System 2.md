# Multi-Agent System 2

- The primary benefits of using multi-agent systems are:
  - **Modularity**: Separate agents make it easier to develop, test, and maintain agentic systems.
  - **Specialization**: You can create expert agents focused on specific domains, which helps with the overall system performance.
  - **Control**: You can explicitly control how agents communicate (as opposed to relying on function calling).

## Multi-agent architectures

- **Network**: each agent can communicate with every other agent. Any agent can decode which other agent to call next.
- **Supervisor**: each agent communicates with a single supervisor agent. Makes decisions on which agent should be called next.
- **Supervisor (tool-calling)**: individual agents can be represented as tools. A supervisor agent uses a tool-calling LLM to decide which of the agent tools to call as well as the arguments to pass to those agents.
- **Hierarchical**: define multi-agent system with a supervisor of supervisors. A generalization of the supervisor architecture and allows for more complex control flows.
- **Custom multi-agent workflow**: each agent communicates with only a subset of agents. Parts of the flow are deterministic, and only some agents can decide which other agents to call next.

## Handoffs

- In MA architectures, agents can be represented as graph nodes.
- Each node executes its step and decodes whether to finish execution or route to another agent.
- A common pattern in multi-agent interactions is handoffs, when one control the other.
- Handoffs allow us to specify:
  - **destination**: target agent to navigate to (e.g., name of the node to go to)
  - **payload**: information to pass to that agent (e.g., state update)
- If you have two agents, alice and bob (subgraph nodes in a parent graph), and alice needs to navigate to bob, you can set `graph=Command.PARENT` in the `Command` object.

## Custom multi-agent workflow

- In this architecture we add individual agents as graph nodes and define the order in which agents are called ahead of time, in a custom workflow. In LangGraph the workflow can be defined in two ways:
  - **Explicit control flow (normal edges)**: LangGraph allows you to explicitly define the control flow of your application (i.e. the sequence of how agents communicate) explicitly, via normal graph edges. This is the most deterministic variant of this architecture above — we always know which agent will be called next ahead of time.
  - **Dynamic control flow (Command)**: in LangGraph you can allow LLMs to decide parts of your application control flow. This can be achieved by using Command. A special case of this is a supervisor tool-calling architecture. In that case, the tool-calling LLM powering the supervisor agent will make decisions about the order in which the tools (agents) are being called.

## Handoffs vs Tool Calling

- In most of the architectures discussed above, the agents communicate via handoffs and pass the graph state as part of the handoff payload.
- Specifically, agents pass around lists of messages as part of the graph state. In the case of the supervisor with tool-calling, the payloads are tool-call arguments.  
  ![Request](https://langchain-ai.github.io/langgraph/concepts/img/multi_agent/request.png)

## Message passing between agents

- A shared channel is the most common way for agents to communicate.  
  ![Response](https://langchain-ai.github.io/langgraph/concepts/img/multi_agent/response.png)

- **Shared full thought process**:
  - Can share full history of their thought process with all other agents,
  - This scratchpad would look like a list of messages.
  - Benefit – might help other agents make better decisions.

- **Sharing only final results**
  - Only the final result is shared with the rest of the agents.
  - Works better for the systems with many agents or agents that are more complex.
  - In that case, we have to define agents with different state schemas.

- **Indicating agent name in messages**
  - Helpful to indicate which agent a particular AI message is from, especially long messages.
  - Some LLM providers (like OpenAI) support adding a name parameter to messages — you can use that to attach the agent `name` to the message.
  - If that is not supported, you can consider manually injecting the agent name into the message content, e.g.,  
    `<agent>alice</agent><message>message from alice</message>`

- **Representing handoffs in message history**
  - Most LLM providers don't support receiving AI messages with tool calls without corresponding tool messages.
  - Add an extra tool message to the message list, e.g., "Successfully transferred to agent X"
  - Remove the AI message with the tool calls

## State Management for subagents

- A common practice is to have multiple agents communicating on a shared message list, but only adding their final messages to the list. This means that any intermediate messages (e.g., tool calls) are not saved in this list.
- There are two high-level approaches to achieve that:
  - Store these messages in the shared message list, but filter the list before passing it to the subagent LLM. For example, you can choose to filter out all tool calls from other agents.
  - Store a separate message list for each agent (e.g., `alice_messages`) in the subagent's graph state. This would be their "view" of what the message history looks like.

## Using different state schemas

- An agent might need to have a different state schema from the rest of the agents.
- Here are two ways to achieve this in LangGraph:
  - Define subgraph agents with a separate state schema. If there are no shared state keys (channels) between the subgraph and the parent graph, it’s important to add input / output transformations so that the parent graph knows how to communicate with the subgraphs.
  - Define agent node functions with a private input state schema that is distinct from the overall graph state schema. This allows passing information that is only needed for executing that particular agent.
