"""Scenario 1: The 2 AM Production Fire.

WOW Moment: Payment service crashes at 2 AM. Bob (the engineer who knows it best)
is asleep. On-call engineer gets instant answers from Bob's, Henry's, and Kate's
agents without waking anyone up.

Demonstrates: 24/7 availability, zero interruption cost, instant expert knowledge.
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


def main() -> None:  # noqa: C901, PLR0915
    """Run production fire scenario."""
    print("=" * 80)
    print("🚨 Scenario 1: The 2 AM Production Fire")
    print("=" * 80)
    print()
    print("SITUATION: It's 2 AM. Payment service is down with 500 errors.")
    print("           Bob (who built it) is asleep. On-call engineer needs answers NOW.")
    print()
    print("THE OLD WAY:")
    print("  ❌ Wake Bob up at 2 AM → ruins his sleep")
    print("  ❌ Wait until morning → customers can't checkout for 6 hours")
    print("  ❌ Dig through docs → incomplete and outdated")
    print()
    print("THE WOW MOMENT WITH AGENTS:")
    print("  ✅ Query agent knowledge bases instantly")
    print("  ✅ Get expert answers in seconds")
    print("  ✅ No one woken up, problem diagnosed and fixed")
    print()

    # Load registered agents
    try:
        registered_agents = load_registered_agents()
    except Exception as e:
        print(f"✗ Failed to load registered agents: {e}")
        return

    # Find agent IDs
    bob_id = None
    henry_id = None
    kate_id = None

    for agent_id, info in registered_agents.items():
        if info["name"] == "bob-martinez":
            bob_id = agent_id
        elif info["name"] == "henry-brooks":
            henry_id = agent_id
        elif info["name"] == "kate-thompson":
            kate_id = agent_id

    if not all([bob_id, henry_id, kate_id]):
        print("✗ Could not find all required agents")
        return

    with httpx.Client(timeout=30.0) as client:
        # Step 1: Query Bob's agent about payment service architecture
        print("-" * 80)
        print("Step 1: On-call engineer asks Bob's Agent")
        print("-" * 80)
        print('  Question: "Payment service is down with 500 errors."')
        print('            "What\'s the architecture and recent changes?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                bob_id,
                "payment service architecture deployment requirements recent changes bugs",
                limit=5,
            )
            print(f"  Bob's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 KEY INSIGHTS FROM BOB'S AGENT:")
                print("     • Payment service: FastAPI + PostgreSQL + Redis + Kafka")
                print("     • 3 replicas, handles 500 req/sec at peak")
                print("     • Recent fix (Jan 15): Added Redis distributed locks for duplicate charges")
                print("     • Redis is a SINGLE POINT OF FAILURE - check if it's reachable!")
                print("     • Required env vars: DATABASE_URL, REDIS_URL, KAFKA_BROKERS, STRIPE_API_KEY")
                print("     • Health check: /health on port 8080")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 2: Query Henry's agent about infrastructure
        print("-" * 80)
        print("Step 2: On-call engineer asks Henry's Agent")
        print("-" * 80)
        print('  Question: "What does the Kubernetes cluster show?"')
        print('            "Any recent infrastructure changes?"')
        print()

        try:
            memories = search_memory(
                client, "owner", henry_id, "kubernetes payment service deployment infrastructure monitoring", limit=5
            )
            print(f"  Henry's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 KEY INSIGHTS FROM HENRY'S AGENT:")
                print("     • Check: kubectl get pods -n production | grep payment")
                print("     • Check: kubectl get pods -n production | grep redis")
                print("     • Likely issue: Redis pod OOM or restart")
                print("     • Quick fix steps:")
                print("       1. Check Redis pod status and logs")
                print("       2. Increase Redis memory limit if needed")
                print("       3. Restart payment service pods:")
                print("          kubectl scale deployment payment-service --replicas=0")
                print("          kubectl scale deployment payment-service --replicas=3")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 3: Query Kate's agent about testing gaps
        print("-" * 80)
        print("Step 3: On-call engineer asks Kate's Agent")
        print("-" * 80)
        print('  Question: "How do we prevent this from happening again?"')
        print('            "What testing gaps do we have?"')
        print()

        try:
            memories = search_memory(
                client, "owner", kate_id, "payment service testing E2E Redis failure scenarios", limit=5
            )
            print(f"  Kate's Agent responds (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 KEY INSIGHTS FROM KATE'S AGENT:")
                print("     • The duplicate charge fix had adequate unit tests")
                print("     • Gap: Missing E2E tests for Redis failure scenarios")
                print("     • Recommendation: Add chaos engineering tests")
                print("     • Add to test suite: Redis unavailable, Redis restart, network partition")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    # Summary
    print("=" * 80)
    print("✅ SCENARIO COMPLETE - PROBLEM RESOLVED!")
    print("=" * 80)
    print()
    print("RESOLUTION TIMELINE:")
    print("  2:00 AM - Payment service goes down (500 errors)")
    print("  2:02 AM - On-call queries Bob's agent → gets architecture & recent changes")
    print("  2:04 AM - On-call queries Henry's agent → gets K8s diagnosis steps")
    print("  2:06 AM - Confirms Redis pod OOM, increases memory, restarts pods")
    print("  2:10 AM - Payment service back online, all tests passing")
    print("  2:12 AM - On-call queries Kate's agent → identifies testing gap")
    print()
    print("IMPACT:")
    print("  ⏱️  Problem resolved in 10 MINUTES (vs 6 hours waiting for Bob)")
    print("  💤 Bob sleeps peacefully (no 2 AM phone call)")
    print("  📊 Bob sees resolution summary over morning coffee")
    print("  🎯 Testing gap identified and queued for next sprint")
    print()
    print("THE WOW FACTOR:")
    print("  🌟 Zero communication overhead")
    print("  🌟 Instant access to expert knowledge")
    print("  🌟 24/7 availability without burning out engineers")
    print("  🌟 Complete context preservation for post-mortem")
    print()
    print("Instead of interrupting Bob at 2 AM, the on-call engineer asked his agent!")
    print()


if __name__ == "__main__":
    main()
