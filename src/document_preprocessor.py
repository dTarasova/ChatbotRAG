
import pymupdf
import re

def process_pdf(input_pdf_path: str, output_pdf_path: str) -> str:
    text = extract_paragraphs_from_pdf(input_pdf_path)
    wo_ref_paragraphs = remove_ref_paragraphs(text)
    cleaned_paragraphs = filter_text(wo_ref_paragraphs)
    final_text = save_paragraphs_to_txt(cleaned_paragraphs, output_pdf_path)
    return final_text

def extract_paragraphs_from_pdf(pdf_path: str) -> list[str]:
    document = pymupdf.open(pdf_path)
    paragraphs = []
    doc_len = len(document)
    for page_num in range(doc_len):
        page = document.load_page(page_num)
        blocks = page.get_text("blocks")
        text_elements = [block[4] for block in blocks]
        paragraphs.extend(text_elements)
    return paragraphs


def remove_ref_paragraphs(paragraphs: list[str]) -> list[str]:
    for i, paragraph in enumerate(reversed(paragraphs)):
            paragraph_text = paragraph.strip().lower()
            if paragraph_text == "references" or paragraph_text == "bibliography":
                cut_index = len(paragraphs) - i - 1
                return paragraphs[:cut_index]
    return paragraphs



def save_text_to_txt(text: str, file_path: str):
    try: 
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"An error occurred: {e}")

def save_paragraphs_to_txt(paragraphs, file_path) -> str:
    paragraphs_text = ''
    for paragraph in paragraphs:
        paragraphs_text += paragraph + '\n\n'
    save_text_to_txt(paragraphs_text, file_path)
    return paragraphs_text




def filter_text(paragraphs: list[str]) -> list[str]:
    # Define the pattern to match unwanted lines
    pattern = re.compile(r'(.*\..*){4,}')

    filtered_paragraphs = []

    # Split the text into lines
    for p in paragraphs:
        lines = p.split('\n')

        # Filter out lines that match the pattern
        filtered_lines = [line for line in lines if not pattern.match(line)]

        # Join the filtered lines back into a single string
        # filtered_text.extend(filtered_lines)

        filtered_text = '\n' + ''.join(filtered_lines)

        filtered_paragraphs.extend([filtered_text])


    return filtered_paragraphs
