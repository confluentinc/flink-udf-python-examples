from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from pyflink.table import DataTypes
from pyflink.table.types import DataType
from pyflink.table.udf import udf

nlp_engine = SpacyNlpEngine([{
    "lang_code": "en",
    "model_name": "en_core_web_sm",
}])
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
# print(analyzer.nlp_engine.get_supported_entities())
anonymizer = AnonymizerEngine()
def _anonymize_pii(text: str) -> str:
    analyzer_results = analyzer.analyze(text=text, language="en")
    # print(analyzer_results)
    result = anonymizer.anonymize(
        text=text, 
        analyzer_results=analyzer_results
    )
    return result.text

_anonymize_pii_input_types: list[DataType] = [DataTypes.STRING()]
anonymize_pii = udf(
    _anonymize_pii,
    input_types=_anonymize_pii_input_types,
    result_type=DataTypes.STRING(),
)
# print(anonymize_email("test@example.com"))
# print(anonymize_email("My name is Bond, James Bond. Contact me at james.bond@secretagent.com"))