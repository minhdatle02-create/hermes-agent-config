---
name: baoyu-visualization
description: "Baoyu AI-generated visual content: article illustrations, knowledge comics, and infographics with prompt-only image generation."
version: 1.0.0
author: Hermes Agent (adapted from JimLiu/baoyu-skills)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, image-generation, illustration, comic, infographic, baoyu, jimliu, prompts]
---

# Baoyu Visualization Ecosystem

Unified entry point for the Baoyu image-generation skill family. All three
skills share the same core workflow: analyze content, build prompts, generate
with `image_generate`, download the result.

Load the standalone skill for full details, prompt templates, and reference libraries.

## Article Illustration: baoyu-article-illustrator

Illustrate articles with **Type × Style × Palette** consistency.

**Trigger:** "illustrate this article", "add images to the article", "配图"

**Dimensions:**
- **Type**: infographic, scene, flowchart, comparison, framework, timeline
- **Style**: notion, warm, minimal, blueprint, watercolor, elegant
- **Palette**: macaron, warm, neon

**Output:** article markdown with inserted PNGs + prompts directory.

See standalone `baoyu-article-illustrator` for the full 7-step workflow,
modification procedures, and references.

## Knowledge Comics: baoyu-comic

Create original knowledge/educational comics from text, files, or topics.

**Trigger:** "create a knowledge comic", "education comic", "教程漫画"

**Options:**
- **Art**: ligne-claire, manga, realistic, ink-brush, chalk, minimalist
- **Tone**: neutral, warm, dramatic, romantic, energetic, vintage, action
- **Layout**: standard, cinematic, dense, splash, mixed, webtoon, four-panel
- **Presets**: ohmsha, wuxia, shoujo, concept-story, four-panel

**Output:** `comic/{topic-slug}/` with storyboard, prompts, generated pages,
and optional character sheet.

See standalone `baoyu-comic` for the full 8-step workflow, character/sheet
management, and references.

## Infographics: baoyu-infographic

Generate infographics combining 21 layouts × 21 styles.

**Trigger:** "create an infographic", "visual summary", "信息图", "可视化"

**Dimensions:**
- **Layout**: bento-grid (default), linear-progression, binary-comparison,
  hierarchical-layers, dashboard, and 16 others
- **Style**: craft-handmade (default), corporate-memphis, cyberpunk-neon,
  pixel-art, technical-schematic, and 20 others

**Output:** `infographic/{topic-slug}/` with structured content, prompt, and image.

See standalone `baoyu-infographic` for the full 7-step workflow, keyword
shortcuts, and references.

## Core Workflow (Shared Across All Variants)

1. **Analyze** source content (file or paste)
2. **Confirm** options (type/style/layout via `clarify`)
3. **Generate outline / storyboard / structured content**
4. **Build prompt** from templates in the skill's `references/`
5. **Generate image** via `image_generate(prompt, aspect_ratio)`
6. **Download** the returned URL to a local PNG
7. **Report** results and paths

## Common Pitfalls

- `image_generate` returns a URL, not a local file — always download it
- Use **absolute paths** for `curl -o`; never rely on shell CWD persistence
- Prompt files are reproducibility records — save before generating
- Strip secrets/credentials from source content before writing outputs
- The image backend is user-configured; do not select models in prompts
