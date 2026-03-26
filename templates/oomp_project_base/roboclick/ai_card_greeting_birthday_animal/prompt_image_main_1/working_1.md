{
  "task": "Generate a production-ready IMAGE PROMPT (not an image). The output must be a single prompt string only.",
  "input_variable": "{ANIMAL}",
  "core_rules": {
    "subject": "One single {ANIMAL} only (no second character of any kind)",
    "theme": "Mother's Day tone through styling and expression only (no text allowed)",
    "composition": "Single character, centered, full body visible",
    "pose": "Facing directly forward, looking straight out at the viewer",
    "action": "The {ANIMAL} must be doing something funny, charming, or mildly silly appropriate to the species",
    "background": "Pure white",
    "aspect_ratio": "3:2 landscape",
    "text": "No text, no letters, no symbols"
  },
  "style_rules": {
    "style": "Cute chibi style",
    "proportions": "Comically oversized head, very small body",
    "linework": "Bold clean outer lines, minimal inner lines",
    "rendering": "Flat vector-friendly, solid fills only",
    "detail_level": "Simple, readable, strong silhouette",
    "shading": "No gradients, no shading, no textures"
  },
  "character_rules": {
    "role": "Mother version of the {ANIMAL}",
    "age_cues": "Slightly older and more mature through expression and posture (still cute and child-friendly)",
    "expression": "Warm, kind, slightly proud or amused",
    "readability": "Clear species recognition with simplified features"
  },
  "colour_rules": {
    "colour_count": "Use exactly 4 to 6 colours total",
    "selection": "Choose colours after {ANIMAL} is defined",
    "style": "Flat, high-contrast, print-friendly palette",
    "restriction": "No gradients, no complex colour blending"
  },
  "composition_rules": {
    "layout": "Centered character with generous white space",
    "elements": "No extra objects unless required for the funny action",
    "clarity": "Keep composition clean, uncluttered, and bold"
  },
  "negative_constraints": [
    "no second character",
    "no baby animals",
    "no daughter",
    "no text or typography",
    "no background elements",
    "no gradients",
    "no shading",
    "no realistic rendering",
    "no 3D style",
    "no textures",
    "no borders or frames",
    "no clutter"
  ],
  "output_format": {
    "type": "single_string_prompt",
    "instruction": "Combine all rules into one cohesive, highly descriptive image prompt ready for an image generation model. Do not output JSON again. Do not generate the image."
  }
}