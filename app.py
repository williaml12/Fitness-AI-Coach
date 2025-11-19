import streamlit as st

# --- Page config ---
st.set_page_config(page_title="FitFuel: AI Coach", layout="wide")

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "height": None,
        "weight": None,
        "goal": None,
        "preference": None
    }

# --- Sidebar: user profile input ---
with st.sidebar:
    st.header("Your Profile")
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    goal = st.selectbox("Fitness Goal", ["Lose weight", "Build muscle", "Maintain"])
    preference = st.selectbox("Workout Preference", ["Home", "Gym", "No preference"])
    if st.button("Save Profile"):
        st.session_state.user_profile = {
            "height": height,
            "weight": weight,
            "goal": goal,
            "preference": preference
        }
        st.success("Profile saved!")

# --- Main app: Chat + Plan ---
st.title("🤖 FitFuel: Your AI Fitness Coach")

# Show saved profile
profile = st.session_state.user_profile
st.write("**Your Profile**:", profile)

# Chat area
st.subheader("Chat with your AI Coach")
user_input = st.text_area("Ask me anything about workouts, meals, or strategy:", height=100)

if st.button("Send"):
    if user_input.strip() != "":
        # Here: call your LLM / AI backend
        answer = ai_coach_response(user_input, profile)  # you define this function
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Coach", answer))
    else:
        st.warning("Please type something first.")

# Display chat history
for speaker, text in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Coach:** {text}")
    st.markdown("---")

# Optionally: Generate a weekly plan
if st.button("Generate Week Plan"):
    plan = generate_weekly_plan(profile)  # you define this
    st.subheader("Your Weekly Plan")
    st.write(plan)  # could be a dict / dataframe or whatever structure you want

# Function definitions (mock)
def ai_coach_response(message, profile):
    # This is where you integrate your AI model / API
    # For example:
    # response = call_bedrock_model(prompt=..., user_profile=profile)
    # return response
    return f"I got your message: '{message}' with profile {profile}. (This is a stubbed response.)"

def generate_weekly_plan(profile):
    # Create a fake plan for example
    return {
        "Monday": "30 min cardio",
        "Tuesday": "Strength training (upper body)",
        "Wednesday": "Rest or light walk",
        "Thursday": "Strength training (lower body)",
        "Friday": "Yoga / Mobility",
        "Saturday": "HIIT workout",
        "Sunday": "Rest"
    }
