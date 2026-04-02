import os
import asyncio
from dotenv import load_dotenv

from workflow import multi_agent_app
from state import AgentState
from voice.speech_to_text import record_audio, transcribe_audio
from voice.text_to_speech import text_to_speech

load_dotenv()

stop_keywords = ["stop", "exit", "thank you", "that's all", "no more", "bye", "quit", "done"]

def main():
    print("🎙️ Welcome to the Multi-Agent Voice System!")

    step_counter = 0
    agent_trace = []
    next_agent = "realist"

    realist_agent = ""
    optimist_agent = ""
    expert_agent = ""

    transcript = ""

    while True:
        if step_counter == 0 or next_agent == "user":
            print("\n🎤 Please speak now...")
            record_audio()

            new_transcript = asyncio.run(transcribe_audio())
            if not new_transcript:
                print("❌ No speech detected or transcription failed. Try again.")
                continue

            if any(kw in new_transcript.lower() for kw in stop_keywords):
                print("[System] Thank you for your time. Conversation ended by user.")
                break

            print(f"\n🗣️ You said: {new_transcript}\n")
            transcript = new_transcript  

        state = AgentState(
            transcript=transcript,
            step_counter=step_counter,
            agent_trace=agent_trace,
            next=next_agent,
            realist_agent=realist_agent,
            optimist_agent=optimist_agent,
            expert_agent=expert_agent
        )

        final_state_data = multi_agent_app.invoke(state)
        final_state = AgentState(**final_state_data)

        print("\n🤖 Agent Responses:")
        spoken_agents = set()

        for agent in final_state.agent_trace[len(agent_trace):]:
            if agent not in spoken_agents:
                spoken_agents.add(agent)
                reply = getattr(final_state, f"{agent}_agent", "")
                if reply:
                    print(f"{agent.capitalize()}: {reply}")
                    try:
                        text_to_speech(reply)
                    except Exception as e:
                        print(f"⚠️ TTS failed: {e}")

        step_counter = final_state.step_counter
        agent_trace = final_state.agent_trace
        next_agent = final_state.next
        realist_agent = final_state.realist_agent
        optimist_agent = final_state.optimist_agent
        expert_agent = final_state.expert_agent

if __name__ == "__main__":
    main()
