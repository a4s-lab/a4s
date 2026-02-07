"""Scenario 5: The Lightning-Fast Decision (5 People, 5 Minutes).

WOW Moment: Product Manager Maya needs input from Design, Engineering, QA, and
Marketing to decide on a feature. Instead of scheduling a meeting (takes a week),
she queries 5 agents and gets all input in 5 minutes. Makes informed decision before lunch.

Demonstrates: Meeting-free decision making, parallel consultation, zero scheduling overhead.
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
    """Run lightning-fast decision scenario."""
    print("=" * 80)
    print("💡 Scenario 5: The Lightning-Fast Decision (5 People, 5 Minutes)")
    print("=" * 80)
    print()
    print("SITUATION: Maya (Product Manager) needs to decide:")
    print('           "Should we add saved payment methods NOW or wait until Q2?"')
    print()
    print("           Needs input from:")
    print("           • Olivia (Design) - Design effort estimate")
    print("           • Emily (Frontend) - Engineering complexity")
    print("           • Bob (Backend) - Backend implementation scope")
    print("           • Kate (QA) - Testing requirements")
    print("           • Rachel (Marketing) - Customer value")
    print()
    print("THE OLD WAY:")
    print("  ❌ Email chain with 5 people → takes 3 days, messy thread")
    print("  ❌ Schedule meeting → earliest slot is next week")
    print("  ❌ By meeting time, context is stale and decision is late")
    print()
    print("THE WOW MOMENT WITH AGENTS:")
    print("  ✅ Query 5 agents simultaneously")
    print("  ✅ Get all input in 5 minutes")
    print("  ✅ Make informed decision before lunch")
    print()

    # Load registered agents
    try:
        registered_agents = load_registered_agents()
    except Exception as e:
        print(f"✗ Failed to load registered agents: {e}")
        return

    # Find agent IDs
    olivia_id = None
    emily_id = None
    bob_id = None
    kate_id = None
    rachel_id = None

    for agent_id, info in registered_agents.items():
        if info["name"] == "olivia-taylor":
            olivia_id = agent_id
        elif info["name"] == "emily-wang":
            emily_id = agent_id
        elif info["name"] == "bob-martinez":
            bob_id = agent_id
        elif info["name"] == "kate-thompson":
            kate_id = agent_id
        elif info["name"] == "rachel-green":
            rachel_id = agent_id

    if not all([olivia_id, emily_id, bob_id, kate_id, rachel_id]):
        print("✗ Could not find all required agents")
        return

    with httpx.Client(timeout=30.0) as client:
        # Step 1: Query Olivia's agent (Design)
        print("-" * 80)
        print("Step 1: Maya asks Olivia's Agent (Design Lead)")
        print("-" * 80)
        print('  Question: "What\'s the design effort for saved payment methods?"')
        print()

        try:
            memories = search_memory(
                client, "owner", olivia_id, "saved payment methods design effort UI components", limit=3
            )
            print(f"  Olivia's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 DESIGN ASSESSMENT:")
                print("     Effort: LOW ✅")
                print("     Rationale: PaymentMethodSelector component already designed with saved cards")
                print("     Work needed:")
                print("       • Add 'Save for later' checkbox to payment form")
                print("       • Design 'Manage saved cards' screen")
                print("     Estimate: 3 design days")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 2: Query Emily's agent (Frontend)
        print("-" * 80)
        print("Step 2: Maya asks Emily's Agent (Senior Frontend Engineer)")
        print("-" * 80)
        print('  Question: "What\'s the frontend engineering complexity?"')
        print()

        try:
            memories = search_memory(
                client, "owner", emily_id, "saved payment methods frontend React state management localStorage", limit=3
            )
            print(f"  Emily's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 FRONTEND ASSESSMENT:")
                print("     Complexity: MEDIUM ⚠️")
                print("     Work needed:")
                print("       • Add localStorage/backend sync for saved methods")
                print("       • Implement card management UI (edit/delete)")
                print("       • Handle expired cards gracefully")
                print("       • Add encryption for card last-4 digits display")
                print("     Estimate: 5 engineering days")
                print("     Blockers: None")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 3: Query Bob's agent (Backend)
        print("-" * 80)
        print("Step 3: Maya asks Bob's Agent (Senior Backend Engineer)")
        print("-" * 80)
        print('  Question: "What\'s the backend implementation scope?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                bob_id,
                "saved payment methods backend Stripe payment gateway customer vault",
                limit=3,
            )
            print(f"  Bob's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 BACKEND ASSESSMENT:")
                print("     Complexity: LOW ✅")
                print("     Rationale: Stripe already stores payment methods in their vault (PCI compliant!)")
                print("     Work needed:")
                print("       • Store customer_id mapping in our database")
                print("       • Add /payment-methods GET/POST/DELETE endpoints")
                print("       • Add token refresh logic for expired cards")
                print("     Estimate: 3 engineering days")
                print("     Security: Stripe handles PCI compliance, we just store references")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 4: Query Kate's agent (QA)
        print("-" * 80)
        print("Step 4: Maya asks Kate's Agent (QA Lead)")
        print("-" * 80)
        print('  Question: "What\'s the QA scope and testing requirements?"')
        print()

        try:
            memories = search_memory(
                client, "owner", kate_id, "saved payment methods testing QA E2E security validation", limit=3
            )
            print(f"  Kate's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 QA ASSESSMENT:")
                print("     Scope: MEDIUM ⚠️")
                print("     Test coverage needed:")
                print("       • Save/retrieve/delete payment method flows")
                print("       • Expired card handling and refresh")
                print("       • Multiple browsers/devices sync")
                print("       • Security: Verify no plaintext card data stored")
                print("     Estimate: 4 QA days")
                print("     Note: Can run in parallel with development")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 5: Query Rachel's agent (Marketing)
        print("-" * 80)
        print("Step 5: Maya asks Rachel's Agent (Marketing Manager)")
        print("-" * 80)
        print('  Question: "What\'s the customer value and marketing perspective?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                rachel_id,
                "saved payment methods customer feedback feature requests checkout conversion",
                limit=3,
            )
            print(f"  Rachel's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 MARKETING ASSESSMENT:")
                print("     Value: HIGH 🚀")
                print("     Customer feedback:")
                print("       • 64% of users want saved payment methods (TOP feature request)")
                print("       • Reduces checkout friction significantly")
                print("       • Increases conversion rate (industry benchmark: +15%)")
                print("     Marketing narrative:")
                print("       • Perfect for Q1 launch: 'Faster, easier checkout'")
                print("       • Competitive parity (competitors all have this)")
                print("     Recommendation: Ship ASAP")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    # Summary and Decision
    print("=" * 80)
    print("✅ SCENARIO COMPLETE - DECISION MADE!")
    print("=" * 80)
    print()
    print("TIMELINE:")
    print("  10:00 AM - Maya needs to decide on saved payment methods feature")
    print("  10:01 AM - Queries Olivia's agent → Design effort: LOW (3 days)")
    print("  10:02 AM - Queries Emily's agent → Frontend: MEDIUM (5 days)")
    print("  10:03 AM - Queries Bob's agent → Backend: LOW (3 days)")
    print("  10:04 AM - Queries Kate's agent → QA scope: MEDIUM (4 days, parallel)")
    print("  10:05 AM - Queries Rachel's agent → Customer value: HIGH")
    print("  10:10 AM - Analyzes all input, makes decision")
    print()
    print("📊 DECISION MATRIX:")
    print("  ┌─────────────────┬────────────┬──────────────┐")
    print("  │ Function        │ Effort     │ Assessment   │")
    print("  ├─────────────────┼────────────┼──────────────┤")
    print("  │ Design          │ 3 days     │ ✅ LOW       │")
    print("  │ Frontend        │ 5 days     │ ⚠️  MEDIUM   │")
    print("  │ Backend         │ 3 days     │ ✅ LOW       │")
    print("  │ QA              │ 4 days     │ ⚠️  MEDIUM   │")
    print("  │ Marketing Value │ N/A        │ 🚀 HIGH      │")
    print("  └─────────────────┴────────────┴──────────────┘")
    print()
    print("  Total effort: ~15 engineering days")
    print("  Can be parallelized: Design + Dev + QA → ~1.5 weeks")
    print("  Customer value: Very high (top feature request)")
    print("  Risk: Low (Stripe handles PCI compliance)")
    print()
    print("🎯 MAYA'S DECISION:")
    print("  ✅ SHIP IT IN Q1!")
    print()
    print("  Rationale:")
    print("    • Customer value is very high (top request)")
    print("    • Implementation is straightforward (~1.5 weeks)")
    print("    • Low risk (Stripe handles security)")
    print("    • Great marketing narrative for Q1")
    print()
    print("  Next steps:")
    print("    • Add to Q1 sprint (starting next week)")
    print("    • Emily to lead frontend, Bob to lead backend")
    print("    • Kate to prepare test plan")
    print("    • Rachel to prepare launch announcement")
    print()
    print("WHAT THE TEAM EXPERIENCED:")
    print("  👩‍🎨 Olivia: Deep work (uninterrupted), sees agent query notification")
    print("  👩‍💻 Emily: Coding session (uninterrupted)")
    print("  👨‍💻 Bob: Focus time (uninterrupted)")
    print("  🧪 Kate: Testing work (uninterrupted)")
    print("  📣 Rachel: Campaign planning (uninterrupted)")
    print()
    print("IMPACT:")
    print("  ⏱️  Decision made in 10 MINUTES (vs 1 week meeting scheduling)")
    print("  🚀 Feature approved and planned before lunch")
    print("  💪 Zero team interruption (everyone stayed focused)")
    print("  📊 High-quality decision (all stakeholders consulted)")
    print()
    print("TRADITIONAL DECISION-MAKING:")
    print("  Monday: Maya sends email to 5 people")
    print("  Tuesday-Wednesday: Fragmented email responses trickle in")
    print("  Thursday: Try to schedule meeting")
    print("  Next Tuesday: Finally find 30-min slot where everyone is free")
    print("  Next Wednesday: Meeting happens, decision made (context already stale)")
    print("  Total time: 9 DAYS")
    print()
    print("AGENT-ASSISTED DECISION-MAKING:")
    print("  10:00 AM: Query 5 agents simultaneously")
    print("  10:05 AM: Have all input")
    print("  10:10 AM: Decision made")
    print("  Total time: 10 MINUTES")
    print()
    print("  📈 77,760X FASTER (9 days → 10 minutes)")
    print()
    print("THE WOW FACTOR:")
    print("  🌟 Instant parallel consultation (5 experts at once)")
    print("  🌟 Meeting-free decision making")
    print("  🌟 Zero scheduling overhead")
    print("  🌟 Team productivity unaffected")
    print("  🌟 Perfect context preservation (no 'forgot what we discussed')")
    print()
    print("Instead of scheduling a meeting with 5 people (taking a week),")
    print("Maya asked 5 agents and made an informed decision in 10 minutes!")
    print()


if __name__ == "__main__":
    main()
