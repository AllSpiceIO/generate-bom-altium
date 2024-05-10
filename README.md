# Generate BOM for Altium Projects

Generate a BOM for an Altium project on AllSpice Hub using py-allspice.

## Usage

Add the following steps to your actions:

```yaml
# Checkout is only needed if columns.json is committed in the repo.
- name: Checkout
  uses: actions/checkout@v3

- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom-altium@main
  with:
    project_path: Archimajor.PrjPcb
    pcb_path: Archimajor.PcbDoc
    columns: .allspice/columns.json
    output_file_name: bom.csv
```

where `.allspice/columns.json` looks like:

```json
{
  "part_number": ["PART", "MANUFACTURER #", "MPN"],
  "manufacturer": ["Manufacturer", "MANUFACTURER", "MFG", "Mfg"],
  "designator": ["Designator", "REFDES", "Refdes", "Ref"],
  "part_id": ["_part_id"],
  "description": ["PART DESCRIPTION", "_description"]
}
```
