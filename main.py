import os
import shutil
import fitz
from pdf2image import convert_from_path
import pytesseract

from helpers import convert_date, is_numeric_ignore_spaces
from nlp_utils import nlp, predict, health_number_questions, outbreak_questions
from classification import classify_results, bucket_classification, cid_urgent_extract_lines, pregnancy_extract_lines
from rdnf_check import process_rdnf_check


def process_fax_pdf(pdf_path, poppler_path, output_folder):
    # Output folders
    no_results_path = os.path.join(output_folder, 'No Testing Results')
    rdnf_path = os.path.join(output_folder, 'RDNF')

    bucket_paths = {
        "Heps": os.path.join(output_folder, "Heps"),
        "STI": os.path.join(output_folder, "STI"),
        "Measles": os.path.join(output_folder, "Measles"),
        "Respiratory": os.path.join(output_folder, "Respiratory"),
        "CID": os.path.join(output_folder, "CID"),
        "TB": os.path.join(output_folder, "TB"),
        "Other": os.path.join(output_folder, "Other")
    }

    if process_rdnf_check(pdf_path, poppler_path, output_folder, rdnf_path):
        return

    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    extracted_texts = []
    page_health_numbers = {}
    page_outbreak_numbers = {}
    no_testing_pages = []
    date_from_page = "No_Date"

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.png')
        image.save(image_path, 'PNG')
        text = pytesseract.image_to_string(image)
        extracted_texts.append(text)

        if predict(text) != 1:
            no_testing_pages.append(i)
            continue

        date_result = nlp(image_path, "What is the date?")
        date_from_page = date_result[0]['answer'] if date_result else "No_Date"

        best_hn = {"answer": None, "score": 0}
        for q in health_number_questions:
            res = nlp(image_path, q)
            best = max(res, key=lambda x: x['score'])
            if best['score'] > best_hn['score']:
                best_hn = best

        if best_hn['score'] < 0.9 or not is_numeric_ignore_spaces(best_hn['answer']):
            health_number = f"Unknown_{i+1}"
        else:
            health_number = best_hn['answer'].replace(" ", "")

        if health_number not in page_health_numbers:
            page_health_numbers[health_number] = []
        page_health_numbers[health_number].append(i)

        best_ob = {"answer": None, "score": 0}
        for q in outbreak_questions:
            res = nlp(image_path, q)
            best = max(res, key=lambda x: x['score'])
            if best['score'] > best_ob['score']:
                best_ob = best

        if best_ob['score'] >= 0.9 and best_ob['answer'].strip():
            outbreak_number = best_ob['answer'].replace(" ", "")
        else:
            outbreak_number = None

        page_outbreak_numbers[health_number] = outbreak_number

    if no_testing_pages:
        no_results_pdf = fitz.open()
        pdf_document = fitz.open(pdf_path)
        for p in no_testing_pages:
            no_results_pdf.insert_pdf(pdf_document, from_page=p, to_page=p)

        try:
            date_str = convert_date(date_from_page)
        except Exception:
            date_str = "UnknownDate"

        base_name = os.path.basename(pdf_path).replace(".pdf", "")
        filename = f"{date_str}_{base_name}_No_Testing_Results.pdf"
        os.makedirs(no_results_path, exist_ok=True)
        no_results_pdf.save(os.path.join(no_results_path, filename))
        no_results_pdf.close()

    pdf_document = fitz.open(pdf_path)
    for health_number, pages in page_health_numbers.items():
        new_pdf = fitz.open()
        for p in pages:
            new_pdf.insert_pdf(pdf_document, from_page=p, to_page=p)

        text = "\n".join([extracted_texts[p] for p in pages])
        lines = [line for p in pages for line in extracted_texts[p].split('\n')]
        classified = classify_results(lines)
        bucket = list(bucket_classification(text))[0]
        base_path = bucket_paths[bucket]

        if bucket == "CID":
            urgency = "High Urgency" if cid_urgent_extract_lines(text) else "Low Urgency"
            base_path = os.path.join(base_path, urgency)

        if bucket == "Heps":
            preg = "Pregnant" if pregnancy_extract_lines(text) else "Not Pregnant"
            result = "Negative Results"
            for _, c in classified:
                if c == "Positive":
                    result = "Positive Results"
                    break
            destination = os.path.join(base_path, result, preg)
        else:
            result = "Negative Results"
            for _, c in classified:
                if c == "Positive":
                    result = "Positive Results"
                    break
            destination = os.path.join(base_path, result)

        os.makedirs(destination, exist_ok=True)
        page_str = "-".join(str(p+1) for p in pages)
        base_name = os.path.basename(pdf_path).replace(".pdf", "")
        date_str = convert_date(date_from_page)
        outbreak = page_outbreak_numbers.get(health_number)
        filename = f"{date_str}_{base_name}_Pages_{page_str}.pdf"

        out_path = os.path.join(output_folder, filename)
        new_pdf.save(out_path)
        new_pdf.close()

        shutil.move(out_path, os.path.join(destination, filename))

    pdf_document.close()
    print(f"Processed: {os.path.basename(pdf_path)}")
