EchoVerse: An AI-Powered Audiobook Creation Tool
Welcome to EchoVerse, a generative AI system that transforms written text into expressive, downloadable audio with a customizable tone and voice. Developed for the hackathon, EchoVerse is designed to address accessibility needs, boost productivity, and enable creative content reuse for students, professionals, and visually-impaired users.


🚀 Features
Tone-Adaptive AI Rewriting: Rewrites text to match one of three selectable tones: Neutral, Suspenseful, or Inspiring.
Multi-Voice Narration: Uses IBM Watson Text-to-Speech to convert text into natural-sounding audio with multiple voice options available.
Dual Output Modes: The generated audio can be streamed directly in the app or downloaded as an .mp3 file.
Side-by-Side Text Comparison: Provides transparency and user trust by displaying the original text alongside the rewritten, AI-enhanced version.
Intuitive User Interface: The front-end is built with Streamlit for a simple, accessible experience.

⚙️ How It Works
EchoVerse follows a clear plan of action to convert your text into an audiobook:
Input & Tone Selection: A user pastes or uploads a .txt file and selects a tone.
AI Rewriting: A large language model rewrites the text to preserve its meaning while enhancing its expressiveness for the chosen tone.
Voice Narration: The rewritten text is converted into natural-sounding audio.
Output: The final audio can be streamed or downloaded as an .mp3 file.

💻 Installation & Usage
To run EchoVerse locally, you'll need Python and a few key libraries.
Clone the Repository:
git clone https://github.com/your-repo/echoverse.git

Navigate to the Project Directory:
cd echoverse
Install Dependencies:
pip install -r requirements.txt
(Your requirements.txt should contain streamlit, torch, transformers, accelerate, pydub, num2words, pyttsx3)

Run the Application:
streamlit run app.py
The app will open in your web browser.

🌟 Innovation & Impact
Uncommon Functionality: The core innovation lies in the tone-adaptive AI rewriting that happens before narration, which is uncommon in standard text-to-speech tools.
Efficiency: The system ensures consistent tonal quality throughout the text using a process called Prompt Chaining.
Accessibility & Productivity: EchoVerse provides accessibility for visually-impaired users and a productivity boost for students and professionals by allowing them to consume content in a new format.
Cost Savings: It drastically reduces costs compared with outsourcing professional audiobook production.

📈 Future Scope
EchoVerse is built with a modular architecture to simplify future updates. Planned enhancements include:
Multi-language and multi-accent expansion.
Potential integrations with Learning Management Systems (LMS) or podcast platforms.
Cloud deployment to widen its reach to a larger audience.

🤝 Team
This solution was developed by 
TEAM SYNTRIX for the IBM COGNITEX hackathon.

