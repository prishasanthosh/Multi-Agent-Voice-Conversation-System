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

def realist_agent(state: AgentState) -> dict:
    try:
        user_input = state.transcript.strip()
        print(f"[Realist Agent] Using transcript: {state.transcript}")
        prior_discussion = (
            f"Optimist: {state.optimist_agent}\n"
            f"Expert: {state.expert_agent}\n"
            f"Realist: {state.realist_agent}"
        ).strip()

        spoken_agents = set(state.agent_trace)
        already_spoken = ", ".join(spoken_agents)

        # Retrieve memory context
        retrieved_context = memory_tool.retrieve_memory(user_input)
        memory_snippets = "\n".join(f"- {mem}" for mem in retrieved_context)

        # Decide if web search is needed
        tool_decision_prompt = f"""
        You are the Realist AI Agent in a multi-agent discussion panel with Optimist and Expert agents.

        Your job is to provide practical, fact-based responses.

        Before responding, decide if you need **real-time search data**. Consider:
        - Is the user asking for something recent, data-backed, or uncertain?
        - Does the current context lack reliable information?

        Respond in ONE LINE using EXACTLY this format:
        TOOL: yes - QUERY: <your Google search query>
        or
        TOOL: no

        User input:
        "{user_input}"

        Prior discussion:
        {prior_discussion}
        """
        decision = llm.generate_content(tool_decision_prompt).text.strip()
        use_tool = decision.lower().startswith("tool: yes")
        search_results = ""

        if use_tool:
            try:
                query = decision.split("QUERY:")[1].strip()
                print(f"[Realist Agent] Searching: {query}")
                search_results = search_tool.invoke(query)
            except Exception as e:
                print(f"[Realist Agent] Search failed: {e}")
                search_results = "[Search failed]"

        # Final response prompt
        response_prompt = f"""
        You are the Realist Agent in a 3-agent discussion with Optimist and Expert.

        Your role is to:
        - Provide a realistic, fact-based perspective
        - Build on the ongoing conversation

        Respond based on:
        - The user's query
        - Search results (if any)
        - The ongoing discussion
        - Memory context (if any)

        You must:
        - Be concise (1–2 lines)
        - Add NEW insight, not repetition
        - Choose the next speaker: 'optimist', 'expert', 'user', or 'end'
        - BUT if the agent you're suggesting has already spoken, or all 3 have spoken, choose 'user'

        Already spoken agents: {already_spoken}

        Format:
        RESPONSE:
        <your grounded reply here>

        NEXT: <next agent>

        ---

        USER INPUT:
        {user_input}

        DISCUSSION:
        {prior_discussion}

        SEARCH RESULTS:
        {search_results}

        MEMORY CONTEXT:
        {memory_snippets}
        """
        agent_output = llm.generate_content(response_prompt).text.strip()
        segment = agent_output.split("NEXT:")
        answer = segment[0].replace("RESPONSE:", "").strip()
        next_agent = segment[1].strip().lower() if len(segment) > 1 else "end"

        if next_agent in spoken_agents or len(spoken_agents) >= 3:
            next_agent = "user"

        memory_tool.store_memory(
            content=f"User asked: {user_input}",
            metadata={"agent": "user"}
        )
        memory_tool.store_memory(
            content=f"Realist Agent said: {answer}",
            metadata={"agent": "realist", "topic": user_input}
        )

        print(f"[Realist Agent] {answer} ➜ NEXT: {next_agent}")

        return {
            "realist_agent": answer,
            "next": next_agent,
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["realist"],
            "transcript": user_input
        }

    except Exception as e:
        print(f"[Realist Agent Error]: {e}")
        return {
            "realist_agent": "Sorry, I encountered an issue.",
            "next": "end",
            "step_counter": state.step_counter + 1,
            "agent_trace": state.agent_trace + ["realist"]
        }
