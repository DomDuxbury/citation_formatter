import re
from dataclasses import dataclass

@dataclass
class Item():
    author: str

@dataclass
class Article(Item):
    name: str
    doi: str
    journal: str
    title: str
    year: str
    issn: str = None
    volume: str = None
    number: str = None
    pages: str = None
    month: str = None
    date_accessed: str="Nov 15 2023"

    def create_reference(self):
      reference = f"\\bibitem{{{self.name}}} {self.author},"
      reference +=f" ``{self.title}'' in \emph{{{self.journal}}}, "
      if self.volume:
        reference += f"vol. ${self.volume}$,"
      if self.number:
        reference += f" no. ${self.number}$,"
      if self.pages:
        reference += f" pp. \emph{{{self.pages}}},"
      if self.month:
        reference += f" {self.month.capitalize()},"
      
      reference += f" {self.year}."
      reference += f" Accessed on: {self.date_accessed},"
      reference += f" DOI: {self.doi}, [Online]."
      return reference

def load_references_file():
  with open('./reference_data.bib') as f:
    file_str = f.read()
  return file_str


def parse_item(item_string_groups):
  article_type = item_string_groups[0].replace("@", "") \
                    .replace("{", "")
  article_name = item_string_groups[1].replace(",", "")
  content = item_string_groups[2].split("\n")
  article_fields = Article.__dataclass_fields__

  content_dict = {}
  if article_type == "article":
    for line in content:
      key, value = get_line_key_and_value(line)
      if key in article_fields:
        content_dict[key] = value
  
    item = Article(name=article_name, **content_dict)
    print(item.create_reference())
    print("")


def get_all_articles(file_str: str):
  items_string_groups = re.findall(
    "(@.+{)(.+)((?:\n.+)+})", file_str
  )
  for item in items_string_groups:
    parse_item(item)

def get_line_key_and_value(line: str):
  line_string_groups = re.findall(
    "\s*([a-zA-Z]+)\s*=\s*{(.+)}", line
  )
  if line_string_groups:
    group = line_string_groups[0]
    key = group[0]
    value = group[1]
    return (key, value)
  else:
    return (None, None)


def main():
  file_str = load_references_file()
  get_all_articles(file_str)

if __name__ == '__main__':
  main()