import streamlit as st
import base64
import os
import time
import subprocess
import threading
import random
from streamlit.components.v1 import html
from datetime import datetime
import io

# --- REWRITER AND TTS LOGIC ---
# This now imports the hybrid function
from rewriter import hybrid_rewrite
from tts import synthesize

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🎵 EchoVerse - Audio Magic",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ SETTINGS ------------------
BANNER_IMAGES = ["slide.jpg", "slide2.jpg", "Background.png"]
SLIDESHOW_DELAY = 4000  # 4 seconds

# ------------------ UTILITIES ------------------
def file_to_base64(path: str) -> str:
    """Convert file to base64 string"""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""

def get_placeholder_audio_bytes():
    """Returns a placeholder audio file for demonstration."""
    sample_path = "sample.mp3"
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            return f.read()
    else:
        return None

def trigger_mega_confetti():
    """Epic confetti celebration for audio generation"""
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    window.megaConfettiShow = function() {
        var duration = 5 * 1000;
        var animationEnd = Date.now() + duration;
        var defaults = {startVelocity: 30, spread: 360, ticks: 60, zIndex: 999};
        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }
        var interval = setInterval(function() {
            var timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) {
                return clearInterval(interval);
            }
            var particleCount = 50 * (timeLeft / duration);
            confetti(Object.assign({}, defaults, {
                particleCount,
                origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                colors: ['#FFD700', '#FF69B4', '#00CED1', '#FF6347', '#9370DB', '#32CD32']
            }));
            confetti(Object.assign({}, defaults, {
                particleCount,
                origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                colors: ['#FFD700', '#FF69B4', '#00CED1', '#FF6347', '#9370DB', '#32CD32']
            }));
            confetti(Object.assign({}, defaults, {
                particleCount: particleCount * 2,
                origin: { x: 0.5, y: 0.3 },
                colors: ['#FFD700', '#FFA500', '#FF4500']
            }));
        }, 250);
        console.log('🎉 MEGA CONFETTI ACTIVATED! 🎉');
    }
    setTimeout(window.megaConfettiShow, 500);
    </script>
    """
    html(confetti_js, height=0, width=0)

# --- INTEGRATING YOUR AI FUNCTIONS ---
def rewrite_text_with_llm(text: str, tone: str) -> str:
    """
    This function now calls the hybrid rewriter to choose the best method.
    """
    if not text or not text.strip():
        return ""
    
    with st.spinner(f"⏳ Processing with hybrid rewriter for '{tone}' tone..."):
        try:
            rewritten = hybrid_rewrite(text, tone)
            st.success(f"✨ Text successfully transformed with {tone} tone!")
            return rewritten
        except Exception as e:
            st.error(f"Rewriting error: {str(e)}")
            return text

def text_to_speech(text: str, voice: str) -> bytes:
    """
    Calls the synthesize function from your tts.py script and
    reads the resulting file into bytes for Streamlit.
    """
    with st.spinner(f"⏳ Converting text to speech with voice '{voice}'..."):
        try:
            audio_path = synthesize(text, voice)
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                return audio_bytes
            else:
                return None
        except Exception as e:
            st.error(f"Error during text-to-speech conversion: {e}")
            return None

# ------------------ MODERN ENHANCED STYLES ------------------
def apply_modern_styles():
    """Apply cutting-edge CSS styles"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        .stApp {
            background: radial-gradient(ellipse at top, #1a1a2e, #16213e, #0f0f23);
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: white;
        }
        .main .block-container {
            padding: 2rem;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-top: 1rem;
        }
        .stButton > button {
            background: linear-gradient(135deg, #FFD700, #FF8C00, #FF6347);
            border: none;
            border-radius: 25px;
            color: #000;
            font-weight: 700;
            padding: 12px 24px;
            font-size: 16px;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(255, 140, 0, 0.4);
            position: relative;
            overflow: hidden;
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(255, 140, 0, 0.6);
            background: linear-gradient(135deg, #FF6347, #FF8C00, #FFD700);
        }
        .stButton > button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        .stButton > button:hover:before {
            left: 100%;
        }
        .modern-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            margin: 15px 0;
        }
        .modern-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 215, 0, 0.3);
        }
        .text-content {
            color: rgba(255, 255, 255, 0.95);
            line-height: 1.8;
            font-size: 16px;
            margin: 0;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px 20px;
            text-align: center;
            margin: 10px 5px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .stat-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #FFD700, #FF8C00, #FF6347);
        }
        .main-title {
            font-size: 4.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #FFD700, #FF8C00, #FF6347);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 15px;
            filter: drop-shadow(0 4px 12px rgba(255, 215, 0, 0.3));
        }
        .subtitle {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.8);
            text-align: center;
            font-weight: 300;
            margin-bottom: 30px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        .loading-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            padding: 20px;
        }
        .loading-dots {
            display: flex;
            gap: 8px;
        }
        .loading-dot {
            width: 12px;
            height: 12px;
            background: #FFD700;
            border-radius: 50%;
            animation: loadingPulse 1.4s infinite ease-in-out;
        }
        .loading-dot:nth-child(2) { animation-delay: 0.2s; }
        .loading-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes loadingPulse {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1.2); opacity: 1; }
        }
        .floating-action {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: #000;
            box-shadow: 0 15px 35px rgba(255, 140, 0, 0.4);
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        .floating-action:hover {
            transform: scale(1.1) rotate(10deg);
            box-shadow: 0 20px 45px rgba(255, 140, 0, 0.6);
        }
        @media (max-width: 768px) {
            .main-title { font-size: 3rem; }
        }
        @media (max-width: 480px) {
            .main-title { font-size: 2.5rem; }
        }
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            padding: 8px;
            gap: 8px;
            backdrop-filter: blur(10px);
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 20px;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 600;
            padding: 15px 25px;
            transition: all 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #FFD700, #FF8C00);
            color: #000;
            box-shadow: 0 5px 15px rgba(255, 140, 0, 0.4);
        }
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #FFD700, #FF8C00, #FF6347);
        }
        .css-1d391kg {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
        }
        .stSuccess {
            background: rgba(50, 205, 50, 0.1);
            border: 1px solid rgba(50, 205, 50, 0.3);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .stWarning {
            background: rgba(255, 165, 0, 0.1);
            border: 1px solid rgba(255, 165, 0, 0.3);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .stAudio {
            border-radius: 15px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ------------------ MAIN APPLICATION ------------------
def main():
    # Apply modern styles
    apply_modern_styles()
    
    # Modern header
    st.markdown(
        """
        <div style='text-align: center; padding: 30px 0; margin-bottom: 20px;'>
            <h1 class='main-title'>🎵 EchoVerse</h1>
            <p class='subtitle'>Transform your text into captivating audio experiences ✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Modern divider
    st.markdown(
        """
        <div style='height: 3px; 
                     background: linear-gradient(90deg, transparent, #FFD700, #FF8C00, #FF6347, #FF8C00, #FFD700, transparent); 
                     margin: 40px auto; border-radius: 2px; width: 70%; 
                     box-shadow: 0 2px 10px rgba(255, 215, 0, 0.4);'></div>
        """,
        unsafe_allow_html=True,
    )
    
    # Enhanced sidebar
    st.sidebar.markdown(
        """
        <div style='text-align: center; padding: 25px 15px; 
                     background: rgba(255, 255, 255, 0.05); border-radius: 20px; 
                     margin-bottom: 25px; backdrop-filter: blur(10px);'>
            <h2 style='color: #FFD700; margin: 0; font-weight: 700;'>✨ Control Center</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    uploaded_file = st.sidebar.file_uploader("📄 Upload Text File", type=["txt"])
    input_text = st.sidebar.text_area("✏ Paste Your Text", height=150, placeholder="Paste your amazing content here...")
    
    st.sidebar.markdown("### 🎭 Audio Customization")
    # Correct tone selection as per the solution document
    tone = st.sidebar.selectbox("🎭 Voice Tone", ["Neutral", "Suspenseful", "Inspiring"])
    
    # Multi-voice selection as per the solution document
    voice = st.sidebar.selectbox("🎤 Voice Character", 
        ["Voice A - Warm & Natural", "Voice B - Bold & Dramatic", "Voice C - Calm & Soothing", "Voice D - Energetic & Upbeat"])
    
    # Session state to store output for persistence
    if 'rewritten_text' not in st.session_state:
        st.session_state.rewritten_text = ""
    if 'audio_bytes' not in st.session_state:
        st.session_state.audio_bytes = None
    
    st.sidebar.markdown("### 🎯 Actions")
    audio_clicked = st.sidebar.button("🎙 Generate Audio")
    
    if audio_clicked:
        # Get content from either file or text area
        content = ""
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
        elif input_text.strip():
            content = input_text
        
        if content:
            with st.spinner("⏳ Processing..."):
                # 1. Tone-Adaptive Text Rewriting (now uses the hybrid function)
                rewritten = rewrite_text_with_llm(content, tone)
                st.session_state.rewritten_text = rewritten

                # 2. Voice Narration (using placeholder function)
                audio = text_to_speech(rewritten, voice)
                st.session_state.audio_bytes = audio
            
            if st.session_state.audio_bytes:
                st.success("🎶 Audio Generation Complete!")
                trigger_mega_confetti()
                st.balloons()
            else:
                st.error("❌ Audio generation failed. Please check your credentials and try again.")
            
        else:
            st.warning("⚠ Please provide text to generate audio!")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📄 Text Studio", "🎧 Audio Center", "📊 Analytics Hub"])
    
    with tab1:
        st.markdown("### 📝 Text Transformation Studio")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Original Content")
            original_content = ""
            if uploaded_file:
                original_content = uploaded_file.read().decode("utf-8")
            elif input_text.strip():
                original_content = input_text
            
            if original_content:
                st.markdown(f'<div class="modern-card"><p class="text-content">{original_content}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="modern-card" style="text-align: center; padding: 50px;"><p style="color: rgba(255,255,255,0.6); font-style: italic; font-size: 18px;">📝 Your original content will appear here...</p></div>', 
                    unsafe_allow_html=True
                )
        
        with col2:
            st.markdown("#### ✨ AI-Enhanced Version")
            if st.session_state.rewritten_text:
                st.markdown(f'<div class="modern-card"><p class="text-content">{st.session_state.rewritten_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="modern-card" style="text-align: center; padding: 50px;"><p style="color: rgba(255,255,255,0.6); font-style: italic; font-size: 18px;">✨ AI-enhanced text will appear here after generation...</p></div>', 
                    unsafe_allow_html=True
                )
    
    with tab2:
        st.markdown("### 🎧 Premium Audio Experience")
        if st.session_state.audio_bytes:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown(
                    '<div class="modern-card" style="text-align: center; padding: 30px;">',
                    unsafe_allow_html=True
                )
                st.audio(st.session_state.audio_bytes, format="audio/mp3")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.download_button("📥 Download MP3", data=st.session_state.audio_bytes, file_name="echoverse_audio.mp3", mime="audio/mp3")
                with col_b:
                    st.download_button("📱 Download for Mobile", data=st.session_state.audio_bytes, file_name="echoverse_mobile.mp3", mime="audio/mp3")
                with col_c:
                    st.button("📤 Share")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="modern-card" style="text-align: center; padding: 50px;"><p style="color: rgba(255,255,255,0.7); font-size: 20px;">🎵 Your audio masterpiece will appear here after generation...</p></div>', 
                unsafe_allow_html=True
            )
    
    with tab3:
        st.markdown("### 📊 Intelligent Text Analytics")
        content = ""
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
        elif input_text.strip():
            content = input_text
        
        if content:
            words = content.split()
            word_count = len(words)
            char_count = len(content)
            sentences = content.count('.') + content.count('!') + content.count('?')
            paragraphs = len([p for p in content.split('\n\n') if p.strip()])
            reading_time = max(1, word_count // 200)
            audio_duration = max(1, word_count // 150)
            
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            complexity_score = min(100, int((avg_word_length * 10) + (sentences / len(words) * 1000) if words else 0))
            
            col1, col2, col3, col4 = st.columns(4)
            
            stats = [
                (word_count, "Words", "linear-gradient(135deg, #FFD700, #FFA500)", "📝"),
                (char_count, "Characters", "linear-gradient(135deg, #FF6347, #FF4500)", "🔤"),
                (sentences, "Sentences", "linear-gradient(135deg, #32CD32, #228B22)", "📖"),
                (f"{reading_time}m", "Read Time", "linear-gradient(135deg, #1E90FF, #0066CC)", "⏱")
            ]
            
            for i, (value, label, gradient, icon) in enumerate(stats):
                with [col1, col2, col3, col4][i]:
                    st.markdown(
                        f"""
                        <div class="stat-card" style="background: {gradient};">
                            <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                            <h2 style="margin: 5px 0; font-size: 2.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{value}</h2>
                            <p style="margin: 0; opacity: 0.95; font-weight: 600; font-size: 16px;">{label}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.markdown("### 🧠 AI Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4 style="color: #FFD700; margin-bottom: 15px;">📈 Content Analysis</h4>
                        <p class="text-content"><strong>Complexity Score:</strong> {complexity_score}/100</p>
                        <p class="text-content"><strong>Estimated Audio Duration:</strong> {audio_duration} minutes</p>
                        <p class="text-content"><strong>Average Word Length:</strong> {avg_word_length:.1f} characters</p>
                        <p class="text-content"><strong>Document Structure:</strong> {paragraphs} paragraphs</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4 style="color: #FFD700; margin-bottom: 15px;">💡 AI Recommendations</h4>
                        <p class="text-content">{'✅ Perfect for audio conversion!' if word_count > 50 else '⚠ Consider adding more content'}</p>
                        <p class="text-content">{'📚 Great for storytelling tone' if sentences > 5 else '📰 Suitable for informational tone'}</p>
                        <p class="text-content">{'🎯 Optimal length for engagement' if 100 <= word_count <= 500 else '📝 Consider adjusting length'}</p>
                        <p class="text-content">{'📊 Recommended speed: 1.0x' if complexity_score < 50 else '📊 Recommended speed: 0.8x'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        else:
            st.markdown(
                '<div class="modern-card" style="text-align: center; padding: 50px;"><p style="color: rgba(255,255,255,0.7); font-size: 20px;">📊 Intelligent analytics will appear here...</p></div>', 
                unsafe_allow_html=True
            )
    
    st.markdown(
        """
        <div style='margin-top: 80px; padding: 50px 30px; 
                     background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 33, 62, 0.8)); 
                     border-radius: 30px; text-align: center; 
                     backdrop-filter: blur(20px); 
                     border: 1px solid rgba(255, 215, 0, 0.2);
                     box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);'>
            <h2 style='color: #FFD700; margin-bottom: 25px; font-weight: 800; font-size: 2.5rem;'>
                🚀 EchoVerse
            </h2>
            <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.4rem; margin: 20px 0; font-weight: 400;'>
                Team SYNTRIX | Next-Generation Audio Intelligence ✨
            </p>
            <div style='margin: 30px 0; display: flex; justify-content: center; flex-wrap: wrap; gap: 20px;'>
                <div style='padding: 15px 30px; background: rgba(255, 215, 0, 0.1); 
                           border-radius: 30px; border: 1px solid rgba(255, 215, 0, 0.3);'>
                    <span style='color: #FFD700; font-weight: 600; font-size: 1.1rem;'>🎵 Advanced AI Engine</span>
                </div>
                <div style='padding: 15px 30px; background: rgba(255, 140, 0, 0.1); 
                           border-radius: 30px; border: 1px solid rgba(255, 140, 0, 0.3);'>
                    <span style='color: #FF8C00; font-weight: 600; font-size: 1.1rem;'>🔊 Premium Audio Quality</span>
                </div>
                <div style='padding: 15px 30px; background: rgba(255, 99, 71, 0.1); 
                           border-radius: 30px; border: 1px solid rgba(255, 99, 71, 0.3);'>
                    <span style='color: #FF6347; font-weight: 600; font-size: 1.1rem;'>✨ Smart Text Processing</span>
                </div>
            </div>
            <div style='margin-top: 30px; padding-top: 30px; 
                         border-top: 1px solid rgba(255, 255, 255, 0.1);'>
                <p style='color: rgba(255, 255, 255, 0.6); font-size: 1rem; margin: 0;'>
                    © 2025 EchoVerse | Powered by Advanced AI | Built for Hackathon Excellence
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
if __name__ == "__main__":
    main()