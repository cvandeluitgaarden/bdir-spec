# Caching Strategy

This document describes recommended caching and deduplication strategies for implementations of the BDIR Patch Protocol.

## Goals

- Avoid duplicate AI requests for identical content
- Reduce latency and operational cost
- Preserve deterministic behavior
- Provide transparency to users

## Cache Key

Implementations SHOULD derive a deterministic cache key from:

- AI model identifier (including version)
- Prompt or instruction version
- Patch schema version
- Hash of the BDIR Edit Packet (canonical JSON bytes)

Example (conceptual):

```
bdir-patch|model=gpt-4.1-mini|prompt=v3|schema=v1|packet=sha256:...
```

## Cache Scope

Caching is most effective at **page level**. Block-level caching is generally not recommended due to low reuse and higher invalidation complexity.

## In-flight Deduplication

Implementations SHOULD prevent concurrent duplicate requests by:

- Tracking in-flight requests by cache key
- Joining or short-circuiting duplicate calls

## Cache Hits

On a cache hit, implementations MAY:

- Return the cached patch immediately
- Inform the caller that a cached result was reused
- Expose token and cost savings

## TTL and Invalidation

- Cache entries MAY have long TTLs, as content hashes prevent stale application
- Cache MUST be invalidated if prompt, model, or schema versions change

## Negative Caching

Results indicating "no changes" SHOULD also be cached to avoid repeated analysis.
