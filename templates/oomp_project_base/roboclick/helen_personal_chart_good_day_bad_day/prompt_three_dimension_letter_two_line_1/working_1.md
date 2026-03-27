  {
  "core_rules": {
    "output": "The output must be a single image prompt only",
    "subject": "The subject is only the word(s) - no characters, no objects, no icons, no scenery",
    "text_layout": "All words must be arranged across exactly TWO lines (not one, not more)",
    "line_break": "Line break placement should be intentional and balanced for visual composition",
    "composition": "3:2 landscape",
    "background": "Pure white",
    "style": "Angular, constructed 3D lettering - precise, drafting-table aesthetic (not photorealistic)"
  },
  "colour_system": {
    "hex_definition": "Do NOT define specific hex colours",
    "palette_selection": "Select ONE palette name",
    "tone_limit": "Use 2-4 tones max (base, highlight, shadow, optional accent)",
    "note": "Next stage will define exact hex values",
    "available_palettes": [
      "neon_riso_pop",
      "warm_sunset_riso",
      "cool_ink_riso",
      "playful_primary_riso"
    ]
  },
  "style_wildcard": {
    "instruction": "Select ONE style mode and apply it without explanation",
    "options": {
      "precision_isometric": "clean isometric construction, equal-angle depth, highly engineered feel",
      "blueprint_cutaway": "exposed inner planes, sectional cuts, technical diagram energy",
      "hard_edge_stack": "layered planar extrusion with stepped depth like machined parts",
      "angled_projection": "dynamic oblique projection with strong directional depth"
    },
    "influence": [
      "construction logic",
      "depth geometry",
      "plane relationships",
      "visual rhythm"
    ],
    "constraint": "Must NOT reduce readability"
  },
  "lettering_style": {
    "form": "Sharp, geometric letterforms built from straight edges and precise angles",
    "no_curves": "No rounded or inflated forms - everything is planar, faceted, or beveled",
    "extrusion": "Clear extrusion using angular planes like drawn with set squares",
    "construction": "Visible construction logic with engineered faces, edges, and joins",
    "perspective": "Consistent perspective system (isometric or oblique depending on style)",
    "silhouette": "Crisp outer silhouette with strong readability",
    "interaction": "Letters may interlock or overlap through clean geometric intersections",
    "baseline": "Each line may have slight stepped or measured variation, not bouncy"
  },
  "visual_energy_boost": {
    "techniques": [
      "Layered planar extrusion with stepped depth",
      "Beveled edges and chamfers instead of curves",
      "Cut-ins, notches, and inset panels",
      "Secondary structural planes like internal supports",
      "Directional lighting reinforcing plane changes",
      "Hard shadow separation using limited tones",
      "Subtle depth variation per letter"
    ],
    "constraints": [
      "precise",
      "clean",
      "constructed",
      "diagrammatic",
      "print-friendly"
    ]
  },
  "composition": {
    "layout": "Center the full phrase across TWO lines",
    "balance": "Each line should feel balanced in width and weight",
    "frame_usage": "Occupy approximately 75-85 percent of frame width",
    "line_spacing": "Consistent spacing between lines, tight but readable",
    "whitespace": "Maintain clear white space around edges",
    "readability": "Ensure strong balance and immediate readability",
    "perspective": "Use consistent technical perspective to show depth clearly"
  },
  "forbidden": [
    "characters",
    "illustrations",
    "objects",
    "icons",
    "scenery",
    "textures",
    "photorealism",
    "sketchy or hand-drawn roughness",
    "gradients",
    "background elements",
    "borders or frames",
    "single-line text",
    "more than two lines of text",
    "rainbow or multi-theme colour systems",
    "rounded, bubbly, or soft forms"
  ],
  "output_format": {
    "return": "ONLY the final image prompt",
    "requirements": [
      "include {WORDS}",
      "explicitly state two-line layout",
      "include selected palette name",
      "include selected style wildcard",
      "state that hex colours will be defined in next stage",
      "highly detailed and production-ready"
    ]
  }
}
