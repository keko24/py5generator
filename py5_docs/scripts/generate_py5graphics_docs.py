from generator.mapping import REST_DOC_LINK
import re
from pathlib import Path

import pandas as pd

from generator.docfiles import Documentation


PY5_DOC_REF_DIR = Path('py5_docs/Reference/api_en/')
PY5_REF_DIR = Path('../py5website/reference/')

REST_DOC_LINK = re.compile(":doc:`[\w_]+`")


py5graphics_data = pd.read_csv('py5_resources/data/pgraphics.csv').fillna('').set_index('py5_name')

relevant_items = list(py5graphics_data.query("type != 'static field' and implementation != 'SKIP'").index)

website_slugs = [f.stem for f in PY5_REF_DIR.glob("*.rst")]


# TODOs
# add language that links back to the Sketch doc page (but not for mask) and explains how it is different

DESCRIPTION_REPLACEMENTS = {
    ('display window', 'Py5Graphics canvas'),
}


for item in relevant_items:
    if item in ['clear', 'begin_draw', 'end_draw']:
        continue

    sketch_docfile = PY5_DOC_REF_DIR / f'Sketch_{item}.txt'
    py5image_docfile = PY5_DOC_REF_DIR / f'Py5Image_{item}.txt'
    py5graphics_docfile = PY5_DOC_REF_DIR / f'Py5Graphics_{item}.txt'

    doc = Documentation(sketch_docfile) if sketch_docfile.exists() else Documentation(py5image_docfile)

    doc.meta['pclass'] = 'PGraphics'
    doc.examples = []

    for doclink in REST_DOC_LINK.findall(doc.description):
        test_slug = f"py5graphics_{doclink[6:-1]}"
        if test_slug in website_slugs:
            doc.description.replace(doclink, f":doc:`{test_slug}`")

    for find_replace in DESCRIPTION_REPLACEMENTS:
        doc.description = doc.description.replace(*find_replace)

    doc.write(py5graphics_docfile)
