from langchain_community.document_loaders import TextLoader as BaseTextLoader
from langchain_core.documents import Document
from pathlib import Path
from typing import List

class TextLoader(BaseTextLoader):
    def load(self) -> List[Document]:
        text = self.file_path.read_text(encoding="utf-8")
        metadata = {"source": str(self.file_path)}
        return [Document(page_content=text, metadata=metadata)]