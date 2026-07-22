// Demo-mode fixtures — only used when the user clicks "Explore with demo
// data" on the sign-in screen, or when a real API call fails and demoMode is
// active. Shaped to match the Pydantic response schemas exactly so swapping
// in the real API later is a no-op for every component that consumes it.

export const DEMO_PROJECTS = [
  {
    id: "proj_01",
    title: "Modular vertical-farming kits for urban restaurants",
    description:
      "A subscription hardware + SaaS product: countertop hydroponic modules that let restaurants grow their own micro-greens and herbs, with a companion app for yield tracking and reorder automation.",
    input_type: "startup_idea",
    status: "completed",
    created_at: "2026-07-14T09:12:00Z",
    updated_at: "2026-07-14T10:58:00Z",
  },
  {
    id: "proj_02",
    title: "Churn dataset — Q2 subscriber cancellations",
    description: "42,000-row export from the billing system, looking for leading indicators of cancellation.",
    input_type: "dataset_analysis",
    status: "completed",
    created_at: "2026-07-10T14:02:00Z",
    updated_at: "2026-07-10T15:40:00Z",
  },
  {
    id: "proj_03",
    title: "Series A pitch: on-device translation earbuds",
    description: "Evaluating whether to raise now or wait for the next hardware revision.",
    input_type: "investment_due_diligence",
    status: "active",
    created_at: "2026-07-18T08:00:00Z",
    updated_at: "2026-07-19T11:20:00Z",
  },
  {
    id: "proj_04",
    title: "Rebuild checkout on microservices",
    description: "Proposal to split the monolith checkout flow into three services ahead of Black Friday load.",
    input_type: "technical_architecture",
    status: "draft",
    created_at: "2026-07-19T17:45:00Z",
    updated_at: "2026-07-19T17:45:00Z",
  },
];

export const DEMO_SESSIONS = {
  proj_01: {
    id: "sess_01",
    project_id: "proj_01",
    status: "completed",
    round_count: 3,
    agents_selected: ["CMO", "COO", "CFO", "CHRO", "CISO", "CCO"],
    started_at: "2026-07-14T09:13:00Z",
    completed_at: "2026-07-14T09:21:00Z",
  },
  proj_03: {
    id: "sess_03",
    project_id: "proj_03",
    status: "round_2",
    round_count: 3,
    agents_selected: ["CFO", "COO", "CMO", "CISO", "CHRO"],
    started_at: "2026-07-19T11:15:00Z",
    completed_at: null,
  },
};

export const DEMO_REPORT = {
  id: "rep_01",
  session_id: "sess_01",
  project_id: "proj_01",
  title: "Board Decision — Modular vertical-farming kits",
  summary:
    "The board recommends proceeding with a modified go-to-market: launch with 10 pilot restaurants in one metro before national rollout.",
  full_content: {
    executive_summary:
      "The unit economics work at a $340/mo subscription once hardware cost is amortized over 18 months, but customer acquisition inside independent restaurants is slower than chains. The board recommends a metro-first pilot to prove retention before raising a seed round.",
    key_decisions: [
      "Launch with 10 pilot restaurants in a single metro area before wider rollout",
      "Price at $340/mo including consumables, re-evaluate after 90-day pilot retention data",
      "Delay hiring a full sales team until pilot cohort hits 80% 90-day retention",
    ],
    strategic_plan:
      "Phase 1 (0-3mo): recruit 10 pilot restaurants via direct outreach in one metro. Phase 2 (3-6mo): instrument yield + reorder data, iterate on module reliability. Phase 3 (6-12mo): expand to 3 metros only if 90-day retention clears 80%.",
    dissenting_opinions_resolved:
      "The Compliance officer flagged that countertop space is the real constraint, not price — kitchens are cramped and owners may not clear a spot for an unproven appliance. The board resolved this by making the pilot's success metric physical retention of the unit past week 2, not just subscription renewal.",
    decision_outcome: "go_with_modifications",
    agent_findings: [
      {
        agent: "CMO",
        summary: "Clear wedge into an underserved segment — independent restaurants are ignored by big vertical-farming players who chase grocery chains.",
        confidence_score: 78,
      },
      {
        agent: "COO",
        summary: "Subscription model is sound but sales cycle to independent restaurant owners is 6-8 weeks, longer than modeled.",
        confidence_score: 71,
      },
      {
        agent: "CFO",
        summary: "Breakeven at 340 active subscriptions given current hardware BOM; achievable in 14 months at modeled growth.",
        confidence_score: 83,
      },
      {
        agent: "CHRO",
        summary: "Kitchen staff, not owners, are the daily users — onboarding needs to target line cooks directly, not just the decision-maker.",
        confidence_score: 74,
      },
      {
        agent: "CISO",
        summary: "Food-safety certification for the growing modules adds 6-8 weeks to launch timeline in most states.",
        confidence_score: 69,
      },
      {
        agent: "CCO",
        summary: "Countertop space is the real constraint, not price. Owners may not clear space for an unproven appliance regardless of ROI.",
        confidence_score: 65,
      },
    ],
  },
  pdf_url: null,
  created_at: "2026-07-14T09:22:00Z",
  updated_at: "2026-07-14T09:22:00Z",
};

export const DEMO_NOTIFICATIONS = [
  { id: "n1", title: "Board session completed", message: "\"Modular vertical-farming kits\" finished — report ready to read.", is_read: false, created_at: "2026-07-14T09:22:00Z" },
  { id: "n2", title: "Round 2 in progress", message: "\"Series A pitch: on-device translation earbuds\" entered peer review.", is_read: false, created_at: "2026-07-19T11:20:00Z" },
  { id: "n3", title: "Report exported", message: "Churn dataset report exported as PDF.", is_read: true, created_at: "2026-07-10T15:41:00Z" },
];

export const DEMO_STATS = {
  activeProjects: 2,
  sessionsRun: 7,
  reportsGenerated: 5,
  avgConfidence: 76,
};

// A scripted event timeline used to animate the live BoardroomTable in demo
// mode, matching the exact shape the real WebSocket emits — see
// backend/app/websocket/events.py.
export function scriptedSessionEvents(agentKeys) {
  const events = [];
  const roundAgents = agentKeys;

  [1, 2, 3].forEach((round) => {
    if (round > 1) {
      events.push({ type: "round_advanced", payload: { round } });
    }
    roundAgents.forEach((agent) => {
      events.push({ type: "agent_started", payload: { agent, round } });
      events.push({ type: "agent_finished", payload: { agent, round } });
    });
  });
  events.push({ type: "ceo_started", payload: {} });
  events.push({ type: "session_completed", payload: {} });
  return events;
}
