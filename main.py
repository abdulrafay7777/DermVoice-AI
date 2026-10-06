from pathlib import Path

import gradio as gr

#from brain_of_the_doctor import brain_of_the_doctor
from brain_of_the_doctor_groq import brain_of_the_doctor
from voice_of_the_doctor import convert_text_to_doctor_audio
from voice_of_the_patient import transcribe_patient_voice


APP_TITLE = "AI Skin Specialist"

with open(Path(__file__).parent / "styles.css", "r", encoding="utf-8") as f:
    CSS = f.read()


def process_inputs(audio_filepath, image_filepath, video_filepath):
    if not audio_filepath:
        raise gr.Error("Please record or upload your voice description first.")

    if not image_filepath and not video_filepath:
        raise gr.Error("Please upload a skin image or video before analysis.")

    patient_text = transcribe_patient_voice(audio_filepath)
    doctor_text = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_filepath,
        video_filepath=video_filepath,
    )
    doctor_audio = convert_text_to_doctor_audio(doctor_text)

    return patient_text, doctor_text, str(Path(doctor_audio))


with gr.Blocks(title=APP_TITLE) as iface:
    with gr.Column(elem_classes="ais-shell"):
        gr.HTML(
            """
            <header class="ais-topbar">
                <div class="ais-brand">
                    <h1>AI Skin Specialist</h1>
                    <p>VOICE, IMAGE, AND VIDEO BASED SKIN CONSULTATION ASSISTANT</p>
                </div>
                <div class="ais-security">
                    <span class="ais-icon">security</span>
                    <span>Privacy-first consultation</span>
                </div>
            </header>
            """
        )

        with gr.Row(elem_classes="ais-grid"):
            with gr.Column(scale=5):
                gr.HTML(
                    """
                    <div class="ais-section-title">
                        <span class="ais-icon">clinical_notes</span>
                        <h2>Patient Input</h2>
                    </div>
                    """
                )

                with gr.Column(elem_classes="ais-card ais-input-card"):
                    gr.HTML('<span class="ais-field-label">Describe your skin concern</span>')
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Patient Voice",
                    )

                    with gr.Row(elem_classes="ais-media-row"):
                        image_input = gr.Image(
                            type="filepath",
                            label="Skin Image",
                            height=280,
                        )
                        video_input = gr.Video(label="Skin Video", height=280)

                    with gr.Column(elem_classes="ais-submit-wrap"):
                        analyze_button = gr.Button(
                            "Analyze Concern",
                            variant="primary",
                            size="lg",
                        )

                    gr.HTML(
                        """
                        <div class="ais-note">
                            <span class="ais-icon">info</span>
                            <span>For better assessment, include a short video showing the affected area from multiple angles and under good lighting.</span>
                        </div>
                        """
                    )

            with gr.Column(scale=7):
                gr.HTML(
                    """
                    <div class="ais-section-title">
                        <span class="ais-icon">smart_toy</span>
                        <h2>Doctor Response</h2>
                    </div>
                    """
                )

                with gr.Column(elem_classes="ais-card ais-response-card"):
                    gr.HTML(
                        """
                        <div class="ais-empty">
                            <span class="ais-icon">pending_actions</span>
                            <div>
                                <strong>Ready for Analysis</strong>
                                <p class="ais-panel-copy">Your consultation summary, transcript, and guidance will appear below after analysis.</p>
                            </div>
                        </div>
                        """
                    )

                    with gr.Column(elem_classes="ais-output-stack"):
                        transcript_output = gr.Textbox(
                            label="Your Speech Transcript",
                            lines=4,
                            interactive=False,
                            elem_classes="ais-transcript",
                        )
                        response_output = gr.Textbox(
                            label="Doctor's Guidance",
                            lines=9,
                            interactive=False,
                        )
                        audio_output = gr.Audio(
                            label="Doctor Voice Response",
                            type="filepath",
                            autoplay=True,
                            elem_classes="ais-audio",
                        )

                gr.HTML(
                    """
                    <div class="ais-security" style="justify-content:center; margin-top:16px;">
                        <span class="ais-icon">verified</span>
                        <span>AI guidance is informational and not a medical diagnosis</span>
                    </div>
                    """
                )

        gr.HTML(
            """
            <footer class="ais-footer">
                <div><strong>AI Skin Specialist</strong><br/>Consult a licensed dermatologist for urgent or serious symptoms.</div>
                <div>Privacy Policy · Terms of Service · Medical Disclaimer</div>
            </footer>
            """
        )

    analyze_button.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, video_input],
        outputs=[transcript_output, response_output, audio_output],
    )


if __name__ == "__main__":
    iface.launch(debug=True, css=CSS, theme=gr.themes.Base())
