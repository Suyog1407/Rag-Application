import PyPDF2

def read_pdf(file_path):
    text = ""
    
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            text += page.extract_text()
    
    return text


if __name__ == "__main__":
    result = read_pdf("data/sample.pdf")
    
    print("Total characters extracted:", len(result))
    print("----")
    print("First 500 characters:")
    print(result[:500])