from langgraph.graph import StateGraph, END
from state import AgentState

from agents.realist_agent import realist_agent
from agents.optimist_agent import optimist_agent
from agents.expert_agent import expert_agent

from voice.speech_to_text import record_audio, transcribe_audio
import asyncio

def user_input_node(state: AgentState) -> dict:
    print("\n[System] Agent asked for user input. Recording...")
    record_audio()
    transcript = asyncio.run(transcribe_audio())

    if not transcript:
        print("❌ No speech detected or transcription failed.")
        return {**state.dict(), "next": "end"}  

    print(f"[DEBUG] New user input: {transcript}")

    stop_keywords = ["stop", "exit", "thank you", "that's all", "no more", "bye", "quit", "done"]
    if any(keyword in transcript.lower() for keyword in stop_keywords):
        print("[System] Thank you for your time. Conversation ended by user.")
        return {**state.dict(), "next": "end"}

    return {
        **state.dict(),
        "transcript": transcript,
        "next": "realist",  # restart the agent loop with the new transcript
    }

def decide_next(state: AgentState) -> str:
    return END if state.next == "end" else state.next

graph = StateGraph(AgentState)

graph.add_node("realist", realist_agent)
graph.add_node("optimist", optimist_agent)
graph.add_node("expert", expert_agent)

graph.add_node("user", user_input_node)

graph.set_entry_point("realist")

for node in ["realist", "optimist", "expert", "user"]:
    graph.add_conditional_edges(node, decide_next)

multi_agent_app = graph.compile()
