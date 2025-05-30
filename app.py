import streamlit as st
import subprocess
import sys
import time

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

# Configuration de la page
st.set_page_config(
    page_title="LeoForge",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne sombre
st.markdown("""
<style>
    /* Variables CSS pour le thème sombre */
    :root {
        --primary-color: #8b5cf6;
        --primary-hover: #7c3aed;
        --secondary-color: #1f2937;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --background-dark: #0f172a;
        --card-background: #1e293b;
        --border-color: #334155;
        --background-gradient: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
        --hero-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Cache le header et footer par défaut de Streamlit */
    .stApp > header {visibility: hidden;}
    .stApp > footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Style général de l'app - Thème sombre */
    .stApp {
        background: var(--background-dark);
        color: var(--text-primary);
    }
    
    /* Override Streamlit default styles pour le thème sombre */
    .stApp, .main, .block-container {
        background-color: var(--background-dark) !important;
        color: var(--text-primary) !important;
    }
    
    /* Container principal */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Header moderne - Version sombre */
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: var(--hero-gradient);
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto;
        color: rgba(255,255,255,0.9);
    }
    
    /* Card style pour les sections - Version sombre */
    .card {
        background: var(--card-background);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        color: var(--text-primary);
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.2);
        border-color: var(--primary-color);
    }
    
    /* Style pour les inputs - Version sombre */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid var(--border-color) !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        background-color: var(--card-background) !important;
        color: var(--text-primary) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        background-color: var(--card-background) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Labels et textes */
    .stTextArea label, .stMarkdown, .stText {
        color: var(--text-primary) !important;
    }
    
    /* Bouton personnalisé - Version sombre */
    .stButton button {
        background: var(--background-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Zone de code améliorée - Version sombre */
    .stCode {
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        background-color: var(--card-background) !important;
    }
    
    .stCode code {
        background-color: var(--card-background) !important;
        color: var(--text-primary) !important;
    }
    
    /* Spinner personnalisé */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* Métriques - Version sombre */
    .metric-container {
        background: var(--card-background);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    [data-testid="metric-container"] {
        background: var(--card-background) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    [data-testid="metric-container"] label, 
    [data-testid="metric-container"] div {
        color: var(--text-primary) !important;
    }
    
    /* Features grid - Version sombre */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Footer moderne - Version sombre */
    .modern-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
        background: var(--card-background);
        border-radius: 12px;
        color: var(--text-secondary);
    }
    
    /* Onglets personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--card-background) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        margin: 0 0.25rem !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Messages d'alerte - Version sombre */
    .stAlert {
        background-color: var(--card-background) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
    }
    
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-color: var(--success-color) !important;
        color: var(--success-color) !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-color: var(--warning-color) !important;
        color: var(--warning-color) !important;
    }
    
    /* Progress bar - Version sombre */
    .stProgress > div > div {
        background-color: var(--primary-color) !important;
    }
    
    .stProgress > div {
        background-color: var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    /* Animation de typing */
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    .typing-text {
        overflow: hidden;
        border-right: .15em solid var(--primary-color);
        white-space: nowrap;
        margin: 0 auto;
        animation: typing 3.5s steps(40, end);
    }
</style>
""", unsafe_allow_html=True)

# Structure de l'application
def main():
    # Logo LeoForge intégré
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <svg width="80" height="80" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 1rem;">
            <defs>
                <linearGradient id="brandGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#16a34a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#15803d;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#84cc16;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#65a30d;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="energyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:1" />
                </linearGradient>
                <filter id="premiumShadow" x="-50%" y="-50%" width="200%" height="200%">
                    <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#15803d" flood-opacity="0.4"/>
                </filter>
                <filter id="brandGlow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge> 
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
                <pattern id="texture" patternUnits="userSpaceOnUse" width="4" height="4">
                    <rect width="4" height="4" fill="url(#brandGradient)"/>
                    <circle cx="2" cy="2" r="0.5" fill="#ffffff" opacity="0.1"/>
                </pattern>
            </defs>
            <circle cx="60" cy="60" r="50" fill="url(#texture)" filter="url(#premiumShadow)"/>
            <circle cx="60" cy="60" r="45" fill="none" stroke="url(#accentGradient)" stroke-width="1" opacity="0.6" stroke-dasharray="8,4">
                <animateTransform attributeName="transform" type="rotate" values="0 60 60;360 60 60" dur="20s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="55" fill="none" stroke="url(#accentGradient)" stroke-width="0.5" opacity="0.4" stroke-dasharray="4,8">
                <animateTransform attributeName="transform" type="rotate" values="360 60 60;0 60 60" dur="30s" repeatCount="indefinite"/>
            </circle>
            <g transform="translate(60, 60)">
                <path d="M -18 -22 L -18 12 L 18 12 L 18 2 L -8 2 L -8 -22 Z" fill="#ffffff" opacity="0.95"/>
                <path d="M -18 -22 L -15 -19 L -15 5 L 15 5 L 15 2 L -8 2 L -8 -22 Z" fill="#ffffff" opacity="0.7"/>
                <polygon points="-8,-12 -3,-12 -3,-7 -8,-7" fill="url(#energyGradient)" filter="url(#brandGlow)"/>
                <circle cx="15" cy="-15" r="3" fill="url(#energyGradient)" filter="url(#brandGlow)"/>
                <path d="M 12 -12 L 18 -18 M 15 -9 L 21 -15 M 18 -6 L 24 -12" stroke="url(#accentGradient)" stroke-width="1.5" opacity="0.8"/>
            </g>
            <g opacity="0.8">
                <rect x="25" y="30" width="4" height="4" rx="1" fill="url(#accentGradient)" transform="rotate(45 27 32)">
                    <animateTransform attributeName="transform" type="rotate" values="45 27 32;405 27 32" dur="8s" repeatCount="indefinite"/>
                </rect>
                <polygon points="90,35 94,31 98,35 94,39" fill="url(#energyGradient)">
                    <animateTransform attributeName="transform" type="rotate" values="0 94 35;360 94 35" dur="12s" repeatCount="indefinite"/>
                </polygon>
                <circle cx="30" cy="85" r="2.5" fill="url(#accentGradient)">
                    <animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/>
                </circle>
                <rect x="85" y="85" width="6" height="2" rx="1" fill="url(#energyGradient)" transform="rotate(30 88 86)">
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" repeatCount="indefinite"/>
                </rect>
            </g>
            <circle cx="60" cy="60" r="52" fill="none" stroke="url(#brandGradient)" stroke-width="2" opacity="0.3"/>
            <g opacity="0.6">
                <circle cx="60" cy="15" r="1" fill="url(#energyGradient)">
                    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="4s" repeatCount="indefinite"/>
                </circle>
                <circle cx="105" cy="60" r="0.8" fill="url(#accentGradient)">
                    <animate attributeName="opacity" values="0.8;0.3;0.8" dur="5s" repeatCount="indefinite"/>
                </circle>
                <circle cx="60" cy="105" r="1.2" fill="url(#energyGradient)">
                    <animate attributeName="opacity" values="0.4;0.9;0.4" dur="3.5s" repeatCount="indefinite"/>
                </circle>
                <circle cx="15" cy="60" r="0.9" fill="url(#accentGradient)">
                    <animate attributeName="opacity" values="0.9;0.4;0.9" dur="4.5s" repeatCount="indefinite"/>
                </circle>
            </g>
        </svg>
    </div>
    
    <div class="hero-section">
        <div class="hero-title">LeoForge</div>
        <div class="hero-subtitle">
            Transformez vos idées en code Leo avec l'intelligence artificielle.<br>
            Créez des smart contracts puissants en quelques secondes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💭 Décrivez votre projet")
        st.markdown("*Expliquez ce que vous souhaitez créer et LeoForge générera le code Leo correspondant.*")
        
        # Zone de texte avec exemples
        user_query = st.text_area(
            "",
            placeholder="Exemple: Créer un token avec des fonctions de mint, burn et transfer, incluant un système de governance...",
            height=150,
            help="Plus votre description est détaillée, meilleur sera le résultat !"
        )
        
        # Suggestions rapides
        st.markdown("**💡 Suggestions rapides:**")
        suggestions = [
            "Token ERC-20 avec staking",
            "NFT avec marketplace",
            "Système de vote décentralisé",
            "DeFi yield farming"
        ]
        
        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"sugg_{i}"):
                    st.session_state.user_query = suggestion
                    st.rerun()
        
        # Bouton principal
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Zone de génération
        if st.button("🚀 Forger le projet", use_container_width=True):
            if not user_query:
                st.warning("⚠️ Veuillez décrire votre projet avant de continuer.")
            else:
                forge_project(user_query)
    
    with col2:
        # Sidebar avec informations
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Statistiques")
        
        # Métriques factices pour l'exemple
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Projets générés", "1,234", "+23")
        with col_b:
            st.metric("Utilisateurs", "456", "+12")
        
        st.markdown("### 🎯 Fonctionnalités")
        features = [
            ("⚡", "Génération rapide"),
            ("🔒", "Code sécurisé"),
            ("📝", "Documentation auto"),
            ("🧪", "Tests inclus")
        ]
        
        for icon, feature in features:
            st.markdown(f"**{icon} {feature}**")
        
        st.markdown("</div>", unsafe_allow_html=True)

def forge_project(query):
    """Gère le processus de génération avec un design amélioré"""
    
    # Progress bar animée
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Animation du progress
    for i in range(100):
        progress_bar.progress(i + 1)
        if i < 30:
            status_text.text("🔍 Analyse de votre demande...")
        elif i < 60:
            status_text.text("🧠 Génération du code Leo...")
        elif i < 90:
            status_text.text("⚙️ Optimisation et validation...")
        else:
            status_text.text("✨ Finalisation...")
        time.sleep(0.02)  # Animation plus fluide
    
    # Simulation d'attente (remplacez par votre vraie fonction)
    with st.spinner("🔥 Forge en cours... Cela peut prendre quelques minutes."):
        try:
            output = run_leoforge_generate(query)
            
            # Nettoyage de la barre de progress
            progress_bar.empty()
            status_text.empty()
            
            # Affichage des résultats
            st.success("✅ Projet généré avec succès !")
            
            # Tabs pour organiser l'output
            tab1, tab2, tab3 = st.tabs(["📄 Code généré", "📋 Logs", "📚 Documentation"])
            
            with tab1:
                st.markdown("### 🎉 Votre projet Leo est prêt !")
                st.code(output, language='rust')
                
                # Boutons d'action
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button("💾 Télécharger", output, file_name="project.leo")
                with col2:
                    if st.button("📋 Copier"):
                        st.success("Code copié !")
                with col3:
                    if st.button("🔄 Régénérer"):
                        forge_project(query)
            
            with tab2:
                st.markdown("### 📊 Logs de génération")
                st.text(output)
            
            with tab3:
                st.markdown("### 📖 Comment utiliser votre code")
                st.markdown("""
                **Étapes suivantes :**
                1. Téléchargez le code généré
                2. Testez-le dans votre environnement Leo
                3. Personnalisez selon vos besoins
                4. Déployez sur le réseau Aleo
                """)
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Erreur lors de la génération: {str(e)}")

# Footer moderne
def render_footer():
    st.markdown("""
    <div class="modern-footer">
        <p style="margin: 0; color: var(--text-secondary);">
            Conçu avec ❤️ pour la communauté Leo • 
            <a href="https://github.com/yourusername/LeoForge" style="color: var(--primary-color); text-decoration: none;">
                GitHub
            </a> • 
            <a href="#" style="color: var(--primary-color); text-decoration: none;">
                Documentation
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    render_footer()