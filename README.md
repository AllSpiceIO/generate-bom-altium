# Generate BOM for Altium Projects

Generate a BOM for an Altium project on AllSpice Hub using py-allspice. This
currently uses the PCB file for computing quantities.

## Usage

Add the following step to your actions:

```yaml
- name: Generate BOM
  uses: https://hub.allspice.io/Actions/generate-bom-altium@main
  with:
    project_path: Archimajor.PrjPcb
    pcb_path: Archimajor.PcbDoc
    output_file_name: bom.csv
    attributes_mapping: '
      {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"]
      }
    '
```
