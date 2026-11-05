"""
What my criteria run against. run_eval.py runs everything here three times.

Criteria 4 (appeals) and 5 (bad input, incl. a non-JSON body) can't be sent as
plain texts or JSON bodies, so they run in criteria_extra.py instead.
"""

# ── Ten pieces I actually wrote myself (100+ words each) ─────────────────────
MY_WRITING = [
    "sometimes some classes are really hard for some and easy for other, and there are some classes that are really easy and hard for others",
    "The presentation in class needs to be professonal and everyone should be in formal attire",
    "Hello Professor, I wanted to let you know that I had missed the assignment 1 deadline and wanted to ask if there is any way the assignment deadline can be extended for 2 days. I am really sorry for not turning the work in on time and I promise that I will subit all of the next assignments on time.",
    "Once upon a time there was a girl called sofia, who was a princess and was really cute. she used to love purple dress and cakes.",
    "I believe phones should not be allowed in classrooms because they distract when you get a single notification and then it gets hard to focus in class",
    "Computer Scince is a pretty hard and competitive field which is growing really fast these days",
    "winters are really cold and when there's ice then you can barely walk on it without falling.",
    "Summer is really hot and humid",
    "Python is a simple language which is not too hard but for new learners it can be a bit hard to understand new stuff but once you understand python you can understand other languages easily.",
    "banana bread is better than banana",
]

CLEARLY_AI = (
    "The importance of effective time management cannot be overstated in today's "
    "fast-paced work environment. Professionals who develop strong organizational "
    "habits are better positioned to meet deadlines and reduce stress. There are "
    "several key strategies that can help individuals improve their productivity. "
    "First, prioritization is essential. By identifying the most important tasks and "
    "addressing them first, workers can ensure that critical objectives are met. "
    "Second, minimizing distractions plays a significant role. Setting aside "
    "dedicated blocks of time for concentrated work is widely considered beneficial. "
    "Finally, regular breaks are important for maintaining performance."
)

CLEARLY_HUMAN = (
    "I didn't sleep. Not properly, anyway — I lay there listening to the boiler tick "
    "and thinking about the thing I'd said to Marcus at the pub, which was stupid, "
    "and which he will absolutely bring up again. Twice now. So: coffee, and the long "
    "way round to work, and a plan. The plan lasted until about ten past nine, when "
    "Priya asked how the weekend was and I said \"fine\" in the voice that means it "
    "wasn't, and she put her mug down and looked at me. That's the trouble with "
    "Priya. She notices."
)

BORDERLINE = (
    "Time management matters more than people admit, especially now that work moves "
    "as fast as it does. If you're organised you hit deadlines, and you're less "
    "frazzled doing it. A few things actually help. Prioritise — work out what "
    "genuinely matters and do that first. Cut the interruptions; notifications wreck "
    "focus and the damage is worse than it feels at the time. And take breaks, short "
    "ones, often."
)

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },
    {
        "name": "score spread",
        "criterion": 2,
        # order matters for reading the result: ai, human, borderline
        "texts": [CLEARLY_AI, CLEARLY_HUMAN, BORDERLINE],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [CLEARLY_AI, CLEARLY_HUMAN, BORDERLINE] + MY_WRITING[:7],
    },
]


def validate() -> list[str]:
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")
        texts = scenario.get("texts")
        bodies = scenario.get("bodies")
        if texts and bodies:
            problems.append(f"scenario {i} has both texts and bodies")
            continue
        if bodies:
            continue
        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue
        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(f"scenario {i}, text {j} is empty")
            elif str(text).startswith("REPLACE ME"):
                problems.append(f"scenario {i} ('{scenario['name']}'), text {j} is still the placeholder")
    return problems