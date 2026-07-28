# Resource Model

Microsoft Purview Unified Catalog organizes governance information as a collection of interconnected resources.

Each resource represents a specific governance concept, such as a Business Domain, Data Product, or Glossary Term. These resources are connected through relationships, allowing organizations to describe how business concepts, data, and governance policies relate to one another.

Understanding the resource model will help you better understand how the SDK is organized and how different resources interact.

---

## Supported Resource Types

The Purview Unified SDK currently supports operations on the following Microsoft Purview resource types.

| Resource | Description |
|----------|-------------|
| Business Domain | Organizes governance resources at the business level. |
| Data Product | Represents a business-owned collection of data. |
| Data Asset | Represents a physical or logical data asset, such as a table or file. |
| Data Column | Represents an individual column or field within a Data Asset. |
| Glossary Term | Defines business terminology and shared vocabulary. |
| Critical Data Element (CDE) | Identifies business-critical information. |
| Objective | Represents a business objective. |
| Key Result | Measures progress toward an Objective. |
| Policy | Represents governance policies. |

---

## Resource Hierarchy

The following diagram illustrates the typical hierarchy within Microsoft Purview Unified Catalog.

```text
Business Domain
        │
        ▼
   Data Product
        │
        ├──────────────┐
        ▼              ▼
  Data Asset      Objective
        │              │
        ▼              ▼
  Data Column     Key Result
        │
        ├──────────────┐
        ▼              ▼
Glossary Term   Critical Data Element
```

Business Domains provide the highest level of organization.

Within a Business Domain, organizations typically create one or more Data Products. A Data Product can then be associated with Data Assets, Objectives, Glossary Terms, and other governance resources.

---

## Relationships

Resources are connected through relationships.

For example:

| Relationship | Purpose |
|--------------|---------|
| Business Domain → Data Product | Organizes Data Products within a business area. |
| Data Product → Data Asset | Associates physical or logical data with a Data Product. |
| Data Product → Objective | Associates business objectives with a Data Product. |
| Glossary Term → Data Asset | Describes the business meaning of a Data Asset. |
| Glossary Term → Data Column | Defines business terminology for a specific column. |
| Critical Data Element → Data Column | Identifies business-critical fields. |
| Objective → Key Result | Measures progress toward an Objective. |

The SDK provides APIs for creating and managing supported relationships between these resources.

---

## Resource Identifiers

Every resource in Microsoft Purview Unified Catalog has a unique identifier (ID).

Resource IDs are UUIDs and are commonly used by the SDK when retrieving, updating, or deleting resources.

Example:

```text
123456ab-7890-abcd-efgh-1234abcd5e6f
```

Many SDK operations require a resource ID.

For example, updating a Business Domain requires the unique identifier of that Business Domain.

---

## Resource Names

In addition to an ID, most resources also include properties such as:

- Name
- Description
- Status
- Owner (where applicable)

While names are intended for display purposes, resource IDs should always be used when referencing resources programmatically.

---

## Learn More

The following sections describe each supported resource in detail:

- Business Domains
- Data Products
- Glossary Terms
- Critical Data Elements
- Data Map Resources
- Relationships

---

## Next Steps

Continue with the **Business Domains** guide to learn about the top-level organizational resource in Microsoft Purview Unified Catalog.

➡️ **Next:** [Getting Started](../getting_started/index.md)