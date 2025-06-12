import re

def classify_results(lines):
    """
    Classifies lines of text based on the presence of specific keywords indicating positive, negative, or neutral results.

    Parameters:
        lines (list of str): The lines of text to be classified.

    Returns:
        list of tuple: Each tuple contains a line of text and its classification ('Positive', 'Negative', or 'Neutral').
    """
    results = []
    for line in lines:
        if re.search(r'(?=.*\bnegative\b)(?=.*\bpositive\b).*', line, re.IGNORECASE):
            results.append((line, "Positive"))
        elif re.search(r'not detected|negative|notdetected|not isolated', line, re.IGNORECASE):
            results.append((line, "Negative"))
        elif re.search(r'detected|positive|reactive|growth|identified', line, re.IGNORECASE):
            results.append((line, "Positive"))
        else:
            results.append((line, "Neutral"))
    return results

def bucket_classification(text):
    buckets = {
        "Heps": ["Hepatitis B", "Hepatitis C"],
        "STI": ["Chlamydia", "Gonorrhea", "Syphilis", "HIV", "Ophthamlia Neonatorum", "Chancroid", "Haemophilus Ducreyi", "H. Ducreyi",
                "Chlamydia Trachomatis", "Neisseria Gonorrhoeae", "O. Neonatorum", "Treponema Pallidum", "Human Immunodeficiency Virus"],
        "Measles": ["Measles"],
        "Respiratory": ["Adenovirus", "Coronavirus", "COVID", "COVID 19", "Enterovirus", "Influenza A", "Influenza B", 
                        "Human Metapneumovirus", "Parainfluenza Virus", "Rhinovirus", "RSV"],
        "TB": ["Acid Fast Bacilli", "AFB", "Mycobacterium", "Mycobacterial Culture", "Tuberculosis"],
        "CID": ["Acute Flaccid Paralysis", "Amebiasis", "Anaplasmosis", "Anthrax", "Babesiosis", "Blastomycosis", "Botulism", 
                "Brucellosis", "Candida Auris", "Campylobacter", "Cryptosporidiosis", "Cyclosporiasis", "Diphtheria", "E. Coli", 
                "Encephalitis", "Giardiasis", "Haemophilus", "Haemophilus Influenzae Disease", "Haemophilus Influenzae", 
                "Legionellosis", "Listeriosis", "Lyme Disease", "Meningococcal", "Monkeypox", "Mpox", "Orthopox", "Paratyphoid", 
                "Pertussis", "Plague", "Poliomyelitis", "Q Fever", "Rabies", "Rubella", "Salmonellosis", "Shigellosis", 
                "Tetanus", "Clostridium tetani", "Clostridium tetanis", "Trichinosis", "Tularemia", "Typhoid", "Varicella", 
                "West Nile", "Yersiniosis", "Salmonella enterica ser. Typhi", "Enterovirus D68", "Entamoeba Histolytica", 
                "Anaplasmosis Phagocytophilum", "Bacillus Anthracis", "Babesia", "Blastomyces Dermatitidis", "Blastomyces Gilchristii", 
                "Clostridium Botulinum", "Brucella Species", "Candida Auris", "C. Auris", "Campylobacter Species", "Vibrio Cholerae", 
                "Cryptosporidium", "Cyclospora Cayetanensis", "Corynebacterium Diphtheriae", "Echinococcus Multilocularis", "SFBI", 
                "Giardia Lamblia", "Streptococcus Pyogenes", "Haemophilus Influenzae Disease", "Hantavirus", "Ebola", "Lassa", "Marburg", 
                "Legionella", "Mycobacterium Leprae", "Listeria monocytogenes", "Borrelia burgdorferi", "Neisseria meningitidis", 
                "Gram Negative Diplococci", "Monkeypox Virus", "Orthopox", "Orthopoxvirus", "Poxvirus", "Salmonella Paratyphi A", 
                "Salmonella Paratyphi B", "Salmonella Paratyphi C", "Bordetella Pertussis", "Yersinia Pestis", "Polio", "Powassan Virus", 
                "Coxiella Burnetii", "Shigella Species", "Variola Virus", "Group B Streptococcus", "Streptococcus Pneumoniae", "Clostridium Tetani", 
                "Creutzfeld-Jakob Disease", "CJD", "Trichinella", "Francisella Tularensis", "Salmonella typhi, Salmonella Enterica ser. Typhi", 
                "Varicella-Zoster Virus", "VZV", "Yersinia Species"]
    }
    matched = set()
    t = text.lower()
    for bucket, keywords in buckets.items():
        if any(k.lower() in t for k in keywords):
            matched.add(bucket)
    if not matched:
        matched.add("Other")
    return matched

def cid_urgent_extract_lines(text):
    """
    Extracts lines from text that contain specific keywords related to high priority CID diseases.

    Parameters:
    text (str): The input text from which lines are to be extracted.

    Returns:
    list of str: Lines containing keywords/phrases.
    """
    
    pattern = re.compile(
        r'.*('
        r'Enterovirus D68|Bacillus Anthracis|Clostridium Botulinum|Brucella Species|Candida Auris|C. Auris|'
        r'Vibrio Cholerae|Corynebacterium Diphtheriae|SFBI|Streptococcus Pyogenes|'
        r'Haemophilus Influenzae Disease|Hantavirus|Ebola|Lassa|Marburg|'
        r'Orthopox|Orthopoxvirus|Poxvirus|Legionella|Listeria Monocytogenes|'
        r'Neisseria Meningitidis|Gram Negative Diplococci|Monkeypox Virus|Orthopox|Orthopoxvirus|Poxvirus|'
        r'Salmonella Paratyphi A|Salmonella Paratyphi B|Salmonella Paratyphi C|Bordetella Pertussis|'
        r'Shigella Species|Variola Virus|Clostridium Tetani|Creutzfeld-Jakob Disease|CJD|'
        r'Francisella Tularensis|Salmonella Typhi|Salmonella Enterica ser. Typhi|'
        r'Acute Flaccid Paralysis|Anthrax|Botulism|Brucellosis|Candida Auris|Cholera|'
        r'Diphtheria|Escherichia Coli|E.Coli|Verotoxin Producing E.Coli|Food Poisoning|'
        r'Group A Streptococca|Streptococcal Group A|Hantavirus Pulmonary Syndrome|'
        r'Haemophilus Influenzae|Hemorrhagic Fevers|Hepatitis A|Avian Influenza|Legionellosis|'
        r'Listeriosis|Monkeypox|Mpox|Orthopox|Orthopoxvirus|Poxvirus|Meningococcal Disease|'
        r'Mumps|Paralytic Shellfish Poisoning|PSP|Paratyphoid Fever|Pertussis|Whooping Cough|'
        r'Plague|Poliomyelitis Acute|Q Fever|Rabies|Human|Rubella|Congenital Syndrome|'
        r'Shigellosis|Smallpox|Tetanus|Transmissible Spongiform Encephalopathy|Clostridium tetanis|'
        r'TSE|Tularemia|Typhoid Fever|Salmonella enterica ser. Typhi|Yersinia Pestis|Polio|Coxiella Burnetii'
        r').*',
        re.IGNORECASE
    )
    lines = [line.strip() for line in text.split('\n') if pattern.search(line)]
    return lines


def pregnancy_extract_lines(text):
    """
    Extracts lines from text that contain specific keywords related to pregnancy.

    Parameters:
    text (str): The input text from which lines are to be extracted.

    Returns:
    list of str: Lines containing keywords/ phrases.
    """
    pattern = re.compile(r'.*(Prenatal|Perinatal|Gestational|Pregnancy|Antenatal|Pregnant).*', re.IGNORECASE)
    lines = [line.strip() for line in text.split('\n') if pattern.search(line)]
    return lines
