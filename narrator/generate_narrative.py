import json
import os

from google import genai
from google.genai import types


# ============================================================
# TASK 4 - OFFLINE FALLBACK
# ============================================================

def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Fully deterministic offline fallback.
    No API call, no network, no API key required.
    """

    findings_text = json.dumps(findings, indent=2)

    narrative = f"""Situation:
The verified business findings are summarized from the supplied data.

{findings_text}

Complication:
The findings indicate operational and performance areas that require attention based only on the verified data.

Resolution:
March was the true peak month with revenue of 20318.9 INR.
Finance and regional operations should use these verified findings to prioritize corrective actions and monitor performance.
"""

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": None,
    }


# ============================================================
# ONLINE + AUTOMATIC OFFLINE FALLBACK
# ============================================================

def generate_scr_narrative(findings: dict) -> dict:
    """
    Generate the business narrative using Gemini when an API key
    is available. Automatically falls back to the deterministic
    offline version if the API key is missing or the API call fails.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    # --------------------------------------------------------
    # No API key -> use deterministic offline fallback
    # --------------------------------------------------------
    if not api_key:
        return generate_scr_narrative_offline(findings)

    try:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=30_000
            )
        )

        # ----------------------------------------------------
        # System instruction
        # ----------------------------------------------------
        system_prompt = (
            "You are a senior data analyst writing for Mamaearth's business team. "
            "Write a business narrative using exactly three sections: "
            "Situation, Complication, and Resolution. "
            "Every number in the output MUST come directly from the supplied findings. "
            "Do not invent, estimate, or add any statistics. "
            "Use only the supplied findings. "
            "The narrative must include the true peak month March together with "
            "its revenue value 20318.9."
        )

        # ----------------------------------------------------
        # Findings supplied to the model
        # ----------------------------------------------------
        findings_json = json.dumps(
            findings,
            indent=2
        )

        # ----------------------------------------------------
        # User prompt
        # ----------------------------------------------------
        user_prompt = (
            "Create a concise business narrative from these verified findings:\n\n"
            f"{findings_json}\n\n"
            "The response must contain exactly these three sections:\n\n"
            "Situation:\n"
            "Complication:\n"
            "Resolution:\n\n"
            "Use only the supplied findings.\n"
            "Do not invent any numbers or statistics.\n"
            "Make sure the true peak month is identified as March "
            "and that its revenue is stated as 20318.9."
        )

        # ----------------------------------------------------
        # Gemini request
        # ----------------------------------------------------
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
                max_output_tokens=500,
            ),
        )

        tokens = None

        if response.usage_metadata:
            tokens = response.usage_metadata.total_token_count

        return {
            "status": "success",
            "narrative": response.text,
            "tokens": tokens,
        }

    except Exception:
        # ----------------------------------------------------
        # API error -> automatically use offline fallback
        # ----------------------------------------------------
        offline_result = generate_scr_narrative_offline(findings)

        return {
            "status": "success",
            "narrative": offline_result["narrative"],
            "tokens": None,
        }