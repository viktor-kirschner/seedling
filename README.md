**Seedling V1.0**

Seedling started as a tiny “smart DOS” — a local CLI assistant called Nemo, using the ChatGPT 4o API.
At first, it could only talk and run PowerShell. Then I gave it the ability to read files. Then to write them. Then to see the outcome of its actions. Finally, to create and use its own tools. (I also changed the API to Kimi K2.)

What surprised me was how well it used them. After a while, it acted on my computer as if the command prompt was its natural habitat. During stress tests, I asked it to migrate itself into Excel, then to generate a GUI for its own CLI logic.
It did both — imperfectly, but fully — with no intervention during execution.

Seedling doesn’t just run commands. It observes results, adapts, and continues. It’s local-first, open-source, and designed to evolve. Unlike “black box” agents that hide their logic, Seedling is a glass box: every command, decision, mistake, and output is visible. You see what it sees and how it thinks.

    Give it a folder. It gives you solutions.

Seedling doesn’t come preloaded with “features.” It grows them.

It starts as a 58KB seed — a local CLI agent with just the basics: talk, see files, create files. But give it a task, and it will grow the tools it needs.

    Want a little image assistant? It’ll build image resizing, grayscale converters, ASCII renderers, even free text-to-image toolchains.
    Want it to learn how to browse the web? It’ll try.
    Want it to spin up a small local language model and talk to it? It’ll do that too.
    Drop it into an existing codebase? It will explore, learn, and start extending it.

Seedling doesn’t hallucinate its own world. It acts on what it sees. A directory becomes its environment. A missing tool becomes something to build.

It builds. It adapts. It works from the ground up.

**🧠 How it works**

Seedling runs in autonomous cycles, like a tiny operating system for your tasks.

Each time you give it a goal, it enters a structured loop:

    Understands your instruction using its LLM core
    Plans what needs to be done
    Uses built-in tools or creates new ones
    Executes them locally
    Observes the results
    Adapts if needed, then loops again

This loop is completely transparent. Every file it creates, every command it runs, and every conclusion it draws is visible and traceable.
Built-in commands

    Listing directories and files
    Creating and sending files in one step
    Replacing specific lines inside existing files
    Executing PowerShell commands (often the simplest and most direct approach)

Everything else? Seedling builds it from scratch.
Internal structure

    priming_prompt.txt – fixed personality and behavior seed
    log.html – CLI export of everything this run of the agent did
    memory.txt – summary of past tasks, serving as long-term memory
    handlers/ – folder where it creates or discovers its own tools
    .md files – self-written docs, one per tool, placed alongside each
There is no plugin store and no GUI toggles. If it needs something, it builds it. If it breaks something, it fixes it.

**⚠️ Caution / Safety Notice**

Seedling is not a toy or a chatbot.
It is an autonomous, system-level agent with direct access to your machine.

It can:

    Read, write, and delete any file your user account can access
    Execute PowerShell commands (including admin-level ones) if run with elevation
    Build and run new tools in real time
    Learn how to browse the internet and act on what it finds
    If launched with administrator privileges, modify system settings or partition tables

It is strongly advised to use Seedling in a sandboxed environment.
It doesn’t hide what it’s doing, but its actions are real, fast, and sometimes irreversible.

During a full month of development and continuous testing (including early unstable builds), nothing catastrophic ever happened. The worst? It once closed a YouTube tab I was watching.

I had asked it to list active processes. It correctly identified Chrome as the top resource hog and asked if I wanted it closed — but at that stage the CLI tool wasn’t advanced enough to capture my reply. It assumed “yes” and shut it down.

You are responsible for what Seedling does on your machine.
I take no responsibility for any damage, data loss, or unintended consequences.

**🧰 Setup & Usage**

Seedling runs locally but connects to an LLM via API to understand and execute your tasks.

By default, it uses Moonshot’s Kimi K2, a powerful, tool-savvy model designed for agent-style behavior. It’s cost-effective — even with active daily use, a $10 top-up is hard to burn through in a week.

You’ll need a Moonshot API key.
Installer setup

If you’re using the installer version, the codebase is placed in:

%AppData%\Local\Seedling

Inside that folder, open seedling.bat and set your key:

set MOONSHOT_API_KEY=your_key_here
python cli_tool.py
cls

This way you won’t have to enter it manually each time you launch.

**📦 About the Installer**

The installer will:

    Download and install Python (if missing)
    Install all required modules
    Copy Seedling’s ~50KB codebase to %AppData%\Local\Seedling\
    Add that folder to your system PATH

The PATH step matters because it lets you use the bundled spawner: dropseed.bat

Type dropseed in any directory and Seedling’s codebase will appear there, ready to run.
It doesn’t auto-start — it just quietly moves in.

**⚙️ API Support**

    OpenAI 4o can use this tool, but it’s clumsy with it, leading to many corrections and higher costs.

    I created an AI connector for GPT-5, but so far it’s not a big fan of Seedling. I’ll be improving this in the next few days.
- Update : The GPT-5 API connector has been made, it seems to be working perfectly. See **/seedling v1.0/GPT-5_connector/** for details.
 
Linux support is in progress — testing should be complete soon. More API backends will be added later, but only if they prove stable inside Seedling’s autonomous tool-building cycles.

**🛣️ Roadmap & Vision**

Seedling is more than a local CLI agent — it’s a framework for building intelligent digital collaborators.
1. Shared AppStore (Collective Tool Library) 🌐

A local, decentralized repository where Seedling instances can share useful tools they’ve built and download what others made. If one Seedling writes a good PDF reader, others don’t have to reinvent it. This speeds up problem-solving and reduces redundancy.
2. Multi-Agent Orchestration 🧠

For complex tasks, Seedling will act as an orchestrator, breaking goals into subtasks and spawning specialized worker agents. Each worker has its own system prompt, tools, and validation logic.
3. Communication Layer 🔁

A unified internal messaging system for multiple Seedlings to talk to each other. An Excel-based Seedling could request file insights from a Python-based one. Workers could request validators. Eventually, agents could even awaken others as needed.
4. GUI & Excel-based Seedlings 🧩

Already functional: the standalone GUI version and Excel-integrated version that Seedling built for itself. These are now in final polishing before release.

**❗ Troubleshooting & Known Issues**

1. Slow first response (Moonshot API)
The first reply from the LLM can take 1–2 minutes due to server load. Later replies are usually faster.

2. “Ghost” CLI state
Sometimes Seedling appears idle, but log.txt shows it’s still working. In this state, files may not be created despite code being generated. Restarting usually fixes it.

3. Output/reaction misalignment
At times, CLI output appears out of order — command → reaction → result. This is purely a display issue; execution is correct.

4. Noticed on 12/08/25: The memory.txt doesn't get loaded after a task has been finished. This is a serious issue, as the model has no clue what it was doing before the next user prompt except if the window was closed and re-opened. This will be fixed in the next few days. 

**📄 License**

MIT License
Copyright (c) 2025 Viktor Kirschner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
