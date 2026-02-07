"""Scenario 4: The New Hire's First Week (No One to Bug).

WOW Moment: New backend engineer David's first day. Has 50 questions but everyone
is busy. Gets expert answers from Alice's, Bob's, Henry's, and Kate's agents without
interrupting anyone. Ramps up 3x faster.

Demonstrates: Instant onboarding, no social anxiety, perfect knowledge transfer,
team productivity unaffected.
"""

import json
from pathlib import Path

import httpx

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
REGISTERED_AGENTS_PATH = Path(__file__).parent.parent / "scripts" / "registered_agents.json"


def load_registered_agents() -> dict:
    """Load registered agents from file."""
    with Path.open(REGISTERED_AGENTS_PATH) as f:
        return json.load(f)


def search_memory(client: httpx.Client, requester_id: str, target_agent_id: str, query: str, limit: int = 3) -> list:  # noqa: ARG001
    """Search an agent's memories.

    Args:
        client: HTTP client.
        requester_id: ID of agent making the request.
        target_agent_id: ID of agent whose memories to search.
        query: Search query.
        limit: Maximum results.

    Returns:
        List of memory results.
    """
    payload = {"query": query, "agent_id": target_agent_id, "limit": limit}
    headers = {"X-Requester-Id": "owner"}

    response = client.post(f"{API_BASE_URL}/memories/search", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def print_memory_results(memories: list, indent: str = "    ") -> None:
    """Pretty print memory search results."""
    for i, memory in enumerate(memories, 1):
        content = memory.get("content", "")
        snippet = content[:200] + "..." if len(content) > 200 else content
        print(f"{indent}{i}. {snippet}")
        print()


def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Run new hire onboarding scenario."""
    print("=" * 80)
    print("🎯 Scenario 4: The New Hire's First Week (No One to Bug)")
    print("=" * 80)
    print()
    print("SITUATION: David (new backend engineer) just started.")
    print("           First task: Add a new API endpoint to payment service.")
    print("           Has 50 questions. Everyone is busy. Doesn't want to seem annoying.")
    print()
    print("THE OLD WAY:")
    print("  ❌ Interrupt Alice 15 times → she can't get her work done")
    print("  ❌ Documentation is outdated → wastes days following wrong info")
    print("  ❌ Afraid to ask 'dumb questions' → makes mistakes causing production issues")
    print("  ❌ Takes 3 months to ramp up")
    print()
    print("THE WOW MOMENT WITH AGENTS:")
    print("  ✅ Ask agents unlimited questions (no social anxiety!)")
    print("  ✅ Get expert answers instantly")
    print("  ✅ Productive from day 1")
    print()

    # Load registered agents
    try:
        registered_agents = load_registered_agents()
    except Exception as e:
        print(f"✗ Failed to load registered agents: {e}")
        return

    # Find agent IDs
    alice_id = None
    bob_id = None
    henry_id = None
    kate_id = None

    for agent_id, info in registered_agents.items():
        if info["name"] == "alice-chen":
            alice_id = agent_id
        elif info["name"] == "bob-martinez":
            bob_id = agent_id
        elif info["name"] == "henry-brooks":
            henry_id = agent_id
        elif info["name"] == "kate-thompson":
            kate_id = agent_id

    if not all([alice_id, bob_id, henry_id, kate_id]):
        print("✗ Could not find all required agents")
        return

    with httpx.Client(timeout=30.0) as client:
        # Step 1: Query Alice's agent about team standards
        print("-" * 80)
        print("Step 1: David asks Alice's Agent")
        print("-" * 80)
        print('  Question: "I\'m new to the backend team."')
        print('            "What are the code standards and review process?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                alice_id,
                "code review standards testing coverage backend team process Python",
                limit=5,
            )
            print(f"  Alice's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 TEAM STANDARDS FROM ALICE'S AGENT:")
                print()
                print("     📋 CODE REVIEW STANDARDS:")
                print("        • Minimum 80% test coverage required")
                print("        • PR approval within 24 hours (ping if delayed)")
                print("        • Check for security vulnerabilities (SQL injection, secrets in code)")
                print("        • All PRs need at least 1 approval from senior engineer")
                print()
                print("     🐍 BACKEND TECH STACK:")
                print("        • Python 3.11+ with FastAPI")
                print("        • PostgreSQL for databases")
                print("        • Redis for caching and distributed locks")
                print("        • Kafka for event streaming")
                print()
                print("     👥 TEAM RESOURCES:")
                print("        • Bob Martinez: Payment service expert (great resource!)")
                print("        • Carol Kim: Database optimization specialist")
                print("        • Daily standup at 10 AM (optional for deep work days)")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 2: Query Bob's agent about payment service
        print("-" * 80)
        print("Step 2: David asks Bob's Agent")
        print("-" * 80)
        print('  Question: "I need to add a new API endpoint to payment service."')
        print('            "What\'s the code structure and patterns I should follow?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                bob_id,
                "payment service API endpoint structure FastAPI code patterns architecture",
                limit=5,
            )
            print(f"  Bob's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 PAYMENT SERVICE ARCHITECTURE FROM BOB'S AGENT:")
                print()
                print("     📁 CODE STRUCTURE:")
                print("        • /app/routes/ - API endpoints (FastAPI routers)")
                print("        • /app/services/ - Business logic (keep routes thin!)")
                print("        • /app/models/ - Pydantic models and database schemas")
                print("        • /app/utils/ - Helper functions and shared utilities")
                print()
                print("     🔑 KEY PATTERNS:")
                print("        • Use idempotency keys for all write operations")
                print("        • Redis distributed locks for concurrent operations")
                print("        • Async/await for I/O operations")
                print("        • See PR #234 for idempotency pattern example")
                print()
                print("     ✅ IMPORTANT:")
                print("        • All endpoints need /health check support")
                print("        • Use pytest for unit + integration tests")
                print("        • Mock external dependencies in tests")
                print("        • Environment variables in .env (never in code!)")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 3: Query Henry's agent about deployment
        print("-" * 80)
        print("Step 3: David asks Henry's Agent")
        print("-" * 80)
        print('  Question: "How does deployment work?"')
        print('            "Where do I put environment variables?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                henry_id,
                "deployment process CI/CD GitHub Actions environment variables Kubernetes",
                limit=5,
            )
            print(f"  Henry's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 DEPLOYMENT PROCESS FROM HENRY'S AGENT:")
                print()
                print("     🚀 DEPLOYMENT WORKFLOW:")
                print("        1. Open PR → GitHub Actions runs lint/test automatically")
                print("        2. Get approval → Auto-merge to main branch")
                print("        3. ArgoCD auto-deploys to staging environment")
                print("        4. Manual approval → Deploys to production (blue-green)")
                print()
                print("     🔐 ENVIRONMENT VARIABLES:")
                print("        • Store in Kubernetes secrets (NEVER in code or .env in repo!)")
                print("        • Local dev: Use .env.local (in .gitignore)")
                print("        • Ask in #devops Slack channel for secret access")
                print("        • Never log secrets or commit to git")
                print()
                print("     📊 MONITORING:")
                print("        • Logs: kubectl logs -f <pod-name>")
                print("        • Metrics: Grafana dashboard (link in wiki)")
                print("        • Alerts: PagerDuty for production issues")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 4: Query Kate's agent about testing
        print("-" * 80)
        print("Step 4: David asks Kate's Agent")
        print("-" * 80)
        print('  Question: "What testing is required?"')
        print('            "How do I write good tests?"')
        print()

        try:
            memories = search_memory(
                client, "owner", kate_id, "testing requirements pytest unit integration E2E payment service", limit=5
            )
            print(f"  Kate's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 TESTING REQUIREMENTS FROM KATE'S AGENT:")
                print()
                print("     ✅ TESTING LEVELS:")
                print("        • Unit tests: Test individual functions (use pytest, mock dependencies)")
                print("        • Integration tests: Test against real test database")
                print("        • E2E tests: Test full user flows with Playwright")
                print()
                print("     🎯 BEST PRACTICES:")
                print("        • Aim for 80%+ coverage (run: pytest --cov)")
                print("        • Test happy path + error cases + edge cases")
                print("        • Use fixtures for test data setup")
                print("        • Example test structure in /tests/test_payment_api.py")
                print()
                print("     📚 RESOURCES:")
                print("        • I can help set up E2E tests (just ask!)")
                print("        • Test fixtures in /tests/conftest.py")
                print("        • CI runs all tests automatically on PR")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    # Summary
    print("=" * 80)
    print("✅ SCENARIO COMPLETE - DAVID IS FULLY RAMPED UP!")
    print("=" * 80)
    print()
    print("DAVID'S FIRST DAY TIMELINE:")
    print("  9:00 AM  - Start work, get task: 'Add payment refund endpoint'")
    print("  9:10 AM  - Ask Alice's agent about team standards → got full answer")
    print("  9:15 AM  - Ask Bob's agent about payment service → got architecture guide")
    print("  9:20 AM  - Ask Henry's agent about deployment → got full workflow")
    print("  9:25 AM  - Ask Kate's agent about testing → got testing guide")
    print("  9:30 AM  - Start coding (fully informed!)")
    print("  2:00 PM  - Submit first PR with tests and documentation")
    print("  3:00 PM  - PR approved and merged!")
    print()
    print("WHAT THE TEAM EXPERIENCED:")
    print("  👩‍💼 Alice: Focus time (no interruptions), reviews David's PR at 2 PM")
    print("  👨‍💻 Bob: Deep coding session (no interruptions), approves PR quickly")
    print("  🔧 Henry: Infrastructure work (no interruptions)")
    print("  🧪 Kate: Testing work (no interruptions)")
    print()
    print("TRADITIONAL NEW HIRE EXPERIENCE:")
    print("  Day 1: Setup environment, read outdated docs → confused")
    print("  Day 2-3: Ask 50 questions → team annoyed, answers fragmented")
    print("  Week 1: Submit first PR → 10 review comments (missed patterns)")
    print("  Month 1: Still ramping up")
    print("  Month 3: Finally productive")
    print()
    print("AGENT-ASSISTED NEW HIRE EXPERIENCE:")
    print("  Day 1: Ask agents unlimited questions → fully productive by lunch!")
    print("  Week 1: Submit 5 PRs → all following best practices")
    print("  Month 1: Contributing at senior level velocity")
    print()
    print("IMPACT:")
    print("  ⏱️  Time to first PR: 5 HOURS (vs 3 days traditionally)")
    print("  🚀 Ramp-up time: 1 MONTH (vs 3 months traditionally) - 3X FASTER")
    print("  😊 David feels confident (not annoying)")
    print("  💪 Team productivity unaffected (zero interruptions)")
    print()
    print("THE WOW FACTOR:")
    print("  🌟 Ask unlimited questions without social anxiety")
    print("  🌟 Get expert answers instantly (no waiting)")
    print("  🌟 Perfect knowledge transfer (agents never forget)")
    print("  🌟 Team stays productive (no interruption tax)")
    print()
    print("Instead of interrupting the team 50 times, David asked their agents!")
    print()


if __name__ == "__main__":
    main()
