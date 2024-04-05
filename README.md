# Generate BOM

Generate a BOM for a project on AllSpice Hub using py-allspice.

Note: currently only works with Altium projects.

## Usage

Add the following step to your actions:

```yaml
- name: Generate BOM
  uses: https://hub.allspice.io/shrikanth-allspice/generate-bom@v1
  with:
    project_path: Archimajor.PrjPcb
    output_file_name: bom.csv
    attributes_mapping: >
      {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"]
      }
    auth_token: ${{ secrets.ALLSPICE_HUB_AUTH_TOKEN }}
```
