# Civilization Core Memory Proposal: Video AI Skills

Status: pending governed memory write proposal
Created: 2026-06-02
Scope: Hermes Memory Fabric, Codex, OpenClaw, Civilization Core memory system

## Purpose

Preserve the important context needed to eventually hand-build a best-in-class,
high-quality, full-featured Video AI production skill system.

This document is a staging artifact only. It must not be treated as a direct
Hermes durable memory write, Memory Graph mutation, or policy change. When the
Hermes memory write tools are available, these entries should be submitted
through the governed gate and write-proposal flow.

## Long-Term Memory Candidates

### collaboration_preference

Important sessions should be automatically analyzed and separated into the
right memory surfaces:

- Long-term memory for stable preferences, long-running project goals,
  architecture decisions, collaboration style, and reusable knowledge.
- Short-term memory for current task state, temporary context, and unfinished
  work.
- Operation ledger for gate decisions, write proposals, audit events, policy
  changes, routing events, federation events, and other governed operations.
- Graph and knowledge surfaces for reusable entity relationships, project
  facts, methodology, and knowledge fragments.

Codex must not directly write Hermes memory files or mutate the Memory Graph.
Durable updates should go through governed gate and write-proposal mechanisms.

### project_goal

The user is building a Civilization Core memory system around Hermes Memory
Fabric, Codex, and OpenClaw. The system should support governed cross-session,
cross-tool, and cross-system memory deposition, recall, audit, and evolution.

One important downstream objective is to build a uniquely capable Video AI
production skill system with broad, high-quality functionality.

### architecture_rule

Memory deposition should preserve boundaries between:

- Long-term preference and identity continuity.
- Short-term task state.
- Operation-ledger audit metadata.
- Graph relationships.
- Searchable knowledge surfaces.

Long-term preference, persona, and collaboration-style continuity require a
governed write proposal. Ledger entries should store operation metadata and
hashes, not full durable memory content.

### environment_fact

In the referenced Codex session, the available `hermes_memory` tools only
included message-bridge operations such as `conversations_list`,
`messages_read`, and `messages_send`. Full Hermes Memory Fabric tools such as
`memory_fabric_search`, `memory_write_proposal`, `memory_operation_ledger`, and
`memory_evolution_status` were not exposed, so Codex could not directly recall
or write governed long-term memory.

## Short-Term Memory Candidates

### current_task_state

The user provided the terminal context from a previous session and asked Codex
to extract the important information for Civilization Core memory deposition.
The immediate purpose is to preserve the video-project validation findings and
the memory-system governance preference for later governed ingestion.

### repo_state

The working directory is `/Users/han/hermes-memory-fabric-plugin`.

The repository history visible in the terminal included `main` at version
`2.3.0`, plus branches such as
`fix/codex-ingestion-risk-normalization-v131` and
`feat/token-authority-boundary-contract-dry-run-v20`. Some branches had gone
upstream references and may need upstream cleanup or baseline confirmation.

### tooling_issue

Codex startup reported invalid HeyGen skill files because their descriptions
exceeded 1024 characters:

- `heygen-avatar/SKILL.md`
- `heygen-video/SKILL.md`

One attempted command contained an abnormal line-separator suffix and failed as
`codex\u2028`; the normal `codex` command launched successfully.

## Operation Ledger Candidates

### video_project_validation

Source projects were cloned only into
`/private/tmp/video-project-validation`. No source was imported into the
current repository.

Validation included repository-structure scans, README and startup-entry
checks, license checks, Docker Compose validation, `npm` dry-runs and installs,
Python `compileall`, minimal startup checks, HTTP health checks, and cleanup of
temporary services.

### temporary_command_authorizations

The user approved temporary validation commands including:

- `npm ci`
- `npm run dev`
- `npm rebuild`
- `curl`
- `docker compose`
- `pip install`
- `npm install`
- `npm run render:preview`
- `kill -TERM`

These approvals should be remembered only as context for that validation
session, not as an unrestricted permanent operating preference.

### local_service_cleanup

Docker was initially unavailable, then started with `open -a Docker`.
ArcReel's Docker container was later stopped with `docker compose down`.
Temporary local ports `3100`, `3013`, `5679`, and `1241` were verified as
released.

## Knowledge Surface Candidates

### gpt_image_2_storyboard_research

On 2026-06-02, the user requested a broad search of X.com and the public web
for advanced GPT Image 2 storyboard tutorials, with the goal of preserving
reusable knowledge for the future Video AI skills system.

Direct X.com pages were not fully readable through static web access because
the public pages returned empty or JavaScript-gated content. Search-index
snippets still exposed several useful X posts:

- Harboris / `@harboriis` posted a GPT Image 1.5 prompt for a 3x4 cinematic
  storyboard grid. The useful pattern is to define one fixed character, one
  coherent location/world, and twelve explicit shot types: close-up, extreme
  close-up, POV, medium shot, low angle, over-the-shoulder, high angle,
  tracking shot, reveal shot, wide establishing shot, Dutch angle, and bird's
  eye view. The prompt explicitly requests consistent character identity across
  all frames.
- Kol Tregaskes / `@koltregaskes` posted a comparison prompt for GPT Image
  v1.5/v2, Nano Banana Pro, Midjourney, Grok, Luma, and Recraft. The reusable
  pattern is a strict 8-panel turnaround sheet: full-body front/back/left/right
  on the top row and head close-up front/back/left/right on the bottom row,
  with exact side views, neutral pose, pure white background, and no props,
  weapons, text, labels, or logos.
- Several X posts claimed GPT Image 2 / ChatGPT Images 2.0 had improved text,
  infographics, realism, and multi-panel coherence. These should be treated as
  market observations unless confirmed by official OpenAI documentation.

Official OpenAI sources confirm that GPT Image 2 is listed as a specialized
image-generation and editing model, and that ChatGPT Images 2.0 thinking mode
can use a reasoning stack to turn basic prompts into more thought-through final
images and generate multiple images from one prompt. OpenAI's public image
prompt guidance emphasizes clear subject, action, location, style, framing,
lighting, constraints, small targeted revisions, and carefully labeled multiple
uploaded images.

Third-party storyboard guides converged on the following practical workflow:

1. Convert a script into 3-6 visual beats before image generation. A beat is an
   establishing moment, reaction, action, reveal, or hook, not a generic scene.
2. Generate character and environment reference sheets before generating
   narrative frames.
3. Generate per-shot frames with role-labeled reference images and fixed
   continuity constraints.
4. Review weak shots individually. Do not regenerate the whole board when only
   one or two panels drift.
5. Feed approved frames into a single image-to-video model rather than mixing
   multiple video models mid-project.
6. Edit final clips by trimming AI hold frames and cutting on character action.

### gpt_image_2_storyboard_prompt_schema

The future Video AI skills system should treat GPT Image 2 storyboard prompting
as a structured production brief, not a moodboard prompt.

Recommended storyboard prompt schema:

- Artifact: contact sheet, storyboard grid, character sheet, shot board, or
  production reference board.
- Format: rows, columns, panel count, aspect ratio, white space, panel borders,
  and whether captions or timestamps are allowed.
- Identity anchors: face, body proportions, hair, wardrobe silhouette, recurring
  props, and invariant visual identifiers.
- World anchors: location geography, time of day, color palette, lighting
  rules, texture, set dressing, and continuity objects.
- Beat list: one visual moment per panel, with active character, action,
  emotion, object, and story function.
- Camera language: shot size, lens feel, camera height, angle, movement cue,
  foreground/background relation, and depth of field.
- Continuity constraints: preserve face, hair, wardrobe, height difference,
  injuries, props, screen direction, and location layout across panels.
- Text constraints: quote any visible text exactly, specify placement and
  typography, and require no extra words or duplicate text.
- Negative constraints: no watermark, no extra characters, no logo drift, no
  changed outfit, no unlabeled panels unless desired.
- Review criteria: identity consistency, panel order, readable text, action
  clarity, no duplicated props, no anatomy failure, no camera contradiction.

For storyboarding, the system should generate at least four artifact types:

- Master character sheet: front/side/back, expressions, full-body, wardrobe,
  props, palette, and details.
- Shot contact sheet: 3x3 or 3x4 grid of approved beats.
- Scene board: hero frame, key props, environment, lighting, shot list, audio
  notes, and camera language.
- Repair prompt: a targeted prompt to regenerate only failed panels while
  preserving the approved character and scene anchors.

### gpt_image_2_to_video_pipeline

The strongest reusable pipeline is:

1. Script to beat map.
2. Beat map to character/world bible.
3. Character/world bible to reference sheets.
4. Reference sheets to storyboard grid.
5. Storyboard grid to individual clean frames.
6. Individual frames to image-to-video generation.
7. Video outputs to edit, pacing, subtitles, sound, and final delivery.

GPT Image 2 should own visual planning, character sheets, contact sheets,
storyboard frames, and visual continuity repair. Video models such as Sora,
Kling, Seedance, Veo, Runway, or similar I2V systems should own motion. Editing
tools such as moviepy, Remotion, HyperFrames, or NLEs should own pacing,
assembly, captions, and deliverables.

The skill system should eventually implement:

- `storyboard_beat_compiler`
- `character_reference_sheet_generator`
- `shot_contact_sheet_generator`
- `reference_image_selector`
- `panel_consistency_reviewer`
- `failed_panel_repair_prompt_builder`
- `storyboard_to_i2v_prompt_adapter`
- `short_video_edit_assembler`

Key sources used for this research:

- OpenAI Models page: `https://developers.openai.com/api/docs/models`
- OpenAI image-generation academy guide:
  `https://openai.com/academy/image-generation/`
- OpenAI ChatGPT Images 2.0 system card:
  `https://deploymentsafety.openai.com/chatgpt-images-2-0/chatgpt-images-2-0.pdf`
- Harboris X post search result:
  `https://x.com/harboriis/status/2020087133285892368`
- Kol Tregaskes X post search result:
  `https://x.com/koltregaskes/status/2041252368042672340`
- Morphed GPT Image 2 prompt guide:
  `https://morphed.app/blog/gpt-image-2-prompt-guide`
- NemoVideo GPT Image 2 storyboard guide:
  `https://www.nemovideo.com/blog/gpt-image-2-storyboard`
- Image Prompt Gallery 12-panel storyboard case:
  `https://imagepromptgallery.com/cases/cinematic-storyboard-grid-gpt-image-2`

### video_project_evaluation_first_tier

First-tier projects were selected for deeper trial runs:

- ArcReel: Docker startup passed, `/health` returned ok, and the web homepage
  returned 200. It appears closest to a full short-drama industrial workbench.
  Real generation still requires model API keys.
- LocalMiniDrama: Vite frontend, backend health, and SQLite migration passed.
  It is suitable for studying private deployment and localized short-drama
  workflows. `better-sqlite3` required native rebuild after install scripts
  were skipped.
- VideoSOS: landing page worked, but core editor route `/en/app` returned 500
  because `indexedDB is not defined`. This is a real SSR browser-API bug and
  should be fixed before further evaluation.
- backgroundremover: Python 3.10 virtual environment installed dependencies,
  CLI and Flask server imports worked, and `--help` worked. Python 3.14 is not
  compatible because `distutils` was removed. Real matting was not run because
  it would load or download U2Net models.
- FunClip: Python 3.10 virtual environment installed dependencies and
  `launch.py --help` worked. Full Gradio service was not launched because the
  next step would initialize FunASR model downloads.

### video_capability_map_second_tier

Second-tier projects were mapped as reusable capability modules:

- moviepy: useful for programmatic editing, concatenation, subtitles, and
  template batch rendering. A one-second MP4 smoke test was generated.
- claude-code-video-toolkit with Remotion: useful for templated ads,
  reports, and explainer videos. The `hello-world` Remotion preview rendered
  successfully.
- LivePortrait: useful for single-image portrait animation and expression or
  motion transfer. Actual inference requires model weights, FFmpeg, and a
  PyTorch environment.
- video-retalking: useful for audio-driven lip sync and localized dubbing.
  It depends on an older Python/CUDA/PyTorch stack and is better isolated as an
  offline service than embedded directly in a main app.

### video_ai_skills_strategy

Suggested priority for building the future Video AI skills system:

1. ArcReel for full workflow and short-drama production architecture.
2. LocalMiniDrama for local/private short-drama workflow and domestic model
   integration patterns.
3. claude-code-video-toolkit plus moviepy for template-driven advertising and
   batch video production.
4. backgroundremover as a material-processing plugin.
5. FunClip for long-video clipping, subtitles, and ASR-assisted workflows.
6. VideoSOS only after fixing its SSR `indexedDB` bug.

## Do Not Persist

Do not preserve repetitive clone logs, full package download output, long curl
HTML responses, Docker layer download logs, temporary PIDs, one-off waiting
messages, terminal noise, or command-output details with no reusable value.

## Risk Notes

No plaintext API keys or durable secrets were identified in the provided
context. ArcReel generated an authentication password during startup; only the
fact that a password is generated should be remembered, not the password
content. Files under `/private/tmp/video-project-validation` are temporary
validation artifacts and should not become durable path dependencies.
