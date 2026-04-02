import os
from dotenv import load_dotenv
from tools.web_search import WebSearchTool
from memory_tool import MemoryTool
from google.generativeai import GenerativeModel
from state import AgentState  

load_dotenv()
llm = GenerativeModel("gemini-2.5-flash-preview-05-20")
search_tool = WebSearchTool()
memory_tool = MemoryTool()

def expert_agent(state: AgentState) -> dict:
    try:
        user_input = state.transcript.strip()
        print(f"[Expert Agent] Using transcript: {state.transcript}")
        prior_discussion = (
            f"Realist: {state.realist_agent}\n"
            f"Optimist: {state.optimist_agent}\n"
            f"Expert: {state.expert_agent}"
        ).strip()

        spoken_agents = set(state.agent_trace)
        already_spoken = ", ".join(spoken_agents)

        retrieved_context = memory_tool.retrieve_memory(user_input)        
        memory_snippets = "\n".join(f"- {mem}" for mem in retrieved_context)

        tool_prompt = f"""
        You are the Expert AI Agent in a multi-agent panel.

        Your goal is to offer clear, factual, domain-specific insight.

        Decide whether web search is needed for accurate, recent, or niche knowledge.

        Respond in ONE line using:
        TOOL: yes - QUERY: <your search query>
        or
        TOOL: no

        USER INPUT:
        "{user_input}"

        PRIOR DISCUSSION:
        {prior_discussion}
        """
        decision = llm.generate_content(tool_prompt).text.strip()
        use_tool = decision.lower().startswith("tool: yes")
        search_results = ""

        if use_tool:
            try:
                query = decision.split("QUERY:")[1].strip()
                print(f"[Expert Agent] Searching: {query}")
                search_results = search_tool.invoke(query)
            except Exception as e:
                print(f"[Expert Agent] Search failed: {e}")
                search_results = "[Search failed]"

        response_prompt = f"""
        You are the Expert Agent in a discussion with Realist and Optimist agents.

        Your response should:
        - Be informative, analytical, and evidence-based
        - Avoid repeating other agents
        - Be clear and technically correct
        - Suggest the best next step in the flow

        Already spoken agents: {already_spoken}

        Format:
        RESPONSE:
        <1-2 line expert opinion>

        NEXT: <realist / optimist / user / end>

        USER INPUT:
        {user_input}

        PRIOR DISCUSSION:
        {prior_discussion}

        SEARCH RESULTS:
        {search_results}

        MEMORY CONTEXT:
        {memory_snippets}

        """
        response = llm.generate_content(response_prompt).text.strip()
        lines = response.split("NEXT:")
        answer = lines[0].replace("RESPONSE:", "").strip()
        next_agent = lines[1].strip().lower() if len(lines) > 1 else "end"
        if next_agent == "expert":
            next_agent = "user"

        memory_tool.store_memory(
            content=f"User asked: {user_input}",
            metadata={"agent": "user"}
        )
        memory_tool.store_memory(
            content=f"Expert Agent said: {answer}",
            metadata={"agent": "expert", "topic": user_input}
        )

        print(f"[Expert Agent] {answer} ➜ NEXT: {next_agent}")

        return {
            "expert_agent": answer,
            "next": next_agent,
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["expert"],
            "transcript": user_input
        }

    except Exception as e:
        print(f"[Expert Agent Error]: {e}")
        return {
            "expert_agent": "Sorry, I encountered an issue.",
            "next": "end",
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["expert"]
        }
