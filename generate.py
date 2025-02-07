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
    mental_health_screening: List[str]
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


import re
import json




def generate_health_insights(input_data: dict) -> ClinicalAssessment:
    prompt = f"""
**Comprehensive Health Risk Assessment & Clinical Guidance**

Analyze the provided patient data and generate a **structured JSON response** with **clinically relevant recommendations** based on validated twice, numerical insights. Ensure precise, non-repetitive, and quantified or changes recommendations with comparisons between the latest and previous data,
**data is in the ascending order with last being the latest validate and generate the content**

#### **Patient Data:**  
{json.dumps(input_data, indent=2)}

---

### **Output Requirements**:
1. **Strict JSON Format**: Follow the exact structure of the `ClinicalAssessment` class and use different action verbs(no repeatation):

**for recommendations just have string lists returned with some metrics comparison wherever necessary also have donts points as well as only do point are here in each item**
"recommendations": {{
            **for each item, search in your knowledge base for every profile what scores or data can be used for generating recommendations and use this scores based on patient data to generate, at least generate 1 value with max being 5 and an average of 2-3 points** 
            "monitoring": **Generate at least two recommendation for monitoring based on the patient's latest data**,
            "medication": **Generate at least two medication recommendation based on the patient's latest data**,
            "heart_health": **Generate at least two recommendation related to heart health based on heart metrics like heart rate, SBP, DBP, cholesterol levels, ASCVD risk, etc.**,
            "liver_health": **Generate at least two recommendation related to liver health based on liver-related metrics such as bilirubin, protein levels, albumin, globulin, etc.**,
            "kidney_health": **Generate at least two recommendation for kidney health based on kidney-related metrics like creatinine, CKD risk, etc.**,
            "mental_health Screening": **Generate at least two recommendation based on mental health indicators from the available patient data**,
            "diet_suggestion": **Generate at least two diet suggestion based on the patient's overall profile data (e.g., waist circumference, BMI, cholesterol levels, heart_profile,liver_profile,kidney_profile)**,
       }}

**for insights return metrics comparison for all points with validation as proof from patient data, triple check **important****.
"insights": {{
           "primary_risk_factors": **each factor when risk is going up ignore age and all show for scores_metrics and health_metrics only with proof based on patient data(latest being at last index)**,
           "trend_analysis": **each analysis should have similar comparisons,do not mix with each other,**validate thrice until you are 100% confident and quantify** based on patient data(latest being at last index)** ,
       }},
       "action_items": {{
           "immediate_actions": ["action1", "action2",..],
           "long_term_goals": ["goal1", "goal2",..]
       }}

"summary": "Detailed Summary **main-content** as per your understanding in 300 words of patient current/latest data",
"""

    try:
        response = ollama.chat(
        model='qwen2.5:3b',
        messages=[{'role': 'user', 'content': prompt}],
        format=ClinicalAssessment.model_json_schema(),
        options={
            'temperature': 0.1,  # Reduce randomness for better structure
            'num_ctx': 6096,
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
