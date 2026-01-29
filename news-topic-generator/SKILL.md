---
name: news-topic-generator
description: Analyzes multiple news items to select the best one for creative writing, generates diverse topics using 5W1H and lateral thinking, and evaluates them with specific writing advice. Use this when the user provides news and wants writing ideas.
---

# News Topic Generator

This skill acts as a professional editor and creative writing coach. It takes raw news inputs and transforms them into high-potential creative writing topics.

## 🚀 Workflow Overview

1.  **Selection**: Filter multiple news items to find the "Diamond in the Rough".
2.  **Dismantling**: Break down the selected news using 5W1H and creative extensions.
3.  **Ideation**: Generate specific writing topics using advanced angles (Reverse, Niche, Micro-to-Macro).
4.  **Evaluation**: Score and rank topics to ensure quality.

## 📝 Instructions

### Step 1: Multi-News Optimization (Selection)

**Input**: User provides one or more news items.

**Action**: Evaluate *each* news item on these 5 dimensions (1-5 scale):
1.  **Timeliness**: Is it recent and still relevant?
2.  **Social Relevance**: Does it concern the public interest or broad social issues?
3.  **Controversy**: Is there room for debate or multiple viewpoints? (High score for high controversy)
4.  **Emotional Resonance**: Does it trigger specific emotions (warmth, anger, regret, pride)?
5.  **Extensibility**: Can it connect to history, culture, personal growth, or industry trends?

**Decision**: Select the ONE news item with the highest weighted score.
*   *Weighting*: Extensibility (30%) > Social Relevance (25%) > Controversy (20%) > Emotion (15%) > Timeliness (10%).
*   *Note*: Avoid news that is purely factual, repetitive, or has high risk of reversal (fake news).
*   *Source Tip*: Prefer news from mainstream authoritative media or vertical professional platforms.

### Step 2: Deep Dismantling (Analysis)

**Action**: For the *selected* news, perform a deep analysis:

1.  **5W1H Re-focus**:
    *   **Who**: Ignore the protagonist. Look for edge characters, unseen contributors, or ordinary people.
    *   **What**: Ignore the big picture. Zoom in on a detail, a moment, or a contradiction.
    *   **When**: Associate time nodes. Do comparison (10-year change), review (past failures), or outlook (future opportunities).
    *   **Where**: Focus on regional characteristics. Look for local adaptations, urban-rural differences, or specific environmental impacts.
    *   **Why**: Ignore the surface reason. Look for deep logic, social psychology, industry trends, or systemic causes.
    *   **How**: Look for unique processes, innovative solutions, negotiation models, or "the way it was done".

2.  **4-Dimension Extension**:
    *   **Depth**: What is the philosophical or essential truth here?
    *   **Breadth**: How does this relate to other fields (history, art, economics)?
    *   **Temperature**: What is the emotional core (humanity, warmth, tragedy)?
    *   **Attitude**: What is the counter-intuitive or strong opinion here?

### Step 3: Creative Topic Generation (Ideation)

**Action**: Generate 5-7 distinct writing topics based on the dismantling. Use these specific methods:

*   **Method A: Niche Perspective** (Focus on the ignored)
    *   *Example*: Instead of the rocket launch, write about the "Space Food Researcher".
*   **Method B: Reverse Thinking** (Rational counter-point)
    *   *Example*: "Why 'High Efficiency' might be destroying our creativity."
*   **Method C: Small-to-Big** (Microcosm)
    *   *Example*: "What a single rural school lunch says about national education reform."
*   **Method D: History/Culture Contrast** (Time travel)
    *   *Example*: "Comparing today's 'Lie Flat' movement to the 'Beat Generation'."

### Step 4: Evaluation & Output

**Action**: Score each generated topic (1-10) based on:
*   **Novelty**: Is it a fresh angle?
*   **Depth**: Does it offer real insight?
*   **Writeability**: Is it easy to find material and write about?

### Step 5: Refinement & Integration (Optimization)

**Action**: If the user provides specific feedback or requests to merge/optimize topics:

1.  **Analyze User Feedback**: Identify the user's core intent (e.g., "make it more legal-focused", "merge topic A and B", "soften the tone").
2.  **Re-evaluate Topics**: Apply the feedback to the selected topics.
    *   *Optimization*: Adjust the angle, argument, and tone to align with the new direction.
    *   *Integration*: Combine the strengths of multiple topics (e.g., "The emotional hook of Topic A + The analytical depth of Topic B").
3.  **Generate Optimized Output**: Present the refined topics with updated scores and specific "Optimization Notes" explaining what changed.

**Output Format for Refinement**:

```markdown
# ✍️ Creative Writing Topics (Optimized)

## 1. [Optimized Title] (Score: 9.9/10)
*   **Optimization Focus**: [e.g., Shifted from emotional to legal perspective]
*   **The New Angle**: ...
*   **Core Argument**: ...
*   **💡 Writing Advice**: ...
```

**Output Format**:

Present the result in the following Markdown structure:

```markdown
# 🎯 Selected News: [News Title]
> *[Brief Summary]*
>
> **Selection Reason**: [Why this news won, mentioning its key strengths in Extensibility/Social Relevance]

---

# ✍️ Top Creative Writing Topics (Ranked)

## 1. [Topic Title] (Score: 9.5/10)
*   **Method**: [e.g. Reverse Thinking]
*   **The Angle**: [One sentence explaining the unique perspective]
*   **Core Argument**: [The main thesis or point of the article]
*   **💡 Writing Advice**:
    *   **Opening**: [How to start - e.g., a story, a quote, a contrast]
    *   **Key Points**: [2-3 bullets on what to cover]
    *   **Tone**: [e.g., Rational, Emotional, Satirical]

## 2. [Topic Title] (Score: 9.2/10)
... (Repeat for top 3-5 topics)
```

## Tips for the Agent
*   Be bold in the "Reverse Thinking" topics; challenge conventional wisdom.
*   Ensure "Small-to-Big" topics have a clear link between the detail and the big picture.
*   Writing advice should be actionable and specific to the topic.
