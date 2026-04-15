#!/bin/bash

# BudgetCLI Usage Examples
# This script demonstrates common BudgetCLI workflows

set -e

echo "BudgetCLI - Usage Examples"
echo "=========================="
echo ""

# Initialize database
echo "1. Initializing database..."
budget init
echo "✓ Database initialized"
echo ""

# Add some budgets
echo "2. Setting up budgets..."
budget budget set-budget --category "Food" --limit 500000
budget budget set-budget --category "Transport" --limit 200000
budget budget set-budget --category "Utilities" --limit 150000
echo "✓ Budgets configured"
echo ""

# Add transactions for April 2026
echo "3. Adding sample transactions..."
budget transaction add --type income --category "Salary" --amount 5000000 --date 2026-04-01 --note "Monthly salary"

budget transaction add --type expense --category "Food" --amount 250000 --date 2026-04-05 --note "Groceries"
budget transaction add --type expense --category "Food" --amount 150000 --date 2026-04-10 --note "Restaurant"
budget transaction add --type expense --category "Food" --amount 80000 --date 2026-04-15 --note "Coffee & snacks"

budget transaction add --type expense --category "Transport" --amount 100000 --date 2026-04-08 --note "Gas"
budget transaction add --type expense --category "Transport" --amount 50000 --date 2026-04-20 --note "Public transit"

budget transaction add --type expense --category "Utilities" --amount 120000 --date 2026-04-03 --note "Electricity and water"

echo "✓ Transactions added"
echo ""

# View budgets
echo "4. Viewing budgets..."
budget budget list
echo ""

# View transactions
echo "5. Viewing transactions..."
budget transaction list --limit 10
echo ""

# Generate monthly report
echo "6. Monthly report for April 2026..."
budget report monthly --month 2026-04
echo ""

# Show ASCII chart
echo "7. ASCII chart visualization..."
budget report chart --month 2026-04
echo ""

# Show summary
echo "8. Financial summary..."
budget report summary --month 2026-04
echo ""

# Export data
echo "9. Exporting data..."
budget report export --format csv --month 2026-04
budget report export --format json --month 2026-04
echo "✓ Data exported to ./exports/"
echo ""

# Generate PNG chart
echo "10. Generating PNG chart..."
budget report plot --month 2026-04 --type bar
budget report plot --month 2026-04 --type pie
echo "✓ Charts generated in ./exports/"
echo ""

echo "All examples completed! 🎉"
echo ""
echo "Check the following for results:"
echo "  - Transaction list: budget transaction list"
echo "  - Budget status: budget budget list"
echo "  - Reports: budget report --help"
echo "  - Exports: ls -la exports/"
