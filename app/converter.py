import fitz 

def convert_to_dark(input_path, output_path):
    doc = fitz.open(input_path)

    for page in doc:
        # Dark background
        rect = page.rect
        page.draw_rect(rect, color=(0, 0, 0), fill=(0, 0, 0))

        # White text
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        page.insert_text(
                            (span["bbox"][0], span["bbox"][1]),
                            span["text"],
                            fontsize=span["size"],
                            color=(1, 1, 1)
                        )

    doc.save(output_path)
