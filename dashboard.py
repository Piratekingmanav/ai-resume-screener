# import streamlit as st
# import requests
# import pandas as pd
# import google.generativeai as genai





# model = genai.GenerativeModel('models/gemini-1.5-flash')

# # 1. Custom Page Configuration
# st.set_page_config(
#     page_title="AI Resume Screener | Workspace",
#     page_icon="⚡",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize Session State for Memory
# if "current_resume_text" not in st.session_state:
#     st.session_state.current_resume_text = ""
# if "current_candidate_name" not in st.session_state:
#     st.session_state.current_candidate_name = ""
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 2. Modern SaaS Custom CSS
# custom_css = """
# <style>
#     #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
#     .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
#     .stButton>button {
#         background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
#         color: white; border: none; border-radius: 8px; font-weight: 600; transition: all 0.3s ease-in-out;
#     }
#     .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(147, 51, 234, 0.4); color: white; }
#     div[data-testid="metric-container"] {
#         background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px);
#         border-left: 4px solid #9333ea; border-top: 1px solid rgba(255, 255, 255, 0.1);
#         border-right: 1px solid rgba(255, 255, 255, 0.1); border-bottom: 1px solid rgba(255, 255, 255, 0.1);
#         padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
#     }
#     [data-testid="stSidebar"] { background-color: #0b0f19; border-right: 1px solid #1e293b; }
#     th { background-color: #312e81 !important; color: #e2e8f0 !important; font-weight: bold !important; }
    
#     /* Chat Message Styling */
#     .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; margin-bottom: 10px;}
# </style>
# """
# st.markdown(custom_css, unsafe_allow_html=True)

# # 3. Sidebar
# with st.sidebar:
#     st.title("⚙️ System Control")
#     st.markdown("---")
#     st.markdown("**Lead Developer:** Manav Singh")
#     st.markdown("**Architecture:** Conversational AI & NLP")
#     st.markdown("---")
#     st.info("This proprietary screening engine extracts skills and features a RAG-based conversational AI interface for deep candidate analysis.")
    
#     if st.button("🧹 Clear Chat History"):
#         st.session_state.chat_history = []
#         st.rerun()

# # 4. Main Header
# st.title("⚡ AI-Powered Resume Screener")
# st.markdown("Automate shortlisting, filter by technical requirements, and chat directly with applicant data.")
# st.markdown("---")

# # 5. Tab Layout (3 Tabs preserved)
# tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "🏆 Leaderboard & Filters", "💬 Chat with Resume"])

# # --- TAB 1: UPLOAD RESUMES ---
# with tab1:
#     st.subheader("Process New Candidates")
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         job_id = st.number_input("Target Job ID", min_value=1, step=1)
#     with col2:
#         uploaded_file = st.file_uploader("Upload Candidate Resume (PDF/DOCX)", type=["pdf", "docx"])
    
#     if st.button("🚀 Process Resume", use_container_width=True):
#         if uploaded_file is not None:
#             with st.spinner(f"Analyzing {uploaded_file.name}..."):
#                 files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 response = requests.post(f"http://api:8000/upload-resume/{job_id}", files=files)
                
#                 if response.status_code == 200:
#                     st.success(f"Successfully processed {uploaded_file.name}!")
#                     data = response.json()
                    
#                     # Save the raw text and name to Streamlit's memory for the Chat Tab
#                     st.session_state.current_resume_text = data.get('raw_text', '')
#                     st.session_state.current_candidate_name = uploaded_file.name
                    
#                     m1, m2 = st.columns(2)
#                     m1.metric(label="Match Score", value=f"{data.get('match_score', 0)}%")
#                     m2.metric(label="Extracted Email", value=data.get('email_found', 'N/A'))
#                 else:
#                     st.error("Upload failed.")

# # --- TAB 2: CANDIDATE RANKINGS & FILTERS ---
# with tab2:
#     st.subheader("Database Rankings & Filtering")
    
#     fetch_job_id = st.number_input("Enter Job ID to view rankings", min_value=1, step=1, key="fetch_job")
    
#     if st.button("📊 Fetch Rankings", type="primary"):
#         with st.spinner("Retrieving database records..."):
#             response = requests.get(f"http://api:8000/candidates/{fetch_job_id}")
            
#             if response.status_code == 200:
#                 candidates = response.json()
#                 if candidates:
#                     # Load data into a Pandas DataFrame
#                     df = pd.DataFrame(candidates)
#                     df = df[["id", "name", "email", "education", "experience", "skills", "certifications", "match_score"]]
#                     df.columns = ["ID", "Resume File", "Email", "Education", "Experience", "Skills", "Certifications", "Match Score (%)"]
                    
#                     # Store dataframe in Streamlit session state so filters don't erase it when they refresh the UI
#                     st.session_state['candidate_df'] = df
#                 else:
#                     st.session_state['candidate_df'] = None
#                     st.info("No candidates found for this Job ID.")
#             else:
#                 st.error("Failed to fetch candidates.")

#     # Show filters and table only if data exists in session state
#     if 'candidate_df' in st.session_state and st.session_state['candidate_df'] is not None:
#         df = st.session_state['candidate_df']
        
#         st.markdown("### 🔍 Filter Candidates")
#         f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
#         with f_col1:
#             skill_filter = st.text_input("Require Skill (e.g., Python)")
#         with f_col2:
#             edu_filter = st.text_input("Education (e.g., B.Tech)")
#         with f_col3:
#             exp_filter = st.text_input("Experience (e.g., Intern)")
#         with f_col4:
#             min_score = st.slider("Minimum Match Score (%)", min_value=0, max_value=100, value=0, step=5)
            
#         # Apply Pandas filtering logic dynamically
#         filtered_df = df.copy()
        
#         if skill_filter:
#             filtered_df = filtered_df[filtered_df['Skills'].str.contains(skill_filter, case=False, na=False)]
#         if edu_filter:
#             filtered_df = filtered_df[filtered_df['Education'].str.contains(edu_filter, case=False, na=False)]
#         if exp_filter:
#             filtered_df = filtered_df[filtered_df['Experience'].str.contains(exp_filter, case=False, na=False)]
            
#         filtered_df = filtered_df[filtered_df['Match Score (%)'] >= min_score]
        
#         # Display the filtered results
#         st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
#         # CSV Download updates dynamically based on the filtered data!
#         csv = filtered_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="📥 Download Filtered Shortlist",
#             data=csv,
#             file_name=f'job_{fetch_job_id}_filtered.csv',
#             mime='text/csv',
#         )

#         # --- EMAIL ACTION SECTION ---
#         st.markdown("---")
#         st.markdown("### ✉️ Candidate Outreach")
        
#         c_col1, c_col2 = st.columns([2, 1])
#         with c_col1:
#             invite_candidate_id = st.number_input("Enter Candidate ID to invite", min_value=1, step=1, key="invite_id")
#         with c_col2:
#             st.write("") # Spacing alignment
#             st.write("")
#             if st.button("📧 Send Interview Invite", type="primary"):
#                 with st.spinner("Queueing email..."):
#                     try:
#                         response = requests.post(f"http://api:8000/send-invite/{invite_candidate_id}")
#                         if response.status_code == 200:
#                             res_data = response.json()
#                             st.success(res_data.get("message", "Invite sent successfully!"))
#                         else:
#                             err_msg = response.json().get("detail", "Failed to send invitation.")
#                             st.error(f"Error: {err_msg}")
#                     except Exception as e:
#                         st.error(f"Connection error: {e}")

# # --- TAB 3: CONVERSATIONAL AI ---
# with tab3:
#     if st.session_state.current_resume_text:
#         st.subheader(f"💬 Conversational Analysis: {st.session_state.current_candidate_name}")
#         st.markdown("Ask the AI recruiter specific questions about this candidate's background.")

#         # --- AI INTERVIEW PREP GENERATOR ---
#         if st.button("🎯 Generate Interview Prep", type="primary"):
#             with st.spinner("Analyzing candidate boundaries..."):
#                 try:
#                     prep_prompt = f"Act as an expert technical recruiter. Based ONLY on the skills and projects listed in this resume, generate 5 challenging technical interview questions to verify the candidate's expertise. Provide a brief 'Ideal Answer' for each.\n\nRESUME TEXT:\n{st.session_state.current_resume_text}"
                    
#                     response = model.generate_content(prep_prompt)
                    
#                     # Append the generated questions directly into the chat feed
#                     st.session_state.chat_history.append({"role": "assistant", "content": f"**Interview Prep Generated:**\n\n{response.text}"})
#                     st.rerun() # Refresh the UI to display the new message instantly
#                 except Exception as e:
#                     st.error(f"Failed to generate questions: {e}")
#         st.markdown("---")


        
#         # Display chat history
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # Chat Input
#         if prompt := st.chat_input("E.g., What is their most impressive machine learning project?"):
#             # Append user question to history
#             st.session_state.chat_history.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             # Generate AI Response
#             with st.chat_message("assistant"):
#                 with st.spinner("Analyzing resume context..."):
#                     try:
#                         # Feed the AI the resume text AND the user's question
#                         full_prompt = f"You are an expert technical recruiter. Based ONLY on the following resume text, answer the question. If the answer is not in the resume, say 'I cannot find that in the resume.'\n\nRESUME TEXT:\n{st.session_state.current_resume_text}\n\nQUESTION: {prompt}"
                        
#                         response = model.generate_content(full_prompt)
#                         st.markdown(response.text)
                        
#                         # Save AI response to history
#                         st.session_state.chat_history.append({"role": "assistant", "content": response.text})
#                     except Exception as e:
#                         st.error(f"AI API Error: {e}")
#                         st.info("Did you remember to add your API Key at the top of dashboard.py?")
#     else:
#         st.info("👈 Please upload a resume in Tab 1 first to start chatting!")




# import streamlit as st
# import requests
# import pandas as pd
# from google import genai

# # --- AI CONFIGURATION ---
# 

# # 1. Custom Page Configuration
# st.set_page_config(
#     page_title="AI Resume Screener | Workspace",
#     page_icon="⚡",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize Session State for Memory
# if "current_resume_text" not in st.session_state:
#     st.session_state.current_resume_text = ""
# if "current_candidate_name" not in st.session_state:
#     st.session_state.current_candidate_name = ""
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 2. Modern SaaS Custom CSS
# custom_css = """
# <style>
#     #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
#     .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
#     .stButton>button {
#         background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
#         color: white; border: none; border-radius: 8px; font-weight: 600; transition: all 0.3s ease-in-out;
#     }
#     .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(147, 51, 234, 0.4); color: white; }
#     div[data-testid="metric-container"] {
#         background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px);
#         border-left: 4px solid #9333ea; border-top: 1px solid rgba(255, 255, 255, 0.1);
#         border-right: 1px solid rgba(255, 255, 255, 0.1); border-bottom: 1px solid rgba(255, 255, 255, 0.1);
#         padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
#     }
#     [data-testid="stSidebar"] { background-color: #0b0f19; border-right: 1px solid #1e293b; }
#     th { background-color: #312e81 !important; color: #e2e8f0 !important; font-weight: bold !important; }
    
#     /* Chat Message Styling */
#     .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; margin-bottom: 10px;}
# </style>
# """
# st.markdown(custom_css, unsafe_allow_html=True)

# # 3. Sidebar
# with st.sidebar:
#     st.title("⚙️ System Control")
#     st.markdown("---")
#     st.markdown("**Lead Developer:** Manav Singh")
#     st.markdown("**Architecture:** Conversational AI & NLP")
#     st.markdown("---")
#     st.info("This proprietary screening engine extracts skills and features a RAG-based conversational AI interface for deep candidate analysis.")
    
#     if st.button("🧹 Clear Chat History"):
#         st.session_state.chat_history = []
#         st.rerun()

# # 4. Main Header
# st.title("⚡ AI-Powered Resume Screener")
# st.markdown("Automate shortlisting, filter by technical requirements, and chat directly with applicant data.")
# st.markdown("---")

# # 5. Tab Layout (3 Tabs preserved)
# tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "🏆 Leaderboard & Filters", "💬 Chat with Resume"])

# # --- TAB 1: UPLOAD RESUMES ---
# with tab1:
#     st.subheader("Process New Candidates")
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         job_id = st.number_input("Target Job ID", min_value=1, step=1)
#     with col2:
#         uploaded_file = st.file_uploader("Upload Candidate Resume (PDF/DOCX)", type=["pdf", "docx"])
    
#     if st.button("🚀 Process Resume", use_container_width=True):
#         if uploaded_file is not None:
#             with st.spinner(f"Analyzing {uploaded_file.name}..."):
#                 files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 response = requests.post(f"http://api:8000/upload-resume/{job_id}", files=files)
                
#                 if response.status_code == 200:
#                     st.success(f"Successfully processed {uploaded_file.name}!")
#                     data = response.json()
                    
#                     # Save the raw text and name to Streamlit's memory for the Chat Tab
#                     st.session_state.current_resume_text = data.get('raw_text', '')
#                     st.session_state.current_candidate_name = uploaded_file.name
                    
#                     m1, m2 = st.columns(2)
#                     m1.metric(label="Match Score", value=f"{data.get('match_score', 0)}%")
#                     m2.metric(label="Extracted Email", value=data.get('email_found', 'N/A'))
#                 else:
#                     st.error("Upload failed.")

# # --- TAB 2: CANDIDATE RANKINGS & FILTERS ---
# with tab2:
#     st.subheader("Database Rankings & Filtering")
    
#     fetch_job_id = st.number_input("Enter Job ID to view rankings", min_value=1, step=1, key="fetch_job")
    
#     if st.button("📊 Fetch Rankings", type="primary"):
#         with st.spinner("Retrieving database records..."):
#             response = requests.get(f"http://api:8000/candidates/{fetch_job_id}")
            
#             if response.status_code == 200:
#                 candidates = response.json()
#                 if candidates:
#                     df = pd.DataFrame(candidates)
#                     df = df[["id", "name", "email", "education", "experience", "skills", "certifications", "match_score"]]
#                     df.columns = ["ID", "Resume File", "Email", "Education", "Experience", "Skills", "Certifications", "Match Score (%)"]
#                     st.session_state['candidate_df'] = df
#                 else:
#                     st.session_state['candidate_df'] = None
#                     st.info("No candidates found for this Job ID.")
#             else:
#                 st.error("Failed to fetch candidates.")

#     if 'candidate_df' in st.session_state and st.session_state['candidate_df'] is not None:
#         df = st.session_state['candidate_df']
        
#         st.markdown("### 🔍 Filter Candidates")
#         f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
#         with f_col1:
#             skill_filter = st.text_input("Require Skill (e.g., Python)")
#         with f_col2:
#             edu_filter = st.text_input("Education (e.g., B.Tech)")
#         with f_col3:
#             exp_filter = st.text_input("Experience (e.g., Intern)")
#         with f_col4:
#             min_score = st.slider("Minimum Match Score (%)", min_value=0, max_value=100, value=0, step=5)
            
#         filtered_df = df.copy()
        
#         if skill_filter:
#             filtered_df = filtered_df[filtered_df['Skills'].str.contains(skill_filter, case=False, na=False)]
#         if edu_filter:
#             filtered_df = filtered_df[filtered_df['Education'].str.contains(edu_filter, case=False, na=False)]
#         if exp_filter:
#             filtered_df = filtered_df[filtered_df['Experience'].str.contains(exp_filter, case=False, na=False)]
            
#         filtered_df = filtered_df[filtered_df['Match Score (%)'] >= min_score]
#         st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
#         csv = filtered_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="📥 Download Filtered Shortlist",
#             data=csv,
#             file_name=f'job_{fetch_job_id}_filtered.csv',
#             mime='text/csv',
#         )

#         # --- EMAIL ACTION SECTION ---
#         st.markdown("---")
#         st.markdown("### ✉️ Candidate Outreach")
        
#         c_col1, c_col2 = st.columns([2, 1])
#         with c_col1:
#             invite_candidate_id = st.number_input("Enter Candidate ID to invite", min_value=1, step=1, key="invite_id")
#         with c_col2:
#             st.write("") 
#             st.write("")
#             if st.button("📧 Send Interview Invite", type="primary"):
#                 with st.spinner("Queueing email..."):
#                     try:
#                         response = requests.post(f"http://api:8000/send-invite/{invite_candidate_id}")
#                         if response.status_code == 200:
#                             res_data = response.json()
#                             st.success(res_data.get("message", "Invite sent successfully!"))
#                         else:
#                             err_msg = response.json().get("detail", "Failed to send invitation.")
#                             st.error(f"Error: {err_msg}")
#                     except Exception as e:
#                         st.error(f"Connection error: {e}")

# # --- TAB 3: CONVERSATIONAL AI ---
# with tab3:
#     if st.session_state.current_resume_text:
#         st.subheader(f"💬 Conversational Analysis: {st.session_state.current_candidate_name}")
#         st.markdown("Ask the AI recruiter specific questions about this candidate's background.")
        
#         # --- AI INTERVIEW PREP GENERATOR ---
#         if st.button("🎯 Generate Interview Prep", type="primary"):
#             with st.spinner("Analyzing candidate boundaries..."):
#                 try:
#                     prep_prompt = f"Act as an expert technical recruiter. Based ONLY on the skills and projects listed in this resume, generate 5 challenging technical interview questions to verify the candidate's expertise. Provide a brief 'Ideal Answer' for each.\n\nRESUME TEXT:\n{st.session_state.current_resume_text}"
                    
#                     # New SDK call
#                     response = client.models.generate_content(model='gemini-1.5-flash', contents=prep_prompt)
                    
#                     st.session_state.chat_history.append({"role": "assistant", "content": f"**Interview Prep Generated:**\n\n{response.text}"})
#                     st.rerun() 
#                 except Exception as e:
#                     st.error(f"Failed to generate questions: {e}")
#         st.markdown("---")

#         # Display chat history
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # Chat Input
#         if prompt := st.chat_input("E.g., What is their most impressive machine learning project?"):
#             st.session_state.chat_history.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.chat_message("assistant"):
#                 with st.spinner("Analyzing resume context..."):
#                     try:
#                         full_prompt = f"You are an expert technical recruiter. Based ONLY on the following resume text, answer the question. If the answer is not in the resume, say 'I cannot find that in the resume.'\n\nRESUME TEXT:\n{st.session_state.current_resume_text}\n\nQUESTION: {prompt}"
                        
#                         # New SDK call
#                         response = client.models.generate_content(model='gemini-1.5-flash', contents=full_prompt)
#                         st.markdown(response.text)
                        
#                         st.session_state.chat_history.append({"role": "assistant", "content": response.text})
#                     except Exception as e:
#                         st.error(f"AI API Error: {e}")
#     else:
#         st.info("👈 Please upload a resume in Tab 1 first to start chatting!")

import streamlit as st
import requests
import pandas as pd
from google import genai


# --- AI CONFIGURATION ---
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# 1. Custom Page Configuration
st.set_page_config(
    page_title="AI Resume Screener | Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Memory
if "current_resume_text" not in st.session_state:
    st.session_state.current_resume_text = ""
if "current_candidate_name" not in st.session_state:
    st.session_state.current_candidate_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 2. Modern SaaS Custom CSS
custom_css = """
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
        color: white; border: none; border-radius: 8px; font-weight: 600; transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(147, 51, 234, 0.4); color: white; }
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px);
        border-left: 4px solid #9333ea; border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1); border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stSidebar"] { background-color: #0b0f19; border-right: 1px solid #1e293b; }
    th { background-color: #312e81 !important; color: #e2e8f0 !important; font-weight: bold !important; }
    
    /* Chat Message Styling */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; margin-bottom: 10px;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("⚙️ System Control")
    st.markdown("---")
    st.markdown("**Lead Developer:** Manav Singh")
    st.markdown("**Architecture:** Conversational AI & NLP")
    st.markdown("---")
    st.info("This proprietary screening engine extracts skills and features a RAG-based conversational AI interface for deep candidate analysis.")
    
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# 4. Main Header
st.title("⚡ AI-Powered Resume Screener")
st.markdown("Automate shortlisting, filter by technical requirements, and chat directly with applicant data.")
st.markdown("---")

# 5. Tab Layout
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "🏆 Leaderboard & Filters", "💬 Chat with Resume"])

# --- TAB 1: UPLOAD RESUMES ---
with tab1:
    st.subheader("Process New Candidates")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        job_id = st.number_input("Target Job ID", min_value=1, step=1)
    with col2:
        uploaded_file = st.file_uploader("Upload Candidate Resume (PDF/DOCX)", type=["pdf", "docx"])
    
    if st.button("🚀 Process Resume", use_container_width=True):
        if uploaded_file is not None:
            with st.spinner(f"Analyzing {uploaded_file.name}..."):
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"http://api:8000/upload-resume/{job_id}", files=files)
                
                if response.status_code == 200:
                    st.success(f"Successfully processed {uploaded_file.name}!")
                    data = response.json()
                    
                    st.session_state.current_resume_text = data.get('raw_text', '')
                    st.session_state.current_candidate_name = uploaded_file.name
                    
                    m1, m2 = st.columns(2)
                    m1.metric(label="Match Score", value=f"{data.get('match_score', 0)}%")
                    m2.metric(label="Extracted Email", value=data.get('email_found', 'N/A'))
                else:
                    st.error("Upload failed.")

# --- TAB 2: CANDIDATE RANKINGS & FILTERS ---
with tab2:
    st.subheader("Database Rankings & Filtering")
    
    fetch_job_id = st.number_input("Enter Job ID to view rankings", min_value=1, step=1, key="fetch_job")
    
    if st.button("📊 Fetch Rankings", type="primary"):
        with st.spinner("Retrieving database records..."):
            response = requests.get(f"http://api:8000/candidates/{fetch_job_id}")
            
            if response.status_code == 200:
                candidates = response.json()
                if candidates:
                    df = pd.DataFrame(candidates)
                    df = df[["id", "name", "email", "education", "experience", "skills", "certifications", "match_score"]]
                    df.columns = ["ID", "Resume File", "Email", "Education", "Experience", "Skills", "Certifications", "Match Score (%)"]
                    st.session_state['candidate_df'] = df
                else:
                    st.session_state['candidate_df'] = None
                    st.info("No candidates found for this Job ID.")
            else:
                st.error("Failed to fetch candidates.")

    if 'candidate_df' in st.session_state and st.session_state['candidate_df'] is not None:
        df = st.session_state['candidate_df']
        
        st.markdown("### 🔍 Filter Candidates")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        with f_col1:
            skill_filter = st.text_input("Require Skill (e.g., Python)")
        with f_col2:
            edu_filter = st.text_input("Education (e.g., B.Tech)")
        with f_col3:
            exp_filter = st.text_input("Experience (e.g., Intern)")
        with f_col4:
            min_score = st.slider("Minimum Match Score (%)", min_value=0, max_value=100, value=0, step=5)
            
        filtered_df = df.copy()
        
        if skill_filter:
            filtered_df = filtered_df[filtered_df['Skills'].str.contains(skill_filter, case=False, na=False)]
        if edu_filter:
            filtered_df = filtered_df[filtered_df['Education'].str.contains(edu_filter, case=False, na=False)]
        if exp_filter:
            filtered_df = filtered_df[filtered_df['Experience'].str.contains(exp_filter, case=False, na=False)]
            
        filtered_df = filtered_df[filtered_df['Match Score (%)'] >= min_score]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Shortlist",
            data=csv,
            file_name=f'job_{fetch_job_id}_filtered.csv',
            mime='text/csv',
        )

        # --- EMAIL ACTION SECTION ---
        st.markdown("---")
        st.markdown("### ✉️ Candidate Outreach")
        
        c_col1, c_col2 = st.columns([2, 1])
        with c_col1:
            invite_candidate_id = st.number_input("Enter Candidate ID to invite", min_value=1, step=1, key="invite_id")
        with c_col2:
            st.write("") 
            st.write("")
            if st.button("📧 Send Interview Invite", type="primary"):
                with st.spinner("Queueing email..."):
                    try:
                        response = requests.post(f"http://api:8000/send-invite/{invite_candidate_id}")
                        if response.status_code == 200:
                            res_data = response.json()
                            st.success(res_data.get("message", "Invite sent successfully!"))
                        else:
                            err_msg = response.json().get("detail", "Failed to send invitation.")
                            st.error(f"Error: {err_msg}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

# --- TAB 3: CONVERSATIONAL AI ---
with tab3:
    if st.session_state.current_resume_text:
        st.subheader(f"💬 Conversational Analysis: {st.session_state.current_candidate_name}")
        st.markdown("Ask the AI recruiter specific questions about this candidate's background.")
        
        # --- AI INTERVIEW PREP GENERATOR ---
        if st.button("🎯 Generate Interview Prep", type="primary"):
            with st.spinner("Analyzing candidate boundaries..."):
                try:
                    prep_prompt = f"Act as an expert technical recruiter. Based ONLY on the skills and projects listed in this resume, generate 5 challenging technical interview questions to verify the candidate's expertise. Provide a brief 'Ideal Answer' for each.\n\nRESUME TEXT:\n{st.session_state.current_resume_text}"
                    
                    # Updated to flash-latest
                    response = client.models.generate_content(model='gemini-1.5-flash-latest', contents=prep_prompt)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": f"**Interview Prep Generated:**\n\n{response.text}"})
                    st.rerun() 
                except Exception as e:
                    st.error(f"Failed to generate questions: {e}")
        st.markdown("---")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("E.g., What is their most impressive machine learning project?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing resume context..."):
                    try:
                        full_prompt = f"You are an expert technical recruiter. Based ONLY on the following resume text, answer the question. If the answer is not in the resume, say 'I cannot find that in the resume.'\n\nRESUME TEXT:\n{st.session_state.current_resume_text}\n\nQUESTION: {prompt}"
                        
                        # Updated to flash-latest
                        response = client.models.generate_content(model='gemini-1.5-flash-latest', contents=full_prompt)
                        st.markdown(response.text)
                        
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"AI API Error: {e}")
    else:
        st.info("👈 Please upload a resume in Tab 1 first to start chatting!")