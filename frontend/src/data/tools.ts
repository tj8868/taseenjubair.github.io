export type ToolCategory = "harness" | "workflow" | "agent" | "plugin";

export interface ToolItem {
  id: string;
  name: string;
  category: ToolCategory;
  platforms: string[];
  summary: string;
  repoUrl?: string;
  lastVerified: string;
}

export const categoryLabels: Record<ToolCategory, string> = {
  harness: "Agentic Harnesses",
  workflow: "Workflows & Methodology",
  agent: "AI Agents",
  plugin: "Plugins & Skills",
};

export const tools: ToolItem[] = [
  {
    id: "hermes-agent",
    name: "Hermes Agent",
    category: "harness",
    platforms: ["Hermes", "Linux", "CLI"],
    summary: "Multi-agent execution harness for long-running research synthesis, gateway automation, and reproducible pipelines.",
    lastVerified: "2026-11",
  },
  {
    id: "claude-code",
    name: "Claude",
    category: "harness",
    platforms: ["Claude", "CLI", "IDE"],
    summary: "Anthropic agentic coding and reasoning environment used for codebase refactoring, structured planning, and review.",
    lastVerified: "2026-11",
  },
  {
    id: "codex-harness",
    name: "Codex",
    category: "harness",
    platforms: ["Codex", "CLI"],
    summary: "OpenAI terminal coding agent for isolated task execution, automated test generation, and diff verification.",
    lastVerified: "2026-11",
  },
  {
    id: "antigravity",
    name: "Antigravity",
    category: "harness",
    platforms: ["Gemini", "IDE", "CLI"],
    summary: "Google DeepMind agentic workspace supporting parallel subagents, browser automation, and artifact-driven workflows.",
    lastVerified: "2026-11",
  },
  {
    id: "deepseek-harness",
    name: "DeepSeek Harness",
    category: "harness",
    platforms: ["DeepSeek", "CLI"],
    summary: "Lightweight reasoning-model execution wrapper for cost-efficient batch code analysis and data processing.",
    lastVerified: "2026-11",
  },
  {
    id: "pi-harness",
    name: "Pi",
    category: "harness",
    platforms: ["Pi", "CLI"],
    summary: "Minimalist terminal agent harness optimized for fast single-file edits and composable shell pipelines.",
    lastVerified: "2026-11",
  },
  {
    id: "opencode",
    name: "OpenCode",
    category: "harness",
    platforms: ["OpenCode", "CLI"],
    summary: "Open-source terminal coding harness supporting provider-agnostic model switching and local MCP servers.",
    lastVerified: "2026-11",
  },
  {
    id: "spec-driven-dev",
    name: "Spec-Driven Development",
    category: "workflow",
    platforms: ["Claude", "Gemini", "Codex", "Hermes"],
    summary: "Authoring formal specifications, invariants, and acceptance criteria before generating or modifying any code.",
    lastVerified: "2026-11",
  },
  {
    id: "cv-tailor-plugin",
    name: "CV Tailor & Academic Bio Plugin",
    category: "plugin",
    platforms: ["Claude", "Gemini", "Codex", "Hermes"],
    summary: "Cross-platform skill suite enforcing anti-AI tone, privacy-by-design, and Harvard/academic CV formatting.",
    repoUrl: "https://github.com/tj8868",
    lastVerified: "2026-11",
  },
  {
    id: "egm-review-workflow",
    name: "Elephant-Goldfish Review Workflow",
    category: "agent",
    platforms: ["Claude", "Gemini", "Codex", "Hermes"],
    summary: "Multi-lens adversarial review workflow spawning fresh-context subagents to audit design docs and codebases.",
    lastVerified: "2026-11",
  },
];
