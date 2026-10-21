from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

OUT = Path("output/pdf")
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.black, spaceAfter=10))
styles.add(ParagraphStyle(name="Meta", parent=styles["Normal"], fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=colors.black, spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=colors.black, spaceBefore=9, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12, spaceAfter=5))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.6, leading=9.4))
styles.add(ParagraphStyle(name="SmallBold", parent=styles["Small"], fontName="Helvetica-Bold"))

def P(text, style="Bodyx"):
    return Paragraph(str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), styles[style])

def rawp(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def title(story, name, subtitle):
    story += [P(name, "DocTitle"), P(subtitle, "Meta"), P("Student: Albert Muratbaev", "Meta"), Spacer(1, 7*mm)]

def h1(story, text): story.append(P(text, "H1x"))
def h2(story, text): story.append(P(text, "H2x"))
def para(story, text): story.append(P(text))
def bullet(story, text): story.append(rawp("&#8226; " + text, "Bodyx"))

def tbl(story, rows, widths=None, font=7.3, header=True):
    data = [[P(c, "SmallBold" if header and r == 0 else "Small") for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    ts = [
        ("GRID", (0,0), (-1,-1), 0.45, colors.HexColor("#D9D9D9")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]
    if header:
        ts += [("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DCE6F1")), ("TEXTCOLOR", (0,0), (-1,0), colors.black)]
    for r in range(1 if header else 0, len(rows)):
        if r % 2 == 0: ts.append(("BACKGROUND", (0,r), (-1,r), colors.HexColor("#F7F9FC")))
    t.setStyle(TableStyle(ts)); story += [t, Spacer(1, 3*mm)]

def doc(path, story):
    def footer(canvas, d):
        canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#666666"));
        canvas.drawRightString(A4[0]-16*mm, 10*mm, f"Page {d.page}"); canvas.restoreState()
    SimpleDocTemplate(str(path), pagesize=A4, rightMargin=14*mm, leftMargin=14*mm, topMargin=14*mm, bottomMargin=16*mm,
                      title=path.stem, author="Albert Muratbaev").build(story, onFirstPage=footer, onLaterPages=footer)

def practical():
    s=[]; title(s, "Practical Work 2", "Software Development Life Cycle and Requirements")
    h1(s,"Task 1 The six phases")
    rows=[["No.","Phase","Correct output","What goes wrong if skipped"],
    ["1","Requirement gathering","SRS document signed by the customer","The team may build functions that users did not ask for and miss essential rules."],
    ["2","Feasibility study","A report stating whether the project is approved","The university may start a project that is too expensive, too slow, technically impossible or unlawful."],
    ["3","Design","HLD and LLD documents","Developers may create incompatible modules, weak data structures and an interface that does not support the workflow."],
    ["4","Coding","Source code and unit tests","There is no executable system to test or deploy."],
    ["5","Testing","Test report and list of defects","Payment, ordering and load defects may reach students and cafeteria staff."],
    ["6","Deployment and maintenance","Working system and a user manual","Users cannot use the product reliably, and defects or changing needs remain unresolved."]]
    tbl(s,rows,[9*mm,31*mm,45*mm,93*mm])
    h1(s,"Task 2 The cost of a late mistake")
    h2(s,"2.1 Changes required during testing")
    bullet(s,"Correct the threshold in the SRS from 5,000,000 soum to 500,000 soum and review related rules.")
    bullet(s,"Change the delivery-fee calculation in the source code and unit tests.")
    bullet(s,"Update test cases, expected results, user-interface messages and any help text that shows the wrong threshold; then repeat regression testing.")
    h2(s,"2.2 Damage money cannot repair")
    para(s,"Customer trust and the shop's reputation can be damaged. Customers who were charged incorrectly may stop using the shop even after refunds are issued.")
    h2(s,"2.3 Cheapest phase")
    para(s,"The error should be caught during requirement gathering and requirements review at a relative cost of 1. The analyst would read the numeric rule back to the customer and compare the written SRS with the interview note before approval.")
    h1(s,"Task 3 Functional or non-functional")
    tbl(s,[["No.","Type","Quality if N","Reason"],
    ["1","F","-","Shows today's menu."],["2","N","Performance","Sets response time and concurrent load."],["3","F","-","Provides card payment."],
    ["4","N","Security","Protects card data."],["5","F","-","Sends a ready notification."],["6","N","Usability","Specifies supported interface languages."],
    ["7","F","-","Creates a unique daily order number."],["8","N","Portability","Specifies browsers and devices."],["9","F","-","Shows unprepared orders."],
    ["10","N","Reliability","Limits downtime."],["11","F","-","Provides a sales count by dish."],["12","N","Maintainability","Limits the effect of a future change."]],[9*mm,16*mm,29*mm,124*mm])
    h1(s,"Task 4 Rewritten requirements")
    tbl(s,[["ID","Corrected requirement","Test"],
    ["NFR-01","The menu page shall load within 2 seconds for at least 1,000 simultaneous students on the university Wi-Fi.","Open the page with a 1,000-user load test and verify every response is at most 2 seconds."],
    ["NFR-02","A first-year student shall find and add a dish to an order in no more than 3 clicks after opening the menu.","Ask 5 first-year students to add a named dish and count clicks; each must use at most 3."],
    ["NFR-03","The system shall support at least 2,000 registered students and 1,000 simultaneous active sessions.","Create 2,000 accounts, run 1,000 sessions and verify successful menu and order operations."],
    ["NFR-04","The system shall transmit payment data only through TLS 1.3 and shall store no card number or CVV in the cafeteria database.","Inspect network traffic during a payment and search all database fields for card number and CVV."],
    ["FR-11","The system shall show a paid order on the kitchen screen within 5 seconds after payment confirmation.","Pay for 10 orders and verify each appears within 5 seconds."],
    ["FR-12","The system shall produce by 18:05 a daily report containing total orders, portions sold for every dish and total revenue in soum.","Place 10 known orders, generate the report after 18:00 and compare all totals with the orders."]],[18*mm,91*mm,69*mm])
    h1(s,"Task 5 Requirements analysis")
    h2(s,"5.1 Requirements list")
    tbl(s,[["ID","Requirement"],
    ["FR-01","The system shall allow a student to sign in with one university account."],["FR-02","The system shall show the menu for the current day with the price of every dish."],
    ["FR-03","The system shall allow a student to add up to 5 dishes to one order."],["FR-04","The system shall allow payment by bank card or payment at the counter."],
    ["FR-05","The system shall assign every order a number unique within that calendar day."],["FR-06","The system shall show every confirmed order on the kitchen screen within 5 seconds."],
    ["FR-07","The system shall allow kitchen staff to mark an order as ready."],["FR-08","The system shall notify the student within 10 seconds after the order is marked ready."],
    ["FR-09","The system shall allow cancellation only while an order has the status Not started."],["FR-10","The system shall produce a daily report of portions sold for every dish and total revenue."],
    ["NFR-01 Performance","The menu page shall load within 2 seconds for 1,000 simultaneous students on university Wi-Fi."],
    ["NFR-02 Security","Payment data shall use TLS 1.3 and card numbers and CVVs shall not be stored by the cafeteria system."],
    ["NFR-03 Usability","The interface shall be available in Uzbek, Russian and English."],
    ["NFR-04 Reliability","Downtime shall not exceed 10 minutes during one working day from 08:00 to 18:00."],
    ["NFR-05 Maintainability","An authorized manager shall add a dish category through the admin screen without changing source code."],
    ["NFR-06 Portability","Student ordering functions shall work in the two latest major versions of Chrome and Safari and on university tablets."]],[36*mm,142*mm])
    h2(s,"5.2 Collection techniques")
    tbl(s,[["Technique","Source","What will be learned"],
    ["Interview","Cafeteria manager, cashier and cook","Payment rules, kitchen workflow, reporting needs and exceptions."],
    ["Questionnaire","300-500 students","Expected usage, preferred payment method, languages and notification preferences."],
    ["Observation","Cafeteria during two busy breaks","Actual queue time, bottlenecks, collection process and peak order volume."],
    ["Document analysis","Menus, price lists, receipts and daily cash reports","Dish categories, prices, taxes, sales fields and reconciliation rules."],
    ["Prototyping","10 students and 3 staff members","Whether ordering, kitchen and manager screens are understandable before coding."]],[31*mm,49*mm,98*mm])
    para(s,"First choice: observation. It reveals the real peak-time workflow and bottlenecks without relying on memory, so later interviews can ask precise questions about events already seen.")
    h2(s,"5.3 Questions not answered")
    for q in ["What happens to a paid order that the student never collects?","When is a refund allowed and how long may it take?","How are allergies and ingredients shown and confirmed?","Who may change prices, dishes and the number of available portions?","What should happen when the internet or payment provider is unavailable?"]: bullet(s,q)
    h2(s,"5.4 Self-check")
    tbl(s,[["ID","Clear","Testable","Complete","Consistent","Necessary","Traceable"],["FR-01","yes","yes","yes","yes","yes","yes"],["FR-06","yes","yes","yes","yes","yes","yes"],["NFR-01","yes","yes","yes","yes","yes","yes"]],[25*mm]+[25.5*mm]*6)
    para(s,"No correction is required: the selected requirements identify the actor or system behaviour, contain measurable conditions where needed, do not conflict with the case, support a stated stakeholder need and can be traced to authentication, kitchen processing and peak-load performance.")
    h1(s,"Task 6 Bonus")
    para(s,"6.1 FR-20 contradicts FR-21. If cooking starts immediately after payment, cancellation at any moment before collection can waste prepared food and cannot always reverse the kitchen action.")
    para(s,"6.2 NFR-09 is not a software requirement. It is a business goal for cafeteria operations and should be measured in the project plan, not imposed as an absolute software behaviour.")
    para(s,"6.3 Corrected pair: FR-20 The student shall be able to cancel an order only while its status is Not started. FR-21 The kitchen shall change a confirmed order to Preparing before cooking, after which cancellation shall be disabled.")
    doc(OUT/"Muratbaev_Albert_Prac2.pdf",s)

def lab2():
    s=[]; title(s,"Lab 2","Requirements Analysis of the TTPU Student Print Service")
    h1(s,"Task 1 Requirements")
    rows=[["ID","Requirement","F/N","How it would be tested"],
    ["FR-01","The system shall give every new student 100 free pages at the beginning of each semester.","F","Register a student and verify a balance of 100 free pages."],
    ["FR-02","The system shall allow a student to submit a document as a print job.","F","Submit a valid document and verify that a job is created."],
    ["FR-03","The system shall reject a print job longer than 50 pages.","F","Submit 50-page and 51-page files; accept the first and reject the second."],
    ["FR-04","The system shall assign every accepted print job a unique job number.","F","Submit 100 jobs and verify that no job number repeats."],
    ["FR-05","The system shall deduct printed pages from the student's free-page balance before charging money.","F","Print 10 pages from a balance of 100 and verify a balance of 90."],
    ["FR-06","After the free balance reaches 0, the system shall charge 200 soum for each black-and-white page.","F","Print 3 black-and-white pages with zero balance and verify 600 soum."],
    ["FR-07","After the free balance reaches 0, the system shall charge 400 soum for each colour page.","F","Print 3 colour pages with zero balance and verify 1,200 soum."],
    ["FR-08","The system shall allow a student to cancel a job only while its status is Waiting.","F","Cancel one waiting and one printed job; only the waiting job is cancelled."],
    ["FR-09","The system shall show the operator all jobs whose status is Waiting.","F","Create waiting and completed jobs and verify only waiting jobs appear."],
    ["FR-10","The system shall let the operator mark a waiting job as Printed.","F","Mark a waiting job printed and verify its status and removal from the queue."],
    ["FR-11","At the end of each day, the system shall report the total number of pages printed.","F","Print known jobs and compare the report page total."],
    ["FR-12","At the end of each day, the system shall report the total money collected in soum.","F","Complete paid jobs and compare the report with calculated charges."],
    ["NFR-01","The operator shall complete submission-to-queue entry in no more than 3 screens and 5 clicks.","N Usability","Ask the operator to add 5 jobs and count screens and clicks."],
    ["NFR-02","The waiting-job list shall open within 2 seconds with 500 jobs stored.","N Performance","Load 500 jobs and measure the list response time."],
    ["NFR-03","Only an authenticated operator shall change a job status or view daily revenue.","N Security","Try both actions with student and operator accounts."],
    ["NFR-04","The system shall preserve all confirmed jobs and balances after an unexpected restart.","N Reliability","Create jobs, interrupt the server and verify all records after restart."],
    ["NFR-05","The operator application shall run in the two latest major versions of Chrome and Edge.","N Portability","Repeat the operator workflow in the specified browser versions."]]
    tbl(s,rows,[16*mm,88*mm,22*mm,52*mm])
    s.append(PageBreak())
    h1(s,"Task 2 Requirement collection plan")
    tbl(s,[["Technique","From whom or where","What is still unknown"],
    ["Interview","Department head, operator and accountant","Approval rules, payment handling, roles, exceptions and required reports."],
    ["Questionnaire","At least 100 students","File types, colour demand, expected volume and preferred status notifications."],
    ["Observation","Existing print room during busy periods","Actual service steps, bottlenecks, reprints, abandoned jobs and queue size."],
    ["Document analysis","Student lists, price rules, receipts and semester calendar","Identity fields, accounting evidence, semester dates and retention rules."],
    ["Prototyping","Operator and 5 students","Whether submission, queue and cancellation screens are understandable."]],[31*mm,53*mm,94*mm])
    para(s,"First choice: interview the operator. The operator performs the daily process and can quickly expose exceptions and practical constraints; observation should follow to verify that the described process matches reality.")
    h2(s,"Interview questions")
    para(s,"Money")
    for q in ["How and when does a student pay for pages beyond the free allowance?","Are unused free pages carried to the next semester?","When is a refund or free reprint allowed?"]: bullet(s,q)
    para(s,"Jobs and documents")
    for q in ["Which file formats and maximum file size must be accepted?","May a job mix colour and black-and-white pages?","What should happen to a paid job that is never collected?"]: bullet(s,q)
    para(s,"Users and operation")
    for q in ["How is a student identified and who may correct a page balance?","How should the queue work when the printer or network is unavailable?"]: bullet(s,q)
    h1(s,"Task 3 Repair another analyst's requirements")
    rows=[["Item","Broken properties and reason","Corrected requirement","Test"],
    ["a","Clear and testable: fast has no limit.","NFR-06 The waiting-job screen shall open within 2 seconds for 500 stored jobs.","Load 500 jobs and measure 20 openings."],
    ["b","Clear, complete and testable: handle is undefined and no actor or operation is named.","FR-13 The system shall allow an operator to find a student by university ID and view the current page balance.","Search a known ID and compare the displayed record."],
    ["c","Consistent: limits of 50 and 80 pages conflict.","FR-03 The system shall accept jobs of 1-50 pages and reject jobs of 51 pages or more.","Submit 1-, 50- and 51-page files."],
    ["d","Necessary and testable: modern and beautiful are subjective and not tied to a user need.","NFR-01 The operator shall add a job in no more than 5 clicks after signing in.","Perform 5 additions and count clicks."],
    ["e","Complete and testable: the pricing rules and inputs are absent.","FR-14 The system shall calculate 200 soum per black-and-white page and 400 soum per colour page after free pages are used.","Price a mixed known job and compare the total."],
    ["f","Consistent and complete: it conflicts with paid printing after the allowance.","FR-15 The first 100 pages per student per semester shall be free; later pages shall use FR-14 prices.","Use 100 pages, then print one additional page."],
    ["g","Clear, complete and testable: probably, some kind and something are ambiguous.","FR-16 The system shall show a cancellation confirmation containing the job number within 2 seconds.","Cancel 10 waiting jobs and verify message, number and time."],
    ["h","Necessary and traceable: it is an unsupported design decision, not a stakeholder requirement.","Do not rewrite as a requirement; move the database choice to the design document after architecture evaluation.","Review the design decision against volume, skills and maintenance constraints."]]
    tbl(s,rows,[11*mm,48*mm,77*mm,42*mm])
    para(s,"The two statements that should not be repaired merely by wording are (d) and (h). Statement (d) expresses subjective aesthetic taste with no established stakeholder need; first elicit a measurable usability need. Statement (h) prescribes implementation technology; evaluate it during design and record it in the design document only if justified.")
    h1(s,"Task 4 What the customer did not say")
    tbl(s,[["Missing situation","Requirement added"],
    ["A student pays but never collects the output.","FR-17 The system shall change an uncollected printed job to Abandoned 3 working days after printing and include it in the daily report."],
    ["The printer jams after charging but before the full job prints.","FR-18 The operator shall mark a failed job for one free reprint of its unprinted pages."],
    ["A file is corrupt or has an unsupported format.","FR-19 The system shall reject an unreadable file before payment and show a reason."],
    ["A student submits the same job twice.","FR-20 The system shall warn when the same student submits a file with the same name and page count within 2 minutes."],
    ["The semester changes while balances still exist.","FR-21 An administrator shall reset every active student's free balance to 100 pages on the configured semester start date."],
    ["The operator makes an incorrect status or balance change.","FR-22 The system shall record operator ID, time, old value and new value for every manual status or balance change."]],[76*mm,102*mm])
    para(s,"The most dangerous omission is charging for a job that fails during printing. If discovered only at deployment, students may be charged for pages they did not receive, causing disputes and loss of trust. The repair may require changes to requirements, transaction design, code, database records, accounting procedures and tests; using the lecture cost chart, a defect that costs about 1 unit in requirements can cost roughly 50-100 units after release.")
    h1(s,"Task 5 The project through six phases")
    tbl(s,[["Phase","What is done in this project","Output","Who does it"],
    ["1 Requirement gathering","Interview the operator and department head, observe printing, survey students and define prices, queue, cancellation and reports.","Approved SRS with use cases and acceptance tests.","Analyst, customer, operator, students."],
    ["2 Feasibility study","Estimate six-week scope, reuse university accounts, check printer integration, legal handling of student data and operating cost.","Go/no-go report and limited version-1 scope.","Analyst, developer, IT administrator, department head."],
    ["3 Design","Design student submission, operator queue, pricing, balances, job states, database, security and reporting.","HLD, LLD, data model and interface prototype.","Developer/architect with operator review."],
    ["4 Coding","Implement authentication, uploads, page counting, queue, prices, cancellation, reporting and unit tests.","Source code, database migrations and unit tests.","One developer."],
    ["5 Testing","Test rules, prices, 50-page limit, 100-page balance, permissions, failures, performance and usability.","Test report, defects and acceptance result.","Developer, analyst, operator and pilot students."],
    ["6 Deployment and maintenance","Install in the print room, import users, train the operator, monitor, back up data and correct defects.","Working service, user guide, backups and maintenance log.","Developer, university IT and operator."]],[31*mm,76*mm,42*mm,29*mm])
    para(s,"Feasibility answer: yes, but only for a small version 1 with the listed core functions and existing university infrastructure. The decision mainly depends on schedule feasibility because one programmer has only 6 weeks; it also depends on technical feasibility of document page counting and printer integration. Scope must be frozen, a simple web architecture reused and advanced features deferred.")
    doc(OUT/"Muratbaev_Albert_Lab2.pdf",s)

def review():
    s=[]; title(s,"Lab 2.1","Reviewing Requirements Documents")
    h1(s,"Exercise 1 TTPU library system")
    h2(s,"1.1 Contradictions")
    tbl(s,[["Pair","Why they contradict"],["FR-01 and FR-02","The maximum is 5 books, but FR-02 permits a 6th book."],["FR-04 and FR-06","A reference book may not leave the building, yet FR-06 treats it as an ordinary renewable loan."],["FR-07 and FR-08","The same reminder is required both 2 days before and only after the due date."],["FR-16 and FR-17","Full history forever conflicts with deletion of personal data 1 year after departure."]],[45*mm,133*mm])
    h2(s,"1.2 Lines that are not requirements")
    tbl(s,[["ID","What it really is","Where it belongs"],["FR-13","Design decision: MySQL 8 is an implementation technology.","Design document after technical evaluation."],["FR-18","Business/organisational goal: purchasing books is not system behaviour.","Library business plan or project plan."],["NFR-03","Impossible promise: no software can be guaranteed never to fail.","Nowhere; replace it with a measurable reliability target."]],[20*mm,94*mm,64*mm])
    h2(s,"1.3 Untestable lines repaired")
    tbl(s,[["ID","Corrected requirement","Test"],["FR-09","NFR-04 A first-year student shall find and reserve a known available book in no more than 4 clicks after sign-in.","Ask 5 first-year students to reserve a named book and count clicks."],["FR-14","NFR-05 Search results shall appear within 2 seconds for a catalogue of 50,000 books and 100 concurrent users.","Run 100 searches against 50,000 records and measure response time."],["FR-15","NFR-06 The first page of search results shall appear within 2 seconds for 95% of 100 test searches.","Execute 100 representative searches and time each result."],["NFR-03","NFR-03 The system shall have at least 99.5% availability during library working hours each semester.","Compare monitoring downtime with scheduled working hours."]],[20*mm,95*mm,63*mm])
    h2(s,"1.4 Contradictions repaired")
    for x in ["FR-01 The system shall allow a registered student to borrow at most 5 books without special approval.","FR-02 The system shall allow a librarian to approve one additional book, increasing the limit to 6 for that loan.","FR-04 Books marked Reference shall be used only inside the library and shall not create a take-home loan.","FR-06 The system shall not offer online renewal for a book marked Reference.","FR-07 The system shall send an email reminder 2 days before the due date for a loan that is not returned.","FR-08 The system shall send one overdue email at 09:00 on the first day after the due date if the book remains unreturned.","FR-16 The system shall retain borrowing transactions in anonymised form indefinitely for statistics.","FR-17 The system shall delete or anonymise data identifying a student within 1 year after the student leaves the university."]: bullet(s,x)
    h1(s,"Exercise 2 TTPU canteen pre-order system")
    h2(s,"2.1 Full review table")
    rows=[["ID","Defect","What is wrong","Corrected line or action"],
    ["FR-03","C","Contradicts FR-02 on when and how payment occurs.","The student shall pay in the application; cash payment is not supported in version 1."],
    ["FR-06","C","Changes until 11:45 conflict with cooking starting at 11:30.","A student shall change an order until 11:25 while its status is Not started."],
    ["FR-08","C","Contradicts FR-09 about zero-stock dishes.","Delete; FR-09 remains the stock rule."],
    ["FR-11","C","Immediate delivery conflicts with the single list at 11:00.","Each confirmed order shall appear on the kitchen screen within 5 seconds."],
    ["FR-12","C","Conflicts with FR-11 and can delay the kitchen.","At 11:00 the system shall show a summary of all confirmed orders in addition to individual orders."],
    ["FR-13","A/T/W","Work without internet is ambiguous, unmeasurable and is non-functional in the functional list.","NFR-05 The kitchen screen shall show cached confirmed orders for up to 30 minutes after internet loss."],
    ["FR-15","C","English-only messages conflict with three interface languages.","Messages shall use the language selected by the user from Uzbek, Russian and English."],
    ["FR-17","N","Django is a design decision, not required behaviour.","Delete and evaluate technology in the design document."],
    ["FR-18","N","Reducing waste is a business goal, not software behaviour.","Move to project success criteria; use reports to measure it."],
    ["FR-19","T/W","Secure is unmeasurable and is non-functional.","NFR-04 Payment data shall use TLS 1.3 and no CVV shall be stored."],
    ["FR-20","N","A delivery deadline is a project constraint, not system behaviour.","Move to the project plan as a milestone."],
    ["NFR-03","T","Easy to use is subjective and has no measure.","NFR-03 A first-year student shall place a standard order in at most 6 clicks without training."]]
    tbl(s,rows,[17*mm,16*mm,65*mm,80*mm])
    h2(s,"2.2 Missing requirements")
    for x in ["FR-21 The system shall mark a paid order Uncollected if it is not collected within 60 minutes after it is marked Ready.","FR-22 The system shall return a cancelled card payment to the original payment method within 5 working days.","FR-23 The system shall show declared allergens for every dish before the student confirms the order.","FR-24 The system shall prevent ordering on dates marked Closed in the manager calendar.","FR-25 Only an authenticated user with the Manager role shall open the manager screen and view revenue."]: bullet(s,x)
    h2(s,"2.3 SDLC timing and late cost")
    tbl(s,[["ID","Found now","Should be found","If found after release"],["FR-03","Requirements review","Requirement gathering/review","About 50-100 units: payment flow, UI, accounting and training would need correction."],["FR-06","Requirements review","Requirement review","About 50 units: students could change food already cooking, causing refunds and waste."],["FR-11","Requirements review","Requirement review","About 50-100 units: the kitchen screen and staff workflow would need redesign and retraining."],["FR-15","Requirements review","Requirement review/prototyping","About 50 units: messages and translations across all screens would need rework after users complain."]],[18*mm,38*mm,46*mm,76*mm])
    h2(s,"2.4 Use case Student orders a meal")
    para(s,"Actor: Student. Precondition: the student is signed in, ordering is open from 08:00 to 11:00, and at least one dish has portions available.")
    for x in ["1. The system shows today's menu, prices, available portions and allergens.","2. The student selects one or more available dishes.","3. The system shows the order summary and total amount.","4. The student confirms the order and chooses application payment.","5. The payment service confirms payment.","6. The system assigns a daily unique order number.","7. The order appears on the kitchen screen within 5 seconds.","8. The system shows the order number and confirmation to the student."]: bullet(s,x)
    para(s,"Alternative flow - payment fails: At step 5, if payment is rejected or times out, the system does not create a confirmed kitchen order, shows the failure reason, and lets the student retry once or cancel.")
    para(s,"Postcondition: a paid order with a unique number is stored and visible to the kitchen, or no confirmed order exists if payment failed. Traceability: FR-01, FR-02, FR-04, FR-07, FR-09, FR-10, corrected FR-11, FR-21, FR-23 and NFR-01.")
    doc(OUT/"Muratbaev_Albert_Lab2_1_Review.pdf",s)

def lab3():
    s=[]; title(s, "Lab 3", "Fundamental Software Design Principles")

    h1(s, "Part A - Modularity and information hiding")
    h2(s, "Q1. One job, one sentence")
    tbl(s,[["Item","One module or two","The modules and their jobs"],
    ["(a)","Two","Timetable: stores the lessons of a group. ReminderSender: sends SMS reminders to the students."],
    ["(b)","One","Grades: computes the final mark of a student."],
    ["(c)","Two","Auth: checks a password. LoginScreen: draws the login screen."],
    ["(d)","One","Export: turns a finished report into a PDF file."]],[14*mm,26*mm,138*mm])

    h2(s, "Q2. Cut a system into modules")
    bullet(s,"Session: keeps the film session and its seat map.")
    bullet(s,"Seats: shows which seats of the chosen session are free.")
    bullet(s,"Ticket: sells a ticket for a session and records the sale.")
    bullet(s,"TicketPrint: prints a sold ticket with its QR code.")
    bullet(s,"SalesReport: at night counts how many tickets each film sold.")
    para(s,"Arrows: Seats uses Session; Ticket uses Session; TicketPrint uses Ticket; SalesReport uses Ticket.")
    para(s,"Module with the most arrows pointing at it: Ticket (two arrows: from TicketPrint and from SalesReport). This is not a problem by itself: it is the central business object and other modules naturally record or read what it sells. It becomes a problem only if Ticket keeps growing (pricing, printing, reporting inside it); then every small change touches many modules.")

    h2(s, "Q3. Where is the border wrong?")
    tbl(s,[["Case","Broken rule","Where the border should be"],
    ["(a)","A module must own one job (a piece of knowledge), not one kind of syntax.","Loops and checks belong inside the modules whose data they serve; no separate loops.py and checks.py."],
    ["(b)","Data must have one owner; nobody changes another module's data directly.","balance lives in an Account module that exposes deposit() and withdraw(); Booking, Refund and Admin call these methods."],
    ["(c)","One external dependency must have one boundary.","A Telegram module wraps the API; Booking, Report and Admin call it instead of the API."],
    ["(d)","Things that change together belong together.","Price and tax are one tariff rule set; they live in one Pricing module, tax.py is merged into it."]],[20*mm,70*mm,88*mm])

    h2(s, "Q4. A parking lot with no secrets")
    para(s,"Which coupling: content coupling - outside code reads and writes the internal fields of Parking.")
    para(s,"After places becomes a dict {place_number: car_number}:")
    tbl(s,[["Outside line","Still correct?","Why"],
    ["parking.places[12] = \"01A123BC\"","Looks correct","Writing a dict entry happens to match the new representation, but it still skips any booking check."],
    ["if None in parking.places:","Wrong, and dangerous","The dict holds place numbers as keys, never None, so the condition is always false: the screen says there is a free place even when the parking is full."],
    ["hours * parking.prices[\"car\"]","Correct","The price table did not change."]],[46*mm,30*mm,102*mm])
    para(s,"Most dangerous: the free-place check. It does not crash; it silently gives a wrong answer, so users keep trusting a lie - a loud crash, by contrast, is noticed and fixed at once.")
    para(s,"Public interface: book(place_number, car_number) -> bool; free_place() -> place number or None; leave(car_number) -> bool; price(vehicle_type, hours) -> sum.")
    para(s,"Two secrets: (1) how the places are stored (list, dict or anything else); (2) the price table and how the cost is computed.")

    h2(s, "Q5. Just give me the list")
    para(s,"No: get_places() would hand out the internal representation and create content coupling with every screen. Instead I would add free_places() -> int (or is_free(n)), which returns only the answer the screen needs.")

    h1(s, "Part B - Abstraction")
    h2(s, "Q6. Three words students confuse",)
    para(s,"One word for each sentence:")
    tbl(s,[["Sentence","Word"],["(a)","encapsulation"],["(b)","information hiding"],["(c)","abstraction"],["(d)","information hiding"],["(e)","abstraction"]],[30*mm,148*mm])

    h2(s, "Q7. Procedural or data abstraction?")
    tbl(s,[["Item","P or D","What the caller does not know"],["(a) queue enqueue/dequeue","D","How the queue stores its elements (list, linked cells...)."],["(b) print_certificate","P","How the certificate is laid out and produced."],["(c) backup_database","P","How the backup is made and where copies are stored."],["(d) phonebook add/find","D","The internal phonebook structure."],["(e) convert_to_pdf","P","How the PDF file is generated."],["(f) cart add/total","D","How the cart stores and computes its items."]],[52*mm,16*mm,110*mm])

    h2(s, "Q8. Put the levels in order")
    para(s,"Order from the user (highest) to the hardware (lowest): C, D, F, A, E, B.")
    tbl(s,[["Level","One thing it knows","One thing it does not know"],
    ["C - the user taps Send","That the user wants to send this text to this chat","That the message will travel as JSON, bytes or radio waves"],
    ["D - chat.send(chat_id, text)","Which chat and text the user chose","How the network or the message record is built"],
    ["F - Message.create(sender_id, text)","The structure of a message","Where the message physically goes"],
    ["A - http.post(/messages, json)","The URL, the JSON body and status codes","Who the user is or what a chat is"],
    ["E - socket.send(bytes)","Ports, packets, bytes","URLs, JSON, users, chats"],
    ["B - the Wi-Fi chip","Radio signals and frames","Everything about the chat application"]],[54*mm,55*mm,69*mm])

    h2(s, "Q9. One interface, two implementations")
    para(s,"Nothing in the program that uses the interface must change; only the line that constructs a Counter is rewritten. The two versions have identical method signatures.")
    para(s,"With one million words and 1,000 count() calls, version 2 wins. Version 1 scans the whole list for every count(), about 1,000 x 1,000,000 comparisons in total; version 2 keeps a ready dict, so each count() is a single lookup and the 1,000 calls cost almost nothing.")
    para(s,"The interface promises that the answer is correct. It says nothing about speed. This is exactly what lets the implementer choose or replace the implementation: as long as every caller gets the correct answer, the team may trade speed, memory and simplicity inside the class without breaking anyone.")

    h2(s, "Q10. How much should the interface show?")
    para(s,"(a) too much: everyone reads and writes the inside of the timer, including the admin writing timer.running = False.")
    para(s,"(b) too little: the screen team must rebuild the remaining-time rule from the start time; that knowledge belongs to the timer.")
    para(s,"(c) just enough: start(minutes), stop(), seconds_left() and is_finished() cover all the needs with no internals exposed.")
    para(s,"In (b) the rule broken a few months later is DRY: the remaining time is now computed in two places (the timer and the screen code). People notice when the two copies disagree - for example after an exam rule change one screen shows the wrong time.")
    para(s,"Test of slide 24 applied to (c): tonight I could replace the stored countdown by a recomputation from the start timestamp, and I could change how is_finished() is decided (for example from a recorded end moment), and no caller would have to hear about it, because both details are hidden behind the same four methods.")

    h1(s, "Part C - Cohesion")
    h2(s, "Q11. Name the cohesion")
    tbl(s,[["Piece","Level","How I recognized it"],
    ["(a) make_thumbnail","Sequential","Each step consumes the result of the previous one: load -> resize -> grayscale -> save."],
    ["(b) end_of_day","Temporal","Unrelated jobs that happen at the same moment (closing, backup, report, lights)."],
    ["(c) is_leap_year","Functional","One tiny job and nothing else."],
    ["(d) class Misc","Coincidental","Three unrelated helpers only share the file name."],
    ["(e) passport_summary","Communicational","All three calls work on the same passport; no pipeline between them."],
    ["(f) export(report, fmt)","Logical","Same kind of work with one branch chosen by a flag."],
    ["(g) register_for_exam","Procedural","Fixed steps of one workflow, but the steps share no data."]],[36*mm,34*mm,108*mm])

    h2(s, "Q12. Three versions, three levels")
    para(s,"A: sequential. B: communicational - every call works on the same card; the order of the warnings does not matter. C: procedural.")
    para(s,"The one question: is the output of one line the input of the next line? If yes - sequential. If no, but all the lines work on the same piece of data - communicational. If the lines have a fixed order but do not pass data to each other - procedural.")
    para(s,"Difference: temporal means the parts only belong together because they run at the same moment and share nothing; procedural means the parts are steps of one workflow that would run in this order even in the middle of the day. Version C is procedural: open- header- date- close is a sequence of the printing job, not a nightly coincidence.")

    h2(s, "Q13. The and-test on a real class")
    para(s,"One sentence: Invoice adds lines, computes the total, converts itself into a PDF, e-mails the customer and saves itself into the database - the word and appears three times, so the class has at least four or five jobs.")
    tbl(s,[["Change","Method that must be edited"],["(a) the e-mail provider changes","email_to_customer"],["(b) the tax rate changes","total (and often add_line)"],["(c) the database moves to PostgreSQL","save_to_db"],["(d) the PDF must show the shop logo","to_pdf"]],[62*mm,116*mm])
    para(s,"Number of different reasons to change: four (at least).")
    para(s,"Split (names and methods only):")
    bullet(s,"Invoice: add_line(product, qty); total()")
    bullet(s,"PdfFormatter: to_pdf(invoice)")
    bullet(s,"CustomerEmailer: send(invoice, address)")
    bullet(s,"InvoiceRepository: save(invoice)")

    h2(s, "Q14. Read the signals")
    tbl(s,[["Signal","Evidence in the story"],["The module is too long","1,400 lines and about a hundred more every week."],["Many unrelated dependencies","It imports sqlite3, smtplib, reportlab and requests - four different worlds in one file."],["Methods that do not share data","Half of the methods use self.connection, the other half use self.smtp and never touch the database."],["Many people change it for different reasons","In one month Aziza fixed the PDF, Bekzod added an SMS provider, Dilnoza fixed a SQL query."],["A meaningless name","DataProcessor says nothing about one job."]],[52*mm,126*mm])
    para(s,"Strongest signal: the split between self.connection and self.smtp users. Check in thirty seconds: search the file for which methods mention connection and which mention smtp - if the two sets of method names do not overlap, the class is really two classes.")

    h2(s, "Q15. When is temporal cohesion acceptable?")
    para(s,"It is acceptable when the only thing the parts have in common is the moment they run, and each job itself lives in its own cohesive module: end_of_day() is then just a scheduled trigger, like slide 6 - timing does not stop the jobs from being separated. It is not acceptable when the jobs themselves are mixed inside the same function.")
    para(s,"Two concrete problems of the second version: (1) the business rule (summing the day's sales) is written inline in the driver, so a change of the rule touches a night job; (2) storage and infrastructure are hard-coded (sqlite3.connect, smtp.send, lights.off), so changing the database or the message system means editing this one function that also turns off the lights - exactly the mix that temporal cohesion is supposed to avoid.")

    h1(s, "Part D - Coupling")
    h2(s, "Q16. Name the coupling")
    tbl(s,[["Case","Coupling"],["(a) send_sms(user)","Stamp - the whole User with 15 fields travels, only phone is used."],["(b) bookings.csv with ;","External - two modules depend on the same outside file format."],["(c) area(width, height)","Data - exactly the values needed are passed."],["(d) db._connection...","Content - Report reaches inside Database and uses its private part."],["(e) CURRENT_USER global","Common - both functions read and write the same global data."],["(f) format_price(amount, style)","Control - the style flag picks the branch inside the function."]],[60*mm,118*mm])
    para(s,"From the worst to the best: d (content), e (common), b (external), f (control), a (stamp), c (data).")

    h2(s, "Q17. Move one step down the table")
    para(s,"(a) Stamp -> data:")
    bullet(s,"def send_sms(phone): sms_gateway.send(phone, \"Your code: 4821\")")
    bullet(s,"call: send_sms(user.phone)")
    para(s,"(e) Common -> data:")
    bullet(s,"def login(name): return Session(name)")
    bullet(s,"def can_delete(session): return session.name == \"admin\"")
    para(s,"(f) Control -> data:")
    bullet(s,"def format_price_short(amount): return f\"{amount} sum\"")
    bullet(s,"def format_price_long(amount): return f\"{amount:,} UZS\"")
    para(s,"(d) Content -> data:")
    bullet(s,"Database gets a public method: get_sales() -> rows")
    bullet(s,"def build(self, db): rows = db.get_sales()")

    h2(s, "Q18. The same boolean, two kinds of coupling")
    para(s,"create_user(name, is_admin) is data coupling: True/False becomes a stored attribute of the new user; no branch inside changes meaning. save(user, to_cloud) is control coupling: the flag chooses which of two branches inside save() will run.")
    para(s,"A reader of save(user, True) does not know what True means - upload where? overwrite what? The call says nothing about the target.")
    para(s,"Rewrite without a flag:")
    bullet(s,"def save(user, storage): storage.write(user)")
    bullet(s,"storage is a CloudStorage or a DiskStorage object; both offer write(user) - no branch inside save.")

    h2(s, "Q19. Who decides the messenger?")
    para(s,"Three decisions AttendanceReport makes that are not its job: (1) it chooses the messenger (Telegram); (2) it owns the secret token; (3) it names the recipient @group_ce22.")
    para(s,"Wish 1 (send by e-mail): the constructor and the body must be rewritten to call the e-mail library; Wish 2 (tests send nothing): a test must succeed in stopping the sending - usually an if inside send(), which pushes test knowledge into production code.")
    para(s,"Rewrite:")
    bullet(s,"class AttendanceReport: def __init__(self, sender): ... def send(self, text): self.sender.post(text)")
    bullet(s,"for real use: AttendanceReport(TelegramBot(\"TOKEN-123\"))")
    bullet(s,"for a test: AttendanceReport(NullSender()) - a sender that never contacts any network.")

    h2(s, "Q20. Place it on the golden-rule square")
    tbl(s,[["Design","Cohesion","Coupling","Corner"],["(a) System, 3,000 lines, everyone imports it","low","high","the worst corner"],["(b) five small classes + global SETTINGS","high","high","high cohesion, high coupling"],["(c) three unrelated utils files","low","low","low cohesion, low coupling"],["(d) O receives Pricing, Storage, Receipt","high","low","the goal corner"]],[62*mm,24*mm,22*mm,70*mm])
    para(s,"Change that moves (b) to the goal corner: make one Settings module the owner of the dictionary and expose get(name)/set(name, value); the five classes then receive the values they need as ordinary parameters (or call the single owner), so no global shared state is left.")

    h1(s, "Part E - Separation of concerns, DRY, KISS, YAGNI")
    h2(s, "Q21. Which rule is broken?")
    tbl(s,[["Case","Rule broken","One-line repair"],["(a)","DRY","One constant MAX_STUDENTS and one full-limit message live in group.py; enroll.py and messages.py use them."],["(b)","KISS","Write return age >= 18."],["(c)","YAGNI","Build one role now; add the twelfth when a second real role appears."],["(d)","Separation of concerns","Compute the price in a rule function, save through a repository, show the result in the screen - three separate lines/calls."],["(e)","KISS","Write max(a, b, c)."]],[16*mm,38*mm,124*mm])

    h2(s, "Q22. Same code, different knowledge")
    para(s,"I do not fully agree. The two functions serve different concerns with different owners and names (shipping vs parking), so fee(x) would replace two clear names with one flag-driven function - but the repeated knowledge inside them, the tariff 2000, is a real DRY item.")
    para(s,"What to do with 2000: name it in each owning module - UZS_PER_KG and UZS_PER_HOUR - or hold one named tariff constant in one place if the university really prices both with the same table; the number itself must never be typed twice without a name.")

    h2(s, "Q23. YAGNI or simple good design?")
    para(s,"Developer B breaks YAGNI; developer A is doing good design. A pays almost nothing today (one messages.py) and removes a real cost later: when a second language does come, the texts are already out of the code and moving them is cheap. B pays for an engine, a picker and a download system today, with seven languages to test and maintain, while the customer asked for one language - the cost is real now and the saving never arrives, because features nobody asked for usually never get used.")

    h2(s, "Q24. Sort the lines by concern")
    tbl(s,[["Line","Concern"],["1  if balance < price: refuse()","Business rules"],["2  INSERT INTO orders ...","Storage"],["3  show_message(...)","Presentation"],["4  logger.info(...)","Infrastructure"],["5  discount = 0.1 if has_meal_card ...","Business rules"],["6  sms.send(phone, ...)","Infrastructure"],["7  button.color = green","Presentation"],["8  SELECT balance FROM wallets ...","Storage"]],[90*mm,88*mm])
    para(s,"A class named OrderScreen may contain only the Presentation concern (showing results, collecting input); it must not write SQL, decide rules or send SMS itself.")

    h1(s, "Part F - Case study: the dormitory laundry")
    h2(s, "Q25. Count the jobs")
    para(s,"Jobs of book(): (1) checks whether the machine is free; (2) writes the busy state into the global STATUS; (3) computes the price from the mode flag; (4) applies the resident discount; (5) appends the booking to bookings.txt; (6) sends the Telegram notification; (7) prints a confirmation - five or six jobs depending on whether pricing and discount are counted as one.")
    para(s,"Level of cohesion: coincidental (dragged together only by the booking event), with a control flag for the mode; reason: checking, pricing, storage, notification and printing are unrelated jobs.")
    para(s,"Three different numbers are written directly inside book(): 8000, 6000 and 0.10 - and 8000 is written twice, in the wash and the wash+dry branch.")

    h2(s, "Q26. Name every coupling")
    tbl(s,[["Item","Coupling"],["(a) the global STATUS","Common coupling"],["(b) the parameter mode","Control coupling"],["(c) bookings.txt with ; (also read by WeeklyReport)","External coupling - two modules depend on the same file format"],["(d) the whole student object (only 3 of its fields used)","Stamp coupling"],["(e) telegram.send(...) inside book()","External coupling to a concrete device/service"]],[96*mm,82*mm])

    h2(s, "Q27. Who owns STATUS?")
    para(s,"Rustam books machine 3 at 10:00; the entry stays forever, so Malika at 18:00 is refused with Machine is busy. Tomorrow it is the same: nothing ever clears STATUS and book() never looks at the hour, so machine 3 is dead until the program is restarted.")
    para(s,"The data must be owned by a schedule module (rule 2 of slide 15: one owner of the data). Call it MachineSchedule.")
    para(s,"Public interface of MachineSchedule:")
    bullet(s,"book(machine, hour, student) -> bool")
    bullet(s,"is_booked(machine, hour) -> bool")
    bullet(s,"release(machine, hour) -> bool")
    bullet(s,"bookings(machine) -> list")
    para(s,"After the change nobody else may write to that data: MachineSchedule is the single writer; every other module goes through its methods (WeeklyReport may read, but only through a reader method or repository).")

    h2(s, "Q28. Redesign on paper")
    para(s,"Classes (names and methods only):")
    bullet(s,"MachineSchedule: book(machine, hour, student) -> bool; is_booked(machine, hour); bookings(machine)")
    bullet(s,"PriceCalculator: price(mode, is_resident) -> sum")
    bullet(s,"BookingRepository: append(booking); read_all() -> lines")
    bullet(s,"TelegramNotifier: notify(telegram_id, text)")
    bullet(s,"BookingService (the connector): receives schedule, calculator, repository, notifier in its constructor; book(student, machine, hour, mode) -> receipt")
    para(s,"Boxes and arrows: BookingService points to the four classes; WeeklyReport points to BookingRepository. That is five arrows; counting them stops me from adding a sixth dependency (for example calling Telegram directly from the schedule).")
    para(s,"Where the numbers live now: 8000, 6000 and 0.10 all live inside PriceCalculator, and each is written exactly once.")
    para(s,"After the redesign the confirmation Booked! Price: ... is printed by the caller of BookingService - the screen or presentation module; the service itself only returns the price in a receipt.")

    h2(s, "Q29. The two numbers")
    tbl(s,[["Change","Old design: what is edited","New design: which classes change"],
    ["(a) discount 15%","The number 0.10 inside book()","PriceCalculator only"],["(b) SMS instead of Telegram","The telegram.send call inside book() and the imports","Replace the Notifier used by BookingService (one class, no service change)"],["(c) SQLite instead of bookings.txt","book() file code AND WeeklyReport","Add SqliteBookingRepository; the service is unchanged; WeeklyReport reads through the repository"],["(d) test with no messages and no files","Nothing clean is possible in the old design - the test must fake telegram, files and stdout","Pass NullNotifier and an in-memory repository into BookingService in the test"]],[38*mm,62*mm,78*mm])
    para(s,"Why only one class changes in the old design is not good news: that one class is the laundry class that holds all the jobs, so every change is made inside the same crowded body, the file is a shared point of conflict for every future wish, and nothing about the change can be tested in isolation.")

    h1(s, "Part G - Coupling in depth")
    h2(s, "Q30. The settings everybody reads")
    para(s,"Coupling between settings.py and each of the three: common coupling - all four share one mutable global dictionary.")
    para(s,"Pairs that depend on each other without importing: cart.py and invoice.py (their outputs must agree: the total rounded in the cart and the digits printed on the invoice lines), and both of them with admin.py, because admin silently redefines the values they already computed with.")
    para(s,"Two wrong things the customer can see after switch_to_usd() at 10:01: (1) totals of carts that were already filled at 10:00 are printed in USD but rounded with 0 decimals - a soum amount displayed as whole dollars; (2) the cart and the invoice of the same order can disagree, because each module rounds at the moment it reads the shared dictionary.")
    para(s,"The one thing inside switch_to_usd() that allows an inconsistent read: the change is not atomic - it writes two keys in two separate statements, so an unlucky reader can observe currency = USD together with decimals = 0, a pair that does not belong together.")
    para(s,"If decimals must become a rounding step, cart.py and invoice.py must be edited (round(sum, n) and the .{n}f format both assume whole digits); if one module owned the whole rule, zero outside files would change.")
    para(s,"The owner (Prices) exposes at most four methods:")
    bullet(s,"round(amount) -> number")
    bullet(s,"format(amount) -> string")
    bullet(s,"currency() -> string")
    bullet(s,"set_rule(currency, step) - called only by the admin")
    para(s,"After the change cart.py and invoice.py know nothing about currency: they handle plain amounts and call the owner for rounding and formatting. Only the owner (through set_rule, called by the admin function) may change the currency.")

    h2(s, "Q31. Data that only travels")
    para(s,"All three calls (checkout -> confirm -> schedule) are stamp coupling: each passes the whole Order while using none of it (checkout, confirm) or only two fields (schedule). The functions that only carry data they do not use are checkout and confirm.")
    para(s,"When order.address becomes order.addresses: only schedule() must change, because it is the only function that touches the address; checkout and confirm are unchanged. The function that should have been the only one to know about addresses is schedule (and behind it delivery_date receives city and weight as plain values already).")
    para(s,"Rewrite so each function receives only what it uses:")
    bullet(s,"def checkout(payment) -> confirm(payment) - 1 parameter")
    bullet(s,"def confirm(payment) -> schedule(payment) - 1 parameter")
    bullet(s,"def schedule(city, weight_kg) -> delivery_date(city, weight_kg) - 2 parameters")
    bullet(s,"def delivery_date(city, weight_kg) - 2 parameters")
    para(s,"(In real code checkout and confirm, which add nothing, would collapse and disappear.)")
    para(s,"Choosing between six values and the Order object: six separate values keep data coupling but the call contracts grow - every time Order gains a field somebody must update the parameter lists. Passing the Order is stamp coupling - schedule and confirm stay aware of the whole type and break whenever its shape changes. Cost of data choice: long parameter lists and their maintenance; cost of stamp choice: the whole call chain is welded to the Order class.")

    h2(s, "Q32. Fewer arrows, more surprises")
    para(s,"Version 1 knows 3 modules (fines, notifier, stats); version 2 knows 1 abstraction (its listeners).")
    para(s,"Version 2 still couples to its listeners by data coupling - they read named fields of the same Loan object. If Loan loses the field they read, all three listeners break at the same call (the first loop iteration raises AttributeError inside return_book).")
    para(s,"Order: version 1 shows it literally in the body (close -> check -> tell -> record). Version 2 hides it inside the subscription order. A bug possible only in version 2: an out-of-order or duplicated subscription, for example a listener subscribed twice or after the notifier, so the next reader is told the book is free before the fine has been recorded, or receives two notifications.")
    para(s,"Two listeners that never change: keep version 1 - three explicit lines are cheaper to write, read and debug than a subscription mechanism. Twelve listeners written by five teams: version 2 - adding a listener then requires no change to Loans, so the teams do not edit, build and conflict on one shared module.")

    h2(s, "Q33. The loop of imports")
    para(s,"Import arrows: orders -> inventory (reserve), inventory -> pricing (stock_value), pricing -> orders (Order). To test one file alone it must be importable without the others: orders needs inventory and pricing; inventory needs pricing; pricing needs orders - and through that, all three. Because of the loop, in practice none of them can be tested alone.")
    para(s,"To ship pricing.py as a separate package, the Order class must travel with it (a copy or a shared base/protocol), because pricing imports it.")
    para(s,"First way - move one function: move stock_value() from pricing.py into inventory.py (inventory still can do its own logging with it):")
    bullet(s,"orders -> inventory -> (nothing); pricing -> orders. Loop broken; test order: inventory alone, orders with inventory, pricing with orders.")
    para(s,"Second way - change what discount() receives:")
    bullet(s,"def discount(level): return 0.1 if level == \"gold\" else 0.0")
    bullet(s,"arrows: orders -> inventory -> pricing -> (nothing); the caller passes order.customer.level.")
    para(s,"Order from knows nothing to knows the most (second way): pricing, inventory, orders. This gives the build a fixed bottom-up sequence and gives each module unit tests that run against nothing but the layer below it - in a loop no such order exists, so the build and the tests are interleaved and cannot be isolated.")

    h1(s, "Part H - Separation of concerns, DRY, KISS, YAGNI in depth")
    h2(s, "Q34. One rule, five places")
    tbl(s,[["Piece of knowledge","Files holding it"],["A number is valid: +998 and 9 more digits, 13 characters","registration.py (the regex), sms.py (len == 13), schema.sql (code + length), test_data.py (13-character examples)"],["A number has a leading + that must be stripped for the external gateway","sms.py"],["Public display rule: first 4 shown, rest masked","receipt.py"],["Two concrete valid formats as examples","test_data.py"]],[70*mm,108*mm])
    para(s,"No line is copied - the knowledge is repeated.")
    para(s,"Kazakhstan (+7, 12 characters): four places must be edited (registration.py, sms.py, schema.sql, test_data.py). The one that will be forgotten is test_data.py, because it is the least visible; the error shows up later as tests that still pass on old numbers while valid new numbers are rejected in production - or vice versa, valid production numbers rejected by an old test.")
    para(s,"Owner module PhoneNumbers:")
    bullet(s,"is_valid(phone) -> bool")
    bullet(s,"digits_only(phone) -> string")
    bullet(s,"mask(phone) -> string")
    bullet(s,"COUNTRY_CODE (constant)")
    para(s,"The place that cannot use it: schema.sql - the database check is plain SQL and cannot import a module, so the CHECK stays a deliberate copy.")
    para(s,"Is the remaining database check a DRY violation? No - a deliberate copy at a trust boundary is correct: the database protects against every future writer (other services, manual inserts), not just this module. Add one test that pushes a valid and an invalid number through both the module and the schema, so the two copies cannot silently drift apart.")

    h2(s, "Q35. DRY gone too far")
    para(s,"The flags create control coupling; the cohesion of calculate() is coincidental - nothing holds its parts together except one entry point; a caller can ask for 2^4 = 16 behaviours, the three callers use 3.")
    para(s,"The author followed DRY (one function for all variants) and broke KISS (a four-flag switchboard instead of clear names) and separation of concerns (pricing, tax, rounding and notification in one body).")
    para(s,"Redesign - the smallest shared piece and the three callers on top:")
    bullet(s,"def sum_products(items): return sum(i.price * i.qty for i in items)  # the only shared piece")
    bullet(s,"def quote(items): return sum_products(items)")
    bullet(s,"def invoice(items): return round_up(apply_tax(sum_products(items)))")
    bullet(s,"def refund(items): return -apply_tax(sum_products(items))")
    bullet(s,"notification is a separate call made by whoever needs it; flags left: zero")
    bullet(s,"(a) two functions checking the 13-character phone: extract one shared validator - it is the same knowledge about one format; (b) two four-line loops summing prices and weights: keep both - they are unrelated copies of a pattern that will diverge; extracting saves nothing and costs a shared dependency.")

    h2(s, "Q36. When two principles disagree")
    tbl(s,[["Situation","Disagreeing principles","My choice","The fact that would make me change sides"],["(a) 40-line VAT in two services","DRY vs decoupling / release independence","Keep two copies: sharing welds two releases together","If the law required the invoices of both services to use one identical VAT value at every moment, one shared owner would be right"],["(b) 15-line script split into five classes","KISS vs separation of concerns","Keep the script","If it becomes a monthly process several people edit and must not break, the split earns its cost"],["(c) slow get(key) on a million entries","Information hiding vs performance","Keep the secret; fix performance inside","If no internal change can be fast enough, the Cache has to publish a new bulk operation - an interface change, not a public list"]],[30*mm,42*mm,44*mm,62*mm])
    para(s,"(c) change that keeps the secret and removes the slowness: add one public bulk method, for example read_entries(batch_size) or an internal index, that reads a million entries through a controlled method while the storage layout stays private.")

    h2(s, "Q37. The arrows point the wrong way")
    para(s,"Import arrows: screens -> rules -> storage (the natural direction), and storage -> screens - the wrong arrow: Storage knows the presentation and raises an Exception carrying Uzbek error text.")
    para(s,"Concerns inside the wrong modules: storage.py contains presentation (the Uzbek message); rules.py contains presentation (HTML with <p class='red'>); screens.py adds none of its own.")
    para(s,"Telegram bot in Russian: the new bot module must copy the call structure and the knowledge of the cases (found/not found, debt) because the business result is only available as Uzbek-shaped HTML; it either parses that HTML or repeats the rule work with its own Russian answer.")
    para(s,"Redesign (no text, no HTML):")
    bullet(s,"storage.find_student(student_id) -> row/dict or raises StudentNotFound")
    bullet(s,"rules.check_in(student_id, room) -> Allowed(room) or Denied(reason) with machine reasons like 'debt'")
    bullet(s,"screens.check_in_page(form) -> maps Allowed/Denied to Uzbek HTML; the bot maps the same verdict to Russian")
    para(s,"The texts now live in the presentation modules themselves (screens.py for Uzbek, the bot for Russian); the business rules return only reason codes.")
    para(s,"Arrows after the change: screens -> rules -> storage = 2 arrows. rules.py may know about storage; screens.py may know about rules (and, on that allowed direction, storage as the layer below); storage.py may know about none of the others.")

    h1(s, "Part I - Case study: the library fines")
    h2(s, "Q38. Audit the code")
    para(s,"Evidence - copying the exact problem lines for five of the seven areas:")
    bullet(s,"Cohesion: the whole return_book method - it checks, computes, discounts, caps, stores, e-mails and prints in one body.")
    bullet(s,"Coupling: FINES = []  # global - common coupling (plus the CSV contract with MonthlyReport).")
    bullet(s,"Separation of concerns: the rule (days_late * 500, gold / 2, cap by book.price), the file write and email.send(...) live in one method.")
    bullet(s,"DRY: the CSV format written here (reader.name + ',' + ... + str(fine)) and separately re-invented by MonthlyReport's line.split(',')).")
    bullet(s,"YAGNI: total_fines() - nothing in the story or the code ever calls it.")
    para(s,"Two areas with no evidence in this code: information hiding and KISS. Information hiding: no outside module touches the private work of Library - nothing is exposed beyond the two methods and the shared files, so there is no line to cite. KISS: every individual rule line (fine = days_late * 500, gold / 2, the cap) is as simple as the rule itself - the mess of this code is cohesion, coupling and duplicated knowledge, not over-complex logic. I do not invent a problem for them because an audit that stretches for missing evidence would itself be dishonest - the honest answer is that these two principles are currently satisfied.")
    para(s,"A book titled Algorithms, Part 1: the stored line contains a comma inside the title, so MonthlyReport's line.split(',') produces more than three parts and the report crashes with a ValueError (too many values to unpack). Kind of coupling: external - two modules depend on the same outside file format. Which module is at fault and why neither is better: the Library writes without quoting and MonthlyReport splits without escaping, so each module is locally reasonable; the real fault is the missing owner of the storage format - a rule (no unquoted commas, or a quoted CSV) that belongs to a design decision written nowhere, so blaming one module is less accurate than saying the format has no owner.")
    para(s,"Restart difference: FINES is an in-process list, so after a restart total_fines() sums from zero while month_total('fines.csv') still counts every stored fine - two truths about one data set. Root cause: DRY (the same data is stored in two different places, one of which is not durable).")
    para(s,"Three changes in an order that keeps the program working after every step:")
    bullet(s,"1. Write the fine record with proper quoting (csv.writer or a separator that cannot appear in titles), and read it the same way in MonthlyReport - this alone fixes the crash for titles like Algorithms, Part 1, which is the most visible failure today.")
    bullet(s,"2. Make one store the single source of truth: the file (via a small Ledger/Repository) is written and read by everyone; FINES is removed or rebuilt from the store, so total_fines() and the report can never disagree after a restart.")
    bullet(s,"3. Keep money as whole sum integers: replace fine = fine / 2 with an integer operation (for example (days_late * 500) // 2 capped by the book price) so no receipt ever shows fractional sum.")

    h2(s, "Q39. Two designs, five changes")
    tbl(s,[["Change","Design X (4 classes)","Design Y (11 classes)"],["(a) gold discount 30%","edit FineCalculator","edit GoldDiscountRule"],["(b) new silver card 80%","edit FineCalculator","add SilverRule and register it in RuleChain"],["(c) fines in SQLite","edit FineLedger","add SqliteFineRepository, change the wiring in Library"],["(d) first three days free","edit FineCalculator","edit DaysLateRule (or add FreeDaysRule to RuleChain)"],["(e) also send an SMS","edit Notifier","add SmsChannel next to EmailChannel, change the wiring"]],[38*mm,62*mm,78*mm])
    para(s,"Arrows. X: Library -> FineCalculator, Library -> FineLedger, Library -> Notifier, MonthlyReport -> FineLedger = 4 arrows. Y: Library -> FineService; FineService -> RuleChain, FineRepository, NotificationChannel; the three rules -> FineRule; CsvFineRepository -> FineRepository; EmailChannel -> NotificationChannel; MonthlyReport -> CsvFineRepository - about 11 arrows counting every implementation-to-interface edge.")
    para(s,"Owner of the format of a stored fine: in X it is FineLedger (one visible class); in Y it is CsvFineRepository - hidden behind the FineRepository interface.")
    para(s,"I hand in Design X. The principle of Part E that Y breaks is YAGNI (with KISS right behind it): a rule-engine of interfaces and five rule classes is built for fine rules that are today one short formula. The customer's sentence that shows it: the gold discount becomes 30 percent - in X this is one number in one class, while Y's engine was never asked for. The one fact about the library that would move me toward Y: if new, quickly-changing fine rules from many independent people kept arriving every semester (staff cards, category exemptions, seasonal rules), the plugin structure would start paying for itself.")

    doc(OUT/"Muratbaev_Albert_Lab3.pdf", s)

if __name__ == "__main__":
    lab3()
    print("Created:")
    for p in sorted(OUT.glob("*.pdf")): print(p, p.stat().st_size)
