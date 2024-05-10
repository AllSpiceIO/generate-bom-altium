# Generate BOM for Altium Projects

Generate a BOM output file for an Altium project on AllSpice Hub using [AllSpice Actions](https://learn.allspice.io/docs/actions-cicd).

## Usage

Add the following steps to your actions:

```yaml
# Checkout is only needed if columns.json is committed in your Altium project repo.
- name: Checkout
  uses: actions/checkout@v3

- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom-altium@main
  with:
    # The path to the Altium project file in your repo.
    project_path: Archimajor.PrjPcb
    # A path to a JSON file mapping columns to the attributes they are from.
    columns: .allspice/columns.json
    # [optional] The path to the output file that will be generated.
    # Default: 'bom.csv'
    output_file_name: bom.csv
    # [optional] A comma-separated list of columns to group the BOM by. If empty
    # or not present, the BOM will be flat.
    # Default: ''
    group_by: 'Part ID'
    # [optional] The variant of the project to generate the BOM for. If empty
    # or not present, the BOM will be generated for the default variant.
    # Default: ''
    variant: ''
```

### Customizing the Attributes Extracted by the BOM Script

This script relies on a `columns.json` file. This file maps the Component
Attributes in the SchDoc files to the columns of the BOM. An example for
`columns.json` file content is:

```json
{
  "description": ["PART DESCRIPTION"],
  "designator": ["Designator"],
  "manufacturer": ["Manufacturer", "MANUFACTURER"],
  "part_number": ["PART", "MANUFACTURER #"]
}
```

In this file, the keys are the names of the columns in the BOM, and the values
are a list of the names of the attributes in the SchDoc files that should be
mapped to that column. For example, if your part number is stored either in the
`PART` or `MANUFACTURER #` attribute, you would add both of those to the list.
If there is only one attribute, you can omit the list and just use a string. The
script checks these attributes in order, and uses the _first_ one it finds. So
if both `PART` and `MANUFACTURER #` are defined, it will use `PART`.

Note that py-allspice also adds two attributes: `_part_id` and `_description`.
These correspond to the Library Reference and description fields of the
component. The underscore is added ahead of the name to prevent these additional
attributes from overriding any of your own. You can use these like:

```json
{
  "Description": ["PART DESCRIPTION", "_description"],
  "Part Number": ["PART", "_part_id"]
}
```

By default, the script picks up a `columns.json` file from the working
directory. If you want to keep it in a different place, or rename it, you can
pass the `--columns` argument to the script to specify where it is.

## Variants

To generate the BOM for a variant of the project, pass the `--variant` argument
to the script. For example:

```yaml
- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom-altium@main
  with:
    project_path: Archimajor.PrjPcb
    columns: .allspice/columns.json
    output_file_name: bom-lite.csv
    variant: 'LITE'
```

When no variant is given, the BOM is generated without considering any variants.
