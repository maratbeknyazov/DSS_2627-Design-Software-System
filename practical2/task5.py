"""Practical Work 2 - Task 5: Requirements analysis."""

REQUIREMENTS = [
    ("FR-01", "The system shall allow a student to sign in with one university account."),
    ("FR-02", "The system shall show the menu for the current day with the price of every dish."),
    ("FR-03", "The system shall allow a student to add up to 5 dishes to one order."),
    ("FR-04", "The system shall allow payment by bank card or payment at the counter."),
    ("FR-05", "The system shall assign every order a number unique within that calendar day."),
    ("FR-06", "The system shall show every confirmed order on the kitchen screen within 5 seconds."),
    ("FR-07", "The system shall allow kitchen staff to mark an order as ready."),
    ("FR-08", "The system shall notify the student within 10 seconds after the order is marked ready."),
    ("FR-09", "The system shall allow cancellation only while an order has the status Not started."),
    ("FR-10", "The system shall produce a daily report of portions sold for every dish and total revenue."),
    ("NFR-01 Performance", "The menu page shall load within 2 seconds for 1,000 simultaneous students on university Wi-Fi."),
    ("NFR-02 Security", "Payment data shall use TLS 1.3, and card numbers and CVVs shall not be stored by the cafeteria system."),
    ("NFR-03 Usability", "The interface shall be available in Uzbek, Russian, and English."),
    ("NFR-04 Reliability", "Downtime shall not exceed 10 minutes during one working day from 08:00 to 18:00."),
    ("NFR-05 Maintainability", "An authorized manager shall add a dish category through the admin screen without changing source code."),
    ("NFR-06 Portability", "Student ordering functions shall work in the two latest major versions of Chrome and Safari and on university tablets."),
]

TECHNIQUES = [
    ("Interview", "Cafeteria manager, cashier, and cook", "Payment rules, kitchen workflow, reporting needs, and exceptions."),
    ("Questionnaire", "300-500 students", "Expected usage, preferred payment method, languages, and notification preferences."),
    ("Observation", "Cafeteria during two busy breaks", "Actual queue time, bottlenecks, collection process, and peak order volume."),
    ("Document analysis", "Menus, price lists, receipts, and daily cash reports", "Dish categories, prices, taxes, sales fields, and reconciliation rules."),
    ("Prototyping", "10 students and 3 staff members", "Whether ordering, kitchen, and manager screens are understandable before coding."),
]

FIRST_TECHNIQUE = (
    "Observation should be used first. It reveals the real peak-time workflow and "
    "bottlenecks without relying on memory, so later interviews can ask precise questions."
)

QUESTIONS = [
    "What happens to a paid order that the student never collects?",
    "When is a refund allowed and how long may it take?",
    "How are allergies and ingredients shown and confirmed?",
    "Who may change prices, dishes, and the number of available portions?",
    "What should happen when the internet or payment provider is unavailable?",
]

SELF_CHECK = {
    "FR-01": ["yes", "yes", "yes", "yes", "yes", "yes"],
    "FR-06": ["yes", "yes", "yes", "yes", "yes", "yes"],
    "NFR-01": ["yes", "yes", "yes", "yes", "yes", "yes"],
}


def main():
    print("TASK 5 - REQUIREMENTS ANALYSIS\n")
    print("5.1 Requirements list")
    for req_id, text in REQUIREMENTS:
        print(f"{req_id}: {text}")

    print("\n5.2 Collection techniques")
    for technique, source, learning in TECHNIQUES:
        print(f"{technique}\n  From: {source}\n  Learn: {learning}")
    print(f"\nFirst technique: {FIRST_TECHNIQUE}")

    print("\n5.3 Questions the customer did not answer")
    for number, question in enumerate(QUESTIONS, 1):
        print(f"{number}. {question}")

    print("\n5.4 Self-check")
    columns = ["Clear", "Testable", "Complete", "Consistent", "Necessary", "Traceable"]
    print("ID       " + " | ".join(columns))
    for req_id, answers in SELF_CHECK.items():
        print(f"{req_id:<8} " + " | ".join(answers))
    print("\nNo correction is required because every selected requirement satisfies all six properties.")


if __name__ == "__main__":
    main()
