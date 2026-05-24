import gradio as gr
from predictor import CCBEdemaPredictor

predictor = CCBEdemaPredictor()

custom_css = """
.container { max-width: 1050px; margin: 0 auto; padding-top: 20px; }
.clinical-card { 
    background-color: #f8fafc; 
    border: 1px solid #e2e8f0; 
    border-radius: 12px; 
    padding: 20px; 
    margin-bottom: 15px; 
}
.card-header { 
    font-size: 1.15em; 
    font-weight: 600; 
    color: #1e293b; 
    border-bottom: 1px solid #e2e8f0; 
    padding-bottom: 8px; 
    margin-bottom: 15px; 
}
"""

def process_prediction(age, gender, daily_standing_hours, ccb_dose, taking_raas_inhibitor):
    prob = predictor.calculate_risk(age, gender, daily_standing_hours, ccb_dose, taking_raas_inhibitor)
    
    if prob < 20.0:
        bg, border, text = "#f0fdf4", "#bbf7d0", "#166534"
        tier = "LOW OVERALL RISK"
        plan = "• Proceed with standard treatment plan.<br>• Perform routine surveillance during regular clinical follow-ups."
    elif 20.0 <= prob < 40.0:
        bg, border, text = "#fffbeb", "#fef3c7", "#92400e"
        tier = "MODERATE OVERALL RISK"
        plan = "• Initiate non-pharmacological counseling (strategic sitting windows, lower extremity elevation).<br>• Establish baseline lower limb inspection notes."
    else:
        bg, border, text = "#fef2f2", "#fecaca", "#991b1b"
        tier = "HIGH OVERALL RISK"
        plan = ("• High predisposition to drug-induced capillary fluid retention.<br>"
                "• Consider down-titration of CCB or pairing with synergistic classes if clinically appropriate.<br>"
                "• Optimize or initiate a <strong>concomitant ACEi / ARB</strong> to mitigate precapillary hydrostatic pressure.<br>"
                "• Proactively counsel patient to avoid unnecessary loops or secondary prescribing cascades.")

    html_output = f"""
    <div style="background-color: {bg}; border: 1px solid {border}; color: {text}; padding: 24px; border-radius: 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid {border}; padding-bottom: 10px; margin-bottom: 16px;">
            <span style="font-weight: 700; letter-spacing: 0.05em; font-size: 0.95em;">{tier}</span>
            <span style="font-size: 0.85em; opacity: 0.85;">Based on Retrospective Cohort Model</span>
        </div>
        <div style="margin-bottom: 18px;">
            <p style="margin: 0; font-size: 0.95em; opacity: 0.9;">Calculated Probability of Peripheral Edema:</p>
            <h1 style="margin: 4px 0 0 0; font-size: 2.8em; font-weight: 800; color: {text};">{prob}%</h1>
        </div>
        <div>
            <h4 style="margin: 0 0 8px 0; font-size: 1.05em; font-weight: 600;">Actionable Clinical Guidance:</h4>
            <div style="font-size: 0.95em; line-height: 1.6; opacity: 0.95;">{plan}</div>
        </div>
    </div>
    """
    return html_output

with gr.Blocks(theme=gr.themes.Default(primary_hue="slate", font=["Inter", "sans-serif"]), css=custom_css) as demo:
    with gr.Div(elem_classes="container"):
        gr.Markdown(
            """
            # CCB-Induced Peripheral Edema Calculator
            *A point-of-care stratification assistant implementing risk profiles derived from multi-center clinical data.*
            """
        )
        
        with gr.Row():
            with gr.Column(scale=12):
                with gr.Box(elem_classes="clinical-card"):
                    gr.HTML("<div class='card-header'>1. Patient Characteristics</div>")
                    age = gr.Slider(minimum=18, maximum=100, value=55, step=1, label="Patient Age (Years)")
                    gender = gr.Radio(choices=["Male", "Female"], value="Male", label="Biological Sex")
                
                with gr.Box(elem_classes="clinical-card"):
                    gr.HTML("<div class='card-header'>2. Postural Exposure</div>")
                    daily_standing_hours = gr.Slider(
                        minimum=0, maximum=16, value=2, step=0.5, 
                        label="Average Daily Standing (Hours)",
                        info="Durations ≥ 3 hours represent an independent clinical risk factor (AOR=1.92)."
                    )
            
            with gr.Column(scale=12):
                with gr.Box(elem_classes="clinical-card"):
                    gr.HTML("<div class='card-header'>3. Pharmacotherapeutic Profile</div>")
                    ccb_dose = gr.Dropdown(
                        choices=["Low Dose (e.g., Amlodipine 5mg)", "High Dose (e.g., Amlodipine 10mg, Nifedipine ≥40mg)"],
                        value="Low Dose (e.g., Amlodipine 5mg)",
                        label="Calcium Channel Blocker Regimen"
                    )
                    taking_raas_inhibitor = gr.Checkbox(
                        value=False, 
                        label="Concomitant RAAS Inhibitor (ACEi / ARB)",
                        info="Co-administration offers counter-regulatory venodilation to balance capillary pressure."
                    )
                
                submit_btn = gr.Button("Generate Risk Profile Evaluation", variant="primary", size="lg")
        
        with gr.Row(style="margin-top: 20px;"):
            with gr.Column(scale=24):
                output_html = gr.HTML(
                    value="""
                    <div style="text-align: center; color: #64748b; padding: 30px; border: 2px dashed #cbd5e1; border-radius: 10px; background-color: #f8fafc;">
                        Complete the diagnostic entries above and click "Generate Risk Profile Evaluation" to see structural analytics.
                    </div>
                    """
                )

        submit_btn.click(
            fn=process_prediction, 
            inputs=[age, gender, daily_standing_hours, ccb_dose, taking_raas_inhibitor], 
            outputs=output_html
        )

if __name__ == "__main__":
    demo.launch()