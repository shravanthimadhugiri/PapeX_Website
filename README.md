# .shared/ui-ux-pro-max

Searchable design intelligence database for PapeX. Powers the `.cursor/commands/ui-ux-pro-max.md` skill.

## Structure

```
.shared/ui-ux-pro-max/
├── scripts/
│   ├── search.py         # CLI entry point (BM25 + regex hybrid)
│   ├── core.py           # Search engine core
│   └── design_system.py  # Design system generation
└── data/
    ├── styles.csv        # 67 UI styles
    ├── colors.csv        # 161 color palettes
    ├── typography.csv    # 57 font pairings
    ├── ux-guidelines.csv # 99 UX guidelines
    ├── charts.csv        # 25 chart types
    ├── landing.csv       # Landing page patterns
    ├── products.csv      # Product type patterns
    ├── icons.csv         # Icon recommendations
    └── stacks/           # Stack-specific guidelines (nextjs, react, etc.)
```

## Usage

```bash
# Full design system (recommended starting point)
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech SaaS minimal" --design-system -p "PapeX"

# Domain search
python3 .shared/ui-ux-pro-max/scripts/search.py "clean minimal" --domain style -n 3

# Stack-specific
python3 .shared/ui-ux-pro-max/scripts/search.py "dashboard" --stack nextjs
```

Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
