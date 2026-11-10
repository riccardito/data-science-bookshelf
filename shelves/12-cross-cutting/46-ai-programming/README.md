# 46 · AI-Assisted Programming

*Shelf XII · Cross-Cutting Skills · FHNW modules: kip*

## Why It Matters

This is the revolution. The same revolution as CNC replacing 200 hours of hand-filing. The same pattern, one level of abstraction higher.

"My teacher filed metal for 200 hours. A CNC machine does it in minutes. Metal became data. The file became the prompt."

AI-assisted programming is the CNC machine of software development. The human brings the structure — the domain knowledge, the architecture, the judgment. The AI writes the strings. Together, they produce in hours what a team would take weeks to build.

## Key Concepts

### The Human-AI Division of Labor

| Human | AI |
|-------|-----|
| Domain understanding | Code generation |
| Architecture decisions | Boilerplate, repetition |
| Quality judgment | Pattern application |
| Problem framing | Solution implementation |
| "What to build" | "How to express it in code" |

### Prompt Engineering for Code
- **Be specific**: "Create a Flask route that accepts JSON with fields X, Y, Z" beats "make an API"
- **Provide context**: show existing code patterns, conventions, file structure
- **Iterate**: first draft → review → refine → review → done
- **Constrain**: specify framework, library versions, coding style
- **Break down**: large features into small, testable units

### Tool Use Pattern (How LLMs Work as Developers)
```
Human: "I need a patient search endpoint"
  ↓
LLM receives:
  - System prompt (conventions, architecture)
  - Context (existing models, route patterns)
  - Request (the feature)
  ↓
LLM generates:
  - Route function
  - Model query
  - Template fragment
  - Test skeleton
  ↓
Human reviews:
  - Does it match the architecture?
  - Is the security correct?
  - Does it handle edge cases?
  - Does it pass tests?
```

This is the same tool-use pattern an agent follows anywhere:
- Request → function call → response → human evaluates

### Structure is the bottleneck

The key insight: **the bottleneck was never the typing. It was the structure.** An AI can write any code you ask for. The question is: do you know what to ask for?

### Risks & Pitfalls
- **Hallucinated APIs**: AI invents function signatures that don't exist
- **Subtle bugs**: code looks correct but has edge-case failures
- **Security blind spots**: AI may not consider injection, auth bypass, IDOR
- **Over-reliance**: losing the ability to debug without AI
- **Context drift**: long sessions where the AI forgets earlier decisions
- **Licensing**: generated code may resemble copyrighted patterns

### Best Practices
- Always review generated code before committing
- Run tests — AI-generated code needs the same validation as human code
- Use AI for first drafts, not final products
- Maintain your own understanding of every line in the codebase
- Keep the human in the loop for architecture, security, and domain logic

## Tools

| Tool | Use Case |
|------|----------|
| Claude Code (CLI) | Terminal-based AI pair programming (this tool) |
| Claude (API) | Programmatic code generation via Anthropic API |
| GitHub Copilot | In-editor code completion |
| Cursor | AI-first IDE |
| Aider | Terminal AI coding assistant |

## Chapters

Read in order: each chapter builds on the one before it.

1. Prompting
2. Agents and tools
3. Evaluating agent work
4. The risks

## Challenge

→ [`agora-method`](https://github.com/riccardito/agora-method)

## Where it was learned

FHNW `kip`
