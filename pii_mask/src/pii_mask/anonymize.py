from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_anonymizer.operators import Operator
from presidio_anonymizer.operators.operator import OperatorType
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from pyflink.table import DataTypes
from pyflink.table.udf import udf, ScalarFunction


class DynamicMaskOperator(Operator):
    """
    Custom Presidio operator that dynamically masks each character with asterisks
    based on the length of the detected entity.
    """
    
    def operator_name(self) -> str:
        """
        Return the name of this operator.
        
        Returns:
            The operator name "dynamic_mask"
        """
        return "dynamic_mask"
    
    def operator_type(self) -> OperatorType:
        """
        Return the type of this operator.
        
        Returns:
            OperatorType.Anonymize
        """
        return OperatorType.Anonymize
    
    def operate(self, text: str, params: dict = None) -> str:
        """
        Replace each character in the text with an asterisk.
        
        Args:
            text: The text to mask (the detected PII entity)
            params: Optional parameters (not used in this implementation)
            
        Returns:
            A string of asterisks with the same length as the input text
        """
        if not text:
            return text
        return "*" * len(text)
    
    def validate(self, params: dict = None) -> None:
        """
        Validate operator parameters. This operator doesn't require any parameters.
        
        Args:
            params: Optional parameters to validate
        """
        # No parameters required for this operator
        pass


class AnonymizePii(ScalarFunction):
    """
    Flink UDF to anonymize PII (Personally Identifiable Information) using Presidio.
    """
    def __init__(self):
        self.open()
    
    def open(self, function_context=None):
        # Initialize the NLP engine with the spaCy model
        # The model should be pre-installed and included in the
        model_name = "en_core_web_sm"
        nlp_engine = SpacyNlpEngine([{
            "lang_code": "en",
            "model_name": model_name,
        }])
        
        # Initialize the analyzer and anonymizer engines
        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
        
        # Initialize anonymizer and register the custom operator
        self.anonymizer = AnonymizerEngine()
        # Register the custom operator class (not instance) with the operators factory
        self.anonymizer.operators_factory.add_anonymize_operator(DynamicMaskOperator)
        
        # Configure anonymizer to use the custom dynamic mask operator for all entity types
        # This operator will automatically mask each character with asterisks
        # based on the detected entity's length
        self.operators = {
            "DEFAULT": OperatorConfig("dynamic_mask", {})
        }
    
    def eval(self, text: str) -> str:
        """
        Anonymize PII in the input text.
        
        Args:
            text: Input text that may contain PII
            
        Returns:
            Text with PII anonymized, or None if input is None
        """
        if text is None:
            return None
        
        # Analyze the text for PII
        analyzer_results = self.analyzer.analyze(text=text, language="en")
        
        # Anonymize the detected PII with asterisks
        result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,
            operators=self.operators
        )
        
        return result.text


anonymize_pii = udf(
    AnonymizePii(),
    input_types=[DataTypes.STRING()],
    result_type=DataTypes.STRING()
)


def _anonymize_pii(text: str) -> str:
    instance = AnonymizePii()
    instance.open(None)  # None is acceptable for testing
    return instance.eval(text)

