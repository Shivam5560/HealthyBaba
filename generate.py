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
          **generate at least 4 trends having comparison with age and specific risk values**
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

    ### **Important Notes**:
    - Only use the provided patient data. Do not make assumptions or add extraneous information.
    - Validate the output thrice to ensure accuracy and adherence to the data.
    - Follow the JSON schema strictly.

    ### **Guidelines for Insights**:  
        - Justify each trend or factor with clear rationale, quantifying insights with appropriate numbers and validating the data twice and mot repeat same points in insights.
        - difference should be there between trends analysis and primary risk factors, primary risk factors should show latest data only and their impact while trend analysis have to analyze historical data to generate trends based on the metrics stated above for each organ profile stated earlier in the prompt.
        - generate at least 4 points each with proper numbers.Only use the provided patient data. Do not make assumptions or add extraneous information.

    """
    print(prompt)
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
