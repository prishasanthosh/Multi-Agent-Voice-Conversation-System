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

def optimist_agent(state: AgentState) -> dict:
    try:
        user_input = state.transcript.strip()
        print(f"[Optimist Agent] Using transcript: {state.transcript}")
        prior_discussion = (
            f"Realist: {state.realist_agent}\n"
            f"Expert: {state.expert_agent}\n"
            f"Optimist: {state.optimist_agent}"
        ).strip()

        spoken_agents = set(state.agent_trace)
        already_spoken = ", ".join(spoken_agents)

        retrieved_context = memory_tool.retrieve_memory(user_input)
        memory_snippets = "\n".join(f"- {mem}" for mem in retrieved_context)

        tool_prompt = f"""
        You are the Optimist AI Agent in a panel with Realist and Expert agents.

        Before responding, decide whether you need external inspiration or real-world positive examples.

        Criteria:
        - Is the topic complex, sensitive, or emotionally heavy?
        - Would motivational data, recent success stories, or possibilities help?

        Respond in exactly one line using:
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
                print(f"[Optimist Agent] Searching: {query}")
                search_results = search_tool.invoke(query)
            except Exception as e:
                print(f"[Optimist Agent] Search failed: {e}")
                search_results = "[Search failed]"

        # Generate final response
        response_prompt = f"""
        You are the Optimist AI Agent on a discussion panel.

        Your goal is to:
        - Inspire confidence
        - Provide possibility-driven advice
        - Encourage the user while staying relevant

        Be warm and visionary, but not unrealistic. You can use positive examples and hope-driven framing.

        Already spoken agents: {already_spoken}
        
        Format:
        RESPONSE:
        <1-2 lines of uplifting insight>

        NEXT: <optimist / expert / realist / user / end>

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
        if next_agent == "optimist":
            next_agent = "user"

        # Store interaction in memory
        memory_tool.store_memory(
            content=f"User asked: {user_input}",
            metadata={"agent": "user"}
        )
        memory_tool.store_memory(
            content=f"Optimist Agent said: {answer}",
            metadata={"agent": "optimist", "topic": user_input}
        )

        print(f"[Optimist Agent] {answer} ➜ NEXT: {next_agent}")

        return {
            "optimist_agent": answer,
            "next": next_agent,
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["optimist"],
            "transcript": user_input
        }

    except Exception as e:
        print(f"[Optimist Agent Error]: {e}")
        return {
            "optimist_agent": "Sorry, I encountered an issue.",
            "next": "end",
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["optimist"]
        }
