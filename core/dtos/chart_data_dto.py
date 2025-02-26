class ChartDataResponseDTO:
    """
    Data Transfer Object for ChartData Model
    """
    @staticmethod
    def transform_chart_data(chart_data):
        """
        Transforms a ChartData model instance into a dictionary.
        """
        if isinstance(chart_data, dict):
            return {
                "chartDataId": chart_data.get('chartDataId'),
                "behaviors": chart_data.get('behaviors'),
                "behaviorsDescription": chart_data.get('behaviorsDescription'),
                "vitals": chart_data.get("vitals"),
                "createdAt": chart_data.get('createdAt')
            }
        else:
            return {
                "chartDataId": chart_data.chartDataId,
                "behaviors": chart_data.behaviors,
                "behaviorsDescription": chart_data.behaviorsDescription,
                "vitals": chart_data.vitals,
                "createdAt": chart_data.createdAt
            }

    @staticmethod
    def transform_chart_data_list(chart_data_list):
        """
        Transforms a list of ChartData model instances into a list of dictionaries.
        """
        return [ChartDataResponseDTO.transform_chart_data(data) for data in chart_data_list]
