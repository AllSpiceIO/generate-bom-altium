# Generate BOM for E-CAD Projects

Generate a BOM output file for an Altium project on AllSpice Hub using [AllSpice Actions](https://learn.allspice.io/docs/actions-cicd).

## Usage

Add the following steps to your actions:

```yaml
# Checkout is only needed if columns.yml is committed in your Altium project repo.
- name: Checkout
  uses: actions/checkout@v3

- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom@v0.3
  with:
    # The path to the project file in your repo (.PrjPcb for Altium, .DSN for OrCad).
    source_path: Archimajor.PrjPcb
    # [optional] A path to a YAML file mapping columns to the component
    # attributes they are from.
    # Default: 'columns.yml'
    columns: .allspice/columns.yml
    # [optional] The path to the output file that will be generated.
    # Default: 'bom.csv'
    output_file_name: bom.csv
    # [optional] A comma-separated list of columns to group the BOM by. If empty
    # or not present, the BOM will be flat.
    # Default: ''
    group_by: "Part ID"
    # [optional] The variant of the project to generate the BOM for. If empty
    # or not present, the BOM will be generated for the default variant.
    # Default: ''
    variant: ""
```

### Customizing the Attributes Extracted by the BOM Script

This script relies on a YAML file to specify the columns in the BOM and which
attributes or properties of the components they are populated from. This file is
typically called `columns.yml` and can be checked into your repo. To learn more
about YAML, [check out the AllSpice Knowledge Base.](https://learn.allspice.io/docs/yaml)

The format of this YAML file is as follows:

```yml
columns:
  - column_name: Manufacturer
    part_attributes:
      - Manufacturer
      - MANUFACTURER
  - column_name: Part Number
    part_attributes:
      - PART
      - MANUFACTURER \#
      - _part_id
  - column_name: Designator
    part_attributes: Designator
  - column_name: Description
    part_attributes:
      - PART DESCRIPTION
      - _description
```

First, you have the key `columns:` which is mapped to a list. Each element of
the list has two key/value pairs. The first is `column_name`, which is used to
as the name of the column. Next, you have `part_attributes`. This can either be
just a string (like in the case of the `Designator` column) or a list of strings
(like in the other cases.)

If `part_attributes` is just a string, that property or attribute of the
component is used as the value for that column. If that property is not present
in a particular part, that column will be blank for that part. If
`part_attributes` is a list, those properties will be checked in the order they
are defined for each part. The _first_ property found is used as the value for
that column in the row for that part. So if both `PART` and `MANUFACTURER #` are
defined, it will use `PART`.

An example for OrCad `columns.yml` file content is:

```yml
columns:
  - column_name: Part Number
    part_attributes:
      - Part Number
      - _name
  - column_name: Designator
    part_attributes: Part Reference
  - column_name: Type
    part_attributes: Part Type
  - column_name: Value
    part_attributes: Value
```

By default, the action will pick up a `columns.yml` file from the working
directory. If you want to keep it in a different place, or rename it, you can
pass the `--columns` argument to the step in the workflow to specify where it
is.

### Py-allspice injected attributes

Note that py-allspice also adds a few static attributes, which are taken from
the part itself, and not from the properties or attributes. For Altium projects,
`_part_id` and `_description` are available, which correspond to the Library
Reference and Description fields of the component. For OrCAD projects, `_name`
is available, which corresponds to the name of the component.

The underscore is added ahead of the name to prevent these additional attributes
from overriding any of your own.

## Group By

You can also group lines by a column value. The most common is `_part_id`. You
can combine this with the columns YAML example above, like so:

```yaml
- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom@v0.3
  with:
    project_path: Archimajor.PrjPcb
    columns: .allspice/columns.yml
    group_by: "Part ID"
```

Which will generate a BOM squashed by components with matchin Part IDs.

## Variants

To generate the BOM for a variant of the project, pass the `--variant` argument
to the script. For example:

```yaml
- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom@v0.3
  with:
    project_path: Archimajor.PrjPcb
    columns: .allspice/columns.yml
    output_file_name: bom-lite.csv
    variant: "LITE"
```

When no variant is given, the BOM is generated without considering any variants.
