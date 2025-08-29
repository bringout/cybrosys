# Cybrosys Odoo Packages

This repository contains **10** Odoo packages from Cybrosys vendor.

## About Cybrosys

Cybrosys is a recognized vendor in the Odoo ecosystem, providing specialized addons and customizations.

## Packages Included (10 packages)

- **odoo-bringout-cybrosys-hr_payroll_input_add** - Hr Payroll Input Add
- **odoo-bringout-cybrosys-ohrms_loan** - Ohrms Loan
- **odoo-bringout-cybrosys-order_line_sequences** - Order Line Sequences
- **odoo-bringout-cybrosys-product_brand_ecommerce** - Product Brand Ecommerce
- **odoo-bringout-cybrosys-product_brand_inventory** - Product Brand Inventory
- **odoo-bringout-cybrosys-product_brand_invoicing** - Product Brand Invoicing
- **odoo-bringout-cybrosys-product_brand_purchase** - Product Brand Purchase
- **odoo-bringout-cybrosys-product_brand_sale** - Product Brand Sale
- **odoo-bringout-cybrosys-stock_move_invoice** - Stock Move Invoice
- **odoo-bringout-cybrosys-warehouse_reports** - Warehouse Reports


## Installation

Install any package from this collection:

```bash
# Install from local directory
pip install packages/cybrosys/PACKAGE_NAME/

# Install in development mode  
pip install -e packages/cybrosys/PACKAGE_NAME/

# Using uv (recommended for speed)
uv add packages/cybrosys/PACKAGE_NAME/
```

## Repository Structure

Each package in this repository follows the standard Odoo addon structure:

```
cybrosys/
├── odoo-bringout-cybrosys-ADDON/
│   ├── ADDON_NAME/           # Complete addon code
│   │   ├── __init__.py
│   │   ├── __manifest__.py
│   │   └── ... (models, views, etc.)
│   ├── pyproject.toml        # Python package configuration
│   └── README.md            # Package documentation
└── ...
```

## License

Each package maintains its original license as specified by Cybrosys.

## Support

For support with these packages, please refer to the original Cybrosys documentation or community resources.
