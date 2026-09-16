# Case Study — Australian Job Intelligence Dashboard

## Problem

Technology job descriptions are unstructured and use inconsistent terminology. Candidates and recruiters often want a fast way to explore requested technical skills, locations, cloud platforms and role types.

## Solution

This project converts a reproducible Australian technology-job demo market into an interactive analytics product. The full implementation uses FastAPI, SQLAlchemy and PostgreSQL. It normalises technical skills, exposes analytics endpoints and calculates **Technical Skill Coverage** between CV text and a selected role.

## Why transparent NLP first

Version 1 uses a canonical dictionary and deterministic matching. Variants such as `python3`, `PowerBI`, `k8s`, `Amazon Web Services` and `GitHub` can map to standard skills. The behaviour is explainable and testable, while embeddings could be added later.

## Interpretation rule

Technical Skill Coverage is simply:

`matched tracked skills / tracked skills requested by selected role × 100`

It is **not** a probability of being hired, an employability score or an assessment of experience quality.

## Data ethics

The repository uses deterministic synthetic/curated portfolio records, not copied live vacancies. A production ingestion path should use public APIs, open datasets, licensed feeds or sources that explicitly permit automated collection.
