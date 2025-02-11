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


import re
import json




def generate_health_insights(input_data: dict) -> ClinicalAssessment:
    prompt = f"""
    **Comprehensive Health Risk Assessment & Clinical Guidance**
    ### **Analyze the provided patient data in chronological order with latest data is in last index and prior to it as previous values and generate a **structured JSON response** with **clinically relevant recommendations** based on validated twice, numerical insights. Ensure precise, non-repetitive, and quantified or changes recommendations with comparisons between the latest and previous data with their ideal ranges of normal type for justification ,**data is in a chronological order with last index being the latest **important** validate thrice and generate the content as per our format**, also have strings with no brackets (,[ and asterisk(*) symbol with having justification of the **insights,recommendations and summary** data with their ideal range of values which can be termed as normal along with the present scores for better understanding and remove all symbols like (,* from the genrated string**

    #### **Patient Data:**  
    {json.dumps(input_data, indent=2)}

    ---

    ### **Output Requirements**:
    1. **Strict JSON Format**: Follow the exact structure of the `ClinicalAssessment` class and use different action verbs(no repeatation):
    **metrics to be included are wt_kg, waist_circumference, family_h_o_dm, family_h_o_heart_disease, heart_rate, sbp, dbp, spo2, temp_f, hb, wbc, plt, fbs, ppbs, hba1c, t_choles, hdl, ldl, t_bilirubin, sr_creatinine, t_protein, sr_albumin, sr_globulin, bmi, chd_risk, chd_risk_category, enhanced_ascvd_risk, ascvd_category, Total_Stroke_Points,adjusted_stroke_risk, stroke_risk_category, Total_Diabetes_Points, base_diabetes_risk, base_diabetes_risk_type,ckd_risk_points, ckd_risk_group, ckd_kidney_risk_category, overall_risk_percentage, overall_risk_category of the patient data, **choose as per the most drastic changes important**

    **for recommendations just have string lists returned with some metrics comparison wherever necessary also have donts points as well as only do point are here in each item **do not use any brackets have string**
    "recommendations": {{
                **for each item, search in your knowledge base for every profile what scores or data can be used for generating recommendations and use this scores based on patient data to generate, at least generate 1 value with max being 5 and an average of 2-3 points also justify your answers with giving the ideal range of the values** 
                "monitoring": **Generate at least two recommendation for monitoring based on the patient's latest data**,
                "medication": **Generate at least two medication recommendation based on the patient's latest data**,
                "heart_health": **Generate at least two recommendation related to heart health based on heart metrics like heart rate, SBP, DBP, cholesterol levels, ASCVD risk, etc.**,
                "liver_health": **Generate at least two recommendation related to liver health based on liver-related metrics such as bilirubin, protein levels, albumin, globulin, etc.**,
                "kidney_health": **Generate at least two recommendation for kidney health based on kidney-related metrics like creatinine, CKD risk and ckd risk category**,
                "diet_suggestion": **Generate at least two diet suggestion based on the patient's overall profile data (e.g., waist circumference, BMI, cholesterol levels, heart_profile,liver_profile,kidney_profile)**,
        }}

    ** For insights return metrics comparison for all points with validation as proof from patient data, triple check **important** and 4 values at least
    ** for each item, use risk_category columns type for [ascvd,chd,ckd,stroke and overall risk] based on this paramaters, use patient data to generate at least 4 points with max being 6 and also justify your answers with giving the ideal range of the values given below :
        ascvd enhanced risk - 0 to 100 percent
        chd risk - 0 to 32 for Female and 0-56 for Male this are points
        ckd score group - 0 to 5 or G1 and G2 etc type category
        enhanced stroke risk - 0 to 100 percent
        overall risk percent - 0 to 100
        and all other health metrics search in your knowledge base and show it in all the points **important** 

    "insights": {{
            "primary_risk_factors": **each factor when risk is going up ignore age and all show for scores_metrics and health_metrics only with proof based on patient data(latest being at last index)**,
            "trend_analysis": **each analysis should have similar comparisons,do not mix with each other,**validate thrice until you are 100% confident and quantify** based on patient data(latest being at last index)**,
        }},
        "action_items": {{
            "immediate_actions": ["action1", "action2",..],
            "long_term_goals": ["goal1", "goal2",..]
        }}

    "summary": "Detailed Summary **main-content** as per your understanding in 300 words of patient current/latest data, also have the range for that metrics in numbers which is justifying the summary **important**",
    
    ### **Points Check for Assistant(AI) important **
    1. If proper quantifying of metrics with changes justified , you will get 10 positive points and in case of unfullfillment 20 negative penalty points 
    2. If proper justification is given with ideal ranges of values, you will get 5 positive points and in case of unfullfillment 20 negative penalty points
    3. Proper formatting with no extra special symbols or brackets, you will get 10 positive points and in case of unfullfillment 20 negative penalty points
    4. No blank values, you will get 10 positive points and in case of unfullfillment 20 negative penalty points
    5. For overall clean format and no spelling mistake and proper grammar with no repeatation of sentence carrying same meaning as well as for action verbs you will get 30 positive points and in case of unfullfillment 20 negative penalty points
    
    **Calculate this score based on your generated texts and rate yourself, if any condition is fullfilled positive points showing goood response quality else negative penalty points showing bad response from you, so make yourself the winner and beat everyone out there or be a LOSER.
    
    ### **Additional Guidelines for Insights**:
    
    1. **Primary Risk Factors**:
       - Prioritize the following metrics **only if they are out of the ideal range or concerning**:
         - Metrics like BMI, FBS, Hb, t_choles,ldl,hdl, sr_creatinine,overall_risk_category - for overall profile **important**
         - base_diabetes_risk_type - for diabetic profile
         - stroke_risk_category - for stroke profile
         - chd_risk_category - for heart profile
         - ckd_kidney_risk_category - for kidney profile

       - Include justification for each trend by quantifying with proper numbers and validation of it twice.

    2. **Trend Analysis**:
       - Analyze trends for the following metrics from patient data keys:
         - Total_Diabetes_Points, base_diabetes_risk, base_diabetes_risk_type keys -  for diabetic profile
         - Total_Stroke_Points, adjusted_stroke_risk, stroke_risk_category keys -  for stroke profile
         - chd_risk, chd_risk_category,enhanced_ascvd_risk keys -  for heart profile
         - ckd_kidney_risk_category, ckd_risk_points keys -  for kidney profile 
         - overall_risk_category, overall_risk_percentage - for overall profile

        - Include justification for each trend by quantifying with proper numbers and validation of it twice average of 4 points.

    ## primary risk factors can have Bmi and common metrics values as well apart from categories and both this sections should have a ideal range for that metrics in the sentence and min 3 points to max 6 points on an average 5.

    3. **Avoid Repetition**:
       - Ensure there is no repetition of sentences or content between `primary_risk_factors` and `trend_analysis`**important**.
       - Each section should have unique insights and justifications with quantifying with metrics values latest .

    4. **Validation**:
       - Validate the generated output twice to ensure:
         - No repetition of sentences or content.
         - All sentences are in passive voice.
         - The JSON structure is correct and adheres to the template.
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
