# Illustrated submission report

- `Verdant_Capital_Submission_Report.pdf`: the 23-page presentation/print version.
- `Verdant_Capital_Submission_Report.docx`: editable Word document with embedded images and native equation objects.
- `Verdant_Capital_Submission_Report.html`: self-contained HTML with embedded images and MathML equations; no CDN or external scripts required.
- `SUBMISSION_REPORT.md`: editable content source in the requested mission → problem → solution → challenges → conclusion order.
- `report_assets/`: actual additional app captures, analytical figures, financial-loss curve CSV and the numerical evidence underlying the report.

All 15 document figures have explanatory captions. Existing charcoal/gold app
captures and the three C06 attribution plots are also embedded in the exported
PDF/Word/HTML files. The reports remain usable without the application running.
The historical allocation table is explicitly identified as user-provided evidence;
it is not represented as a recomputed market run in this cloud checkout.

Implementation baseline: `501c33a`. Optional RAG/provider and production-readiness
limits are retained. No portfolio or benchmark code is changed for this document.

## Editing and rebuilding

Edit the Word document directly for presentation changes, then export it to PDF
with Word or LibreOffice. Alternatively edit the Markdown source and use Pandoc
with the existing Word file as the style reference:

```bash
pandoc docs/SUBMISSION_REPORT.md --resource-path=docs \
  --reference-doc=docs/Verdant_Capital_Submission_Report.docx \
  -o revised-report.docx
```

Rebuilding from Markdown retains the reference styles but may need table widths,
page breaks and captions checked again in Word. The supplied PDF and DOCX have
already been inspected for pagination, equations, figures and readable tables.
The standalone HTML is generated with Pandoc's `--embed-resources --mathml` flags
and `report_assets/report.css`.
