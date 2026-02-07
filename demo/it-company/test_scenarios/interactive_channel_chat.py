"""Interactive CLI for testing channel chat API.

This script provides an interactive REPL interface for sending messages to
multiple agents simultaneously via the A4S channel chat API. It automatically
manages conversation history and includes context in subsequent queries.

Usage:
    uv run python interactive_channel_chat.py --channel-id <channel_id>
    uv run python interactive_channel_chat.py  # Interactive mode
"""

import argparse
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Self

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ConversationHistory:
    """Manages conversation history for context building."""

    def __init__(self, max_history: int = 10) -> None:
        """Initialize conversation history.

        Args:
            max_history: Maximum number of exchanges to keep in history
        """
        self._messages: list[dict[str, Any]] = []
        self._max_history = max_history

    def add_user_message(self, message: str) -> None:
        """Add user message to history.

        Args:
            message: User message text
        """
        self._messages.append({"role": "user", "content": message, "timestamp": datetime.now(UTC)})
        self._trim_history()

    def add_agent_responses(self, results: list[dict]) -> None:
        """Add agent responses to history.

        Args:
            results: List of agent response dictionaries from API
        """
        for result in results:
            if result.get("response"):
                self._messages.append(
                    {
                        "role": "agent",
                        "agent_id": result["agent_id"],
                        "agent_name": result["agent_name"],
                        "content": result["response"],
                        "timestamp": datetime.now(UTC),
                    }
                )
        self._trim_history()

    def _trim_history(self) -> None:
        """Trim history to max_history exchanges."""
        # Count user messages (exchanges)
        user_count = sum(1 for msg in self._messages if msg["role"] == "user")

        if user_count > self._max_history:
            # Remove oldest exchange (user message + all following agent responses)
            # until we're at max_history user messages
            while user_count > self._max_history:
                # Find first user message and remove it + subsequent agent responses
                # until the next user message
                first_user_idx = next(i for i, msg in enumerate(self._messages) if msg["role"] == "user")
                # Find next user message or end of list
                next_user_idx = next(
                    (i for i in range(first_user_idx + 1, len(self._messages)) if self._messages[i]["role"] == "user"),
                    len(self._messages),
                )
                # Remove messages from first_user_idx to next_user_idx (exclusive)
                del self._messages[first_user_idx:next_user_idx]
                user_count -= 1

    def format_for_context(self, new_query: str, include_context: bool = True) -> str:
        """Format message with conversation history.

        Args:
            new_query: New query to send
            include_context: Whether to include conversation history

        Returns:
            Formatted message with or without context
        """
        if not include_context or not self._messages:
            return new_query

        # Build context from history
        context_lines = ["Previous conversation:", "---"]

        for msg in self._messages:
            if msg["role"] == "user":
                context_lines.append(f"[User]: {msg['content']}")
            else:
                # Truncate long responses in context
                content = msg["content"]
                if len(content) > 300:
                    content = content[:297] + "..."
                context_lines.append(f"[{msg['agent_name']}]: {content}")

        context_lines.append("---")
        context_lines.append("")
        context_lines.append(f"New question: {new_query}")

        return "\n".join(context_lines)

    def clear(self) -> None:
        """Clear all conversation history."""
        self._messages.clear()

    def display(self) -> None:
        """Print formatted conversation history."""
        if not self._messages:
            print("No conversation history yet.")
            return

        print("\n" + "=" * 80)
        print("Conversation History")
        print("=" * 80 + "\n")

        for msg in self._messages:
            timestamp = msg["timestamp"].strftime("%H:%M:%S")
            if msg["role"] == "user":
                print(f"[{timestamp}] User:")
                print(f"  {msg['content']}\n")
            else:
                print(f"[{timestamp}] {msg['agent_name']} ({msg['agent_id']}):")
                print(f"  {msg['content']}\n")

        print("=" * 80 + "\n")

    def get_count(self) -> int:
        """Get number of exchanges in history.

        Returns:
            Number of user messages (exchanges) in history
        """
        return sum(1 for msg in self._messages if msg["role"] == "user")


class ChannelChatClient:
    """Client for channel chat API communication."""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", timeout: float = 60.0) -> None:
        """Initialize HTTP client.

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client: httpx.Client | None = None

    def __enter__(self) -> Self:
        """Context manager entry."""
        self._client = httpx.Client(timeout=self._timeout)
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        if self._client:
            self._client.close()

    def get_channel(self, channel_id: str) -> dict:
        """Fetch channel information from API.

        Args:
            channel_id: Channel ID

        Returns:
            Channel information dictionary

        Raises:
            httpx.HTTPStatusError: If API returns error status
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use context manager.")

        url = f"{self._base_url}/channels/{channel_id}"
        logger.info("Fetching channel info: %s", url)

        response = self._client.get(url)
        response.raise_for_status()

        return response.json()

    def send_chat(self, channel_id: str, message: str, agent_ids: list[str]) -> dict:
        """Send chat message to channel agents.

        Args:
            channel_id: Channel ID
            message: Message text (may include context)
            agent_ids: List of agent IDs to send to

        Returns:
            API response dictionary with results

        Raises:
            httpx.HTTPStatusError: If API returns error status
            httpx.TimeoutException: If request times out
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use context manager.")

        url = f"{self._base_url}/channels/{channel_id}/chat"
        payload = {"message": message, "agent_ids": agent_ids}

        logger.info("Sending chat to %d agents", len(agent_ids))

        response = self._client.post(url, json=payload)
        response.raise_for_status()

        return response.json()


class InteractiveChatCLI:
    """Interactive CLI for channel chat."""

    def __init__(
        self, channel_id: str | None = None, api_url: str = "http://localhost:8000/api/v1", include_context: bool = True
    ) -> None:
        """Initialize CLI.

        Args:
            channel_id: Channel ID to use (optional)
            api_url: API base URL
            include_context: Whether to include context in messages
        """
        self._channel_id = channel_id
        self._api_url = api_url
        self._channel_info: dict | None = None
        self._registered_agents: dict = {}
        self._selected_agent_ids: list[str] = []
        self._history = ConversationHistory()
        self._include_context = include_context
        self._client: ChannelChatClient | None = None
        self._running = True

    def run(self) -> None:
        """Main entry point - setup and start REPL loop."""
        try:
            with ChannelChatClient(self._api_url) as client:
                self._client = client

                if not self._setup():
                    return

                self._main_loop()

        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            print(f"\nError: {e}")
        finally:
            self._display_summary()

    def _setup(self) -> bool:
        """Load agents, validate channel, display welcome.

        Returns:
            True if setup successful, False otherwise
        """
        # Load registered agents
        agents_path = Path(__file__).parent.parent / "scripts" / "registered_agents.json"
        try:
            with agents_path.open() as f:
                self._registered_agents = json.load(f)
            logger.info("Loaded %d registered agents", len(self._registered_agents))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading registered agents: {e}")
            return False

        # Get channel ID if not provided
        if not self._channel_id:
            self._channel_id = input("Enter channel ID: ").strip()
            if not self._channel_id:
                print("No channel ID provided.")
                return False

        # Fetch and validate channel
        try:
            self._channel_info = self._client.get_channel(self._channel_id)
        except httpx.HTTPStatusError as e:
            print(f"Error fetching channel: {e.response.status_code} - {e.response.text}")
            return False
        except Exception as e:
            print(f"Error connecting to API: {e}")
            return False

        # Display welcome message
        print("\n" + "=" * 80)
        print("Interactive Channel Chat CLI")
        print("=" * 80)
        print(f"\nChannel: {self._channel_info['name']}")
        print(f"Description: {self._channel_info.get('description', 'N/A')}")
        print(f"Channel ID: {self._channel_id}")
        print(f"\nContext inclusion: {'enabled' if self._include_context else 'disabled'}")
        print("\nType /help for available commands, /quit to exit")
        print("=" * 80 + "\n")

        # Select agents
        self._select_agents()

        return True

    def _main_loop(self) -> None:
        """Main REPL loop - prompt, process, repeat."""
        while self._running:
            try:
                user_input = input("You> ").strip()

                if not user_input:
                    continue

                if not self._process_input(user_input):
                    break

            except KeyboardInterrupt:
                print()
                break
            except EOFError:
                print()
                break

    def _process_input(self, user_input: str) -> bool:  # noqa: C901, PLR0912
        """Process user input (command or message).

        Args:
            user_input: User input string

        Returns:
            True to continue loop, False to exit
        """
        # Check if it's a command
        if user_input.startswith("/"):
            command = user_input[1:].lower().split()[0]
            args = user_input[1:].split(maxsplit=1)[1] if " " in user_input else ""

            if command in ("quit", "exit", "q"):
                return False
            if command == "help":
                self._display_help()
            elif command == "agents":
                self._select_agents()
            elif command == "list":
                self._list_agents()
            elif command == "history":
                self._history.display()
            elif command == "clear":
                self._history.clear()
                print("Conversation history cleared.")
            elif command == "context":
                if args.lower() == "on":
                    self._include_context = True
                    print("Context inclusion enabled.")
                elif args.lower() == "off":
                    self._include_context = False
                    print("Context inclusion disabled.")
                else:
                    print(f"Context is currently {'enabled' if self._include_context else 'disabled'}.")
                    print("Usage: /context on|off")
            else:
                print(f"Unknown command: /{command}")
                print("Type /help for available commands.")
        else:
            # It's a message to send
            self._send_message(user_input)

        return True

    def _send_message(self, message: str) -> None:
        """Format with context, send to API, display responses, update history.

        Args:
            message: User message text
        """
        if not self._selected_agent_ids:
            print("No agents selected. Use /agents to select agents.")
            return

        try:
            # Format message with context
            formatted_message = self._history.format_for_context(message, self._include_context)

            # Send to API
            print(f"\nSending to {len(self._selected_agent_ids)} agent(s)...\n")
            response = self._client.send_chat(self._channel_id, formatted_message, self._selected_agent_ids)

            # Display responses
            results = response.get("results", [])
            self._display_responses(results)

            # Update history with original message (not formatted)
            self._history.add_user_message(message)
            self._history.add_agent_responses(results)

        except httpx.TimeoutException:
            print("Error: Request timed out. Please try again.")
        except httpx.HTTPStatusError as e:
            print(f"Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.exception("Error sending message: %s", e)
            print(f"Error: {e}")

    def _select_agents(self) -> None:
        """Prompt user to select agents (all or specific IDs)."""
        print("\nAvailable agents in this channel:\n")

        channel_agent_ids = self._channel_info.get("agent_ids", [])

        for agent_id in channel_agent_ids:
            agent_info = self._registered_agents.get(agent_id, {})
            name = agent_info.get("name", "Unknown")
            role = agent_info.get("role", "")
            description = agent_info.get("description", "")

            print(f"  {agent_id}")
            print(f"    Name: {name}")
            if role:
                print(f"    Role: {role}")
            if description:
                print(f"    Description: {description}")
            print()

        while True:
            selection = input("Select agents ('all' or comma-separated IDs): ").strip()

            if not selection:
                print("No selection made. Please try again.")
                continue

            try:
                self._selected_agent_ids = parse_agent_selection(selection, channel_agent_ids)
                print(f"\nSelected {len(self._selected_agent_ids)} agent(s).")
                break
            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.")

    def _list_agents(self) -> None:
        """Display available agents in channel."""
        print("\n" + "=" * 80)
        print("Available Agents in Channel")
        print("=" * 80 + "\n")

        channel_agent_ids = self._channel_info.get("agent_ids", [])

        for agent_id in channel_agent_ids:
            agent_info = self._registered_agents.get(agent_id, {})
            name = agent_info.get("name", "Unknown")
            role = agent_info.get("role", "")

            selected = " [SELECTED]" if agent_id in self._selected_agent_ids else ""
            print(f"  {agent_id}{selected}")
            print(f"    Name: {name}")
            if role:
                print(f"    Role: {role}")
            print()

        print("=" * 80 + "\n")

    def _display_responses(self, results: list[dict]) -> None:
        """Display agent responses with simple formatting.

        Args:
            results: List of agent response dictionaries
        """
        print("=" * 80)
        print(f"Agent Responses ({len(results)} agents)")
        print("=" * 80 + "\n")

        for result in results:
            agent_name = result.get("agent_name", "Unknown")
            agent_id = result.get("agent_id", "Unknown")
            response = result.get("response")
            error = result.get("error")

            print(f"[{agent_name} ({agent_id})]")

            if error:
                print(f"ERROR: {error}\n")
            elif response:
                print(f"{response}\n")
            else:
                print("No response\n")

        print("=" * 80 + "\n")

    def _display_help(self) -> None:
        """Show available commands."""
        print("\n" + "=" * 80)
        print("Available Commands")
        print("=" * 80 + "\n")
        print("  <message>          Send message to selected agents")
        print("  /agents            Change agent selection")
        print("  /list              List available agents in channel")
        print("  /history           Display conversation history")
        print("  /clear             Clear conversation history")
        print("  /context on|off    Toggle context inclusion in messages")
        print("  /help              Show this help message")
        print("  /quit or /exit     Exit the CLI")
        print("\n" + "=" * 80 + "\n")

    def _display_summary(self) -> None:
        """Display session summary."""
        print("\n" + "=" * 80)
        print("Session Summary")
        print("=" * 80)
        print(f"Messages sent: {self._history.get_count()}")
        print(f"Agents queried: {len(self._selected_agent_ids)}")
        print("=" * 80 + "\n")


def parse_agent_selection(input_str: str, channel_agent_ids: list[str]) -> list[str]:
    """Parse agent selection input.

    Args:
        input_str: User input string ('all' or comma-separated IDs)
        channel_agent_ids: Available agent IDs in channel

    Returns:
        List of selected agent IDs

    Raises:
        ValueError: If selection is invalid
    """
    input_str = input_str.strip().lower()

    if input_str == "all":
        return channel_agent_ids

    # Parse comma-separated IDs
    selected_ids = [agent_id.strip() for agent_id in input_str.split(",")]

    # Validate all IDs are in channel
    invalid_ids = [agent_id for agent_id in selected_ids if agent_id not in channel_agent_ids]
    if invalid_ids:
        raise ValueError(f"Invalid agent IDs: {', '.join(invalid_ids)}")

    if not selected_ids:
        raise ValueError("No agents selected")

    return selected_ids


def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="Interactive CLI for testing channel chat API")
    parser.add_argument(
        "--channel-id", "-c", type=str, help="Channel ID to use (optional, will prompt if not provided)"
    )
    parser.add_argument(
        "--api-url",
        "-u",
        type=str,
        default="http://localhost:8000/api/v1",
        help="API base URL (default: http://localhost:8000/api/v1)",
    )
    parser.add_argument("--no-context", action="store_true", help="Start with context disabled (default: enabled)")

    args = parser.parse_args()

    cli = InteractiveChatCLI(channel_id=args.channel_id, api_url=args.api_url, include_context=not args.no_context)
    cli.run()


if __name__ == "__main__":
    main()
