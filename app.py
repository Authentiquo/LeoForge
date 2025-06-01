import streamlit as st
import subprocess
import sys
import time
import asyncio
from src.streamlit_bridge import generate_with_status

def run_leoforge_generate(query: str):
    """Runs the leoforge generate command with the given query."""
    command = ["./launch.sh", "generate", query, "--no-interactive"]
    
    process = subprocess.Popen(
        command,
        cwd=".",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    output = []
    for line in process.stdout:
        output.append(line)

    process.wait()
    return "".join(output)

# Page configuration
st.set_page_config(
    page_title="LeoForge - AI Smart Contract Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

# Custom CSS with particles and animations
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root variables */
    :root {
        --primary-color: #00D9FF;
        --primary-dark: #00A8CC;
        --secondary-color: #7B61FF;
        --accent-color: #FF6B6B;
        --success-color: #4ECDC4;
        --warning-color: #FFE66D;
        --background-dark: #0A0E27;
        --background-secondary: #151A3A;
        --card-background: rgba(21, 26, 58, 0.6);
        --glass-background: rgba(255, 255, 255, 0.05);
        --border-color: rgba(255, 255, 255, 0.1);
        --text-primary: #FFFFFF;
        --text-secondary: #B8BCC8;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #00D9FF 0%, #7B61FF 100%);
        --gradient-3: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        --shadow-glow: 0 0 40px rgba(0, 217, 255, 0.3);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #0A0E27, #151A3A, #1A1F4E, #0F1430);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: var(--text-primary);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles background */
    .particles-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        display: block;
        width: 4px;
        height: 4px;
        background: #00D9FF;
        border-radius: 50%;
        opacity: 0;
        animation: float-up 20s infinite;
    }
    
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; }
    .particle:nth-child(2) { left: 20%; animation-delay: 2s; background: #7B61FF; }
    .particle:nth-child(3) { left: 30%; animation-delay: 4s; }
    .particle:nth-child(4) { left: 40%; animation-delay: 6s; background: #FF6B6B; }
    .particle:nth-child(5) { left: 50%; animation-delay: 8s; }
    .particle:nth-child(6) { left: 60%; animation-delay: 10s; background: #7B61FF; }
    .particle:nth-child(7) { left: 70%; animation-delay: 12s; }
    .particle:nth-child(8) { left: 80%; animation-delay: 14s; background: #4ECDC4; }
    .particle:nth-child(9) { left: 90%; animation-delay: 16s; }
    
    @keyframes float-up {
        0% {
            transform: translateY(100vh) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 0.6;
        }
        90% {
            opacity: 0.6;
        }
        100% {
            transform: translateY(-10vh) translateX(100px);
            opacity: 0;
        }
    }
    
    /* Main container adjustments */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        position: relative;
        z-index: 1;
    }
    
    /* Glassmorphism card with hover effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 217, 255, 0.15);
        padding: 2rem;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-glow);
        border-color: var(--primary-color);
    }
    
    /* Hero section with animation */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 3rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-bg-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(0, 217, 255, 0.1) 0%, transparent 70%);
        transform: translate(-50%, -50%);
        animation: pulse 4s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.5;
        }
        50% { 
            transform: translate(-50%, -50%) scale(1.1);
            opacity: 0.8;
        }
    }
    
    /* Hero title with safe gradient */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #00D9FF;
        text-shadow: 0 0 40px rgba(0, 217, 255, 0.5);
        letter-spacing: -2px;
        animation: glow 2s ease-in-out infinite alternate;
        display: inline-block;
        background-image: linear-gradient(135deg, #00D9FF 0%, #7B61FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes glow {
        from { 
            filter: drop-shadow(0 0 20px rgba(0, 217, 255, 0.5));
        }
        to { 
            filter: drop-shadow(0 0 30px rgba(123, 97, 255, 0.8));
        }
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 300;
        color: #B8BCC8;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
        opacity: 0;
        animation: fadeInUp 1s ease-out 0.5s forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Logo animation */
    .logo-container {
        margin-bottom: 2rem;
        animation: logoFloat 3s ease-in-out infinite;
    }
    
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Modern input styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        padding: 1.25rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00D9FF !important;
        box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.2), var(--shadow-glow) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Modern button design with hover animation */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #7B61FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.875rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 217, 255, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(0, 217, 255, 0.5) !important;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    /* Code block styling */
    .stCode {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }
    
    /* Metrics with animation */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: scale(1.05);
        border-color: var(--primary-color);
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
    }
    
    /* Feature cards with hover */
    .feature-item {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        transform: translateX(10px);
        border-color: #00D9FF;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Progress bar animated */
    .stProgress > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        height: 8px !important;
        overflow: hidden !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(135deg, #00D9FF 0%, #7B61FF 100%) !important;
        height: 100% !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.5) !important;
        animation: shimmer 2s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
        100% { filter: brightness(1); }
    }
    
    /* Loading animation */
    .loading-dots span {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--primary-color);
        margin: 0 4px;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
    .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
    .loading-dots span:nth-child(3) { animation-delay: 0; }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

# Add particles background
particles_html = """<div class="particles-bg">
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
    <span class="particle"></span>
</div>"""
st.markdown(particles_html, unsafe_allow_html=True)

# Application structure
def main():
    # Hero section with animated logo - Using simpler structure
    logo_svg = """<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00D9FF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#7B61FF;stop-opacity:1" />
            </linearGradient>
            <filter id="blur1">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <g>
            <circle cx="50" cy="50" r="45" fill="none" stroke="url(#lg1)" stroke-width="2" opacity="0.3">
                <animate attributeName="r" values="45;48;45" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="50" cy="50" r="35" fill="none" stroke="url(#lg1)" stroke-width="1" opacity="0.5" stroke-dasharray="5,5">
                <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="20s" repeatCount="indefinite"/>
            </circle>
            <path d="M 35 30 L 45 45 L 38 45 L 48 65 L 65 35 L 55 35 L 60 20 Z" 
                  fill="url(#lg1)" 
                  filter="url(#blur1)"
                  opacity="0.9">
                <animate attributeName="opacity" values="0.9;1;0.9" dur="2s" repeatCount="indefinite"/>
            </path>
            <circle cx="30" cy="30" r="2" fill="#00D9FF" opacity="0.8">
                <animate attributeName="opacity" values="0;0.8;0" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="70" cy="25" r="1.5" fill="#7B61FF" opacity="0.8">
                <animate attributeName="opacity" values="0;0.8;0" dur="3s" begin="1s" repeatCount="indefinite"/>
            </circle>
            <circle cx="75" cy="70" r="2" fill="#00D9FF" opacity="0.8">
                <animate attributeName="opacity" values="0;0.8;0" dur="3s" begin="2s" repeatCount="indefinite"/>
            </circle>
        </g>
    </svg>"""
    
    # Display hero section with safe HTML
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-bg-glow"></div>
        <div class="logo-container">
            {logo_svg}
        </div>
        <div class="hero-title">LeoForge</div>
        <p class="hero-subtitle">
            Next-generation AI-powered smart contract development.
            Build, deploy, and scale with confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Create Your Smart Contract")
        st.markdown("*Describe your vision and let our AI transform it into production-ready Leo code.*")
        
        # Text input
        user_query = st.text_area(
            "Describe your smart contract",
            placeholder="Example: Build a NFT marketplace...",
            height=150,
            help="Be specific about features, tokenomics, and technical requirements for best results.",
            key="main_query",
            label_visibility="collapsed"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate button
        if st.button("⚡ Generate Smart Contract", use_container_width=True):
            if not user_query:
                st.warning("⚠️ Please describe your project before generating.")
            else:
                forge_project(user_query)
    
    with col2:
        # Stats section
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Platform Stats")
        
        st.metric("Active Projects", "2,847", "+127")
        st.metric("Total Value Locked", "$12.4M", "+8.3%")
        
        st.markdown("### ✨ Features")
        
        features = [
            ("⚡", "Lightning Fast"),
            ("🛡️", "Security First"),
            ("📊", "Gas Optimized"),
            ("🔄", "Auto Testing")
        ]
        
        for icon, feature in features:
            st.markdown(f"""<div class="feature-item">
                <span style="font-size: 1.5rem;">{icon}</span>
                <span>{feature}</span>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def forge_project(query):
    """Handles the generation process with modern animations"""
    
    # Create containers for dynamic content
    progress_bar = st.progress(0)
    status_container = st.container()
    
    # Run the async generation with status updates
    try:
        # Run the async function in the sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            generate_with_status(query, None, status_container, progress_bar)
        )
        
        # Clear progress bar after completion
        progress_bar.empty()
        
        if result.success:
            # Success message
            st.success("✅ Smart contract generated successfully!")
            
            # Results tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Smart Contract", "🔍 Analysis", "📊 Gas Report", "📚 Documentation"])
            
            with tab1:
                st.markdown("### 🎉 Your Smart Contract is Ready!")
                
                # Show the final code
                if result.final_code:
                    st.code(result.final_code, language='rust')
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            "⬇️ Download Contract",
                            result.final_code,
                            file_name=f"{result.project_name}.leo",
                            mime="text/plain"
                        )
                    with col2:
                        if st.button("📋 Copy to Clipboard"):
                            st.success("✅ Copied to clipboard!")
                    with col3:
                        if st.button("🔄 Regenerate"):
                            forge_project(query)
                else:
                    st.error("No code was generated")
            
            with tab2:
                st.markdown("### 🔍 Code Analysis")
                
                # Show evaluation from the last iteration
                if result.iterations:
                    last_eval = result.iterations[-1].evaluation
                    score_color = "🟢" if last_eval.score >= 7 else "🟡" if last_eval.score >= 5 else "🔴"
                    st.info(f"{score_color} Code Quality Score: **{last_eval.score:.1f}/10**")
                    st.info(f"✅ Features Complete: **{'Yes' if last_eval.is_complete else 'No'}**")
                    st.info(f"🐛 Has Errors: **{'No' if not last_eval.has_errors else 'Yes'}**")
                    
                    if last_eval.missing_features:
                        st.warning("**Missing Features:**")
                        for feature in last_eval.missing_features:
                            st.write(f"• {feature}")
                
                st.info(f"🔄 Total Iterations: **{result.total_iterations}**")
                st.info(f"⏱️ Generation Time: **{result.total_duration:.2f}s**")
            
            with tab3:
                st.markdown("### 📊 Build Report")
                
                # Show build information from iterations
                build_attempts = 0
                successful_builds = 0
                
                for iteration in result.iterations:
                    if iteration.build:
                        build_attempts += 1
                        if iteration.build.success:
                            successful_builds += 1
                
                st.metric("Build Attempts", build_attempts)
                st.metric("Successful Builds", successful_builds)
                
                if result.iterations and result.iterations[-1].build:
                    last_build = result.iterations[-1].build
                    st.metric("Final Build Time", f"{last_build.build_time:.2f}s")
            
            with tab4:
                st.markdown("### 📚 Getting Started")
                st.markdown(f"""
                **🚀 Your Project is Ready!**
                
                Project Name: `{result.project_name}`
                
                Location: `{result.workspace_path}`
                
                **Next Steps:**
                
                1. **Navigate to your project**
                   ```bash
                   cd output/{result.project_name}
                   ```
                
                2. **Review the code**
                   ```bash
                   cat src/main.leo
                   ```
                
                3. **Test your contract**
                   ```bash
                   leo test
                   ```
                
                4. **Deploy to Aleo**
                   ```bash
                   leo deploy
                   ```
                """)
                
        else:
            st.error(f"❌ Generation failed: {result.error_message}")
            st.info("💡 Try refining your description or check the error details above.")
            
            # Show iteration history if available
            if result.iterations:
                with st.expander("View Generation History"):
                    for iteration in result.iterations:
                        st.write(f"**Iteration {iteration.iteration_number}:**")
                        st.write(f"• Score: {iteration.evaluation.score:.1f}/10")
                        st.write(f"• Build: {'✅ Success' if iteration.success else '❌ Failed'}")
                        if iteration.build and iteration.build.errors:
                            st.write("• Errors:")
                            for error in iteration.build.errors[:3]:
                                st.code(error, language='text')
                
    except Exception as e:
        progress_bar.empty()
        status_container.empty()
        st.error(f"❌ Generation failed: {str(e)}")
        st.info("💡 Try refining your description or contact support.")

# Modern footer
def render_footer():
    st.markdown("""
    <div class="modern-footer" style="text-align: center; padding: 3rem 2rem; margin-top: 4rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: #B8BCC8;">
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
            <a href="https://github.com/leoforge" style="color: #00D9FF; text-decoration: none; font-weight: 600;">GitHub</a>
            <a href="#" style="color: #00D9FF; text-decoration: none; font-weight: 600;">Documentation</a>
            <a href="#" style="color: #00D9FF; text-decoration: none; font-weight: 600;">Community</a>
        </div>
        <p style="margin: 0; opacity: 0.7;">
            Built with ⚡ by LeoForge Team | Powered by Aleo
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    render_footer()