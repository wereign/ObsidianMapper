import markdown
from bs4 import BeautifulSoup

def parse_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    html_content = markdown.markdown(content)
    soup = BeautifulSoup(html_content, 'html.parser')

    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    text_blocks = soup.find_all(['p', 'ul', 'ol'])

    heading_texts = [heading.get_text() for heading in headings]
    text_block_texts = [text_block.get_text() for text_block in text_blocks]

    return heading_texts, text_block_texts

# Example usage
file_path = './4.Data Engineering.md'
headings, text_blocks = parse_markdown_file(file_path)

print("Headings:")
print(headings)

print("\nText Blocks:")
print(text_blocks)
