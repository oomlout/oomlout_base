{
  "task": "Generate a production-ready IMAGE PROMPT (not an image). The output must be a single prompt string only.",
  "input_variable": "{THEME}",
  "core_rules": {
    "subject": "One single character representing {THEME} only (no second character of any kind)",
    "interpretation": "{THEME} can be a person, place, or thing and must be expressed as a single character or mascot-style figure",
    "composition": "Single character, centered, full body visible",
    "pose": "Facing directly forward, looking straight out at the viewer",
    "action": "The character must be doing something funny, charming, or mildly silly that fits the nature of {THEME}",
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
    "role": "Mascot-style character representing {THEME}",
    "design": "Translate {THEME} into a clear, instantly recognisable visual character with simplified features",
    "expression": "Friendly, appealing, and slightly playful or amused",
    "readability": "Must be immediately recognisable as {THEME} even in simplified chibi form"
  },
  "colour_rules": {
    "colour_count": "Use exactly 4 to 6 colours total",
    "selection": "Choose colours after {THEME} is defined",
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