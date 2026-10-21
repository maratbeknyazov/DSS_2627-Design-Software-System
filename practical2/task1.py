"""Practical Work 2 - Task 1: The six SDLC phases."""

PHASES = [
    (1, "Requirement gathering", "SRS document signed by the customer",
     "The team may build functions users did not ask for and miss essential rules."),
    (2, "Feasibility study", "A report stating whether the project is approved",
     "The university may start a project that is too expensive, too slow, technically impossible, or unlawful."),
    (3, "Design", "HLD and LLD documents",
     "Developers may create incompatible modules, weak data structures, and an unsuitable interface."),
    (4, "Coding", "Source code and unit tests",
     "There will be no executable system to test or deploy."),
    (5, "Testing", "Test report and list of defects",
     "Payment, ordering, and load defects may reach students and cafeteria staff."),
    (6, "Deployment and maintenance", "Working system and a user manual",
     "Users cannot use the product reliably, and defects or changing needs remain unresolved."),
]


def main():
    print("TASK 1 - THE SIX PHASES\n")
    for number, phase, output, consequence in PHASES:
        print(f"{number}. {phase}")
        print(f"   Output: {output}")
        print(f"   If skipped: {consequence}\n")


if __name__ == "__main__":
    main()
