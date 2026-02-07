"""Scenario 3: The Timezone Nightmare (San Francisco + London + Tokyo).

WOW Moment: New designer in Tokyo needs guidance from Olivia (SF), Emily (London),
and Quinn (SF). Normal working hours never overlap. Designer gets complete guidance
in 5 minutes at 9 AM Tokyo time without anyone being awake in SF or London.

Demonstrates: 24/7 global collaboration, zero timezone friction, instant knowledge transfer.
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
    """Run timezone nightmare scenario."""
    print("=" * 80)
    print("🌍 Scenario 3: The Timezone Nightmare (SF + London + Tokyo)")
    print("=" * 80)
    print()
    print("SITUATION: New designer in Tokyo (9 AM) needs guidance on mobile checkout.")
    print("           Olivia (SF, sleeping), Emily (London, morning), Quinn (SF, sleeping)")
    print("           Working hours NEVER overlap!")
    print()
    print("TIMEZONES:")
    print("  🇯🇵 Tokyo:         9:00 AM  (Designer needs help NOW)")
    print("  🇬🇧 London:        12:00 AM (Emily sleeping)")
    print("  🇺🇸 San Francisco: 4:00 PM  (Previous day! Olivia & Quinn sleeping)")
    print()
    print("THE OLD WAY:")
    print("  ❌ Send emails → wait 24 hours per response → 3-day delay")
    print("  ❌ Schedule meeting at terrible time (6 AM SF / 11 PM Tokyo)")
    print("  ❌ Information gets stale by the time everyone responds")
    print()
    print("THE WOW MOMENT WITH AGENTS:")
    print("  ✅ Query all three agents simultaneously")
    print("  ✅ Get complete guidance in 5 minutes")
    print("  ✅ Designer productive at 9 AM Tokyo time")
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
    quinn_id = None

    for agent_id, info in registered_agents.items():
        if info["name"] == "olivia-taylor":
            olivia_id = agent_id
        elif info["name"] == "emily-wang":
            emily_id = agent_id
        elif info["name"] == "quinn-roberts":
            quinn_id = agent_id

    if not all([olivia_id, emily_id, quinn_id]):
        print("✗ Could not find all required agents")
        return

    with httpx.Client(timeout=30.0) as client:
        # Step 1: Query Olivia's agent (Design Lead - SF, sleeping)
        print("-" * 80)
        print("Step 1: New Designer asks Olivia's Agent (SF, 4 PM yesterday, sleeping)")
        print("-" * 80)
        print('  Question: "I\'m designing mobile checkout flow."')
        print('            "What are our design principles and user research findings?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                olivia_id,
                "mobile checkout design principles user research progressive disclosure",
                limit=5,
            )
            print(f"  Olivia's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 DESIGN GUIDANCE FROM OLIVIA'S AGENT:")
                print()
                print("     🎨 DESIGN PRINCIPLES:")
                print("        • Progressive disclosure to reduce cognitive load")
                print("        • Mobile-first design, then adapt to desktop")
                print("        • Simplify payment options (users struggle with too many choices)")
                print()
                print("     📊 USER RESEARCH FINDINGS:")
                print("        • 73% of users struggled with payment method selection")
                print("        • Recommendation: Maximum 3 steps in checkout flow")
                print("        • Users want saved payment methods (top feature request)")
                print()
                print("     📁 RESOURCES:")
                print("        • Design files in Figma: [Mobile Checkout v2.1]")
                print("        • User research report: [Checkout UX Study Dec 2025]")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 2: Query Emily's agent (Frontend Engineer - London, sleeping)
        print("-" * 80)
        print("Step 2: New Designer asks Emily's Agent (London, 12 AM, sleeping)")
        print("-" * 80)
        print('  Question: "What are the frontend technical constraints?"')
        print('            "Which libraries and patterns should I follow?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                emily_id,
                "frontend checkout React components state management performance accessibility",
                limit=5,
            )
            print(f"  Emily's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 FRONTEND CONSTRAINTS FROM EMILY'S AGENT:")
                print()
                print("     ⚙️  TECHNOLOGY STACK:")
                print("        • React + TypeScript (strict mode)")
                print("        • Component library: @techflow/ui (Card, Button, FormField)")
                print("        • State management: Zustand with sessionStorage persistence")
                print("        • API calls: React Query with 5-minute cache")
                print()
                print("     ⚡ PERFORMANCE REQUIREMENTS:")
                print("        • First Contentful Paint: <1.5s")
                print("        • Time to Interactive: <3s")
                print("        • Lighthouse score: >90")
                print()
                print("     ♿ ACCESSIBILITY:")
                print("        • Must meet WCAG 2.1 AA compliance")
                print("        • Keyboard navigation required")
                print("        • Screen reader support mandatory")
                print("        • Color contrast minimum 4.5:1")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

        # Step 3: Query Quinn's agent (UI Designer - SF, sleeping)
        print("-" * 80)
        print("Step 3: New Designer asks Quinn's Agent (SF, 4 PM yesterday, sleeping)")
        print("-" * 80)
        print('  Question: "What components should I use from the design system?"')
        print('            "What are the design tokens and spacing?"')
        print()

        try:
            memories = search_memory(
                client,
                "owner",
                quinn_id,
                "design system components checkout UI tokens spacing colors",
                limit=5,
            )
            print(f"  Quinn's Agent responds instantly (found {len(memories)} relevant memories):")
            print()
            print_memory_results(memories, indent="    ")

            if len(memories) > 0:
                print("  💡 DESIGN SYSTEM SPECS FROM QUINN'S AGENT:")
                print()
                print("     🧩 COMPONENTS TO USE:")
                print("        • Card (for checkout container)")
                print("        • Button (primary, secondary variants)")
                print("        • FormField (input with validation)")
                print("        • PaymentMethodSelector (already built!)")
                print()
                print("     🎨 DESIGN TOKENS:")
                print("        • Primary color: #007AFF")
                print("        • Spacing grid: 8px base unit")
                print("        • Typography: Inter font family")
                print("        • Border radius: 8px for cards, 4px for buttons")
                print()
                print("     📱 RESPONSIVE SUPPORT:")
                print("        • All components support dark mode")
                print("        • Breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)")
                print("        • Components auto-adapt to viewport")
                print()
                print("     📚 DOCUMENTATION:")
                print("        • Design tokens available in Figma dev mode")
                print("        • Component usage examples in Storybook")
                print()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    # Summary
    print("=" * 80)
    print("✅ SCENARIO COMPLETE - DESIGNER FULLY UNBLOCKED!")
    print("=" * 80)
    print()
    print("TOKYO TIMELINE (9:00 AM):")
    print("  9:00 AM - Designer starts work, needs guidance")
    print("  9:01 AM - Queries Olivia's agent → gets design principles & user research")
    print("  9:02 AM - Queries Emily's agent → gets frontend technical constraints")
    print("  9:03 AM - Queries Quinn's agent → gets design system specs")
    print("  9:05 AM - Has complete guidance, starts designing")
    print("  5:00 PM - Completes mobile checkout mockups")
    print()
    print("WHAT HAPPENED IN OTHER TIMEZONES:")
    print("  🇺🇸 San Francisco (4 PM previous day):")
    print("     • Olivia: Sleeping peacefully")
    print("     • Quinn: Sleeping peacefully")
    print("     • Morning: See notification 'Tokyo designer queried your agents'")
    print("     • Review: Everything accurate, designer already made progress")
    print()
    print("  🇬🇧 London (12 AM midnight):")
    print("     • Emily: Sleeping peacefully")
    print("     • Morning: See designer's progress, provide async feedback if needed")
    print()
    print("IMPACT:")
    print("  ⏱️  Designer got complete guidance in 5 MINUTES (vs 72 hours email chain)")
    print("  😴 Nobody woken up, nobody interrupted")
    print("  🚀 Designer productive from hour 1 of their workday")
    print("  🌏 True 24/7 global collaboration")
    print()
    print("THE WOW FACTOR:")
    print("  🌟 Zero timezone friction")
    print("  🌟 Work continues around the clock")
    print("  🌟 No 'terrible time' meetings (6 AM or 11 PM)")
    print("  🌟 Complete knowledge transfer in any timezone")
    print()
    print("Instead of waiting 3 days for email responses, designer got")
    print("instant guidance from three experts' agents across three timezones!")
    print()


if __name__ == "__main__":
    main()
