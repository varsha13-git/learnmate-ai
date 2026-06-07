import streamlit as st
import google.generativeai as genai

if "topics_learned" not in st.session_state:
    st.session_state.topics_learned = []

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🎓 LearnMate AI")

st.caption(
    "Your Personalized AI Learning Companion"
)
st.info(
    """
👋 Welcome to LearnMate AI!

Tell me what you want to learn and I'll explain it based on your interests and learning style.

✨ Features:
- Personalized explanations
- Story Mode
- Visual Learning
- Exam Preparation
- Interactive Quizzes
"""
)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Quiz Me"):
        st.session_state.quick_prompt = "Quiz me on this topic"

with col2:
    if st.button("🎨 Give Example"):
        st.session_state.quick_prompt = "Give me an example"

with col3:
    if st.button("📚 Simplify"):
        st.session_state.quick_prompt = "Explain this in a simpler way"


with st.sidebar:

    st.title("👤 Student Profile")

    name = st.text_input(
    "Your Name",
    placeholder="Enter your name"
)

    interest = st.text_area(
    "Your Interests",
    placeholder="Dance, Music, Art..."
)
    learning_style = st.selectbox(
    "Learning Style",
    [
        "Beginner",
        "Visual Learner",
        "Exam Preparation",
        "Story Mode"
    ]
)

    st.markdown("---")

    st.success("🚀 LearnMate AI")
    st.markdown("### 📈 Learning History")

    for topic in st.session_state.topics_learned[-5:]:
        st.write("✅", topic)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_input = st.chat_input("Ask what you want to learn...")

if "quick_prompt" in st.session_state:
    user_input = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if user_input:
    st.session_state.topics_learned.append(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
    Student Name: {name}

    Student Interests: {interest}

    Learning Style: {learning_style}

    The student asked:
    {user_input}

   Rules:

1. If the student asks for a quiz, generate a quiz.
2. If the student asks for examples, give examples.
3. If the student asks for a simpler explanation, simplify it.
4. If the student asks for story mode, explain as a story.
5. If the student asks to learn a topic, teach it.
6. Always use the student's interests when possible.
7. Be friendly and interactive like a tutor.

If Learning Style is "Visual Learner",
use visual descriptions and comparisons.

If Learning Style is "Story Mode",
teach using stories.

If Learning Style is "Exam Preparation",
focus on important points and definitions.

If Learning Style is "Beginner",
explain in the simplest way possible.

Respond according to the student's request.
    """

    response = model.generate_content(prompt)

    ai_reply = response.text

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(ai_reply)