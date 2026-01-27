from presidio_anonymizer import AnonymizerEngine, RecognizerResult
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from pyflink.table.types import DataTypes, DataType
from pyflink.table.udf import udf, ScalarFunction, FunctionContext
from typing_extensions import override


class MaskPii(ScalarFunction):
    """Flink UDF to anonymize PII (Personally Identifiable
    Information) using Presidio.

    """

    def __init__(self) -> None:
        # Setup all your variables you will lazy load with `None`
        # values.

        self._analyzer: AnalyzerEngine | None = None

        # Quick loading values can still be set here.

        self._anonymizer = AnonymizerEngine()  # type: ignore[no-untyped-call]

        # Configure anonymizer to use asterisks for all entity types
        # This creates a default operator that replaces with asterisks
        self._operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "****"})}

    @override
    def open(self, function_context: FunctionContext) -> None:
        # Initialize the NLP engine with the spaCy model
        # The model should be pre-installed and included in the build zip file
        model_name = "en_core_web_sm"
        nlp_engine = SpacyNlpEngine(
            [
                {
                    "lang_code": "en",
                    "model_name": model_name,
                }
            ]
        )

        # Then init your expensive lazy-loaded values.
        self._analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

    @override
    def eval(self, text: str | None) -> str | None:
        """Anonymize PII in the input text.

        Args:

            text: Input text that may contain PII

        Returns:

            Text with PII anonymized, or None if input is None
        """
        if text is None:
            return None

        # Assert that the lazy load happened.
        assert self._analyzer is not None

        # Analyze the text for PII
        analyzer_results = self._analyzer.analyze(text=text, language="en")

        anonymizer_input = [
            RecognizerResult(r.entity_type, r.start, r.end, r.score)
            for r in analyzer_results
        ]

        # Anonymize the detected PII with asterisks
        result = self._anonymizer.anonymize(
            text=text,
            analyzer_results=anonymizer_input,
            operators=self._operators,
        )

        return result.text


_mask_pii_input_types: list[DataType] = [DataTypes.STRING()]
mask_pii = udf(
    MaskPii(),
    input_types=_mask_pii_input_types,
    result_type=DataTypes.STRING(),
)
