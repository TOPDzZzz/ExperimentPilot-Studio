import streamlit as st
from expilot.core.agent import AgentEngine
from expilot.i18n import t

lang = st.session_state.get("lang", "zh")

st.title(f"💬 {t('chat_title', lang)}")

if "messages" not in st.session_state:
    st.session_state.messages = []

AVATAR_MAP = {"user": "👤", "assistant": "🧪"}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATAR_MAP.get(msg["role"], "💬")):
        st.markdown(msg["content"])

if user_input := st.chat_input(t("chat_placeholder", lang)):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🧪"):
        agent = AgentEngine(
            max_steps=st.session_state.get("max_steps", 8),
            profile=st.session_state.get("profile", "general"),
        )
        history = [m for m in st.session_state.messages if m["role"] == "assistant"]

        status = st.status(t("agent_thinking", lang), expanded=True)
        final_box = st.empty()
        step_count = 0

        for step_info in agent.run_stream(user_input, history):
            step_count += 1

            if step_info["type"] == "thought":
                status.update(label=f"Step {step_count}: {step_info['content'][:80]}")

            elif step_info["type"] == "tool_call":
                status.update(label=f"Step {step_count}: Using {step_info.get('tool_name', '')}...")

            elif step_info["type"] == "final":
                status.update(label=t("completed", lang), state="complete")
                final_box.markdown(step_info["content"])
                st.session_state.messages.append({"role": "assistant", "content": step_info["content"]})
                break

            elif step_info["type"] == "error":
                status.update(label=t("status_error", lang), state="error")
                final_box.error(step_info["content"])
                st.session_state.messages.append({"role": "assistant", "content": step_info["content"]})
                break

        st.caption(f"{t('steps', lang)}: {step_count}")
