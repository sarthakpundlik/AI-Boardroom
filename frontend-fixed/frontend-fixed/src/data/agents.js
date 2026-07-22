// Mirrors backend/app/core/constants.py — AgentName + AGENT_COLORS + AGENT_SELECTION_MATRIX
// Keeping this in lockstep with the backend enum values is what keeps the
// integration "precise" per the brief — these are the exact string values
// the API sends over REST and WebSocket (see AGENT_MAP in
// app/orchestrator/nodes.py, which uses these same keys).

export const AGENTS = {
  CEO: {
    key: "CEO",
    label: "CEO",
    title: "Chief Executive — Synthesis",
    color: "#FFD700",
    seat: "head",
    description: "Chairs the session, reads every department's analysis, and writes the final board decision.",
  },
  CFO: {
    key: "CFO",
    label: "CFO",
    title: "Chief Financial Officer",
    color: "#10B981",
    seat: "table",
    description: "Focuses on ROI, budget constraints, financial risks, revenue modeling, and cost-benefit analysis.",
  },
  CTO: {
    key: "CTO",
    label: "CTO",
    title: "Chief Technology Officer",
    color: "#8B5CF6",
    seat: "table",
    description: "Architecture feasibility, build complexity, technical risk, and engineering trade-offs.",
  },
  CMO: {
    key: "CMO",
    label: "CMO",
    title: "Chief Marketing Officer",
    color: "#F59E0B",
    seat: "table",
    description: "Positioning, go-to-market strategy, brand, and customer acquisition.",
  },
  COO: {
    key: "COO",
    label: "COO",
    title: "Chief Operating Officer",
    color: "#00D4FF",
    seat: "table",
    description: "Operational feasibility, execution planning, resourcing, and process risk.",
  },
  CISO: {
    key: "CISO",
    label: "CISO",
    title: "Chief Information Security Officer",
    color: "#FF4D4D",
    seat: "table",
    description: "Security posture, data protection, and threat exposure.",
  },
  CHRO: {
    key: "CHRO",
    label: "CHRO",
    title: "Chief Human Resources Officer",
    color: "#EC4899",
    seat: "table",
    description: "People impact, organizational structure, culture, and talent implications.",
  },
  CCO: {
    key: "CCO",
    label: "CCO",
    title: "Chief Compliance Officer",
    color: "#2563EB",
    seat: "table",
    description: "Legal, regulatory, and compliance exposure.",
  },
  CDO: {
    key: "CDO",
    label: "CDO",
    title: "Chief Data Officer",
    color: "#06B6D4",
    seat: "table",
    description: "Data quality, statistical validity, and measurable signal.",
  },
};

export const AGENT_LIST = Object.values(AGENTS);

// Mirrors AGENT_SELECTION_MATRIX in app/core/constants.py — which agents
// activate per input type. CEO always runs separately as the final
// synthesis step and is never part of this list.
export const INPUT_TYPES = [
  { value: "startup_idea", label: "Startup Idea", agents: ["CFO", "CMO", "COO", "CISO"] },
  { value: "dataset_analysis", label: "Dataset Analysis", agents: ["CDO", "CFO", "COO"] },
  { value: "research_paper", label: "Research Paper", agents: ["CTO", "CDO", "CISO"] },
  { value: "product_proposal", label: "Product Proposal", agents: ["CTO", "CMO", "COO", "CISO"] },
  { value: "financial_report", label: "Financial Report", agents: ["CFO", "CCO", "COO"] },
  { value: "marketing_strategy", label: "Marketing Strategy", agents: ["CMO", "COO", "CFO"] },
  { value: "technical_architecture", label: "Technical Architecture", agents: ["CTO", "CISO", "COO"] },
  { value: "investment_due_diligence", label: "Investment Due Diligence", agents: ["CFO", "CCO", "COO", "CISO"] },
  { value: "organizational_decision", label: "Organizational Decision", agents: ["CHRO", "COO", "CCO"] },
  { value: "general", label: "General", agents: ["CFO", "CTO", "CMO", "COO", "CISO", "CHRO", "CCO", "CDO"] },
];

export function agentsForInputType(inputType) {
  const found = INPUT_TYPES.find((t) => t.value === inputType);
  const base = found ? found.agents : INPUT_TYPES[INPUT_TYPES.length - 1].agents;
  return base; // CEO is rendered separately at the head of the table
}

// Mirrors SessionStatus enum — used to drive the round tracker / progress rail.
export const SESSION_STAGES = [
  { value: "pending", label: "Queued" },
  { value: "preprocessing", label: "Preprocessing" },
  { value: "agent_selection", label: "Selecting Agents" },
  { value: "round_1", label: "Round 1 — Independent Analysis" },
  { value: "round_2", label: "Round 2 — Peer Review" },
  { value: "round_3", label: "Round 3 — Challenge" },
  { value: "synthesis", label: "CEO Synthesis" },
  { value: "report_generation", label: "Generating Report" },
  { value: "completed", label: "Completed" },
];
