import streamlit as st
from nlu import extract_entities_and_intent, get_memory
from db_connection import db
from dashboard import show_dashboard
from gtts import gTTS
import tempfile

st.set_page_config(page_title="MongoDB QA", layout="centered")
st.title("🧠 Finance Database  Agent")


if "memory" not in st.session_state:
    st.session_state.memory = []

# Text-to-Speech
def speak_text(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            st.audio(tmp.name, format="audio/mp3")
    except Exception as e:
        st.warning(f"TTS failed: {e}")


input_mode = st.radio("Choose input mode:", ["Text", "Voice (use Windows + H)"], horizontal=True)
query = st.text_input("Ask your question:", placeholder="e.g. What are the products of account 371138?")


col1, col2 = st.columns([6, 1])
with col2:
    clear = st.button("🧹 Clear Memory")
with col1:
    submit = st.button("Submit")

if submit and query:
    with st.spinner("Thinking..."):
        pipeline_info = extract_entities_and_intent(query)

        if not pipeline_info or not isinstance(pipeline_info, dict):
            st.error("Could not parse query.")
        elif "collection" not in pipeline_info:
            st.error(" Collection not identified.")
            st.code(pipeline_info.get("raw", "No raw response"))
        else:
            try:
                collection = pipeline_info["collection"]
                pipeline = pipeline_info.get("pipeline", [])
                results = list(db[collection].aggregate(pipeline)) if pipeline else []

                st.subheader("✅ Answer:")
                bot_response = ""

                if not results:
                    bot_response = "No matching data found."
                    st.warning(bot_response)
                else:
                    for result in results:
                        clean = {k: v for k, v in result.items() if k != "_id"}
                        if not clean:
                            bot_response = "No useful fields to display."
                            st.warning(bot_response)
                        elif len(clean) == 1:
                            val = list(clean.values())[0]
                            st.success(val)
                            bot_response = str(val)
                        else:
                            pretty = "\n".join([f"**{k.replace('_', ' ').capitalize()}:** {v}" for k, v in clean.items()])
                            st.markdown(pretty)
                            bot_response = ", ".join(f"{k}: {v}" for k, v in clean.items())

                if bot_response:
                    st.session_state.memory.append({"user": query, "bot": bot_response})
                    speak_text(bot_response)

            except Exception as e:
                st.error("⚠️ MongoDB execution error")
                st.exception(e)


with st.expander("📈 Database Insights"):
    show_dashboard()

if st.session_state.memory:
    st.markdown("---")
    st.markdown("### 🧠 Conversation Memory")
    for chat in st.session_state.memory[::-1]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.markdown("---")

#clear
if clear:
    st.session_state.memory = []
