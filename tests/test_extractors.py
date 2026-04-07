from src.extractors import EmailExtractor, NameExtractor


def test_email_extractor_valid_email() -> None:
    extractor = EmailExtractor()
    text = "JANE DOE\nSeattle, WA\njane.doe@gmail.com\nLinkedIn: github.com/janedoe"
    
    assert extractor.extract(text) == "jane.doe@gmail.com"


def test_name_extractor_standard_casing() -> None:
    extractor = NameExtractor()
    text = "Jane Doe\nAI Engineer\nEmail: jane.doe@gmail.com\nSummary: Experienced developer."
    
    assert extractor.extract(text) == "Jane Doe"


def test_name_extractor_uppercase_casing() -> None:
    extractor = NameExtractor()
    text = "JOHN SMITH\nDATA SCIENTIST\nEMAIL: JOHN.SMITH@EMAIL.COM"
    
    assert extractor.extract(text) == "John Smith"