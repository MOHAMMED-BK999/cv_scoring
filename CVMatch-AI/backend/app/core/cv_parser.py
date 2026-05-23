import re
import tempfile
import unicodedata
import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


MIN_EXTRACTED_WORDS = 20
SUPPORTED_SUFFIXES = {".pdf", ".docx"}
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "with",
    "your",
    "you",
    "avec",
    "dans",
    "des",
    "du",
    "et",
    "la",
    "le",
    "les",
    "un",
    "une",
}


class CVParser:
    """Extract readable markdown/text from uploaded CV files."""

    def __init__(self) -> None:
        self._converter = None

    def _get_docling_converter(self):
        if self._converter is not None:
            return self._converter
        try:
            from docling.document_converter import DocumentConverter

            self._converter = DocumentConverter()
            return self._converter
        except Exception:
            return None

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        text = re.sub(r"\\+", "", text)
        text = re.sub(r"\*\*-----.*?-----\*\*", "", text, flags=re.DOTALL)
        text = re.sub(r"\+\]", "", text)
        encoding_fixes = {
            "ï1⁄4": " | ",
            "â€'": "-",
            "âc": "-",
            "â€": "-",
            "Â": "",
            "&amp;": "&",
        }
        for old, new in encoding_fixes.items():
            text = text.replace(old, new)

        text = unicodedata.normalize("NFKC", text)
        text = CVParser._remove_stop_words(text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def _remove_stop_words(text: str) -> str:
        def replace(match: re.Match[str]) -> str:
            word = match.group(0)
            return "" if word.lower() in STOP_WORDS else word

        text = re.sub(r"\b[A-Za-zÀ-ÿ']+\b", replace, text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r" +([,.;:!?])", r"\1", text)
        text = re.sub(r"([([{]) +", r"\1", text)
        text = re.sub(r" +([])}])", r"\1", text)
        return text

    @staticmethod
    def _has_enough_text(text: str) -> bool:
        return len(re.findall(r"\w+", text or "")) >= MIN_EXTRACTED_WORDS

    def parse_cv(self, file_bytes: bytes, filename: str) -> str:
        suffix = Path(filename or "upload.pdf").suffix.lower() or ".pdf"
        if suffix not in SUPPORTED_SUFFIXES:
            raise RuntimeError("Unsupported file type. Only PDF and DOCX files are supported.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = Path(tmp.name)

        try:
            return self.extract_path(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def extract_path(self, path: str | Path) -> str:
        path = Path(path)
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            try:
                import fitz

                with fitz.open(path) as doc:
                    text = "\n".join(page.get_text("text") for page in doc)
                text = self.clean_text(text)
                if self._has_enough_text(text):
                    return text
            except Exception as exc:
                raise RuntimeError(f"Unable to parse PDF: {exc}") from exc

            ocr_text = self._ocr_pdf(path)
            if self._has_enough_text(ocr_text):
                return ocr_text

            raise RuntimeError(
                "No readable text found in this PDF. It looks like a scanned/image CV, "
                "and OCR is not available. Install tesseract-ocr, pytesseract, and Pillow."
            )

        if suffix == ".docx":
            text = self._extract_docx(path)
            if self._has_enough_text(text):
                return text

        docling_text = self._extract_with_docling(path)
        if self._has_enough_text(docling_text):
            return docling_text

        if suffix == ".docx":
            raise RuntimeError(
                "No readable text found in this DOCX. The file may be empty, corrupted, "
                "or contain only images."
            )

        raise RuntimeError("Unsupported file type. Only PDF and DOCX files are supported.")

    def _extract_with_docling(self, path: Path) -> str:
        converter = self._get_docling_converter()
        if converter is None:
            return ""

        try:
            result = converter.convert(str(path))
            return self.clean_text(result.document.export_to_markdown())
        except Exception:
            return ""

    def _extract_docx(self, path: Path) -> str:
        try:
            with zipfile.ZipFile(path) as archive:
                document_names = [
                    "word/document.xml",
                    *sorted(
                        name
                        for name in archive.namelist()
                        if name.startswith("word/header") or name.startswith("word/footer")
                    ),
                ]
                parts = [
                    self._extract_docx_xml(archive.read(name))
                    for name in document_names
                    if name in archive.namelist()
                ]
        except Exception as exc:
            raise RuntimeError(f"Unable to parse DOCX: {exc}") from exc

        return self.clean_text("\n\n".join(part for part in parts if part))

    def _extract_docx_xml(self, xml_bytes: bytes) -> str:
        namespaces = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        }
        root = ET.fromstring(xml_bytes)
        blocks: list[str] = []

        for paragraph in root.findall(".//w:p", namespaces):
            runs: list[str] = []
            for node in paragraph.iter():
                if node.tag == f"{{{namespaces['w']}}}t" and node.text:
                    runs.append(node.text)
                elif node.tag == f"{{{namespaces['w']}}}tab":
                    runs.append("\t")
                elif node.tag == f"{{{namespaces['w']}}}br":
                    runs.append("\n")

            text = "".join(runs).strip()
            if text:
                blocks.append(text)

        return "\n".join(blocks)

    def _ocr_pdf(self, path: Path) -> str:
        try:
            import fitz
            import pytesseract
            from PIL import Image
        except Exception:
            return ""

        lang = os.getenv("OCR_LANG", "fra+eng")
        pages: list[str] = []
        try:
            with fitz.open(path) as doc:
                for page in doc:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    try:
                        pages.append(pytesseract.image_to_string(image, lang=lang))
                    except Exception:
                        pages.append(pytesseract.image_to_string(image))
        except Exception:
            return ""

        return self.clean_text("\n".join(pages))
