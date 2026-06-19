def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size         # where this chunk ends
        chunk = text[start:end]          # slice the text
        chunks.append(chunk)             # add to list
        start = end - overlap            # move forward, but overlap a little

    return chunks


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from backend.read_pdf import read_pdf

    raw_text = read_pdf("data/sample.pdf")
    print("=" * 80)
    print(raw_text[:2000])
    print("=" * 80)

    chunks = chunk_text(raw_text)

    # see the results
    print(f"Total chunks created: {len(chunks)}")
    print("----")
    print("Chunk 1:")
    print(chunks[0])
    print("----")
    print("Chunk 2:")
    print(chunks[1])