# Fix UI Issues in Tax Calculator Template

## Plan
1. Remove all git merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> 74f72c9 (version-2)`)
2. Remove markdown code block markers (```) mixed into HTML
3. Remove duplicate form sections — keep version-2 form (number inputs, validation classes, `for` attributes)
4. Reconstruct result section combining best of both versions (all rows + gradient total tax card)
5. Add pre-calculation disclaimer below Calculate button
6. Add post-calculation Bootstrap alert disclaimer below result card
7. Clean up JavaScript — remove comma-formatting logic, keep regime toggle only
8. Verify backend compatibility preserved

## Progress
- [x] Create TODO.md
- [x] Rewrite `app/templates/tools/tax.html`
- [x] Verify clean template with no syntax errors

