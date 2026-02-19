import re
from typing import List, Dict
import tiktoken


class LegalChunker:
    """
    Chunk legal text while preserving section and clause boundaries.
    """

    def __init__(
        self,
        chunk_size: int = 700,
        chunk_overlap: int = 100,
        model_name: str = "gpt-3.5-turbo"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def _split_by_sections(self, text: str) -> List[str]:
        """
        Split text by legal sections/clauses.
        """
        pattern = r"(SECTION\s+\d+|Section\s+\d+|CLAUSE\s+\d+|Clause\s+\d+)"
        splits = re.split(pattern, text)

        sections = []
        buffer = ""

        for part in splits:
            if re.match(pattern, part):
                if buffer.strip():
                    sections.append(buffer.strip())
                buffer = part
            else:
                buffer += "\n" + part

        if buffer.strip():
            sections.append(buffer.strip())

        return sections

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Main chunking method.
        Returns list of chunk dicts with metadata.
        """
        sections = self._split_by_sections(text)
        chunks = []

        current_chunk = ""
        current_tokens = 0

        for section in sections:
            section_tokens = self._count_tokens(section)

            if current_tokens + section_tokens <= self.chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section
                current_tokens += section_tokens
            else:
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": metadata
                    })

                # Start new chunk
                current_chunk = section
                current_tokens = section_tokens

        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": metadata
            })

        # Add overlap (simple backward overlap)
        final_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                final_chunks.append(chunk)
            else:
                prev_text = final_chunks[-1]["text"]
                overlap_text = prev_text[-self.chunk_overlap:]
                merged_text = overlap_text + "\n\n" + chunk["text"]

                final_chunks.append({
                    "text": merged_text,
                    "metadata": metadata
                })

        return final_chunks
