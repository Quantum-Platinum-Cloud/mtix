import gzip
import json
import math
from mtix_descriptor_prediction_pipeline import create_descriptor_prediction_pipeline
from nose.plugins.attrib import attr
import os.path
from unittest import skip, TestCase


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DESC_NAME_LOOKUP_PATH = os.path.join(THIS_DIR, "data", "main_heading_names.tsv")
DUI_LOOKUP_PATH = os.path.join(THIS_DIR, "data", "main_headings.tsv")
TEST_SET_DATA_PATH = os.path.join(THIS_DIR, "data", "test_set_data.json.gz")
TEST_SET_PREDICTIONS_PATH = os.path.join(THIS_DIR, "data", "test_set_2017-2022_Listwise22Avg_Results.json.gz")


@attr(test_type="integration")
class TestDescriptorPredictionPipeline(TestCase):

    def setUp(self):
        self.pipeline = create_descriptor_prediction_pipeline(DESC_NAME_LOOKUP_PATH, 
                                                              DUI_LOOKUP_PATH, 
                                                              "tensorflow-inference-2022-04-01-22-15-17-484", 
                                                              "huggingface-pytorch-inference-2022-04-01-22-18-14-890", 
                                                              "huggingface-pytorch-inference-2022-04-01-22-21-50-717",
                                                              pointwise_batch_size=8)

    def test_predict(self):
        limit = 40000
        batch_size = 128

        test_set_data = json.load(gzip.open(TEST_SET_DATA_PATH, "rt", encoding="utf-8"))[:limit]
        expected_predictions = json.load(gzip.open(TEST_SET_PREDICTIONS_PATH, "rt", encoding="utf-8"))[:limit]

        citation_count = len(test_set_data)
        num_batches = int(math.ceil(citation_count / batch_size))

        predictions = []
        for idx in range(num_batches):
            batch_start = idx * batch_size
            batch_end = (idx + 1) * batch_size
            batch_inputs = test_set_data[batch_start:batch_end]
            batch_predictions = self.pipeline.predict(batch_inputs)
            predictions.extend(batch_predictions)
        
        self.assertEqual(predictions, expected_predictions, "Descriptor predictions not as expected.")