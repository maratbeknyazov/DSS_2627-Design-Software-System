"""Practical Work 2 - Task 2: The cost of a late mistake."""

CHANGES_DURING_TESTING = [
    "Correct the SRS threshold from 5,000,000 soum to 500,000 soum and review related rules.",
    "Change the delivery-fee calculation in the source code and unit tests.",
    "Update test cases, expected results, interface messages, and help text; then repeat regression testing.",
]

IRREPARABLE_DAMAGE = (
    "Customer trust and the shop's reputation can be damaged. Customers who were "
    "charged incorrectly may stop using the shop even after refunds are issued."
)

CHEAPEST_PHASE = (
    "The mistake should be caught during requirement gathering and requirements review "
    "at a relative cost of 1. The analyst should read the numeric rule back to the "
    "customer and compare the approved SRS with the interview notes."
)


def main():
    print("TASK 2 - THE COST OF A LATE MISTAKE\n")
    print("2.1 Changes required during testing:")
    for index, change in enumerate(CHANGES_DURING_TESTING, 1):
        print(f"{index}. {change}")
    print(f"\n2.2 Damage money cannot repair:\n{IRREPARABLE_DAMAGE}")
    print(f"\n2.3 Cheapest phase:\n{CHEAPEST_PHASE}")


if __name__ == "__main__":
    main()
