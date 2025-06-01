"""
Streamlit Bridge - Interface between Streamlit app and LeoForge orchestrator
"""
import asyncio
from typing import Optional, Callable, Dict, Any
import streamlit as st
from src.models import UserQuery, ProjectType, ProjectResult
from src.workflow.orchestrator import ProjectOrchestrator
from src.config import get_config
import time

class StreamlitOrchestrator:
    """Bridge between Streamlit and the LeoForge orchestrator"""
    
    def __init__(self, status_container, progress_bar=None):
        self.status_container = status_container
        self.progress_bar = progress_bar
        self.status_history = []
        self.status_elements = []  # Keep track of status elements
        
    def handle_status_update(self, status_type: str, data: Dict[str, Any]):
        """Handle status updates from orchestrator and display in Streamlit"""
        
        # Store status in history
        self.status_history.append({
            "type": status_type,
            "data": data,
            "timestamp": time.time()
        })
        
        # Clear old statuses for certain types to avoid clutter
        if status_type in ["code_generation_start", "code_fix_start", "evaluation_start", "build_start"]:
            # Keep only the last 3 status messages
            if len(self.status_elements) > 3:
                self.status_container.empty()
                self.status_elements = []
        
        # Create a new container for this status
        status_elem = self.status_container.container()
        self.status_elements.append(status_elem)
        
        # Update UI based on status type
        if status_type == "start":
            status_elem.markdown(f"""
            <div class="glass-card" style="text-align: center; margin-bottom: 1rem;">
                <h3>🚀 Starting LeoForge Generation</h3>
                <p style="color: #B8BCC8;">Query: {data['query'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif status_type == "architecture_start":
            status_elem.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">🏗️</div>
                    <div>
                        <h4 style="margin: 0; color: #00D9FF;">Designing Architecture</h4>
                        <p style="margin: 0; color: #B8BCC8;">Analyzing requirements and creating project structure...</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if self.progress_bar:
                self.progress_bar.progress(10)
                
        elif status_type == "architecture_complete":
            features_html = "".join([f"<li>{f}</li>" for f in data['features'][:3]])
            status_elem.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #4ECDC4; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 2rem;">✅</div>
                    <div>
                        <h4 style="margin: 0; color: #4ECDC4;">Architecture Complete</h4>
                        <p style="margin: 0; color: #B8BCC8;">Project: <strong>{data['project_name']}</strong> ({data['project_type']})</p>
                    </div>
                </div>
                <div style="margin-left: 3rem;">
                    <p style="color: #B8BCC8; margin-bottom: 0.5rem;">Key Features:</p>
                    <ul style="color: #B8BCC8; margin: 0; padding-left: 1.5rem;">
                        {features_html}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if self.progress_bar:
                self.progress_bar.progress(20)
                
        elif status_type == "workspace_start":
            status_elem.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">📁</div>
                    <div>
                        <h4 style="margin: 0; color: #00D9FF;">Creating Workspace</h4>
                        <p style="margin: 0; color: #B8BCC8;">Setting up project structure and dependencies...</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if self.progress_bar:
                self.progress_bar.progress(25)
                
        elif status_type == "code_generation_start":
            status_elem.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">✨</div>
                    <div>
                        <h4 style="margin: 0; color: #7B61FF;">Generating Code - Iteration {data['iteration']}</h4>
                        <p style="margin: 0; color: #B8BCC8;">{data['message']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if self.progress_bar:
                progress = 30 + (data['iteration'] - 1) * 15
                self.progress_bar.progress(min(progress, 90))
                
        elif status_type == "code_fix_start":
            status_elem.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">🔧</div>
                    <div>
                        <h4 style="margin: 0; color: #FFE66D;">Fixing Errors - Iteration {data['iteration']}</h4>
                        <p style="margin: 0; color: #B8BCC8;">{data['message']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif status_type == "evaluation_complete":
            score_color = "#4ECDC4" if data['score'] >= 7 else "#FFE66D" if data['score'] >= 5 else "#FF6B6B"
            status_elem.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {score_color}; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">🔍</div>
                    <div>
                        <h4 style="margin: 0; color: {score_color};">Code Quality Score: {data['score']:.1f}/10</h4>
                        <p style="margin: 0; color: #B8BCC8;">
                            Complete: {'✅' if data['is_complete'] else '❌'} | 
                            Errors: {'❌' if data['has_errors'] else '✅'}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif status_type == "build_complete":
            if data['success']:
                status_elem.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #4ECDC4; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">✅</div>
                        <div>
                            <h4 style="margin: 0; color: #4ECDC4;">Build Successful!</h4>
                            <p style="margin: 0; color: #B8BCC8;">Build time: {data['build_time']:.2f}s</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                errors_html = "".join([f"<li style='color: #FF6B6B;'>{e[:100]}...</li>" for e in data.get('errors', [])[:2]])
                status_elem.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #FF6B6B; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">❌</div>
                        <div>
                            <h4 style="margin: 0; color: #FF6B6B;">Build Failed</h4>
                            {f'<ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">{errors_html}</ul>' if errors_html else ''}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        elif status_type == "success":
            # Clear previous statuses for the final success message
            self.status_container.empty()
            status_elem = self.status_container.container()
            
            status_elem.markdown(f"""
            <div class="glass-card" style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.1), rgba(123, 97, 255, 0.1)); border: 2px solid #4ECDC4; margin-bottom: 1rem;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                    <h3 style="color: #4ECDC4; margin: 0;">{data['message']}</h3>
                    <p style="color: #B8BCC8; margin: 0.5rem 0 0 0;">Completed in {data['iterations']} iteration(s)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if self.progress_bar:
                self.progress_bar.progress(100)
                
        elif status_type == "error":
            # Clear previous statuses for error message
            self.status_container.empty()
            status_elem = self.status_container.container()
            
            status_elem.markdown(f"""
            <div class="glass-card" style="border: 2px solid #FF6B6B; background: rgba(255, 107, 107, 0.1); margin-bottom: 1rem;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">❌</div>
                    <h4 style="color: #FF6B6B; margin: 0;">Generation Failed</h4>
                    <p style="color: #B8BCC8; margin: 0.5rem 0 0 0;">{data['message']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

async def generate_with_status(query: str, project_type: Optional[str], status_container, progress_bar) -> ProjectResult:
    """Generate project with real-time status updates"""
    
    # Create bridge
    bridge = StreamlitOrchestrator(status_container, progress_bar)
    
    # Parse project type
    ptype = None
    if project_type:
        try:
            ptype = ProjectType(project_type)
        except ValueError:
            pass
    
    # Create user query
    user_query = UserQuery(
        query=query,
        project_type=ptype
    )
    
    # Create orchestrator with callback
    orchestrator = ProjectOrchestrator(
        max_iterations=5,
        status_callback=bridge.handle_status_update
    )
    
    # Generate project
    result = await orchestrator.generate_project(user_query)
    
    return result 