"""Practical Work 2 - Task 4: Rewrite the bad requirements."""

REQUIREMENTS = [
    {
        "id": "NFR-01",
        "requirement": "The menu page shall load within 2 seconds for at least 1,000 simultaneous students on the university Wi-Fi.",
        "test": "Open the page with a 1,000-user load test and verify that every response is at most 2 seconds.",
    },
    {
        "id": "NFR-02",
        "requirement": "A first-year student shall find and add a dish to an order in no more than 3 clicks after opening the menu.",
        "test": "Ask 5 first-year students to add a named dish and count clicks; each student must use no more than 3 clicks.",
    },
    {
        "id": "NFR-03",
        "requirement": "The system shall support at least 2,000 registered students and 1,000 simultaneous active sessions.",
        "test": "Create 2,000 accounts, run 1,000 sessions, and verify successful menu and order operations.",
    },
    {
        "id": "NFR-04",
        "requirement": "The system shall transmit payment data only through TLS 1.3 and shall store no card number or CVV in the cafeteria database.",
        "test": "Inspect network traffic during a payment and search every database field for the card number and CVV.",
    },
    {
        "id": "FR-11",
        "requirement": "The system shall show a paid order on the kitchen screen within 5 seconds after payment confirmation.",
        "test": "Pay for 10 orders and verify that every order appears on the kitchen screen within 5 seconds.",
    },
    {
        "id": "FR-12",
        "requirement": "The system shall produce by 18:05 a daily report containing total orders, portions sold for every dish, and total revenue in soum.",
        "test": "Place 10 known orders, generate the report after 18:00, and compare all totals with the orders.",
    },
]


def main():
    print("TASK 4 - REWRITTEN REQUIREMENTS\n")
    for item in REQUIREMENTS:
        print(f"{item['id']}  {item['requirement']}")
        print(f"Test: {item['test']}\n")


if __name__ == "__main__":
    main()
