# Multi-Agent Channel Demo

## How to use channel chat via CLI

The interactive channel chat CLI allows you to send messages to multiple agents simultaneously and see their responses in real-time.

### Starting the CLI

```bash
# Interactive mode - will prompt for channel ID
uv run python demo/it-company/test_scenarios/interactive_channel_chat.py

# Specify channel ID directly
uv run python demo/it-company/test_scenarios/interactive_channel_chat.py --channel-id <channel_id>

# Use custom API URL
uv run python demo/it-company/test_scenarios/interactive_channel_chat.py --api-url http://localhost:8000/api/v1
```

### Basic Usage

1. **Select agents**: When prompted, choose which agents to query:
   - Type `all` to select all agents in the channel
   - Or enter comma-separated agent IDs (e.g., `alice,bob,kate`)

2. **Send messages**: Simply type your message and press Enter
   - The CLI automatically includes conversation history for context
   - All selected agents will receive and respond to your message

3. **Use commands**: Type `/help` to see available commands:
   - `/agents` - Change agent selection
   - `/list` - List available agents in channel
   - `/history` - Display conversation history
   - `/clear` - Clear conversation history
   - `/context on|off` - Toggle context inclusion in messages
   - `/quit` or `/exit` - Exit the CLI

## 5 WOW Moment Scenarios

### Core Value Proposition

**Instead of interrupting busy people, ask their AI agent "second-me"**

Each agent is a digital twin of an employee containing:

- All their knowledge and expertise
- Their work patterns and preferences
- Their current projects and context
- Their past decisions and rationale

**Result**: Zero communication overhead, instant answers, 24/7 availability

### Scenario 1: 🚨 The 2 AM Production Fire

**The Problem**: Payment service crashes at 2 AM. Bob (the engineer who knows it best) is asleep. The on-call engineer needs answers NOW.

**The Old Way**:

- Wake Bob up at 2 AM → ruins his sleep
- Wait until morning → customers can't checkout for 6 hours
- Dig through documentation → incomplete and outdated

**The WOW Moment**:
On-call engineer queries Bob's, Henry's, and Kate's agents:

- Gets payment service architecture and recent changes from Bob's agent
- Gets Kubernetes diagnosis steps from Henry's agent
- Gets testing gap analysis from Kate's agent
- **Problem diagnosed and fixed in 10 minutes vs 6 hours**
- **Bob sleeps peacefully, sees resolution summary over coffee**

**Impact**: 36x faster incident resolution, zero engineers woken up

---

### Scenario 2: 👔 The CEO Needs an Answer

**The Problem**: CEO needs technical update on payment migration. Alice (Backend Manager) is in meetings from 9 AM to 5 PM.

**The Old Way**:

- CEO waits until Alice is free → decision delayed by 8 hours
- Alice interrupted mid-meeting → loses focus, meeting derailed
- Play phone tag → takes 3 days to connect

**The WOW Moment**:
CEO queries Alice's and Henry's agents:

- Gets comprehensive project status (40% complete, on track for March 15)
- Gets progress breakdown, risks, and next steps from Alice's agent
- Gets DevOps support confirmation from Henry's agent
- **Complete answer in 30 seconds vs 3 days**
- **Alice stays focused in meetings, no context switching**

**Impact**: 8,640x faster executive decisions, managers preserve deep work

---

### Scenario 3: 🌍 The Timezone Nightmare

**The Problem**: New designer in Tokyo (9 AM) needs guidance from Olivia (SF, sleeping), Emily (London, sleeping), and Quinn (SF, sleeping). Working hours NEVER overlap.

**The Old Way**:

- Send emails → wait 24 hours per response → 3-day delay
- Schedule meeting at terrible time (6 AM SF / 11 PM Tokyo)
- Information gets stale by the time everyone responds

**The WOW Moment**:
Designer in Tokyo queries three agents simultaneously:

- Gets design principles and user research from Olivia's agent (SF, sleeping)
- Gets frontend constraints from Emily's agent (London, sleeping)
- Gets design system specs from Quinn's agent (SF, sleeping)
- **Complete guidance in 5 minutes at 9 AM Tokyo time**
- **Nobody woken up or interrupted**

**Impact**: 864x faster cross-timezone collaboration, true 24/7 work

---

### Scenario 4: 🎯 The New Hire's First Week

**The Problem**: New backend engineer David's first day. Has 50 questions but everyone is busy. Doesn't want to seem annoying.

**The Old Way**:

- Interrupt Alice 15 times → she can't get her work done
- Documentation is outdated → wastes days following wrong info
- Afraid to ask "dumb questions" → makes mistakes causing production issues
- Takes 3 months to ramp up

**The WOW Moment**:
David queries agents unlimited times without social anxiety:

- Gets team standards from Alice's agent
- Gets payment service architecture from Bob's agent
- Gets deployment workflow from Henry's agent
- Gets testing requirements from Kate's agent
- **Productive from day 1, submits first PR in 5 hours**
- **Team productivity unaffected (zero interruptions)**

**Impact**: 3x faster ramp-up (1 month vs 3 months), no social anxiety

---

### Scenario 5: 💡 The Lightning-Fast Decision

**The Problem**: Product Manager Maya needs input from Design, Engineering, QA, and Marketing to decide on a feature. Scheduling a meeting with 5 people takes a week.

**The Old Way**:

- Email chain with 5 people → takes 3 days, messy thread
- Schedule meeting → earliest slot is next week
- By meeting time, context is stale and decision is late

**The WOW Moment**:
Maya queries 5 agents simultaneously about "saved payment methods" feature:

- Design effort: LOW (3 days) - Olivia's agent
- Frontend: MEDIUM (5 days) - Emily's agent
- Backend: LOW (3 days) - Bob's agent
- QA scope: MEDIUM (4 days) - Kate's agent
- Customer value: HIGH (top request!) - Rachel's agent
- **Decision made in 10 minutes vs 9 days**
- **All stakeholders consulted, nobody interrupted**

**Impact**: 77,760x faster decisions (9 days → 10 minutes), meeting-free
