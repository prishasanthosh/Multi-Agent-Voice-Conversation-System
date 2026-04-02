# Multiagent System

- A multiagent system consists of multiple artificial intelligence agents working collectively to perform task on behalf of a user or another system.  
- Each agent within a MAS has individual properties but all agents behave collaboratively to lead to desired global properties.  
- They are valuable in completing large-scale, complex tasks that can encompass a large number of agents.  
- An AI agent refers to a system or program capable of autonomously performing tasks on behalf of a user or another system by designing its workflow and using available tools.  
- The core of AI agents is Large Language Models (LLMs)  
- What differentiates AI agents from traditional LLMs is the use of tools and the ability to design a plan of action.  
- The tools available to an agent can include external datasets, web searches and application programming interfaces (APIs).  

## Feature Comparison

| Feature             | Single-Agent System       | Multi-Agent System                                      |
|---------------------|---------------------------|----------------------------------------------------------|
| Autonomy            | Fully autonomous          | Fully autonomous but cooperative                         |
| Communication       | Not required              | Essential for cooperation & coordination                 |
| Tool Use            | Calls tools independently | May include other agents as tools or peers               |
| Learning            | Learns from its environment | Learns and shares with other agents                    |
| Scalability         | Limited by one agent      | Highly scalable through collaboration                    |
| Performance         | Good for simpler tasks    | Better for complex, distributed tasks                    |
| Knowledge Sharing   | No                        | Yes (policies, experiences, real-time info)              |

## Architectures of Multiagent Systems

- **Centralized networks:**
  - Can operate under various architectures.  
  - A central unit contains the global knowledge base, connects the agents and oversees the information.  
  - A strength of this structure is the ease of communication between agents and uniform knowledge.  
  - A weakness of the centrality is the dependence on the central unit; and if it fails, the entire system of agents fails.

- **Decentralized networks:**
  - Share information with their neighboring agents instead of a global knowledge base.  
  - Benefits - robustness and modularity  
  - Failure of one agent does not cause the overall system to fail since there is no central unit.  
  - Challenge – decentralized agents is coordinating their behaviour to benefit other cooperating agents.

## Structures of Multiagent Systems

- **Hierarchical structure:**
  - A tree-like structure and contains agents with varying levels of autonomy.  
  - In simpler structures – the responsibility can be distributed among multiple agents.

- **Holonic structure:**
  - A holon is an entity that cannot operate without its components.  
  - Self-organized and creates to achieve a goal through the collaboration of the subagents.

- **Coalition structure:**
  - Helpful in cases of underperforming singular agents in a group

- **Teams:**
  - Similar to coalitions.  
  - Agents cooperate to improve the performance of the group.  
  - Agents in teams do not work independently, unlike coalitions.  
  - Agents in teams are much more dependent on one another and their structure is more hierarchical than coalitions.

## Behaviours of MAS

- **Flocking**
  - Agents share an objective and require some organization to coordinate their behavior.  
  - Flocking pertains to directional synchronization and the structure of these flocks can be described by these heuristics:  
    - **Separation:** attempt to avoid collision with nearby agents.  
    - **Alignment:** attempt to match the velocity of nearby agents.  
    - **Cohesion:** attempt to remain close to other agents.

- **Swarming**
  - Spatial positioning of agents in MAS can be compared to the swarming that occurs in nature.  
  - Swarming is the emergent self-organization and aggregation among software agents with decentralized control.  
  - Benefit - one operator can be trained to manage a swarm of agents, this method is less computationally expensive and more reliable than training an operator for each agent.

## Use Cases of MAS

- Transportation  
- Healthcare and public health  
- Supply chain management  
- Defence systems  

## Advantages of Multi-Agent Systems

- Flexibility  
- Scalability  
- Domain specialization  
- Greater performance  

## Challenges of Multi-Agent Systems

- Agent malfunctions  
- Coordination complexity  
- Unpredictable behaviour  
