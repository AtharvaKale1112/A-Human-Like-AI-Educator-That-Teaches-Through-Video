import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.config import (
    BASE_DIR, UPLOAD_DIR, SAMPLE_DATA_DIR, STATIC_DIR,
    TEACHER_PROFILES, SUPPORTED_LANGUAGES
)
from backend.services.gemini_service import gemini_service
from backend.services.rag_service import rag_service
from backend.services.pedagogy_engine import pedagogy_engine
from backend.services.misconception_engine import misconception_engine
from backend.services.assessment_service import assessment_service
from backend.services.profile_service import profile_service
from backend.services.tts_service import tts_service, AUDIO_CACHE_DIR

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ai_teacher_app")

app = FastAPI(
    title="AI Teacher — Human-Like Adaptive Video Classroom API",
    description="Adaptive AI virtual teacher capable of video teaching, RAG document understanding, real-time misconception remediation, and multilingual presentation.",
    version="2.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class LessonPlanRequest(BaseModel):
    topic: str
    level: str = "beginner"
    duration_minutes: int = 20
    language: str = "en"
    teacher_id: str = "sarah"
    doc_id: Optional[str] = None
    custom_instructions: Optional[str] = ""

class CheckpointEvalRequest(BaseModel):
    topic: str
    concept: str
    question: str
    student_answer: str
    correct_answer: str
    expected_reasoning: str = ""
    misconception_traps: Optional[Dict[str, str]] = {}
    language: str = "en"
    teacher_id: str = "sarah"

class TTSRequest(BaseModel):
    text: str
    teacher_id: str = "sarah"
    language: str = "en"

class QuizGenRequest(BaseModel):
    topic: str
    subject: str = "general"
    level: str = "beginner"
    num_questions: int = 4
    language: str = "en"
    teacher_id: str = "sarah"

class QuizEvalRequest(BaseModel):
    topic: str
    subject: str = "general"
    level: str = "beginner"
    duration_minutes: int = 20
    questions: List[Dict[str, Any]]
    answers: Dict[str, str]
    language: str = "en"
    teacher_id: str = "sarah"

class LearningPathRequest(BaseModel):
    topic: str
    target_days: int = 7
    level: str = "beginner"
    language: str = "en"

class StudentQuestionRequest(BaseModel):
    topic: str
    current_segment_title: str
    student_question: str
    lesson_context: str = ""
    language: str = "en"
    teacher_id: str = "sarah"

# Endpoints
@app.get("/api/config")
async def get_config():
    """Returns platform settings, available teachers, and supported languages."""
    return {
        "teachers": TEACHER_PROFILES,
        "languages": SUPPORTED_LANGUAGES,
        "levels": [
            {"id": "beginner", "label": "Beginner", "desc": "Intuitive terminology, daily analogies, core intuition"},
            {"id": "intermediate", "label": "Intermediate", "desc": "Balanced technical rigor, practical code/system mechanics"},
            {"id": "advanced", "label": "Advanced", "desc": "Mathematical derivations, architecture deep dive, edge cases"}
        ],
        "preset_durations": [
            {"minutes": 5, "label": "5 Minutes", "desc": "Speed Concept Sprint"},
            {"minutes": 20, "label": "20 Minutes", "desc": "Standard Interactive Lesson with Checkpoints"},
            {"minutes": 60, "label": "60 Minutes", "desc": "Deep Masterclass with Labs & Quiz"},
            {"minutes": 10080, "label": "7 Days", "desc": "Multi-Day Curriculum Roadmap"}
        ]
    }

@app.post("/api/upload")
async def upload_material(file: UploadFile = File(...)):
    """Uploads textbook, PDF, DOCX, PPTX, or notes and indexes into RAG vector store."""
    try:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".txt", ".md"]:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, PPTX, or TXT.")

        saved_path = UPLOAD_DIR / file.filename
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_meta = rag_service.process_and_index_file(saved_path, file.filename)
        return {"status": "success", "data": doc_meta}
    except Exception as e:
        logger.error(f"Error processing uploaded file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/samples")
async def get_sample_materials():
    """Returns pre-loaded sample textbooks that can be loaded with one click."""
    samples = []
    if SAMPLE_DATA_DIR.exists():
        for file in SAMPLE_DATA_DIR.glob("*.*"):
            samples.append({
                "filename": file.name,
                "title": file.stem.replace("_", " ").title(),
                "size_kb": round(file.stat().st_size / 1024, 1)
            })
    return {"samples": samples}

@app.post("/api/samples/load/{filename}")
async def load_sample_material(filename: str):
    """Loads and indexes a pre-built sample file."""
    sample_path = SAMPLE_DATA_DIR / filename
    if not sample_path.exists():
        raise HTTPException(status_code=404, detail="Sample file not found")
    
    doc_meta = rag_service.process_and_index_file(sample_path, filename)
    return {"status": "success", "data": doc_meta}

@app.post("/api/lesson/plan")
async def plan_lesson(req: LessonPlanRequest):
    """Generates complete structured multi-segment video lesson plan with pedagogical checkpoints."""
    try:
        lesson = pedagogy_engine.plan_and_build_lesson(
            topic=req.topic,
            level=req.level,
            duration_minutes=req.duration_minutes,
            language=req.language,
            teacher_id=req.teacher_id,
            doc_id=req.doc_id,
            custom_instructions=req.custom_instructions or ""
        )
        # Pre-synthesize intro audio for instant playback
        if lesson.get("segments"):
            first_seg = lesson["segments"][0]
            audio_url = await tts_service.generate_audio_file(
                text=first_seg.get("spoken_script", ""),
                teacher_id=req.teacher_id,
                language=req.language
            )
            first_seg["audio_url"] = audio_url

        return {"status": "success", "data": lesson}
    except Exception as e:
        logger.error(f"Error creating lesson plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/lesson/evaluate_checkpoint")
async def evaluate_checkpoint(req: CheckpointEvalRequest):
    """Diagnoses student answers to live checkpoints, identifies root misconceptions, and provides audio remediation."""
    try:
        eval_result = misconception_engine.evaluate_and_adapt(
            topic=req.topic,
            concept=req.concept,
            question=req.question,
            student_answer=req.student_answer,
            correct_answer=req.correct_answer,
            expected_reasoning=req.expected_reasoning,
            misconception_traps=req.misconception_traps or {},
            language=req.language,
            teacher_id=req.teacher_id
        )
        
        # Generate spoken audio for teacher's remedial explanation
        remediation_speech = eval_result.get("teacher_spoken_remediation", "")
        audio_url = await tts_service.generate_audio_file(
            text=remediation_speech,
            teacher_id=req.teacher_id,
            language=req.language
        )
        eval_result["audio_url"] = audio_url

        return {"status": "success", "data": eval_result}
    except Exception as e:
        logger.error(f"Error in evaluate_checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/lesson/synthesize_audio")
async def synthesize_audio(req: TTSRequest):
    """Generates neural TTS audio for any spoken segment in chosen language."""
    try:
        audio_url = await tts_service.generate_audio_file(
            text=req.text,
            teacher_id=req.teacher_id,
            language=req.language
        )
        return {"status": "success", "audio_url": audio_url}
    except Exception as e:
        logger.error(f"Error synthesizing audio: {e}")
        return {"status": "error", "audio_url": None, "message": str(e)}

@app.get("/api/audio/{filename}")
async def serve_audio(filename: str):
    """Serves cached speech audio files."""
    audio_path = AUDIO_CACHE_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(str(audio_path), media_type="audio/mpeg")

@app.post("/api/assessment/generate")
async def generate_assessment(req: QuizGenRequest):
    """Generates end-of-lesson adaptive quiz."""
    try:
        quiz = assessment_service.generate_quiz(
            topic=req.topic,
            subject=req.subject,
            level=req.level,
            num_questions=req.num_questions,
            language=req.language,
            teacher_id=req.teacher_id
        )
        return {"status": "success", "data": quiz}
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/assessment/evaluate")
async def evaluate_assessment(req: QuizEvalRequest):
    """Grades quiz submission and updates student profile with mastery report."""
    try:
        report = assessment_service.evaluate_quiz_submission(
            topic=req.topic,
            subject=req.subject,
            level=req.level,
            questions=req.questions,
            answers=req.answers,
            language=req.language,
            teacher_id=req.teacher_id
        )
        # Update student profile
        updated_profile = profile_service.update_after_lesson(
            profile_id="student_default",
            assessment_report=report,
            duration_minutes=req.duration_minutes
        )
        return {"status": "success", "report": report, "profile": updated_profile}
    except Exception as e:
        logger.error(f"Error evaluating quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profile")
async def get_profile():
    """Returns student learning profile, streak, and mastery history."""
    profile = profile_service.get_or_create_profile("student_default")
    return {"status": "success", "profile": profile}

@app.post("/api/profile/learning_path")
async def generate_learning_path(req: LearningPathRequest):
    """Creates a 7-day or N-stage interactive curriculum roadmap."""
    try:
        path = profile_service.generate_learning_path(
            topic=req.topic,
            target_days=req.target_days,
            level=req.level,
            language=req.language
        )
        return {"status": "success", "data": path}
    except Exception as e:
        logger.error(f"Error generating learning path: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/ask")
async def ask_teacher_question(req: StudentQuestionRequest):
    """Answers a mid-lesson student question while maintaining lesson context."""
    teacher = TEACHER_PROFILES.get(req.teacher_id, TEACHER_PROFILES["sarah"])
    lang_info = SUPPORTED_LANGUAGES.get(req.language, SUPPORTED_LANGUAGES["en"])
    
    prompt = f"""
You are {teacher['name']}, actively teaching a video lesson on "{req.topic}".
Current lesson section: "{req.current_segment_title}".
Lesson Context: "{req.lesson_context}"

A student just paused the lecture and asked you this question:
"{req.student_question}"

Respond directly to the student in {lang_info['name']} ({req.language}).
Guidelines:
1. Maintain your authentic teacher persona ({teacher['style']}).
2. Be concise, clear, and reassuring.
3. Relate your answer directly back to the concept being taught.
4. Conclude by encouraging them to resume the video.

Return ONLY a valid JSON object:
{{
  "answer_text": "Detailed written explanation for the student",
  "spoken_answer": "Concise conversational script for AI Teacher voice to speak aloud",
  "key_insight": "One-sentence core takeaway"
}}
"""
    try:
        resp = gemini_service.generate_json(prompt=prompt)
    except Exception as e:
        logger.warning(f"Using fallback response for student question: {e}")
        resp = {
            "answer_text": f"That is a wonderful question about {req.topic}! When considering {req.student_question}, remember that the core parameters work together to maintain equilibrium. Let's keep exploring the lesson to see how this unfolds.",
            "spoken_answer": f"Great question! Remember that in {req.topic}, every parameter influences the overall state. Let's resume the lesson to see this in action.",
            "key_insight": "Parameters in this system operate in strict equilibrium."
        }

    # Generate spoken audio
    audio_url = await tts_service.generate_audio_file(
        text=resp.get("spoken_answer", ""),
        teacher_id=req.teacher_id,
        language=req.language
    )
    resp["audio_url"] = audio_url
    return {"status": "success", "data": resp}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "gemini_connected": bool(gemini_service.client),
        "tts_ready": True
    }

# Mount frontend static directory if exists
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")
