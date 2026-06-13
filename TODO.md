# TODO - New Calculators (Lumpsum, Compound Interest, Inflation, Emergency Fund, Net Worth)

- [x] Create forms models in `app/forms.py` for 5 calculators

- [x] Create services in `app/services/` for 5 calculators

- [x] Create routers in `app/routers/` for 5 calculators (GET page + POST + JSON API)

- [x] Create templates in `app/templates/tools/` for 5 calculators (clone CAGR architecture; mandatory disclaimer below results)
- [x] Create dedicated JS files in `app/static/js/` for 5 calculators (AJAX/no reload)

- [ ] Update discovery containers:
  - [x] `app/routers/home.py` add 5 tool cards
  - [x] `app/routers/education.py` extend `CALCULATORS`
  - [x] `app/main.py` add 5 URLs to hardcoded `sitemap.xml`

- [ ] Quality checks: verify no existing calculators/routes/APIs/templates/nav/security/CSP changed except discovery + new files
- [x] Run server and validate AJAX + endpoints for all 5 calculators

