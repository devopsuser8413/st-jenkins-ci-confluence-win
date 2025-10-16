def count_sections(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith('## '))

if __name__ == '__main__':
    sample = """
# Title

## Section 1
Some content

## Section 2
More content
"""
    print('Sections:', count_sections(sample))
