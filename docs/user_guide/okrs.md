# Objectives and Key Results (OKRs)

Objectives and Key Results (OKRs) provide a structured framework for defining business goals and measuring progress.

Within Microsoft Purview Unified Catalog, Objectives represent high-level business goals, while Key Results define measurable outcomes used to evaluate progress toward those goals.

The Purview Unified SDK currently provides CRUD operations for **Objectives**. Support for managing **Key Results** will be added in a future SDK release.

A typical relationship pattern is:

```text
Business Domain
        │
        ▼
   Objective
        │
        ├──────────────► Key Result
        │
        └──────────────► Data Product
```

The Purview Unified SDK currently supports the following Objective operations:

- Create an Objective
- Update an Objective
- Delete an Objective

---

## Before You Begin

The examples in this guide assume that authentication and client configuration have already been completed.

A configured client should be available as:

```python
client
```

For complete setup instructions, see:

- [Authentication](../getting_started/authentication.md)
- [Configuration](../getting_started/configuration.md)

Every Objective created by the example belongs to an existing Business Domain.

---

## Create an Objective

Use `client.okrs.create_objective()` to create a new Objective.

### Required Business Domain ID

The example reads the Business Domain ID from the `.env` file:

```python
DOMAIN_ID = os.environ[
    "PURVIEW_DOMAIN_ID"
]
```

Add the value to `.env`:

```text
PURVIEW_DOMAIN_ID=11111111-1111-1111-1111-111111111111
```

!!! danger "Replace the Example Domain ID"

    Replace the example value with the ID of an existing Business Domain in your Microsoft Purview environment.

---

### Objective Values

```python
OBJECTIVE_DEFINITION = (
    "Improve Customer Data Quality"
)

OBJECTIVE_STATUS = (
    "Draft"
)

TARGET_DATE = (
    "2027-12-31T00:00:00"
)
```

The Objective is created with:

- Definition
- Status
- Target completion date
- Business Domain

---

### Target Date

Objectives support a target completion date.

The SDK expects the date in ISO 8601 format.

Example:

```text
2027-12-31T00:00:00
```

---

### Create Example

```python
objective = client.okrs.create_objective(
    definition=OBJECTIVE_DEFINITION,
    domain_id=DOMAIN_ID,
    status=OBJECTIVE_STATUS,
    target_date=TARGET_DATE,
)
```

The complete runnable example is available in:

```text
examples/okrs/create_okr.py
```

The example creates a new Objective within an existing Business Domain and prints the returned properties. :contentReference[oaicite:0]{index=0}

---

### Returned Objective

The create operation returns an Objective model.

Common properties include:

```python
objective.id
objective.definition
objective.status
objective.domain_id
objective.target_date
```

Save the returned Objective ID if it will later be updated, deleted, or linked to a Data Product.

---

## Update an Objective

Use `client.okrs.update_objective()` to update an existing Objective.

The example updates:

- Definition
- Status
- Target date

```python
objective = client.okrs.update_objective(
    objective_id=OBJECTIVE_ID,
    definition=NEW_DEFINITION,
    status=NEW_STATUS,
    target_date=NEW_TARGET_DATE,
)
```

The complete runnable example is available in:

```text
examples/okrs/update_okr.py
```

The update operation returns the updated Objective model, including:

```python
objective.id
objective.definition
objective.status
objective.domain_id
objective.target_date
objective.overall_status
objective.key_results_count
```

`overall_status` represents the current calculated state of the Objective.

`key_results_count` indicates the number of Key Results associated with the Objective. :contentReference[oaicite:1]{index=1}

---

## Delete an Objective

Use `client.okrs.delete_objective()` to delete an existing Objective.

```python
client.okrs.delete_objective(
    OBJECTIVE_ID,
)
```

The complete runnable example is available in:

```text
examples/okrs/delete_okr.py
```

!!! danger "Deletion Is Destructive"

    Deleting an Objective permanently removes it from Microsoft Purview.

    Before deleting an Objective, review any associated Data Products or Key Results.

The delete example removes the specified Objective and prints the deleted Objective ID. :contentReference[oaicite:2]{index=2}

---

## Objective Model

Common Objective properties include:

| Property | Description |
|----------|-------------|
| `id` | Unique identifier. |
| `definition` | Objective definition. |
| `status` | Current lifecycle status. |
| `domain_id` | Business Domain containing the Objective. |
| `target_date` | Target completion date. |
| `overall_status` | Calculated overall progress. |
| `key_results_count` | Number of associated Key Results. |

---

## Objectives and Key Results

Objectives define **what** should be achieved.

Key Results define **how success is measured**.

Although the current SDK focuses on Objective management, Objectives can already participate in relationships with other Microsoft Purview resources.

Support for creating and managing individual Key Results is planned for a future SDK release.

---

## Complete Workflow

A typical Objective workflow is:

```text
Create a Business Domain
        ↓
Create an Objective
        ↓
Record the returned Objective ID
        ↓
Associate the Objective with a Data Product
        ↓
Track progress through Key Results
        ↓
Update the Objective
        ↓
Delete it when it is no longer required
```

---

## Example Files

| File | Purpose |
|------|---------|
| `examples/okrs/create_okr.py` | Creates an Objective. |
| `examples/okrs/update_okr.py` | Updates an Objective. |
| `examples/okrs/delete_okr.py` | Deletes an Objective. |

---

## Common Issues

### Invalid Business Domain ID

Verify that the supplied Domain ID exists and belongs to your Microsoft Purview environment.

### Invalid Target Date

The target date should be supplied in ISO 8601 format.

Example:

```text
2027-12-31T00:00:00
```

### Objective Not Found

Verify that the supplied Objective ID exists.

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview Unified Catalog endpoint.

Then verify that the authenticated identity has permission to manage Objectives.

---

## Next Steps

Continue with the **Relationships** guide.

**Next:** [Policies →](policies.md)