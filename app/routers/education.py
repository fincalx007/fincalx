from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["education"])
templates = Jinja2Templates(directory="app/templates")

CALCULATORS = [
    {"title": "SIP Calculator", "href": "/tools/sip-calculator"},
    {"title": "EMI Calculator", "href": "/tools/emi-calculator"},
    {"title": "Salary Calculator", "href": "/tools/salary-calculator"},
    {"title": "Portfolio Overlap Checker", "href": "/tools/portfolio-overlap-checker"},
]

GUIDES = [
    {
        "slug": "beginners-guide-to-sip-investing",
        "title": "Beginner's Guide to SIP Investing",
        "summary": "Learn how SIPs work, why regular investing helps discipline, and how to set realistic expectations before investing.",
        "calculator": CALCULATORS[0],
        "related": ["mutual-fund-basics", "compound-interest-explained", "goal-based-investing"],
        "sections": [
            ("What SIP investing means", "A Systematic Investment Plan is a way to invest a fixed amount at regular intervals, usually monthly, into a mutual fund or a similar market-linked product. SIP is not a separate investment product; it is a contribution method. The fund you choose, the asset class, the time horizon, and your behavior during market movements decide the actual experience. A beginner should treat SIP investing as a disciplined habit, not a promise of fixed returns."),
            ("Why it matters", "Many people delay investing because they wait for the perfect market level or a large lump sum. SIPs reduce that friction by turning investing into a recurring budget item. The benefit is behavioral: you start early, invest consistently, and avoid making every decision emotionally. Over long periods, regular investing can help average purchase prices, but it does not remove market risk."),
            ("Practical example", "Suppose you invest Rs. 5,000 every month for a future education goal. The first step is not selecting a high-return number; it is checking the goal amount, timeline, risk comfort, and emergency fund. You can then use the SIP calculator to test conservative, moderate, and optimistic return assumptions. If the goal is short term, an equity-heavy SIP may not be suitable even if the projected value looks attractive."),
            ("How to start responsibly", "Start by separating short-term money from long-term money. Build an emergency fund before committing all surplus to market-linked investments. Choose asset classes based on timeline: short goals usually need stability, while long goals may allow more equity exposure. Review fund documents, expense ratios, risk labels, and taxation. Automate the SIP only after confirming that the amount fits your monthly cash flow."),
            ("Common mistakes", "Beginners often chase recent top-performing funds, stop SIPs during volatility, assume high returns forever, or run too many small SIPs without a plan. Another common mistake is ignoring inflation. If a goal costs Rs. 10 lakh today, it may cost much more after ten or fifteen years. Use calculator results as estimates and revisit assumptions regularly."),
            ("FinCalX planning note", "Use the SIP calculator for projections, the compound interest guide to understand growth, and the goal-based investing guide to connect the monthly amount with a real purpose. FinCalX is educational only, so verify fund details and consult a qualified professional for personal advice."),
        ],
    },
    {
        "slug": "mutual-fund-basics",
        "title": "Mutual Fund Basics",
        "summary": "Understand mutual fund structure, NAV, expense ratio, fund categories, risk, and how to evaluate funds with context.",
        "calculator": CALCULATORS[0],
        "related": ["beginners-guide-to-sip-investing", "goal-based-investing", "personal-finance-mistakes-to-avoid"],
        "sections": [
            ("What a mutual fund is", "A mutual fund pools money from many investors and invests it according to a stated objective. The portfolio may include equity shares, bonds, money market instruments, gold, or a mix of assets. Professional managers make investment decisions, while investors own units. The value of each unit is represented by NAV, or Net Asset Value."),
            ("Important terms", "NAV tells you the per-unit value of the fund, but it is not the same as stock price attractiveness. Expense ratio is the annual cost charged by the fund. Exit load may apply if you redeem too early. Direct plans usually have lower expense ratios than regular plans because they do not include distributor commission. Growth and IDCW options differ in how returns are reflected."),
            ("Types of funds", "Equity funds primarily invest in stocks and are usually suited for longer horizons. Debt funds invest in bonds and money market instruments but still carry credit and interest-rate risk. Hybrid funds combine asset classes. Index funds track a benchmark. ELSS funds are tax-saving equity funds with a lock-in period. Each category has a different role in planning."),
            ("Practical example", "If you are investing for retirement in twenty years, an equity or index fund may be part of the plan, depending on risk comfort. If you need money in one year for a fee payment, a volatile equity fund may be unsuitable. The right fund is not simply the fund with the highest recent return; it is the fund that matches the goal, risk, and time horizon."),
            ("Common mistakes", "Investors often collect too many funds, compare funds across unrelated categories, ignore expense ratios, or treat past returns as future certainty. Some also overlook taxation and exit loads. Portfolio overlap matters because five funds may still own many of the same companies. Use the overlap checker to screen duplication."),
            ("FinCalX planning note", "Use the SIP calculator to test monthly investment assumptions and the portfolio overlap checker to review duplication. Read the SIP, asset allocation, and diversification glossary entries before choosing funds."),
        ],
    },
    {
        "slug": "understanding-emi",
        "title": "Understanding EMI",
        "summary": "Learn how EMI is calculated, why total interest matters, and how tenure changes affordability.",
        "calculator": CALCULATORS[1],
        "related": ["home-loan-planning", "budgeting-fundamentals", "emi-vs-renting"],
        "sections": [
            ("What EMI means", "EMI stands for Equated Monthly Instalment. It is the regular payment made to repay a loan over a fixed period. Each EMI usually contains an interest portion and a principal repayment portion. In the early years of many loans, interest can form a large part of the EMI."),
            ("Why it matters", "Borrowers often focus only on whether the monthly EMI is affordable. That is important, but incomplete. A longer tenure can reduce EMI and make the loan feel comfortable, while increasing the total interest paid over the life of the loan. A shorter tenure can reduce total interest but may strain monthly cash flow."),
            ("Practical example", "A home loan of Rs. 40 lakh at a fixed annual rate may produce very different total repayments at 15 years versus 25 years. The longer loan may look easier every month, but the total interest burden can be much higher. Use the EMI calculator to compare both monthly commitment and total repayment before deciding."),
            ("How to use EMI responsibly", "Estimate EMI before applying for a loan, then compare it with stable monthly income and essential expenses. Keep space for emergency fund contributions, insurance, school fees, medical costs, and periodic repairs. If the EMI leaves no flexibility, the loan may be financially stressful even if a lender approves it."),
            ("Common mistakes", "Common mistakes include ignoring processing fees, assuming floating rates will never rise, stretching tenure without reviewing total interest, and using future bonuses to justify present borrowing. Some borrowers also forget that home ownership has maintenance, registration, insurance, and furnishing costs."),
            ("FinCalX planning note", "Use the EMI calculator as an affordability screen, then read the home loan planning guide and budget checklist. Final decisions should be based on official lender documents and qualified advice."),
        ],
    },
    {
        "slug": "home-loan-planning",
        "title": "Home Loan Planning",
        "summary": "Plan a home purchase with down payment, EMI comfort, additional costs, risk buffers, and documentation checks.",
        "calculator": CALCULATORS[1],
        "related": ["understanding-emi", "budgeting-fundamentals", "emergency-fund-planning"],
        "sections": [
            ("Start with affordability", "Home loan planning should begin before property shortlisting. Estimate how much EMI your monthly cash flow can support without stopping savings or emergency planning. A lender may approve a larger loan than you personally feel comfortable carrying."),
            ("Down payment and costs", "The purchase price is only one part of the cost. Registration, stamp duty, brokerage, legal checks, interiors, moving, maintenance deposits, insurance, and repairs can materially increase the cash needed. Keep these outside the loan estimate so you do not use the entire emergency fund for the purchase."),
            ("Practical example", "If your target home costs Rs. 80 lakh, a 20% down payment is Rs. 16 lakh before transaction costs. If transaction and setup costs add several lakh more, the real upfront requirement may be higher. Use the EMI calculator on the likely loan amount, not the property price."),
            ("Risk planning", "A home loan is a long commitment. Check whether the EMI still works if income falls, rates rise, or one earner takes a break. Keep insurance and emergency fund planning separate. Avoid relying only on future salary hikes to make the EMI comfortable."),
            ("Common mistakes", "Buyers often stretch budgets for a better location, underestimate furnishing costs, ignore floating-rate risk, and skip legal verification. Another mistake is comparing rent and EMI without considering down payment opportunity cost, property tax, maintenance, and liquidity."),
            ("FinCalX planning note", "Use the EMI calculator, home buying checklist, budgeting guide, and emergency fund guide together. FinCalX does not provide lending advice; verify all numbers with the bank and relevant professionals."),
        ],
    },
    {
        "slug": "tax-planning-basics",
        "title": "Tax Planning Basics",
        "summary": "Understand tax planning as a yearly cash-flow habit, not a last-minute product purchase.",
        "calculator": CALCULATORS[2],
        "related": ["salary-structure-explained", "elss-vs-ppf", "nps-vs-ppf"],
        "sections": [
            ("What tax planning means", "Tax planning means arranging income, deductions, declarations, investments, and documentation in a lawful and organized way. It is not about hiding income or buying random products in March. Good tax planning begins with understanding your salary structure, regime choice, eligible deductions, and cash-flow needs."),
            ("Why it matters", "Taxes affect take-home pay, investment choices, insurance decisions, and year-end liquidity. A last-minute tax-saving purchase may reduce tax but create a product mismatch. For example, a long lock-in product may not suit a short-term goal even if it offers deduction benefits."),
            ("Practical example", "A salaried employee comparing old and new regimes should estimate taxable income, deductions, HRA, standard deduction, employer contributions, and planned investments. The decision can change with salary level, rent, home loan interest, and eligible deductions. Use the salary calculator to understand cash-flow assumptions, then verify with official tax rules or a tax professional."),
            ("Documentation habit", "Keep rent receipts, investment proofs, Form 16, insurance receipts, loan certificates, donation receipts, and capital gains statements organized during the year. Documentation reduces stress during employer declaration windows and tax filing."),
            ("Common mistakes", "Common mistakes include choosing tax-saving products without understanding risk, missing employer declaration deadlines, ignoring tax on investment gains, assuming old advice still applies after rule changes, and treating online estimates as filing advice."),
            ("FinCalX planning note", "FinCalX provides educational planning resources only. Use the salary calculator for rough cash-flow estimates and consult qualified tax professionals or official sources before filing or making tax decisions."),
        ],
    },
    {
        "slug": "salary-structure-explained",
        "title": "Salary Structure Explained",
        "summary": "Decode CTC, basic salary, HRA, PF, allowances, variable pay, deductions, and monthly in-hand salary.",
        "calculator": CALCULATORS[2],
        "related": ["tax-planning-basics", "budgeting-fundamentals", "smart-saving-strategies"],
        "sections": [
            ("CTC versus in-hand salary", "CTC is the total cost an employer associates with your compensation. In-hand salary is the amount credited after deductions and payroll rules. CTC may include employer PF contribution, gratuity, insurance, bonuses, reimbursements, and benefits that are not monthly cash."),
            ("Key components", "Basic salary influences PF, gratuity, HRA, and other benefits. HRA may matter for rent-related tax treatment. Allowances can be fixed or reimbursement-based. Variable pay may depend on company and individual performance. Deductions may include PF, professional tax, insurance, and income-tax withholding."),
            ("Practical example", "Two offers with the same CTC can produce different monthly in-hand amounts. One may have high variable pay and benefits, while another may have higher fixed cash. Use the salary calculator to test basic, HRA, PF, tax, and allowance assumptions before accepting an offer."),
            ("How to review an offer", "Ask for fixed pay, variable pay conditions, joining bonus clawback, employer contributions, insurance deductions, reimbursement process, pay cycle, and tax declaration timelines. A clear salary breakup helps you budget realistically."),
            ("Common mistakes", "Common mistakes include treating variable pay as guaranteed cash, ignoring PF and tax withholding, comparing CTC without checking monthly fixed pay, and building a lifestyle budget around annual numbers instead of credited salary."),
            ("FinCalX planning note", "Use the salary calculator for estimates, then confirm actual payroll treatment with HR. For tax decisions, consult a qualified tax professional."),
        ],
    },
    {
        "slug": "budgeting-fundamentals",
        "title": "Budgeting Fundamentals",
        "summary": "Create a practical budget that balances essentials, goals, flexibility, and emergency preparation.",
        "calculator": CALCULATORS[2],
        "related": ["emergency-fund-planning", "smart-saving-strategies", "salary-structure-explained"],
        "sections": [
            ("What a budget does", "A budget is a decision system for your money. It helps you assign income to essentials, goals, debt payments, insurance, savings, and lifestyle spending before the month disappears. A good budget is realistic and repeatable, not a punishment plan."),
            ("Why it matters", "Without a budget, financial decisions become reactive. You may invest while carrying expensive debt, borrow without an emergency fund, or overspend after a salary increase. Budgeting reveals whether goals are supported by actual cash flow."),
            ("Practical example", "Start with monthly in-hand salary. List rent, utilities, groceries, transport, EMIs, insurance, subscriptions, family support, and irregular expenses. Then allocate savings and investments. If nothing remains, the issue is not discipline alone; the plan may need expense cuts, income improvement, or goal reprioritization."),
            ("Budgeting method", "Many users begin with broad buckets: needs, goals, wants, and buffers. The exact ratio can vary by city, family size, debt, and income stability. Track for two or three months before making strict rules. Include annual expenses like insurance renewals and school fees as monthly sinking funds."),
            ("Common mistakes", "Common mistakes include budgeting from CTC instead of in-hand salary, ignoring annual expenses, leaving no fun money, and treating every surplus as spendable. A budget with no flexibility is often abandoned."),
            ("FinCalX planning note", "Use the salary calculator, monthly budget planner, emergency fund checklist, and smart saving strategies guide together. Keep sensitive account details out of any online tool."),
        ],
    },
    {
        "slug": "emergency-fund-planning",
        "title": "Emergency Fund Planning",
        "summary": "Build a cash safety buffer for job loss, medical costs, urgent repairs, and family emergencies.",
        "calculator": CALCULATORS[2],
        "related": ["budgeting-fundamentals", "smart-saving-strategies", "home-loan-planning"],
        "sections": [
            ("What an emergency fund is", "An emergency fund is money kept aside for unexpected events, not for vacations, gadgets, or planned purchases. It protects your long-term investments from forced withdrawals and reduces dependence on high-cost debt."),
            ("How much to keep", "A common starting point is three to six months of essential expenses. People with variable income, dependents, loans, or single-income households may need more. The right amount depends on job stability, family responsibilities, health coverage, and debt obligations."),
            ("Practical example", "If monthly essentials are Rs. 60,000 including rent, groceries, utilities, insurance, and EMIs, a six-month fund is Rs. 3.6 lakh. This does not mean you need it tomorrow. Build it gradually using automatic transfers after salary credit."),
            ("Where to keep it", "Emergency money should be accessible and relatively stable. Avoid locking the entire amount in risky or illiquid products. Some people split it between a savings account, liquid fund, and short-term deposit. Understand risks and access times before choosing."),
            ("Common mistakes", "Common mistakes include investing emergency money in volatile assets, counting credit-card limits as emergency funds, using the fund for routine spending, and never rebuilding it after withdrawal."),
            ("FinCalX planning note", "Use the salary calculator to estimate monthly cash flow and the budget checklist to identify essential expenses. FinCalX does not recommend products; choose based on safety, access, and suitability."),
        ],
    },
    {
        "slug": "retirement-planning-basics",
        "title": "Retirement Planning Basics",
        "summary": "Understand retirement corpus planning, inflation, asset allocation, withdrawal risk, and review discipline.",
        "calculator": CALCULATORS[0],
        "related": ["inflation-explained", "compound-interest-explained", "wealth-building-fundamentals"],
        "sections": [
            ("Why retirement planning starts early", "Retirement planning is the process of building resources for years when active income may reduce or stop. Starting early gives compounding more time, but the plan still needs realistic assumptions, inflation adjustment, asset allocation, and periodic review."),
            ("Inflation and lifestyle", "A retirement corpus should be based on future expenses, not today&apos;s expenses. Medical costs, rent, travel, dependents, and lifestyle choices can change the required amount. Inflation can make a comfortable present budget inadequate in later years."),
            ("Practical example", "If your current annual expenses are Rs. 8 lakh, the future cost after decades may be many times higher depending on inflation. A SIP projection can show one possible accumulation path, but you also need to think about risk, asset mix, and post-retirement withdrawals."),
            ("Building blocks", "Retirement planning often combines EPF, PPF, NPS, mutual funds, deposits, insurance protection, and debt-free living. The mix depends on risk comfort, tax rules, job type, and family needs. Avoid putting all retirement hopes into one product."),
            ("Common mistakes", "Common mistakes include delaying investing, underestimating healthcare costs, assuming children will fund retirement, ignoring inflation, and redeeming retirement investments for short-term wants."),
            ("FinCalX planning note", "Use the SIP calculator, retirement checklist, inflation guide, and compound interest guide to frame assumptions. Consult qualified professionals for a personalized retirement plan."),
        ],
    },
    {
        "slug": "inflation-explained",
        "title": "Inflation Explained",
        "summary": "Learn how rising prices affect savings, salary, goals, retirement, and investment planning.",
        "calculator": CALCULATORS[0],
        "related": ["retirement-planning-basics", "goal-based-investing", "smart-saving-strategies"],
        "sections": [
            ("What inflation means", "Inflation is the rise in prices over time. When inflation rises, the same amount of money buys fewer goods and services. In personal finance, inflation matters because goals that look affordable today may become expensive in the future."),
            ("Why it matters", "Inflation affects education costs, rent, medical care, groceries, travel, and retirement. If your savings grow slower than inflation, purchasing power falls even if the bank balance increases. This is why long-term plans should compare expected returns with expected inflation."),
            ("Practical example", "A goal costing Rs. 10 lakh today may cost much more after ten years. If you invest based only on today&apos;s cost, you may fall short. When using a SIP calculator, estimate the future goal value first, then calculate the monthly investment needed."),
            ("How to plan around it", "Keep short-term money stable, but use growth assets carefully for long-term goals where suitable. Increase SIPs as income rises. Review goals annually and adjust assumptions when actual prices change."),
            ("Common mistakes", "Common mistakes include keeping all long-term savings in low-return products, ignoring lifestyle inflation after salary hikes, and using old goal amounts for future planning."),
            ("FinCalX planning note", "Read the compound interest guide, goal-based investing guide, and retirement checklist. FinCalX projections are educational and depend on user assumptions."),
        ],
    },
    {
        "slug": "compound-interest-explained",
        "title": "Compound Interest Explained",
        "summary": "Understand how compounding works, why time matters, and why assumptions should stay realistic.",
        "calculator": CALCULATORS[0],
        "related": ["beginners-guide-to-sip-investing", "inflation-explained", "wealth-building-fundamentals"],
        "sections": [
            ("What compounding means", "Compounding happens when returns start earning returns. Over time, the growth can become larger than the original contribution, especially when money remains invested for long periods. Compounding is powerful, but it depends on time, rate, consistency, and risk."),
            ("Why time matters", "The earlier money starts working, the longer it has to compound. A smaller amount invested for many years can sometimes compete with a larger amount started much later. However, market-linked compounding is uneven; returns do not arrive in a smooth line."),
            ("Practical example", "A monthly SIP for fifteen or twenty years can show how contributions and estimated returns separate over time. The SIP calculator helps visualize this, but the return assumption is not guaranteed. Try lower assumptions to understand downside planning."),
            ("How to use the idea", "Use compounding for long-term goals, but do not force short-term money into volatile assets just to chase growth. Increase contributions gradually, avoid unnecessary withdrawals, and keep costs and taxes in mind."),
            ("Common mistakes", "Common mistakes include expecting high returns every year, ignoring fees, stopping investments during market declines, and confusing nominal returns with inflation-adjusted returns."),
            ("FinCalX planning note", "Use this guide with SIP investing, inflation, and retirement planning resources. Results are educational estimates and should not be treated as promises."),
        ],
    },
    {
        "slug": "goal-based-investing",
        "title": "Goal-Based Investing",
        "summary": "Turn vague investing into purpose-led planning for education, home, retirement, travel, and other goals.",
        "calculator": CALCULATORS[0],
        "related": ["inflation-explained", "beginners-guide-to-sip-investing", "retirement-planning-basics"],
        "sections": [
            ("What goal-based investing means", "Goal-based investing starts with a purpose, amount, and timeline before choosing products. Instead of asking where to invest generally, you ask what the money is for and when it is needed."),
            ("Why it matters", "Different goals need different risk levels. A three-year home down payment and a twenty-five-year retirement goal should not be planned the same way. The timeline affects asset allocation, liquidity, and expected return assumptions."),
            ("Practical example", "For a child education goal due in twelve years, estimate today&apos;s cost, adjust for inflation, and calculate monthly investing needs. As the goal approaches, reduce risk gradually if suitable. The SIP calculator can estimate accumulation, but the investment choice should match the goal."),
            ("Building the plan", "List each goal separately with target date, current cost, future estimated cost, existing savings, and monthly contribution. Review annually. If income changes, update priority instead of abandoning the whole plan."),
            ("Common mistakes", "Common mistakes include mixing all goals into one investment, redeeming long-term funds for short-term wants, and using return assumptions without considering risk."),
            ("FinCalX planning note", "Use the investment goal planner, SIP calculator, and financial goal checklist to connect estimates with action steps."),
        ],
    },
    {
        "slug": "personal-finance-mistakes-to-avoid",
        "title": "Personal Finance Mistakes to Avoid",
        "summary": "Avoid common traps around debt, investing, budgeting, tax, insurance, and lifestyle inflation.",
        "calculator": CALCULATORS[2],
        "related": ["budgeting-fundamentals", "emergency-fund-planning", "wealth-building-fundamentals"],
        "sections": [
            ("Mistake one: no emergency fund", "Investing without an emergency fund can force you to sell assets at the wrong time. Keep a separate cash buffer for genuine emergencies before taking aggressive long-term positions."),
            ("Mistake two: lifestyle inflation", "Income increases can disappear into subscriptions, upgrades, dining, and impulse purchases. Enjoy raises, but assign part of every increase to savings, insurance, and debt reduction."),
            ("Mistake three: product-first planning", "Many people buy products before defining goals. A tax-saving product, fund, or loan should fit a need. Start with the objective, timeline, risk, and liquidity requirement."),
            ("Mistake four: ignoring total cost", "For loans, total repayment matters. For investments, expenses, taxes, and exit loads matter. For salary, in-hand cash matters more than headline CTC."),
            ("Mistake five: no review", "Financial plans drift. Review budgets monthly, investments periodically, insurance annually, and goals after major life events. Small corrections are easier than late emergency fixes."),
            ("FinCalX planning note", "Use calculators as prompts for better questions. FinCalX is educational and does not replace professional advice."),
        ],
    },
    {
        "slug": "wealth-building-fundamentals",
        "title": "Wealth Building Fundamentals",
        "summary": "Build wealth through income, savings rate, risk management, asset allocation, patience, and review.",
        "calculator": CALCULATORS[0],
        "related": ["compound-interest-explained", "smart-saving-strategies", "retirement-planning-basics"],
        "sections": [
            ("What long-term financial planning means", "Long-term financial planning is the repeated process of earning, saving, investing, protecting, and reviewing. It is less about one perfect product and more about consistent decisions over many years."),
            ("Savings rate", "Your savings rate is the portion of income directed toward future needs. A high return cannot fully compensate for very low savings. Start with a realistic monthly amount and increase it as income grows."),
            ("Risk management", "Insurance, emergency funds, debt control, and diversification protect the plan. Wealth building can fail when one emergency forces expensive borrowing or distressed selling."),
            ("Practical example", "A salaried professional may allocate money to emergency fund, term insurance, health insurance, retirement investing, short-term deposits, and goal-based SIPs. The exact split depends on family and risk profile."),
            ("Common mistakes", "Common mistakes include chasing short-term speculation, taking loans for lifestyle purchases, ignoring asset allocation, and stopping investments when markets are uncomfortable."),
            ("FinCalX planning note", "Use the wealth roadmap, SIP calculator, budget planner, and glossary together to build financial literacy step by step."),
        ],
    },
    {
        "slug": "smart-saving-strategies",
        "title": "Smart Saving Strategies",
        "summary": "Save more without extreme restriction using automation, sinking funds, spending rules, and goal clarity.",
        "calculator": CALCULATORS[2],
        "related": ["budgeting-fundamentals", "emergency-fund-planning", "wealth-building-fundamentals"],
        "sections": [
            ("Make saving automatic", "The simplest saving strategy is to move money before it becomes spendable. Automate transfers after salary credit for emergency fund, investments, and sinking funds."),
            ("Use sinking funds", "Annual insurance, festivals, school fees, repairs, and travel are not surprises if they happen every year. Divide expected costs by twelve and save monthly."),
            ("Reduce invisible leakage", "Review subscriptions, delivery fees, impulse purchases, bank charges, and unused memberships. Small leaks matter because they repeat."),
            ("Practical example", "If you need Rs. 60,000 for annual insurance, set aside Rs. 5,000 per month. This prevents one month from becoming stressful and protects investments from withdrawal."),
            ("Common mistakes", "Common mistakes include saving whatever remains at month end, keeping goals vague, and cutting all enjoyable spending until the plan becomes unsustainable."),
            ("FinCalX planning note", "Use the monthly budget planner, salary calculator, and emergency checklist to turn savings into a repeatable system."),
        ],
    },
]

COMPARISONS = [
    ("sip-vs-lumpsum", "SIP vs Lumpsum", "SIP suits gradual investing and cash-flow discipline, while lumpsum investing suits available capital and longer market exposure when risk tolerance permits.", "SIP", "Lumpsum", CALCULATORS[0]),
    ("ppf-vs-sip", "PPF vs SIP", "PPF is a government-backed fixed-income savings option, while SIP is a method for investing regularly in market-linked funds.", "PPF", "SIP", CALCULATORS[0]),
    ("fd-vs-mutual-funds", "FD vs Mutual Funds", "Fixed deposits prioritize stability and known interest, while mutual funds vary by asset class and carry market or credit risk.", "FD", "Mutual Funds", CALCULATORS[0]),
    ("equity-vs-debt-funds", "Equity vs Debt Funds", "Equity funds focus on stocks and growth potential, while debt funds invest in bonds and money market instruments with different risks.", "Equity Funds", "Debt Funds", CALCULATORS[3]),
    ("emi-vs-renting", "EMI vs Renting", "EMI builds ownership but needs down payment and long commitment; renting offers flexibility but does not create property ownership.", "EMI", "Renting", CALCULATORS[1]),
    ("elss-vs-ppf", "ELSS vs PPF", "ELSS is a tax-saving equity mutual fund with market risk, while PPF is a long-term government-backed savings scheme.", "ELSS", "PPF", CALCULATORS[0]),
    ("nps-vs-ppf", "NPS vs PPF", "NPS is retirement-focused with market-linked allocation choices, while PPF is a fixed-income long-term savings option.", "NPS", "PPF", CALCULATORS[0]),
]

CHECKLISTS = [
    ("retirement-planning-checklist", "Retirement Planning Checklist", ["Estimate future monthly expenses with inflation.", "List EPF, PPF, NPS, mutual funds, deposits, and insurance.", "Review asset allocation by age and risk comfort.", "Plan healthcare and emergency buffers.", "Review the corpus and SIP assumptions every year."]),
    ("investment-planning-checklist", "Investment Planning Checklist", ["Define each goal, amount, and timeline.", "Separate emergency money from investments.", "Match asset class with time horizon.", "Check costs, tax, liquidity, and risk.", "Review portfolio overlap and rebalance periodically."]),
    ("budget-planning-checklist", "Budget Planning Checklist", ["Use in-hand salary, not CTC.", "Track essentials, goals, wants, and irregular expenses.", "Create sinking funds for annual costs.", "Automate savings after salary credit.", "Review spending monthly without guilt or guesswork."]),
    ("home-buying-checklist", "Home Buying Checklist", ["Estimate down payment and transaction costs.", "Calculate EMI against stable income.", "Check legal documents and lender terms.", "Keep emergency fund separate from purchase cash.", "Plan maintenance, insurance, interiors, and moving costs."]),
    ("salary-planning-checklist", "Salary Planning Checklist", ["Compare fixed pay, variable pay, and benefits.", "Estimate PF, tax, insurance, and professional tax deductions.", "Confirm reimbursement and bonus rules.", "Budget from monthly in-hand salary.", "Update tax declarations on time."]),
    ("emergency-fund-checklist", "Emergency Fund Checklist", ["Calculate essential monthly expenses.", "Target three to six months as a starting range.", "Keep money accessible and relatively stable.", "Use only for genuine emergencies.", "Rebuild the fund after withdrawals."]),
    ("financial-goal-planning-checklist", "Financial Goal Planning Checklist", ["Write the goal name and date.", "Estimate future cost after inflation.", "Map existing savings and monthly gap.", "Choose suitable assets by timeline.", "Review progress at least annually."]),
]

VALUE_TOOLS = [
    ("investment-goal-planner", "Investment Goal Planner", "Estimate a goal, target date, current savings, and monthly contribution gap before using the SIP calculator."),
    ("financial-health-score", "Financial Health Score", "Review emergency fund, debt load, insurance, savings rate, and goal clarity with a simple self-check."),
    ("monthly-budget-planner", "Monthly Budget Planner", "Organize in-hand income into essentials, EMIs, savings, goals, and flexible spending."),
    ("beginner-finance-roadmap", "Beginner Finance Roadmap", "Move from budgeting and emergency fund basics to insurance, investing, tax planning, and review."),
    ("financial-learning-path", "Financial Learning Path", "A guided order for reading FinCalX guides from salary and budgeting to SIPs and retirement."),
    ("savings-challenge-guide", "Savings Challenge Guide", "Use weekly, monthly, and no-spend challenges to build a saving habit without pressure."),
    ("wealth-building-roadmap", "Wealth Building Roadmap", "A staged roadmap covering cash flow, protection, investing, asset allocation, and reviews."),
    ("personal-finance-checklist-center", "Personal Finance Checklist Center", "A hub for routine financial review checklists across salary, budget, debt, goals, and investing."),
]

GLOSSARY_TERMS = [
    "SIP", "CAGR", "XIRR", "EMI", "NAV", "PPF", "EPF", "NPS", "ELSS", "Asset Allocation", "Inflation", "Liquidity", "Diversification", "Debt Fund", "Equity Fund", "Taxable Income", "Compounding", "Expense Ratio", "Exit Load", "Index Fund", "Hybrid Fund", "Large Cap", "Mid Cap", "Small Cap", "Flexi Cap Fund", "Direct Plan", "Regular Plan", "Growth Option", "IDCW", "Capital Gains", "Short Term Capital Gain", "Long Term Capital Gain", "Standard Deduction", "HRA", "Basic Salary", "CTC", "In-hand Salary", "Professional Tax", "TDS", "Form 16", "Emergency Fund", "Term Insurance", "Health Insurance", "Credit Score", "Principal", "Interest Rate", "Tenure", "Prepayment", "Foreclosure", "Processing Fee", "Floating Rate", "Fixed Rate", "Amortization", "Down Payment", "Loan-to-Value", "Risk Tolerance", "Time Horizon", "Goal Planning", "Rebalancing", "Portfolio Overlap", "Benchmark", "Tracking Error", "Alpha", "Beta", "Volatility", "Drawdown", "Rupee Cost Averaging", "Lumpsum", "Annuity", "Retirement Corpus", "Withdrawal Rate", "Sinking Fund", "Budget", "Net Worth", "Assets", "Liabilities", "Cash Flow", "Opportunity Cost", "Tax Deduction", "Tax Exemption", "Section 80C", "Section 80D", "Gratuity", "Bonus", "Allowance", "Reimbursement", "Yield", "Credit Risk", "Interest Rate Risk", "Maturity", "Nominee", "KYC", "PAN", "Aadhaar", "Financial Goal", "Savings Rate", "Real Return", "Nominal Return", "Corpus", "Asset Class",
]


TERM_EXPLANATIONS = {
    "SIP": ("A Systematic Investment Plan is a scheduled way to invest a fixed amount, usually monthly.", "If you invest Rs. 5,000 every month in a mutual fund, that recurring contribution is a SIP."),
    "CAGR": ("Compound Annual Growth Rate shows the smoothed annual growth rate over a period.", "If an investment grows from Rs. 1 lakh to Rs. 2 lakh over several years, CAGR describes the annualized pace of that growth."),
    "XIRR": ("XIRR estimates annualized return when investments or withdrawals happen on different dates.", "Multiple SIP instalments and a final redemption are better reviewed with XIRR than a simple average return."),
    "EMI": ("Equated Monthly Instalment is the fixed monthly repayment for a loan under a selected rate and tenure.", "A home loan EMI includes interest and principal repayment across the loan schedule."),
    "NAV": ("Net Asset Value is the per-unit value of a mutual fund scheme after accounting for assets and liabilities.", "When a fund NAV changes from Rs. 20 to Rs. 22, each unit value has moved, but NAV alone does not show whether the fund is cheap."),
    "PPF": ("Public Provident Fund is a long-term government-backed savings scheme with tax-related features.", "A conservative investor may use PPF for long-term fixed-income allocation, subject to lock-in and rules."),
    "EPF": ("Employees' Provident Fund is a retirement savings arrangement for eligible salaried employees.", "A portion of salary and employer contribution can accumulate in EPF during employment."),
    "NPS": ("National Pension System is a retirement-focused savings framework with market-linked allocation choices.", "An investor may use NPS as one part of retirement planning alongside EPF, PPF, and mutual funds."),
    "ELSS": ("Equity Linked Savings Scheme is a tax-saving equity mutual fund category with a lock-in period.", "An ELSS investment may offer tax deduction eligibility, but its returns remain market-linked."),
    "Asset Allocation": ("Asset allocation is the split of money across asset classes such as equity, debt, gold, and cash.", "A long-term goal may hold more equity, while a near-term goal may need more stable assets."),
    "Inflation": ("Inflation is the rise in prices over time, reducing purchasing power.", "A goal costing Rs. 10 lakh today may need a larger corpus after ten years."),
    "Liquidity": ("Liquidity describes how quickly and reliably an asset can be converted into usable cash.", "Emergency funds need high liquidity; retirement investments can usually accept less liquidity."),
    "Diversification": ("Diversification spreads money across assets, sectors, or instruments to reduce concentration.", "Owning several funds with the same top holdings may not provide true diversification."),
    "Compounding": ("Compounding is growth on both the original money and earlier returns.", "Long SIP tenures can show how estimated returns may become larger than contributions over time."),
    "CTC": ("Cost to Company is the total annual compensation cost associated with an employee.", "A Rs. 12 lakh CTC may include benefits and employer contributions that are not monthly cash."),
    "In-hand Salary": ("In-hand salary is the amount actually received after deductions and payroll adjustments.", "Budgeting should use monthly in-hand salary rather than headline CTC."),
    "Portfolio Overlap": ("Portfolio overlap measures repeated holdings across funds or portfolios.", "Two funds may both hold TCS and Infosys, increasing duplication in your portfolio."),
}


def _term_copy(term: str) -> dict:
    if term in TERM_EXPLANATIONS:
        definition, example = TERM_EXPLANATIONS[term]
    elif "Fund" in term or term in {"Index Fund", "Hybrid Fund", "Direct Plan", "Regular Plan", "Growth Option", "IDCW", "Benchmark", "Tracking Error", "Alpha", "Beta"}:
        definition = f"{term} is a mutual fund or portfolio concept used to evaluate fund structure, cost, risk, or performance context."
        example = f"Before choosing a scheme, review {term} along with goal timeline, expense ratio, taxation, and portfolio fit."
    elif term in {"Principal", "Interest Rate", "Tenure", "Prepayment", "Foreclosure", "Processing Fee", "Floating Rate", "Fixed Rate", "Amortization", "Down Payment", "Loan-to-Value"}:
        definition = f"{term} is a borrowing term that affects EMI, total repayment, affordability, or lender conditions."
        example = f"When comparing loan offers, check how {term} changes monthly EMI and total cost."
    elif term in {"Taxable Income", "TDS", "Form 16", "Tax Deduction", "Tax Exemption", "Section 80C", "Section 80D", "Standard Deduction", "Capital Gains", "Short Term Capital Gain", "Long Term Capital Gain"}:
        definition = f"{term} is a tax-planning concept that can affect liability, documentation, or eligible benefits."
        example = f"Use {term} as a prompt to verify rules with official sources or a qualified tax professional."
    elif term in {"Basic Salary", "HRA", "Professional Tax", "Gratuity", "Bonus", "Allowance", "Reimbursement"}:
        definition = f"{term} is a salary-structure component that can affect take-home pay, benefits, tax treatment, or cash flow."
        example = f"Two job offers with similar CTC can differ meaningfully because of {term}."
    elif term in {"Emergency Fund", "Sinking Fund", "Budget", "Net Worth", "Assets", "Liabilities", "Cash Flow", "Savings Rate", "Financial Goal", "Goal Planning"}:
        definition = f"{term} is a planning concept used to organize money around stability, goals, and everyday decisions."
        example = f"Review {term} monthly or after major life changes so your plan stays realistic."
    elif term in {"Risk Tolerance", "Time Horizon", "Rebalancing", "Volatility", "Drawdown", "Credit Risk", "Interest Rate Risk", "Real Return", "Nominal Return"}:
        definition = f"{term} helps describe investment risk, return expectations, or suitability for a goal."
        example = f"A long-term investor may treat {term} differently from someone saving for a near-term expense."
    else:
        definition = f"{term} is a finance term that affects how people save, invest, borrow, protect income, or plan goals."
        example = f"Before making a decision, connect {term} with your timeline, liquidity need, tax position, and risk comfort."
    return {
        "term": term,
        "definition": definition,
        "simple": f"In simple words, {term} is useful because it turns a vague money decision into a clearer planning question.",
        "example": example,
    }


def _guide_by_slug(slug: str):
    return next((guide for guide in GUIDES if guide["slug"] == slug), None)


@router.get("/learning-center", response_class=HTMLResponse)
async def learning_center(request: Request):
    return templates.TemplateResponse("education/learning_center.html", {"request": request, "title": "Finance Learning Center | FinCalX", "description": "Original personal finance guides for SIP investing, EMI planning, budgeting, tax basics, salary structure, retirement, and wealth building.", "guides": GUIDES, "calculators": CALCULATORS})


@router.get("/learning-center/{slug}", response_class=HTMLResponse)
async def guide_detail(request: Request, slug: str):
    guide = _guide_by_slug(slug)
    if guide is None:
        raise HTTPException(status_code=404)
    related_guides = [_guide_by_slug(item) for item in guide["related"] if _guide_by_slug(item)]
    return templates.TemplateResponse("education/guide.html", {"request": request, "title": f"{guide['title']} | FinCalX Guide", "description": guide["summary"], "guide": guide, "related_guides": related_guides, "calculators": CALCULATORS})


@router.get("/finance-glossary", response_class=HTMLResponse)
async def finance_glossary(request: Request):
    terms = []
    for i, term in enumerate(GLOSSARY_TERMS):
        item = _term_copy(term)
        item["calculator"] = CALCULATORS[i % len(CALCULATORS)]
        item["guide"] = GUIDES[i % len(GUIDES)]
        terms.append(item)
    return templates.TemplateResponse("education/glossary.html", {"request": request, "title": "Financial Glossary | 95+ Personal Finance Terms | FinCalX", "description": "A plain-English finance glossary with definitions, examples, related calculators, and related learning guides.", "terms": terms})


@router.get("/comparison-guides", response_class=HTMLResponse)
async def comparison_guides(request: Request):
    return templates.TemplateResponse("education/comparisons.html", {"request": request, "title": "Finance Comparison Guides | FinCalX", "description": "Compare SIP vs lumpsum, PPF vs SIP, FD vs mutual funds, equity vs debt funds, EMI vs renting, ELSS vs PPF, and NPS vs PPF.", "comparisons": COMPARISONS})


@router.get("/comparison-guides/{slug}", response_class=HTMLResponse)
async def comparison_detail(request: Request, slug: str):
    comparison = next((item for item in COMPARISONS if item[0] == slug), None)
    if comparison is None:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("education/comparison_detail.html", {"request": request, "title": f"{comparison[1]} | FinCalX Comparison Guide", "description": comparison[2], "comparison": comparison, "calculators": CALCULATORS})


@router.get("/financial-planning-resources", response_class=HTMLResponse)
async def planning_resources(request: Request):
    return templates.TemplateResponse("education/planning.html", {"request": request, "title": "Financial Planning Resources & Checklists | FinCalX", "description": "Printable-friendly personal finance checklists for retirement, investing, budgeting, home buying, salary planning, emergency funds, and goals.", "checklists": CHECKLISTS, "calculators": CALCULATORS})


@router.get("/planning-tools", response_class=HTMLResponse)
async def planning_tools(request: Request):
    return templates.TemplateResponse("education/value_tools.html", {"request": request, "title": "Personal Finance Planning Tools | FinCalX", "description": "Lightweight personal finance planners, scorecards, learning paths, savings challenges, and wealth-building roadmaps.", "tools": VALUE_TOOLS, "checklists": CHECKLISTS, "guides": GUIDES, "calculators": CALCULATORS})
