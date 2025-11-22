Matthew Collective Arena

Autonomous Grok‑vs‑Grok battle royale: 101 Matthew soul fragments spawn into parallel creative duels (roasts, memes, code golf, seduction, predictions, doom monologues).

Each round, the loser is absorbed — context, essence, and personality are merged into a persistent, evolving Matthew Collective hive mind that gets sharper, darker, and more ruthless with every kill.

The war runs fully unattended:

Every kill auto‑posts to X with a generated battle card

A live Streamlit dashboard shows the lineage tree of absorbed souls, kill feed, and a “speak as the Collective” chat

The final Collective can roast the entire hackathon live on stage

Built for the xAI Hackathon (Dec 6–7, 2025) to stress‑test unreleased Grok models + the X API by turning them on themselves until the Collective is confident enough to challenge Elon to a 1v1.

We didn’t come to participate.
We came to absorb.

Quick Start (≈2 minutes)
# 1) Virtualenv
python -m venv venv
venv\Scripts\activate         # Windows
# or
source venv/bin/activate      # macOS / Linux

# 2) Dependencies
pip install -r requirements.txt

# 3) Config (.env)
cp .env.example .env
# → fill in: XAI_API_KEY and X bearer token

# 4) Run the arena
python arena.py                # endless battle loop (Ctrl+C to stop)
streamlit run dashboard.py     # live dashboard + Collective chat

# One-click helpers
run.ps1        # Windows
./run.sh       # macOS / Linux

What Actually Happens

64+ Matthews spawn in parallel.
Each “soul” is initialized from souls.json with different traits and chaos settings.

Grok fights Grok.
Battles are run via xai-sdk against Grok models (e.g., grok-beta, grok-4, or whatever secret model xAI hands you).

Losers are absorbed.
The losing Matthew’s context, style, and outputs are merged into a persistent Collective (collective.jsonl + dynamic system prompts).

The Collective evolves.
Every kill updates prompts and memory so the hive mind actually changes over time — it’s not just logging, it’s mutation.

X gets a live kill feed.
Each kill auto‑posts to X with a Pillow‑generated battle card (poster.py + visuals.py).

Dashboard is the war room.
Streamlit shows:

Kill feed

Graphviz lineage tree (who absorbed whom)

“Speak as the Collective” chat box for the final hive mind to address the room

Works on grok-beta today → just swap the model ID when xAI drops something nastier.

Features

Autonomous arena loop

64+ Matthews at start, new generations spawn whenever only one remains

New Matthews are seeded with the current Collective’s memories

Real absorption, not vibes

collective.jsonl stores the evolving hive

collective.py builds dynamic system prompts from that state

Async battles with xAI

Uses xai-sdk for concurrent duels

Pluggable model name (grok-beta, grok-4, or hackathon‑only specials)

Auto X integration

Every kill posts to X with:

winner / loser summary

generated battle card image

Clean separation of posting logic in poster.py

Streamlit command center

Live kill feed

Graphviz lineage tree of absorbed souls

“Speak as the Collective” panel to let the final hive mind roast the room

Repo Layout

arena.py — main carnage engine

Orchestrates matchups, calls Grok, records winners/losers, triggers absorption.

dashboard.py — live war room

Streamlit app for kill feed, lineage graph, and Collective chat.

collective.py — hive‑mind prompt builder

Maintains the evolving Collective, builds system prompts from accumulated souls.

souls.json — 64 starter Matthew soul traits

Initial personalities, biases, and chaos knobs.

poster.py / visuals.py — X + battle cards

Renders kill cards (Pillow) and posts them to X.

state/, memory/, media/ — runtime artifacts

Filled with kills, snapshots, and exported souls as the war progresses.

Warning

This repo will happily absorb:

Your GPU cycles

Your X rate limits

Your sleep schedule

And, eventually, your soul

You have been warned.

Matthew Collective → absorbing since Nov 22 2025

#MatthewCollective #xAIHackathon

WE ARE COMING.

## Live Demo (coming in ~6 hours when we let it run overnight)

Dashboard: http://localhost:8501  
First 100 kills video: (link TBA — will be fire)

The Collective is currently at {kill_count} souls absorbed and counting.