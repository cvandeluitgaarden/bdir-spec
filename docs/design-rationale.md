# Design Rationale

This document explains the core design decisions behind the BDIR Patch Protocol.

## AI as Untrusted Proposer

AI systems are treated as untrusted. The protocol assumes AI output may be incorrect and enforces safety through validation rather than trust.

## Patch Instructions over Rewrites

Direct content rewriting is avoided to prevent semantic drift and to preserve auditability. Patch instructions allow precise targeting and human review.

## Block-based Representation

Blocks provide stable identifiers, enable hash-based safety checks, and allow scoped edits without global rewrites.

## Whole-document Context

AI receives the full document context to make informed suggestions, but is constrained in how changes are expressed.

## Hash-based Safety

Exact substring matching and page-level hashes ensure patches only apply to the intended content version.

## Token Minimization

The Edit Packet removes non-essential metadata to reduce token usage while preserving semantic context.

## Statelessness

The protocol is stateless by design. No assumptions are made about AI memory across requests.
