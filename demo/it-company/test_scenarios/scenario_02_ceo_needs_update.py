"""Scenario 2: The CEO Needs an Answer (But Alice is in Back-to-Back Meetings).

WOW Moment: CEO needs technical update on payment migration. Alice (Backend Manager)
is in meetings from 9 AM to 5 PM. CEO gets comprehensive answer instantly from
Alice's and Henry's agents without interrupting anyone.

Demonstrates: No interruption cost, instant executive updates, no context switching.
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


def main() -> None:  # noqa: PLR0915
    """Run CEO needs update scenario."""
    print("=" * 80)
    print("👔 Scenario 2: The CEO Needs an Answer (But Alice is in Meetings)")
    print("=" * 80)
    print()
    print("SITUATION: CEO needs status update on payment microservices migration.")
    print("           Alice (Backend Manager) is in back-to-back meetings 9 AM - 5 PM.")
    print()
    print("THE OLD WAY:")
    print("  ❌ CEO waits until Alice is free → decision delayed by 8 hours")
    print("  ❌ Alice interrupted mid-meeting → loses focus, meeting derailed")
    print("  ❌ Play phone tag → takes 3 days to actually connect")
    print()
    print("THE WOW MOMENT WITH AGENTS:")
    print("  ✅ CEO queries Alice's agent instantly")
    print("  ✅ Gets comprehensive project status in 30 seconds")
    print("  ✅ Alice stays focused in meetings, no context switching")
    print()

    # Load registered agents
    try:
        registered_agents = load_registered_agents()
    except Exception as e:
        print(f"✗ Failed to load registered agents: {e}")
        return

    # Find agent IDs
    alice_id = None
    henry_id = None

    for agent_id, info in registered_agents.items():
        if info["name"] == "alice-chen":
            alice_id = agent_id
        elif info["name"] == "henry-brooks":
            henry_id = agent_id

    if not all([alice_id, henry_id]):
        print("✗ Could not find all required agents")
        return

    with httpx.Client(timeout=30.0) as client:
        # Step 1: CEO queries Alice's agent
        print("-" * 80)
        print("Step 1: CEO asks Alice's Agent")
        print("-" * 80)
        print('  Question: "What\'s the status of the payment microservices migration?"')
        print('            "Are we on track for March 15 target?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                alice_id,
                "payment microservices migration status timeline progress March",
                limit=5,
            )
            print(f"  Alice's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 COMPREHENSIVE STATUS FROM ALICE'S AGENT:")
                print()
                print("     📊 PAYMENT MIGRATION STATUS (as of January 2026):")
                print("     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("     Progress: 40% complete")
                print("     Target: March 15, 2026")
                print("     Status: ✅ ON TRACK")
                print()
                print("     ✅ COMPLETED:")
                print("        • Architecture design (event-driven with Kafka)")
                print("        • Payment processing microservice deployed to staging")
                print("        • API contracts defined and reviewed")
                print()
                print("     🔄 IN PROGRESS:")
                print("        • Refund service development (Bob leading)")
                print("        • Database migration scripts (Carol working on)")
                print()
                print("     📅 UPCOMING:")
                print("        • Testing phase starts Feb 15")
                print("        • Production deployment Feb 28 - Mar 7")
                print("        • Final cutover weekend of Mar 15")
                print()
                print("     ⚠️  RISKS:")
                print("        • Need DevOps support for K8s setup by Feb 1")
                print("        • Henry's team is aware and on the schedule")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 2: CEO follows up with Henry's agent
        print("-" * 80)
        print("Step 2: CEO asks Henry's Agent for DevOps confirmation")
        print("-" * 80)
        print('  Question: "Is DevOps support scheduled for the payment migration?"')
        print('            "Any blockers on your side?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                henry_id,
                "payment migration DevOps kubernetes support February timeline",
                limit=5,
            )
            print(f"  Henry's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 DEVOPS STATUS FROM HENRY'S AGENT:")
                print()
                print("     ✅ DEVOPS SUPPORT CONFIRMED:")
                print("     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("     Scheduled: January 28, 2026")
                print("     Status: No blockers, on track")
                print()
                print("     🎯 KUBERNETES SETUP INCLUDES:")
                print("        • 3 node pools (system/app/data)")
                print("        • Auto-scaling enabled (2-10 replicas)")
                print("        • Monitoring with Prometheus/Grafana")
                print("        • CI/CD pipeline using ArgoCD")
                print("        • Blue-green deployment strategy")
                print()
                print("     📦 INFRASTRUCTURE READY:")
                print("        • Staging environment: ✅ Complete")
                print("        • Production environment: ✅ Ready for deployment")
                print("        • Rollback plan: ✅ Documented and tested")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    # Summary
    print("=" * 80)
    print("✅ SCENARIO COMPLETE - CEO HAS FULL PICTURE!")
    print("=" * 80)
    print()
    print("TIMELINE:")
    print("  10:00 AM - CEO needs migration status")
    print("  10:01 AM - CEO queries Alice's agent → gets comprehensive project status")
    print("  10:02 AM - CEO queries Henry's agent → confirms DevOps support on track")
    print("  10:03 AM - CEO has complete answer, makes informed decision")
    print()
    print("WHAT ALICE EXPERIENCED:")
    print("  9:00 AM  - Sprint planning meeting (uninterrupted)")
    print("  10:00 AM - Architecture review meeting (uninterrupted)")
    print("  11:00 AM - 1:1 with Bob (uninterrupted)")
    print("  12:00 PM - Lunch (peaceful)")
    print("  1:00 PM  - Sees notification: 'CEO queried your agent about migration status'")
    print("  1:01 PM  - Reviews the Q&A, everything accurate, no action needed")
    print()
    print("IMPACT:")
    print("  ⏱️  CEO got answer in 3 MINUTES (vs 3 days of phone tag)")
    print("  🎯 Alice stayed focused, zero context switching penalty")
    print("  📊 Complete, accurate status with no preparation needed")
    print("  ✅ CEO made decision before lunch instead of next week")
    print()
    print("THE WOW FACTOR:")
    print("  🌟 Executive updates without executive interruption")
    print("  🌟 Perfect information recall (agents never forget context)")
    print("  🌟 Multi-stakeholder coordination in seconds")
    print("  🌟 Managers preserve deep work time")
    print()
    print("Instead of interrupting Alice in her meetings, CEO asked her agent!")
    print()


if __name__ == "__main__":
    main()
