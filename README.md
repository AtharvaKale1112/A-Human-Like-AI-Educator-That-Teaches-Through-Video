# AuraTeach AI — Human-Like Adaptive AI Educator That Teaches Through Video

> **AI Innovation Hackathon 2026 — Round 2 Technical Assessment**  
> **Challenge Title:** AI Teacher: Build a Human-Like AI Educator That Teaches Through Video

---

## 🌟 Executive Summary & Vision

Traditional digital learning platforms offer either static pre-recorded videos or generic text-based chatbots. **AuraTeach AI** bridges this divide by delivering a genuine **human-like virtual teaching experience**. It reads and understands uploaded learning materials (PDF, DOCX, PPTX, TXT notes, textbooks), accepts any custom topic, structures an adaptive lesson, and presents it through a **synchronized video classroom** featuring an animated AI avatar, natural neural voice, subject-aware interactive simulations, mid-lesson question checkpoints with root-cause misconception diagnosis, and long-term student memory.

---

## 🚀 Key Features

### 1. Multi-Format Knowledge Grounding (RAG Engine)
- Ingests **PDFs, DOCX, PPTX, Markdown, Textbooks, Lecture Notes, and Research Papers**.
- Hierarchical semantic chunking and vector indexing with strict source grounding to prevent hallucinations.
- Cross-lingual teaching: ingest English materials and teach in Hindi/Hinglish, or vice-versa.

### 2. Topic-Based & Time-Based Pedagogical Adaptation
- Teaches any topic without uploaded files (e.g. "Quantum Computing", "Newton's Laws", "React Hooks").
- Adapts explanations across 3 learner levels:
  - **Beginner**: Intuitive terminology, everyday analogies, step-by-step foundation.
  - **Intermediate**: Technical balance, system mechanics, practical code.
  - **Advanced**: Mathematical derivations, algorithmic complexity, architectural edge cases.
- Paces content according to available time: **5 min sprint**, **20 min standard lesson**, **60 min masterclass**, or **7-day roadmap**.

### 3. Synchronized AI Video Classroom
- **Human-Like AI Avatar**: 2.5D SVG/Canvas animated teacher avatars with real-time lip-sync, subtle eye blinking, natural head tilts, and blackboard pointing gestures.
- **Multiple Teacher Personas**:
  - *Prof. Sarah*: Socratic, encouraging, and intuitive.
  - *Dr. Vikram*: Practical, engineering and code-focused.
  - *Priya Sharma*: Visual, energetic storytelling.
  - *Master Chen*: Deep foundational and mathematical rigor.
- **Multilingual Neural Voices**: Natural Edge-TTS synthesis supporting English, Hindi (हिन्दी), Hinglish, Tamil (தமிழ்), Telugu (తెలుగు), Spanish (Español), French (Français), and German (Deutsch).

### 4. Subject-Aware Dynamic Visual Explanations
- **Physics**: Interactive Canvas simulations (Ohm's Law circuit with live voltage/resistance sliders and electron flow, projectile motion trajectory, harmonic pendulum).
- **Mathematics**: Step-by-step LaTeX formula derivations and interactive 2D function curve plotter ($f(x) = \sin(x), \cos(x), \text{polynomials}$).
- **Programming & CS**: Live code editor with run simulation, terminal console, and call-stack frame tracer (e.g., recursive execution).
- **Biology & Chemistry**: Interactive cell organelle anatomy explorer (Nucleus, Mitochondria, Ribosomes) with biochemical pathways.
- **History & Social Studies**: Interactive chronological timeline with milestone cards.
- **Architecture & Systems**: Interactive node relationship flowcharts.

### 5. Pedagogical Loop & Misconception Remediation
- **Human Educator Process**: *Understand → Plan → Explain → Demonstrate → Question → Evaluate → Adapt → Continue*.
- **Diagnostic Misconception Detection**: Evaluates student responses to mid-lesson checkpoints, detects root causes (e.g. confusing inverse proportionality in $V=IR$), generates tailored counter-analogies, and re-evaluates understanding.
- **Mid-Lesson "Ask Teacher" Q&A**: Pauses lecture, answers student voice or text questions with grounded citations, and resumes.

### 6. Assessment, Analytics & Student Profile
- End-of-lesson adaptive quizzes with diagnostic scoring.
- Comprehensive Learning Report Card (Score, Strong Concepts, Needs Improvement, Actionable Revision Plan).
- Student Learning Profile with study streak tracking, domain mastery radar, and 7-day curriculum roadmaps.

---

## 🛠️ Quick Start & Setup Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Web browser (Chrome, Edge, Firefox)

### Installation
1. Clone the repository or navigate to the project directory:
   ```bash
   cd ai-teacher
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pypdf python-docx python-pptx edge-tts numpy scikit-learn google-genai
   ```
3. Set your Gemini API key (optional but recommended for live LLM reasoning):
   ```bash
   set GEMINI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python run.py
   ```
5. Open your browser at `http://127.0.0.1:8000` to start learning!

---

## 📊 Evaluation Criteria Mapping

| Evaluation Area | Weight | Implementation in AuraTeach AI |
|---|---|---|
| **Human-Like Teaching & Adaptation** | 20% | Full 7-stage teaching loop, proactive checkpoint questioning, root-cause misconception diagnosis, adaptive pacing & difficulty. |
| **AI/ML & LLM Implementation** | 15% | Structured Gemini GenAI prompts, Pydantic schemas, pedagogical planning, subject classification. |
| **RAG & Knowledge Grounding** | 15% | Multi-format parsing (PDF, DOCX, PPTX, TXT), TF-IDF / cosine semantic search, grounded source citations. |
| **AI Teaching Video Generation** | 15% | Synchronized video stage with lip-synced avatar, dynamic subject visualizers (circuits, code runner, LaTeX derivations, cell anatomy), live subtitles, and blackboard slides. |
| **Multilingual Capability** | 10% | Support for English, Hindi, Hinglish, Tamil, Telugu, Spanish, French, German with seamless switching and cross-lingual RAG. |
| **Voice & AI Avatar** | 10% | 4 customizable teacher personas, 2.5D SVG animated avatar with viseme lip-sync, neural TTS audio. |
| **Innovation & Originality** | 5% | Live misconception diagnosis with custom analogies, interactive physics/code simulations, 7-day roadmap generator, voice STT input. |
| **User Experience & Interface** | 5% | Modern glassmorphism UI, dual-screen presentation stage, interactive checkpoints, student profile dashboard. |
| **Documentation & Presentation** | 5% | Complete architectural diagrams, RAG methodology, prompt designs, demo walkthrough script. |
| **Total** | **100%** | **Production-grade complete submission** |
