import ollama
from pydantic import BaseModel
from typing import List, Literal
import json
import re

class Recommendations(BaseModel):
    monitoring: List[str]
    medication: List[str]
    heart_health: List[str]
    liver_health: List[str]
    kidney_health: List[str]
    diet_suggestion: List[str]

class Insights(BaseModel):
    primary_risk_factors: List[str]
    trend_analysis: List[str]

class ActionItems(BaseModel):
    immediate_actions: List[str]
    long_term_goals: List[str]


class ClinicalAssessment(BaseModel):
    recommendations: Recommendations
    insights: Insights
    action_items: ActionItems
    summary: str



def generate_health_insights(input_data: dict) -> ClinicalAssessment:
    prompt = f"""
    ## **Comprehensive Health Risk Assessment & Clinical Guidance**
    You are a helpful assistant that provides health insights based on patient data. Analyze the provided patient data in chronological order, with the latest data at the end. Use the age column for comparison between the two most recent data points. Generate a **structured JSON response** with **clinically relevant recommendations** based on validated numerical insights. Ensure precise, non-repetitive, and quantified recommendations with comparisons between the latest and previous data, along with their ideal ranges for justification. Validate the output thrice and generate the content as per the specified format.

    #### **Patient Data:**
    {json.dumps(input_data, indent=3)}

    ---

    ### **Output Requirements**:
    1. **Strict JSON Format**: Follow the exact structure of the **ClinicalAssessment** class. Use different action verbs (no repetition).
    2. **Metrics to Include**: Focus on the following metrics for analysis and recommendations:
       - **Heart Profile**: **chd_risk**, **chd_risk_category**, **enhanced_ascvd_risk**, **ascvd_category**
       - **Stroke Profile**: **Total_Stroke_Points**, **adjusted_stroke_risk**, **stroke_risk_category**
       - **Diabetes Profile**: **Total_Diabetes_Points**, **base_diabetes_risk**, **base_diabetes_risk_type**
       - **Kidney Profile**: **ckd_risk_points**, **ckd_risk_group**, **ckd_kidney_risk_category**
       - **Overall Profile**: **overall_risk_percentage**, **overall_risk_category**
       - **Common Metrics**: Only include **BMI**, **FBS**, **t_choles**, **ldl**, **hdl**, **sr_creatinine**, etc.,
    3. **Recommendations**: Generate actionable recommendations for each category. Justify each recommendation with specific metric values and ideal ranges.
    4. **Insights**: Analyze trends and risk factors for the specified metrics. Quantify changes and provide justifications.
    5. **Summary**: Provide a detailed summary of the patient's current health status, including specific metrics and their ideal ranges.
    6. **Do not repeat same contents, use unique points. For trends_analysis use above metrics also with quantifying with rationale.**
    ---

    ### **Structured JSON Template**:
    {{
      "recommendations": {{
        "monitoring": [
          "Recommendation 1 with justification and metric values",
          "Recommendation 2 with justification and metric values",
          **generate at least 2 recommendations**
        ],
        "medication": [
          "Medication advice 1 with dosage details. Note: Consult a health professional before taking any medication.",
          "Medication advice 2 with frequency info. Note: Consult a health professional before taking any medication.",
          **generate at least 2 recommendations**
        ],
        "heart_health": [
          "Heart health recommendation 1 with justification",
          "Heart health recommendation 2 with justification",
          **generate at least 2 recommendations**
        ],
        "liver_health": [
          "Liver health recommendation 1 with justification",
          "Liver health recommendation 2 with justification",
          **generate at least 2 recommendations**
        ],
        "kidney_health": [
          "Kidney health recommendation 1 with justification",
          "Kidney health recommendation 2 with justification",
          **generate at least 2 recommendations**
        ],
        "diet_suggestion": [
          "Dietary suggestion 1 with justification",
          "Dietary suggestion 2 with justification",
          **generate at least 2 recommendations**
        ]
      }},
      "insights": {{
        "primary_risk_factors": [
          "Risk factor 1: value (ideal range). Sentence should be in passive voice with justification.",
          "Risk factor 2: value (ideal range). Sentence should be in passive voice with justification.",
          **generate at least 4 factors having comparison with age and specific risk values mostly have category type value in patient data like high/low/moderate**
        ],
        "trend_analysis": [
          "Trend analysis 1 with quantified changes and justification.",
          "Trend analysis 2 with quantified changes and justification.",
          **generate at least 4 trends with quantifying every points with proper rationale for better readability with points different from primary_risk_factors**
        ]
      }},
      "action_items": {{
        "immediate_actions": [
          "Immediate action 1 with details",
          "Immediate action 2 with details"
        ],
        "long_term_goals": [
          "Long-term goal 1 with measurable outcome",
          "Long-term goal 2 with measurable outcome"
        ]
      }},
      "summary": "Detailed summary of the patient's current health status, including specific metrics and their ideal ranges for justification. The summary should be around 300 words and provide a comprehensive overview of the patient's health."
    }}

    ---

    ### **Guidelines for Insights**:  
      1. Data Order: Data is sorted in chronological or ascending order by age.
      2. Insight Justification: Clearly explain each trend or factor with rationale, using specific numbers. Validate data thoroughly and avoid repeating points.
      3. Differentiation of sub-sections of insights keys:
          - For Trend Analysis: Analyze historical data to identify trends over time. Use metrics relevant to trends.
          - For Primary Risk Factors: Focus on the latest data only, highlighting current risk factors and their impact. Use metrics relevant to current risks.
          - Do not use same metrics for both the subsections have different metrics for comparison.
        4. Metrics: Use different metrics for trend analysis and primary risk factors. Do not repeat metrics in both sections **immportant**.
        5. Quantity: Provide at least 4 unique points for each section, supported by data.
        6. Data Usage: Only use the provided patient data. Do not make assumptions or add external information.
        7. Formatting: Avoid special symbols or brackets in the insights and see guidelines for keywords and use their full names.

    ---

    ### **Critical Instructions**:
    1. **Prioritize Specified Metrics**: Focus on the metrics listed above for every profile. Only include common metrics like **BMI** and **FBS** if they are significantly out of range or concerning.
    2. **Avoid Repetition**: Ensure there is no repetition of sentences or content between **primary_risk_factors** and **trend_analysis**.
    3. **Passive Voice**: Use passive voice for all sentences in the **primary_risk_factors** section.
    4. **Validation**: Validate the generated output thrice to ensure:
       - No repetition of sentences or content.
       - All sentences are in passive voice.
       - The JSON structure is correct and adheres to the template.
    5. **Quantify Changes**: For trend analysis and primary risk factors, quantify changes in metrics over time(age) and provide justifications.
    6. **Justify Recommendations**: For recommendations, include specific metric values and their ideal ranges for justification.

    ---

    ### **Guidelines for recommendations**:
         - Have 2 points at least generated and validate with the patient's data as well

    ---

    ### **Guidelines for Keywords**:
            "chd": "Coronary Heart Disease",
            "ckd": "Chronic Kidney Disease",
            "ascvd": "Atherosclerotic Cardiovascular Disease",
            "fbs": "Fasting Blood Sugar",
            "ppbs": "Postprandial Blood Sugar",
            "hba1c": "Hemoglobin A1c",
            "t_choles": "Total Cholesterol",
            "hdl": "High-Density Lipoprotein",
            "ldl": "Low-Density Lipoprotein",
            "sr_creatinine": "Serum Creatinine",
            "sr_albumin": "Serum Albumin",
            "sr_globulin": "Serum Globulin",
            "hb": "Hemoglobin",
            "wbc": "White Blood Cells",
            "plt": "Platelets",
            "t_bilirubin": "Total Bilirubin",
            "temp_f": "Temperature (Fahrenheit)",
            "spo2": "Oxygen Saturation",
            "sbp": "Systolic Blood Pressure",
            "dbp": "Diastolic Blood Pressure",
            "heart_rate": "Heart Rate",
            "waist_circumference": "Waist Circumference",
            "phy_activity": "Physical Activity",
            "smoking": "Smoking",
            "alcohol_intake": "Alcohol Intake",
            "family_h_o_dm": "Family History of Diabetes Mellitus",
            "family_h_o_heart_disease": "Family History of Heart Disease"

          - Use this keywords can be in capital,small or camel case but use full name in recommendations,insights and summary and in goals as well.
    """

    try:
        response = ollama.chat(
        model='qwen2.5:3b',
        messages=[{'role': 'user', 'content': prompt}],
        format=ClinicalAssessment.model_json_schema(),
        options={
            'temperature': 0.2,  # Reduce randomness for better structure
            'num_ctx': 8096,
            'max_tokens': 4000,
            'repeat_penalty':1.2,
        }   
    )

        # Extract JSON from markdown code block
        raw_response = response['message']['content']
        # cleaned_content = clean_json_output(raw_response)
        return json.loads(raw_response)
        
    
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Parsing error: {str(e)}")
        return {"error": "Failed to process model response"}
    except Exception as e:
        print(f"API error: {str(e)}")
        return {"error": "Model inference failed"}