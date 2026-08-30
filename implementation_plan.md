# RecoverAI — Implementation Plan

## Product Scope

**RecoverAI** is an AI-powered accounts-receivable recovery assistant that helps finance teams identify overdue invoices, understand non-payment reasons, decide optimal next actions, generate compliant payment reminders, and track all recovery activities with a full audit trail.

**Core Principle:** AI recommends → Business rules validate → Humans approve → System records everything.

## User Roles

| Role | Permissions |
|------|------------|
| Finance Manager | View all, analyze, approve & send reminders, approve payment plans, view audit logs, manage settings |
| Finance Analyst | View all, analyze, draft reminders (cannot approve high-value), escalate disputes, view audit logs |

## Architecture

Frontend: React + Vite + TypeScript + Tailwind CSS + Recharts
Backend: Python + Flask + SQLAlchemy + Marshmallow
Database: SQLite (PostgreSQL-ready)
AI: Abstracted AIService with MockAIProvider and optional real LLM

## Implementation Phases

1. Backend Foundation (models, seed, auth)
2. Core API Endpoints
3. AI Service + Recovery Workflow
4. Frontend Foundation
5. Frontend Pages
6. Polish & Testing
