# Chat Input
user_input = st.chat_input("Ask what you want to learn...")

final_input = user_input

if "quick_prompt" in st.session_state:
    final_input = st.session_state.pop("quick_prompt")

if final_input:

    if final_input not in st.session_state.topics_learned:
        st.session_state.topics_learned.append(final_input)

    st.session_state.messages.append(
        {"role": "user", "content": final_input}
    )

    with st.chat_message("user"):
        st.markdown(final_input)

    prompt = f"""
You are an AI Learning Assistant.

Student Name: {name}

Student Interests: {interest}

Learning Style: {learning_style}

The student asked:
{final_input}

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

    try:
        response = model.generate_content(prompt)

        ai_reply = response.text

    except Exception as e:

        if "ResourceExhausted" in str(e) or "429" in str(e):
            ai_reply = (
                "⚠️ Gemini API quota reached. "
                "Please wait a few minutes and try again."
            )

        else:
            ai_reply = f"Something went wrong: {str(e)}"

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(ai_reply)