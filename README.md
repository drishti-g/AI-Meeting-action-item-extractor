# AI Meeting Action Item Extractor

An LLM-powered application that converts unstructured meeting transcripts into structured, actionable tasks with responsible owners, deadlines, status, and confidence scores.

**Live Demo:** https://aimeetingactionitemextractor.streamlit.app/

---

## Overview

Important action items are often buried inside long and unstructured meeting conversations. This project automates the process of identifying those actions and converting them into a structured format that is easier to review and follow up on.

The system is designed as a multi-stage pipeline:

```text
Meeting Transcript
        │
        ▼
Transcript Cleaning
        │
        ▼
LLM-based Extraction
        │
        ▼
Structured Output
        │
        ▼
Rule-based Validation
        │
        ▼
LLM Verification & Refinement
        │
        ▼
Final Action Items