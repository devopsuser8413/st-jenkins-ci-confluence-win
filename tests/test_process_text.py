from app.process_text import count_sections

def test_count_sections_empty():
    assert count_sections('') == 0

def test_count_sections_multiple():
    txt = '# Title\n\n## One\n## Two\n'
    assert count_sections(txt) == 2
