# My AI Adoption Journey

- **Author**: Mitchell Hashimoto (Ghostty / ex-HashiCorp)
- **Date**: 2026-02-05
- **Source**: <https://mitchellh.com/writing/my-ai-adoption-journey>
- **Via**: HN Top Blogs RSS (#13)

---

My experience adopting any meaningful tool is that I've necessarily gone through three phases: (1) a period of inefficiency (2) a period of adequacy, then finally (3) a period of workflow and life-altering discovery.

In most cases, I have to force myself through phase 1 and 2 because I usually have a workflow I'm already happy and comfortable with. Adopting a tool feels like work, and I do not want to put in the effort, but I usually do in an effort to be a well-rounded person of my craft.

## Step 1: Drop the Chatbot

Immediately cease trying to perform meaningful work via a chatbot (e.g. ChatGPT, Gemini on the web, etc.). Chatbots have real value and are a daily part of my AI workflow, but their utility in coding is highly limited because you're mostly hoping they come up with the right results based on their prior training, and correcting them involves a human (you) to tell them they're wrong repeatedly. It is inefficient.

My first "oh wow" moment was pasting a screenshot of Zed's command palette into Gemini, asking it to reproduce it with SwiftUI, and being truly flabbergasted that it did it very well. The command palette that ships for macOS in Ghostty today is only very lightly modified from what Gemini produced for me in seconds.

But when I tried to reproduce that behavior for other tasks, I was left disappointed. In the context of brownfield projects, I found the chat interface produced poor results very often.

**To find value, you must use an agent.** An agent is the industry-adopted term for an LLM that can chat and invoke external behavior in a loop. At a bare minimum, the agent must have the ability to: read files, execute programs, and make HTTP requests.

## Step 2: Reproduce Your Own Work

I tried Claude Code. I initially wasn't impressed. I felt I had to touch up everything it produced and this process was taking more time than if I had just done it myself.

Instead of giving up, I forced myself to reproduce all my manual commits with agentic ones. I literally did the work twice. I'd do the work manually, and then I'd fight an agent to produce identical results in terms of quality and function.

This was excruciating, because it got in the way of simply getting things done. But expertise formed. I quickly discovered:

1. Break down sessions into separate clear, actionable tasks. Don't try to "draw the owl" in one mega session.
2. For vague requests, split the work into separate planning vs. execution sessions.
3. If you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions.

The negative space here is worth reiterating: **part of the efficiency gains here were understanding when NOT to reach for an agent.** Using an agent for something it'll likely fail at is obviously a big waste of time.

## Step 3: End-of-Day Agents

Block out the last 30 minutes of every day to kick off one or more agents. Instead of trying to do more in the time I have, try to do more in the time I don't have.

Categories of work that were really helpful:
- **Deep research sessions** — survey some field, find all libraries with specific license type, produce multi-page summaries.
- **Parallel agents attempting different vague ideas** — illuminate unknown unknowns when I got to the task the next day.
- **Issue and PR triage/review** — agents using `gh` CLI to triage issues. I would NOT allow agents to respond, just wanted reports the next day.

## Step 4: Outsource the Slam Dunks

I had really high confidence with certain tasks that the AI would achieve a mostly-correct solution. So: let agents do all of that work while I worked on other tasks.

**Very important**: turn off agent desktop notifications. Context switching is very expensive. It was my job as a human to be in control of when I interrupt the agent, not the other way around. During natural breaks, tab over and check.

The thing I liked the most was that I could now **focus my coding and thinking on tasks I really loved** while still adequately completing the tasks I didn't.

## Step 5: Engineer the Harness

Agents are much more efficient when they produce the right result the first time. The most sure-fire way to achieve this is to give the agent fast, high quality tools to automatically tell it when it is wrong.

I've grown to calling this **"harness engineering."** Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

Two forms:
1. **Better implicit prompting (AGENTS.md)** — For simple things, like the agent repeatedly running wrong commands. [Example from Ghostty](https://github.com/ghostty-org/ghostty/blob/ca07f8c3f775fe437d46722db80a755c2b6e6399/src/inspector/AGENTS.md).
2. **Actual, programmed tools** — Scripts to take screenshots, run filtered tests, etc.

## Step 6: Always Have an Agent Running

Operating under the goal of having an agent running at all times. If an agent isn't running, I ask myself "is there something an agent could be doing for me right now?"

I'm not [yet?] running multiple agents. Having one agent running is a good balance between doing deep, manual work I find enjoyable, and babysitting my kind of stupid and yet mysteriously productive robot friend.

Currently effective at having a background agent running 10 to 20% of a normal working day, actively working to improve that.

## Today

Through this journey, I've personally reached a point where I'm having success with modern AI tooling and I believe I'm approaching it with the proper measured view that is grounded in reality. I'm a software craftsman that just wants to build stuff for the love of the game.

> The skill formation issues particularly in juniors without a strong grasp of fundamentals deeply worries me, however.

> I don't work for, invest in, or advise any AI companies.
