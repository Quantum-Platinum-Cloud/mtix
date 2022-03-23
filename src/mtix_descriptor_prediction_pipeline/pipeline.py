from .utils import avg_top_results, base64_decode, create_query_lookup, extract_citation_data


class DescriptorPredictionPipeline:
    def __init__(self, cnn_model_top_n_predictor, pointwise_model_top_n_predictor, listwise_model_top_n_predictor, results_formatter):
        self.input_data_parser = InputDataParser()
        self.cnn_model_top_n_predictor = cnn_model_top_n_predictor
        self.pointwise_model_top_n_predictor = pointwise_model_top_n_predictor
        self.listwise_model_top_n_predictor = listwise_model_top_n_predictor
        self.results_formatter = results_formatter

    def predict(self, input_data):
        citation_data = self.input_data_parser.parse(input_data)
        query_lookup = create_query_lookup(citation_data)
        cnn_results = self.cnn_model_top_n_predictor.predict(citation_data)
        pointwise_results = self.pointwise_model_top_n_predictor.predict(query_lookup, cnn_results)
        pointwsie_avg_results = avg_top_results(cnn_results, pointwise_results)
        listwise_results = self.listwise_model_top_n_predictor.predict(query_lookup, pointwsie_avg_results)
        listwise_avg_results = avg_top_results(pointwsie_avg_results, listwise_results)
        predictions = self.results_formatter.format(listwise_avg_results)
        return predictions


class InputDataParser:
    def __init__(self):
        pass
    
    # TODO: what about null outputs
    def parse(self, input_data):
        citation_data_list = []
        for item in input_data:
            citation_xml = item["data"]
            citation_xml = base64_decode(citation_xml)
            citation_data = extract_citation_data(citation_xml)
            citation_data_list.append(citation_data)
        return citation_data_list


class MtiJsonResultsFormatter:
    def __init__(self, dui_lookup, threshold):
        self.dui_lookup = dui_lookup
        self.threshold = threshold

    def format(self, results):
        mti_json_object = None
        return mti_json_object