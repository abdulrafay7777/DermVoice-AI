# AI Skin Specialist - Overview

## Problem Statement
Accessing preliminary dermatological guidance can be time-consuming and difficult. Patients often have skin concerns they wish to describe verbally while showing a visual representation of the issue, but standard symptom checkers lack interactive voice and image support. 

**AI Skin Specialist** solves this by providing a conversational, Gradio-based consultation assistant. Patients can seamlessly upload a photo/video and verbally describe their symptoms. The application processes both the visual and audio inputs to return an immediate, empathetic, doctor-style spoken and written assessment (for general informational purposes only).

## Models Used
The application leverages several state-of-the-art AI models to handle different modalities:

1. **Speech-to-Text (Patient Voice):**
   - **Groq Whisper (`whisper-large-v3`)**: Used to rapidly and accurately transcribe the patient's spoken audio description into text.

2. **Vision & Text Analysis (The "Brain"):**
   - **Groq Vision (`meta-llama/llama-4-scout-17b-16e-instruct`)**: Acts as the core reasoning engine. It takes the transcribed text and the uploaded skin image to generate informative, context-aware dermatological guidance.
   - *(Alternative)* **MiniMax (`MiniMax-M3`)**: An optional fallback/alternative model compatible with Anthropic's API format, supporting both image and video encoding.

3. **Text-to-Speech (Doctor Voice):**
   - **Deepgram TTS (`aura-2-thalia-en`)**: Converts the AI-generated text response into a highly realistic, human-sounding audio clip for the patient to listen to.

---
*Disclaimer: This project provides general informational guidance only. It is not a medical diagnosis and should not replace professional care from a licensed clinician.*
