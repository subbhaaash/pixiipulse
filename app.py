import os
import json
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# 1. ENV SETUP
# -----------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# 2. PAGE UI
# -----------------------------
st.set_page_config(page_title="PixiiPulse", layout="wide")

st.title("🚀 PixiiPulse")
st.subheader("Amazon Conversion Fix Engine")
st.write("Built for the AI shopping era — optimized for humans + Amazon Rufus.")

url = st.text_input("Paste Amazon Product URL")

# -----------------------------
# 3. AMAZON DATA EXTRACTION
# -----------------------------
def extract_with_jina(product_url: str) -> str:
    product_url = product_url.strip()
    clean_url = product_url.replace("https://", "").replace("http://", "")
    reader_url = f"https://r.jina.ai/http://{clean_url}"

    response = requests.get(
        reader_url,
        timeout=40,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()
    return response.text

# -----------------------------
# 4. CLEAN DATA — FIXED
# -----------------------------
def clean_listing_text(raw_text: str) -> str:
    lines = raw_text.split("\n")
    cleaned = []

    junk = [
        "skip to", "sign in", "cart", "orders", "javascript", "nav_",
        "select the department", "search amazon", "update location",
        "back to top", "all rights reserved"
    ]

    for line in lines:
        line = line.strip()

        # short bullets/features bachane ke liye len 10
        if len(line) < 10:
            continue

        if any(j in line.lower() for j in junk):
            continue

        cleaned.append(line)

    return "\n".join(cleaned[:300])

# -----------------------------
# 5. DATA QUALITY CHECK
# -----------------------------
def evaluate_input_quality(text: str) -> dict:
    length = len(text.strip())

    if length < 300:
        return {
            "confidence": "LOW",
            "allow_full_audit": False,
            "reason": "Insufficient listing data extracted."
        }

    if length < 1200:
        return {
            "confidence": "MEDIUM",
            "allow_full_audit": True,
            "reason": "Partial but usable listing data extracted."
        }

    return {
        "confidence": "HIGH",
        "allow_full_audit": True,
        "reason": "Strong listing data extracted."
    }

# -----------------------------
# 6. JSON SAFE PARSER
# -----------------------------
def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("AI did not return valid JSON.")
        return json.loads(match.group(0))

# -----------------------------
# 7. FALLBACK RESPONSE
# -----------------------------
def fallback_response(confidence: str) -> dict:
    return {
        "score": 25,
        "analysis_confidence": confidence,
        "summary": "Limited data detected. Full audit is not reliable, but PixiiPulse still identified the first obvious gap: the listing needs richer product information.",
        "rufus_readiness_score": 20,
        "rufus_readiness_reason": "Amazon Rufus or any AI shopping assistant may struggle because the extracted listing data is too thin to answer buyer questions confidently.",
        "score_breakdown": {
            "content_clarity": {"score": 10, "max_score": 40, "reason": "Not enough product detail extracted."},
            "trust_signals": {"score": 5, "max_score": 20, "reason": "Trust evidence could not be verified from extracted data."},
            "aeo_readiness": {"score": 5, "max_score": 20, "reason": "AI-readable product context is insufficient."},
            "conversion_triggers": {"score": 5, "max_score": 20, "reason": "Conversion triggers could not be verified."}
        },
        "critical_fixes": [
            {
                "issue": "Insufficient product detail detected",
                "psychology": "Buyers hesitate when they cannot quickly understand use case, benefits, and proof.",
                "impact": "Low clarity can reduce buyer confidence and increase drop-off risk.",
                "fix": "Add clear feature-benefit bullets, use-case explanation, trust proof, and visual explanation.",
                "priority": "High",
                "confidence": 0.7
            }
        ],
        "quick_wins": [
            {
                "action": "Add structured product bullets",
                "why": "Short, clear bullets reduce cognitive load.",
                "impact": "Improves buyer understanding and AI readability."
            }
        ],
        "whats_working": [],
        "aeo_audit": {
            "ai_clarity": "Low confidence because listing data is incomplete.",
            "missing_semantic_keywords": ["use case", "target buyer", "key benefits", "proof points"],
            "ai_blindspots": [
                {
                    "buyer_question": "What is this product best used for?",
                    "why_ai_struggles": "The extracted text does not provide enough structured context.",
                    "revenue_risk": "Buyers may leave if the value is unclear.",
                    "fix": "Add direct use-case and benefit-led bullets."
                }
            ]
        },
        "psychological_audit": {
            "dominant_emotion": "Uncertainty",
            "missing_triggers": ["Trust", "Authority", "Social Proof"],
            "friction_points": ["Insufficient clarity", "Weak proof"]
        },
        "customer_pain_points": ["Unclear value", "Low trust"],
        "listing_transformation": {
            "current_positioning": "Incomplete and unclear",
            "pixii_optimized_positioning": "Clear, trustworthy, and benefit-led",
            "improved_headline": "Clear product headline with key benefit and target use case",
            "improved_bullets": [
                "Explain who this product is for",
                "Highlight top 3 benefits",
                "Add proof or trust signal"
            ]
        },
        "pixii_visual_roadmap": [
            {
                "image_type": "Hero Image",
                "strategy": "Clarify product value instantly",
                "design_brief": "Create a clean hero image showing the product, key benefit, and trust cue.",
                "conversion_why": "A clear visual reduces confusion and increases buyer confidence."
            }
        ],
        "omnichannel_strategy": {
            "tiktok_hook": "Show the product solving one clear pain point in 5 seconds.",
            "instagram_vibe": "Clean, benefit-led product visual with trust badges.",
            "shopify_angle": "Position around clarity, proof, and use case."
        },
        "hooks": ["Know what you are buying before you click", "Clear benefit, less confusion"],
        "projected_impact": {
            "conversion_uplift": "Not reliable from limited data",
            "business_case": "Better listing clarity can improve buyer confidence and reduce hesitation."
        },
        "final_recommendation": "Improve listing clarity first, then use Pixii visuals to convert the core value into buyer-ready creative."
    }

# -----------------------------
# 8. AI CONSULTANT ENGINE
# -----------------------------
def analyze_with_groq(listing_text: str) -> dict:
    quality = evaluate_input_quality(listing_text)

    if not quality["allow_full_audit"]:
        return fallback_response(quality["confidence"])

    prompt = f"""
You are a world-class Amazon Conversion Strategist, AEO Strategist, and Pixii.ai Product Strategist.

Your job:
Analyze this Amazon listing like a paid ecommerce consultant.
Return ONLY valid JSON. No markdown. No text outside JSON.

CRITICAL SAFETY RULES:
- Never give 0/100 score.
- Do not hallucinate product features.
- Do not invent exact revenue numbers.
- Use realistic ranges only.
- Avoid generic advice like "improve description".
- Every fix must include WHY + IMPACT + ACTION.
- If data is partial, reduce confidence.
- Never treat missing images, broken links, unavailable data, or boilerplate return policy as "what's working".
- Pixii designs visuals, so every visual brief must be actionable.

JSON schema:
{{
  "score": 35,
  "analysis_confidence": "{quality['confidence']}",
  "summary": "2-3 line consultant-style summary",

  "rufus_readiness_score": 35,
  "rufus_readiness_reason": "how well Rufus/AI shopping assistant can answer buyer questions",

  "score_breakdown": {{
    "content_clarity": {{"score": 0, "max_score": 40, "reason": ""}},
    "trust_signals": {{"score": 0, "max_score": 20, "reason": ""}},
    "aeo_readiness": {{"score": 0, "max_score": 20, "reason": ""}},
    "conversion_triggers": {{"score": 0, "max_score": 20, "reason": ""}}
  }},

  "critical_fixes": [
    {{
      "issue": "specific bottleneck",
      "psychology": "buyer psychology hurdle",
      "impact": "conversion or trust risk",
      "fix": "specific actionable fix",
      "priority": "High",
      "confidence": 0.8
    }}
  ],

  "quick_wins": [
    {{
      "action": "specific quick fix",
      "why": "why this matters",
      "impact": "conversion logic"
    }}
  ],

  "whats_working": ["only real strengths from listing text"],

  "aeo_audit": {{
    "ai_clarity": "AI-readability diagnosis",
    "missing_semantic_keywords": ["keyword1", "keyword2"],
    "ai_blindspots": [
      {{
        "buyer_question": "real buyer question",
        "why_ai_struggles": "what is missing semantically",
        "revenue_risk": "business risk in non-fake language",
        "fix": "specific content or visual fix"
      }}
    ]
  }},

  "psychological_audit": {{
    "dominant_emotion": "Trust / Excitement / Desire / Security / Neutral / Uncertainty",
    "missing_triggers": ["Social Proof", "Authority", "Scarcity"],
    "friction_points": ["point 1", "point 2"]
  }},

  "customer_pain_points": ["pain 1", "pain 2"],

  "listing_transformation": {{
    "current_positioning": "how listing currently feels",
    "pixii_optimized_positioning": "how it should feel",
    "improved_headline": "better headline",
    "improved_bullets": ["bullet 1", "bullet 2", "bullet 3"]
  }},

  "pixii_visual_roadmap": [
    {{
      "image_type": "Hero Image / Lifestyle Image / Infographic / Trust Badge Image",
      "strategy": "psychological or AEO strategy",
      "design_brief": "specific Pixii design instruction",
      "conversion_why": "why this visual helps conversion"
    }}
  ],

  "omnichannel_strategy": {{
    "tiktok_hook": "short-form hook",
    "instagram_vibe": "visual aesthetic",
    "shopify_angle": "sales positioning"
  }},

  "hooks": ["hook 1", "hook 2", "hook 3"],

  "projected_impact": {{
    "conversion_uplift": "realistic range, not exact guarantee",
    "business_case": "why this matters"
  }},

  "final_recommendation": "one strong use-first recommendation"
}}

Listing text:
{listing_text[:6000]}
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.15,
    )

    data = extract_json(response.choices[0].message.content)

    data["score"] = max(20, int(data.get("score", 20)))
    data["rufus_readiness_score"] = max(20, int(data.get("rufus_readiness_score", 20)))
    data["analysis_confidence"] = data.get("analysis_confidence", quality["confidence"])

    return data

# -----------------------------
# 9. MAIN APP
# -----------------------------
if st.button("Analyze Listing"):
    if not url:
        st.error("Please paste an Amazon product URL.")
    else:
        try:
            with st.status("Running PixiiPulse audit...", expanded=True) as status:
                st.write("🔍 Extracting Amazon listing data...")
                extracted_text = extract_with_jina(url)

                st.write("🧹 Cleaning listing data without removing useful bullets...")
                cleaned_text = clean_listing_text(extracted_text)

                st.write("🧠 Running consultant-grade conversion + AEO audit...")
                data = analyze_with_groq(cleaned_text)

                status.update(label="Audit complete ✅", state="complete", expanded=False)

            st.success("✅ Listing analyzed successfully!")

            score = max(20, int(data.get("score", 20)))
            rufus = max(20, int(data.get("rufus_readiness_score", 20)))
            confidence = data.get("analysis_confidence", "MEDIUM")
            critical_count = len(data.get("critical_fixes", []))
            quick_count = len(data.get("quick_wins", []))

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Conversion Score", f"{score}/100", delta="Needs optimization")

            with col2:
                st.metric("Rufus / AEO Readiness", f"{rufus}/100", delta="AI visibility risk")

            with col3:
                st.metric("Critical Fixes", critical_count)

            with col4:
                st.metric("Quick Wins", quick_count)

            st.caption(f"Analysis Confidence: {confidence}")
            st.caption("Score based on content clarity, trust signals, AEO readiness, and conversion psychology.")

            st.divider()

            st.subheader("📊 Score Breakdown")
            breakdown = data.get("score_breakdown", {})

            b1, b2, b3, b4 = st.columns(4)

            for col, key, label, max_score in [
                (b1, "content_clarity", "Content Clarity", 40),
                (b2, "trust_signals", "Trust Signals", 20),
                (b3, "aeo_readiness", "AEO Readiness", 20),
                (b4, "conversion_triggers", "Conversion Triggers", 20),
            ]:
                with col:
                    item = breakdown.get(key, {})
                    st.metric(label, f"{item.get('score', 0)}/{item.get('max_score', max_score)}")
                    st.caption(item.get("reason", ""))

            st.divider()

            st.subheader("📌 Executive Summary")
            st.info(data.get("summary", "No summary generated."))

            st.subheader("🤖 Rufus / AEO Readiness")
            st.info(data.get("rufus_readiness_reason", "No Rufus readiness reason generated."))

            st.divider()

            col_bad, col_good, col_growth = st.columns(3)

            with col_bad:
                st.subheader("🚨 Critical Fixes")
                for fix in data.get("critical_fixes", []):
                    if isinstance(fix, dict):
                        st.error(
                            f"**[{fix.get('priority', 'High')}] {fix.get('issue', '')}**\n\n"
                            f"**Psychology:** {fix.get('psychology', '')}\n\n"
                            f"**Impact:** {fix.get('impact', '')}\n\n"
                            f"**Fix:** {fix.get('fix', '')}\n\n"
                            f"**Confidence:** {fix.get('confidence', '')}"
                        )
                    else:
                        st.error(fix)

            with col_good:
                st.subheader("✅ What’s Working")
                working = data.get("whats_working", [])
                if working:
                    for item in working:
                        st.success(item)
                else:
                    st.caption("No strong verified strengths detected from extracted listing data.")

            with col_growth:
                st.subheader("💡 Quick Wins")
                for item in data.get("quick_wins", []):
                    if isinstance(item, dict):
                        st.warning(
                            f"**Action:** {item.get('action', '')}\n\n"
                            f"**Why:** {item.get('why', '')}\n\n"
                            f"**Impact:** {item.get('impact', '')}"
                        )
                    else:
                        st.warning(item)

            st.divider()

            st.subheader("🧠 AEO Audit: AI Blindspots")
            aeo = data.get("aeo_audit", {})
            st.info(aeo.get("ai_clarity", "No AI clarity analysis generated."))

            keywords = aeo.get("missing_semantic_keywords", [])
            if keywords:
                st.write("**Missing semantic keywords:**")
                st.write(", ".join(keywords))

            for item in aeo.get("ai_blindspots", []):
                with st.container(border=True):
                    st.markdown(f"### Buyer Question: {item.get('buyer_question', '')}")
                    st.write(f"**Why AI struggles:** {item.get('why_ai_struggles', '')}")
                    st.write(f"**Revenue risk:** {item.get('revenue_risk', '')}")
                    st.write(f"**Fix:** {item.get('fix', '')}")

            st.divider()

            st.subheader("🧩 Psychological Trigger Audit")
            psych = data.get("psychological_audit", {})

            p1, p2 = st.columns(2)

            with p1:
                st.metric("Dominant Emotion", psych.get("dominant_emotion", "N/A"))

            with p2:
                missing = psych.get("missing_triggers", [])
                st.write("**Missing triggers:**")
                st.write(", ".join(missing) if missing else "No missing trigger detected.")

            for point in psych.get("friction_points", []):
                st.warning(point)

            st.divider()

            st.subheader("🧠 Customer Pain Points")
            for pain in data.get("customer_pain_points", []):
                st.write(f"- {pain}")

            st.divider()

            st.subheader("🔁 Listing Transformation Simulation")
            transformation = data.get("listing_transformation", {})

            left, right = st.columns(2)

            with left:
                st.markdown("### Current Listing Feel")
                st.warning(transformation.get("current_positioning", "No current positioning generated."))

            with right:
                st.markdown("### Pixii-Optimized Feel")
                st.success(transformation.get("pixii_optimized_positioning", "No optimized positioning generated."))

            st.markdown("### Improved Headline")
            st.info(transformation.get("improved_headline", "No improved headline generated."))

            bullets = transformation.get("improved_bullets", [])
            if bullets:
                st.markdown("### Improved Bullets")
                for bullet in bullets:
                    st.write(f"- {bullet}")

            st.divider()

            st.subheader("🎨 Pixii Visual Roadmap")
            st.write("What Pixii should design next to improve conversion:")

            for item in data.get("pixii_visual_roadmap", []):
                with st.container(border=True):
                    st.markdown(f"### {item.get('image_type', 'Image Concept')}")
                    st.write(f"**Strategy:** {item.get('strategy', '')}")
                    st.write(f"**Design brief:** {item.get('design_brief', '')}")
                    st.caption(f"Conversion why: {item.get('conversion_why', '')}")

            st.button("✨ Send Brief to Pixii Designer")

            st.divider()

            st.subheader("🌍 Omnichannel Repurposing")
            omni = data.get("omnichannel_strategy", {})

            o1, o2, o3 = st.columns(3)

            with o1:
                st.markdown("### TikTok Hook")
                st.info(omni.get("tiktok_hook", "No TikTok hook generated."))

            with o2:
                st.markdown("### Instagram Vibe")
                st.info(omni.get("instagram_vibe", "No Instagram vibe generated."))

            with o3:
                st.markdown("### Shopify Angle")
                st.info(omni.get("shopify_angle", "No Shopify angle generated."))

            st.divider()

            st.subheader("🪝 Ad / Listing Hooks")
            for hook in data.get("hooks", []):
                st.write(f"- {hook}")

            st.divider()

            st.subheader("💰 Estimated Business Impact")
            impact = data.get("projected_impact", {})
            st.success(
                f"**Estimated uplift:** {impact.get('conversion_uplift', 'Not estimated')}\n\n"
                f"**Business case:** {impact.get('business_case', 'No business case generated.')}"
            )

            st.divider()

            st.subheader("🚀 Use-First Recommendation")
            st.success(data.get("final_recommendation", "No recommendation generated."))

            report_text = json.dumps(data, indent=2, ensure_ascii=False)

            st.download_button(
                label="⬇️ Download Audit Report",
                data=report_text,
                file_name="pixiipulse_audit_report.json",
                mime="application/json",
            )

            with st.expander("🔍 Raw Extracted Data"):
                st.text_area("Raw listing text", extracted_text[:7000], height=350)

        except Exception as e:
            st.error("Error occurred.")
            st.write(e)