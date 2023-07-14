import re
import PyPDF2
import sys
import os

def func(x):
    return x

def extract_sections_from_pdf(pdf_file):
    pdf_sections = []

    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            content = page.extract_text();
            i=2;
            s="";
            for line in content.split('\n'):
                if re.match("Chapter", line):
                    s=line;
                    # print(line)
                    break;



            # print(content.splitlines()[2]);
            # print(content[1]);

            # # Customize this pattern to match your section headers
            # section_header_pattern = r'Chapter \d+'


            # # Find section headers using regex pattern
            # section_headers = re.findall(section_header_pattern, content)
            # print(section_headers);

            # for header in section_headers:

            st=s.replace(" ","");
            if(len(st)>0 and st[-1].isdigit):
                st = st[:-3]
            section = {
            'title': st,
            'page_number': page_num,
            'content': content
            }
            pdf_sections.append(section)
            # print(section);

    return pdf_sections


def extract_pdf_sections(pdf_files):
    all_sections = []

    for pdf_file in pdf_files:
        sections = extract_sections_from_pdf(pdf_file)

        for section in sections:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page = pdf_reader.pages[section['page_number']]
                # section['content'] = page.extract_text()

                # You can also store additional metadata here, such as the PDF file name
                section['pdf_file'] = pdf_file

        all_sections.extend(sections)

    return all_sections
def output_sections_to_files(sections):
    n_sec=[];
    for section in sections:
        section_title = section['title']
        if(section_title==""):
            continue;
        section['title']="";
        content=section['content'];
        for sec_2 in sections:
            sec=sec_2['title'];
            if(sec==section_title):
                content+=sec_2['content'];
                sec_2['title']="";
        secti = {
            'title': section_title,
            'content': content,
            'pdf_file':section['pdf_file']
            }
        n_sec.append(secti);


    for section in n_sec:
        pdf_file = section['pdf_file']
        section_title = section['title']
        content = section['content']

        # Generate a unique file name based on the section title
        file_name = section_title.replace('', '').replace(' ', '_') + '.txt'
        # print(section_title)

        basedir = os.path.abspath(os.path.dirname(__file__))

        with open(os.path.join(basedir,"/Job_hunt/1july23/auxoai/project/uploads",file_name), 'w') as file:
            file.write(content)

        print(f"Section '{section_title}' from '{pdf_file}' is written to '{file_name}'.")
