# User Guide

The User Guide provides detailed documentation for the Microsoft Purview resources and operations supported by the Purview Unified SDK.

Unlike the **Getting Started** section, which focuses on installation, authentication, and initial configuration, the User Guide explains how to work with each resource type and perform common SDK operations.

---

## What You'll Learn

The User Guide covers the following areas:

- Creating, listing, retrieving, updating, and deleting Business Domains
- Creating, listing, retrieving, updating, and deleting Data Products
- Creating, listing, retrieving, updating, and deleting Glossary Terms
- Creating, listing, retrieving, updating, and deleting Critical Data Elements (CDEs)
- Creating, listing, retrieving, updating, and deleting Objectives and Key Results (OKRs)
- Listing Microsoft Purview Policies
- Retrieving Data Assets and Data Columns
- Creating and managing supported relationships
- Inspecting returned model objects and converting them to dictionaries
- Navigating Data Products and related resources

Each guide includes explanations, practical examples, known limitations, and links to corresponding example scripts.

---

## User Guide Sections

### Business Domains

Learn how to:

- Create a Business Domain
- List Business Domains
- Retrieve Business Domain properties
- Update a Business Domain
- Delete a Business Domain

[Open the Business Domains guide](business_domains.md)

### Data Products

Learn how to:

- Create a Data Product
- List Data Products
- Retrieve Data Product properties
- Update a Data Product
- Delete a Data Product
- Navigate related resources

[Open the Data Products guide](data_products.md)

### Glossary Terms

Learn how to:

- Create a Glossary Term
- List Glossary Terms
- Retrieve Glossary Term properties
- Update a Glossary Term
- Delete a Glossary Term

[Open the Glossary Terms guide](glossary.md)

### Critical Data Elements

Learn how to:

- Create a Critical Data Element
- List Critical Data Elements
- Retrieve CDE properties
- Update a Critical Data Element
- Delete a Critical Data Element

[Open the Critical Data Elements guide](cdes.md)

### Data Map Resources

Learn how to:

- List and retrieve Data Assets
- Retrieve Data Column properties
- Use Data Assets and Data Columns in supported relationships

[Open the Data Map guide](data_map.md)

### Objectives and Key Results

Learn how to:

- Create an Objective
- List Objectives
- Retrieve Objective properties
- Update an Objective
- Delete an Objective
- Work with related Key Results

[Open the OKRs guide](okrs.md)

### Relationships

Learn how to create supported relationships between:

- Data Products
- Glossary Terms
- Critical Data Elements
- Data Assets
- Data Columns
- Objectives
- Other supported Microsoft Purview resources

[Open the Relationships guide](relationships.md)

### Policies

Learn how to:

- List Microsoft Purview Policies
- Retrieve Policy properties
- Inspect Policy model objects

[Open the Policies guide](policies.md)

### Listing and Resource Properties

Learn how to:

- Work with list results
- Inspect returned model types
- Read common properties such as `id`, `name`, and `description`
- Convert model objects using `to_dict()`
- Handle large result sets

[Open the Listing and Resource Properties guide](listing_and_properties.md)

---

## Recommended Reading Order

For users who are new to the SDK, we recommend the following order:

1. Business Domains
2. Data Products
3. Glossary Terms
4. Critical Data Elements
5. Objectives and Key Results
6. Data Map Resources
7. Relationships
8. Policies
9. Listing and Resource Properties

---

## Example Programs

Runnable examples are included in the repository under the `examples` directory.

```text
examples/
├── add_relationships/
├── auth_example/
├── cdes/
├── data_products/
├── domains/
├── get_properties/
├── glossary_terms/
├── okrs/
└── policies/
```

These examples demonstrate tested SDK usage patterns for Microsoft Purview Unified Catalog.

---

## Next Steps

Begin with the **Business Domains** guide.

**Next:** [Business Domains →](business_domains.md)