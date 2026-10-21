"""Practical Work 2 - Task 3: Functional or non-functional."""

CLASSIFICATION = [
    (1, "F", None, "Shows the current menu."),
    (2, "N", "Performance", "Defines response time and concurrent load."),
    (3, "F", None, "Provides card payment."),
    (4, "N", "Security", "Protects card data."),
    (5, "F", None, "Sends a ready notification."),
    (6, "N", "Usability", "Specifies supported interface languages."),
    (7, "F", None, "Creates a unique daily order number."),
    (8, "N", "Portability", "Specifies supported browsers and devices."),
    (9, "F", None, "Shows unprepared orders."),
    (10, "N", "Reliability", "Limits downtime."),
    (11, "F", None, "Provides sales totals by dish."),
    (12, "N", "Maintainability", "Limits the effect of a future change."),
]


def main():
    print("TASK 3 - FUNCTIONAL OR NON-FUNCTIONAL\n")
    for number, requirement_type, quality, reason in CLASSIFICATION:
        result = requirement_type
        if quality:
            result += f" ({quality})"
        print(f"{number}. {result}: {reason}")


if __name__ == "__main__":
    main()
