# Jev Choice Question: Company Segmentation Payload

The request body sent to TypeSafe's Jev for each company in the test "Jev in Clay: Company Segmentation for TAM Mapping, Tested". Sent from a Clay HTTP API column to `POST https://openrouter.ai/api/alpha/decisions`, one call per row.

- **`state`** - the inputs: key-value pairs describing one company. In Clay each value is a column reference, so every row sends its own values. Shown here as placeholders.
- **`instructions`** - the question.
- **`criteria`** - the options Jev chooses from. Each option has a definition (`what`), the line to its neighboring options (`not_for`), and `examples`.

```json
{
  "model": "jev-1.13",
  "state": {
    "company_name": "<company name>",
    "linkedin_description": "<company description from LinkedIn>"
  },
  "questions": {
    "segment": {
      "type": "choice",
      "instructions": "Based on `company_name` and `linkedin_description`, which segment is this company? If `company_name` names one arm of a larger firm (for example Credit or Private Equity), classify that arm.",
      "criteria": {
        "Sponsor": {
          "what": "Invests equity in companies: private equity, growth equity, venture capital, or the private equity arm of a larger asset manager",
          "not_for": "The credit or lending arm of the same manager (Lender); banks (Lender or Advisor)",
          "examples": [
            "Buyout firm",
            "Growth equity or venture capital fund",
            "Private equity division of an alternative asset manager"
          ]
        },
        "Lender": {
          "what": "Provides debt to companies or funds: banks, private credit and direct lending funds, insurers and asset managers investing in private debt",
          "not_for": "Firms that only advise on a financing (Advisor); the private equity arm of the same manager (Sponsor)",
          "examples": [
            "Corporate and investment bank with a leveraged finance desk",
            "Direct lending fund",
            "Credit arm of an alternative asset manager",
            "Insurer buying private placements"
          ]
        },
        "Advisor": {
          "what": "Paid to advise on financings, M&A or valuations: debt advisors, M&A investment banks, accounting firms' debt or transaction advisory teams",
          "not_for": "Law firms (Law Firm); strategy or management consultancies (Other); banks that lend (Lender)",
          "examples": [
            "Independent debt advisory firm",
            "M&A advisory boutique",
            "Big Four debt advisory team",
            "Valuation firm"
          ]
        },
        "Law Firm": {
          "what": "A law firm",
          "not_for": "Non-legal advisors (Advisor)",
          "examples": [
            "Corporate law firm with finance and private equity practices"
          ]
        },
        "Other": {
          "what": "Does not invest in, lend to, or advise on companies' financing",
          "not_for": "Any investor, lender, deal advisor or law firm",
          "examples": [
            "Operating or portfolio company",
            "Strategy consultancy",
            "Fund administrator",
            "Rating agency",
            "Insurance broker",
            "University"
          ]
        }
      }
    }
  }
}
```

Notes:
- The option keys (`Sponsor`, `Law Firm`, ...) are spelled exactly like the values in the ground-truth field the answers are compared against, so each answer can be matched directly.
- In my runs, Jev returned the chosen key, a confidence, and a probability for every option. A low confidence marks a row for a person to review.
- Question types and criteria formats: [docs.typesafe.ai](https://docs.typesafe.ai).
