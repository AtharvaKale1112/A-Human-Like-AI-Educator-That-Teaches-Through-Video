# System Architecture & Prompt Pipeline

## 1. High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AuraTeach AI Platform                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
     ┌────────────────────────────────┴────────────────────────────────┐
     ▼                                                                 ▼
[Document Ingestion & RAG]                                     [Topic & Profile Selector]
  ├── Multi-format Parsers (PDF/DOCX/PPTX/TXT)                   ├── Learner Level (Beginner/Inter/Adv)
  ├── Hierarchical Semantic Chunking                             ├── Target Time (5m / 20m / 60m / 7d)
  ├── TF-IDF & Cosine Similarity Search                          ├── Language (EN, HI, Hinglish, ES, etc.)
  └── Grounded Citations Generator                               └── Teacher Persona (Sarah, Vikram, etc.)
     │                                                                 │
     └────────────────────────────────┬────────────────────────────────┘
                                      ▼
                      [Pedagogy & Planning Engine]
                        ├── Understand & Ground Scope
                        ├── Multi-Segment Lesson Plan
                        ├── Avatar State & Gesture Directives
                        └── Subject Classification (Physics/Math/CS/Bio/Hist)
                                      │
                                      ▼
                      [Video Classroom Stage Orchestrator]
     ┌────────────────────────────────┼────────────────────────────────┐
     ▼                                ▼                                ▼
[Animated AI Avatar]         [Multilingual TTS Engine]      [Subject-Aware Visualizer]
  ├── 2.5D SVG Head/Body       ├── Edge-TTS Neural Voices     ├── Physics: Circuits / Projectiles
  ├── Viseme Lip-Sync          ├── Rate & Pitch Modulation    ├── Math: LaTeX Steps / 2D Curves
  ├── Eye Blinking / Tilt      └── Web Speech API Fallback    ├── CS: Code Playground & Call Stack
  └── Pointer Gestures                                        └── Bio: Cellular Organelle Anatomy
                                      │
                                      ▼
                    [Interactive Pedagogical Interventions]
                        ├── Mid-Lesson Checkpoint Modals
                        ├── Voice STT Microphone Input
                        ├── Root-Cause Misconception Diagnostic
                        └── Adaptive Remediation & New Analogies
                                      │
                                      ▼
                    [Post-Lesson Assessment & Student Profile]
                        ├── Multi-Question Diagnostic Quiz
                        ├── Concept Mastery Radar Breakdown
                        ├── Actionable Revision Plan
                        └── Long-Term Memory & Streaks
```

---

## 2. Pedagogical Loop Design

The AI Teacher is built around the human educator loop:

1. **Understand**:
   - Ingests learner level, available time, target language, and uploaded material chunks.
   - Extracts key concepts, formulas, definitions, and prerequisite dependencies.
2. **Plan**:
   - Structures the lesson into progressive pedagogical segments: `Introduction → Core Mechanism → Visual Demonstration → Checkpoint Verification → Synthesis`.
3. **Explain**:
   - Synthesizes spoken scripts for the neural voice, tailored with analogies matching the learner's level.
4. **Demonstrate**:
   - Mounts the appropriate subject-aware visualizer (e.g. interactive circuit with moving electrons, live code runner, or LaTeX equation stepper).
5. **Question**:
   - Proactively pauses at checkpoint segments to ask conceptual questions (MCQs, short answer, or "explain in your own words").
6. **Evaluate**:
   - Diagnoses student answers using the Misconception Engine to uncover *why* the student made an error.
7. **Adapt**:
   - Delivers targeted spoken remediation with a fresh analogy, adjusts difficulty, and offers a follow-up verification question.
8. **Continue**:
   - Advances smoothly to the next concept or concludes with a full assessment report.

---

## 3. RAG Pipeline & Hallucination Prevention

1. **Extraction**:
   - `pypdf` extracts pages and preserves page numbers.
   - `python-docx` extracts structured headings and paragraph blocks.
   - `python-pptx` extracts slide hierarchies and bullet lists.
2. **Chunking**:
   - Sliding window chunking (250 words per chunk with 50-word overlap) preserving document boundaries.
3. **Indexing & Retrieval**:
   - Vectorized TF-IDF matrix with cosine similarity ranking.
   - Top-k retrieval extracts the most relevant excerpts.
4. **Prompt Grounding**:
   - Context is injected directly with `[Source: filename, Page/Slide: X]` headers.
   - Gemini is instructed to ground explanations strictly in the uploaded context.

---

## 4. Multilingual & Cross-Lingual Design

- **Language Mapping**: Supports Indian languages (Hindi, Hinglish, Tamil, Telugu) and International languages (Spanish, French, German, English).
- **Cross-Lingual RAG**: English documents are parsed, indexed, and taught fluently in Hindi or Hinglish without requiring manual translation steps.
- **Dynamic Language Switching**: The student can switch the teaching language at any time; the session context and learning state are preserved.
