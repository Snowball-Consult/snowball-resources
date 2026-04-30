# AI Agent Prompt Building Guide (JSON Format)

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Guide to building AI agent prompts with structured JSON output schemas |
| **Keywords** | AI agent, agent building, Claygent, build agent prompt, JSON, prompts, schema, Clay, output structure, variables, structured output, prompt engineering |
| **Maturity** | Canonical |
| **Last Reviewed** | 2026-02-11 |

---

## CRITICAL: Superseding Instructions

This guide incorporates the most recent superseding instructions for JSON prompt structure. Follow this format exactly.

## FIRST: Clarify Web Access Mode

**Before creating any prompt, ask this question:**

> "Will this Claygent have web access, or will it run on local data only (no web access)?"

This is critical because the prompt structure differs:

| Mode | Structure Required |
|------|-------------------|
| **Web access** | Single combined prompt (standard structure below) |
| **Local/no web access** | Must split into **system prompt** + **user prompt** |

### Local Mode Split Structure

When running without web access, separate the prompt into:

1. **System Prompt**: Contains `role` and `constraints`
2. **User Prompt**: Contains `goal` and `task_steps_to_perform` with the actual data variables

This ensures the agent correctly processes local data without attempting web lookups.

## Overall Structure Requirements

All JSON prompts must follow this exact three-part structure:

1. **Main JSON Prompt** (without output schema)
2. **Separated Output Schema** (after three dashes)
3. **Variables** (at the very end)

## 1. Main JSON Prompt Structure

The main prompt should contain these sections ONLY:

```json
{
  "role": "Specific Expert Type",
  "goal": "Clear objective using {company_name}",
  "task_steps_to_perform": [
    "1. Specific step with {company_name}",
    "2. Next step..."
  ],
  "constraints": [
    "Limitation 1",
    "Limitation 2..."
  ]
}
```

### Important: What NOT to Include

- **DO NOT** include any "final_output" section
- **DO NOT** include any "output_format" section
- **DO NOT** include any schema information in the main prompt

## 2. Separated Output Schema

After the main prompt, add exactly three dashes (`---`) and then provide the complete JSON schema separately:

```
---

{
  "type": "object",
  "properties": {
    "fieldName": {
      "type": "string",
      "description": "What this field contains"
    }
  },
  "required": ["fieldName"]
}
```

### Clay-Specific Requirements

When creating prompts for Clay platform:

- **NEVER** use standalone arrays as the root output type
- **ALWAYS** wrap arrays inside an object structure
- Use `"type": "object"` as the root with arrays as properties inside
- **DO NOT** include `agent_reasoning`, `reasoning`, `evidence_summary`, or similar reasoning/explanation fields in the output schema by default. Clay captures the agent's reasoning trace natively in the Claygent output - adding a reasoning field to the structured schema is redundant and wastes output tokens. Only include a reasoning field if explicitly requested for a specific use case (e.g., the reasoning needs to be written to a CRM field downstream).

**Wrong:**
```json
{
  "type": "array",
  "items": {"type": "object"}
}
```

**Correct:**
```json
{
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field1": {"type": "string"}
        }
      }
    }
  }
}
```

## 3. Variables Format (CRITICAL)

At the very end, list variables in this EXACT format:

```
{company_name}: variable
{company_domain}: variable
```

### Variable Requirements

- Variables in the prompt should be referenced using single curly braces: `{variable_name}`
- Each variable should be on its own line
- Format must be exactly: `{variable_name}: variable`
- No quotes, braces, or additional formatting around the word "variable"
- Use snake_case for variable names

### Purpose of This Format

This structure allows for easy copying and pasting:
- **Main prompt** → Copy to prompt field
- **Schema after dashes** → Copy to output schema field
- **Variables** → Easy replacement without prompt modification

## Complete Example Structure

```json
{
  "role": "Expert Web Researcher",
  "goal": "Analyze {company_name} business model and operations",
  "task_steps_to_perform": [
    "1. Visit {company_domain} and analyze core business",
    "2. Identify products and services offered",
    "3. Determine target market and value proposition"
  ],
  "constraints": [
    "Use only official website information",
    "Focus on explicitly stated information",
    "Provide clear, concise summaries"
  ]
}

---

{
  "type": "object",
  "properties": {
    "business_model": {
      "type": "string",
      "description": "Summary of the company's core business model"
    },
    "target_market": {
      "type": "string",
      "description": "Description of the company's target customers"
    },
    "confidence": {
      "type": "string",
      "enum": ["High", "Medium", "Low"],
      "description": "Confidence level in the analysis"
    }
  },
  "required": ["business_model", "target_market", "confidence"]
}

{company_name}: variable
{company_domain}: variable
```

## Best Practices

### Schema Design
- Use flat structure when possible
- Include clear field descriptions
- Specify required fields
- Use appropriate data types
- Include enumerated values where applicable

### Prompt Design
- Clear role definition
- Specific, actionable steps
- Explicit constraints
- Structured data flow

### Common Mistakes to Avoid
- Including output schema in main prompt
- Wrong variable format
- Using standalone arrays for Clay
- Missing required fields in schema
- Unclear or ambiguous task steps
- Adding reasoning/explanation fields to output schema (Clay captures reasoning natively - see Clay-Specific Requirements)

## Variable Reference Throughout Prompt

- Use `{company_name}` format throughout the prompt
- Variables should be descriptive and consistent
- Reference them in role, goal, and task steps as needed
- Always end with the exact variable format specified

This structure ensures clean separation for UI workflow while maintaining comprehensive analysis capabilities.
