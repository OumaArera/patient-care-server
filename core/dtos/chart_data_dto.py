from core.utils.format_null_values import format_value

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
                "patientId": chart_data.get('patient__patientId'),
                "patientName": format_value(
                    chart_data.get('patient__firstName'),
                    chart_data.get('patient__lastName')
                ),
                "behaviors": chart_data.get('behaviors'),
                "behaviorsDescription": chart_data.get('behaviorsDescription'),
                "vitals": chart_data.get("vitals"),
                "timeToBeTaken": chart_data.get('timeToBeTaken'),
                "createdAt": chart_data.get('createdAt')
            }
        else:
            return {
                "chartDataId": chart_data.chartDataId,
                "patientId": chart_data.patient.patientId,
                "patientName": format_value(
                    chart_data.patient.firstName,
                    chart_data.patient.lastName
                ),
                "behaviors": chart_data.behaviors,
                "behaviorsDescription": chart_data.behaviorsDescription,
                "vitals": chart_data.vitals,
                "timeToBeTaken": chart_data.timeToBeTaken,
                "createdAt": chart_data.createdAt
            }

    @staticmethod
    def transform_chart_data_list(chart_data_list):
        """
        Transforms a list of ChartData model instances into a list of dictionaries.
        """
        return [ChartDataResponseDTO.transform_chart_data(data) for data in chart_data_list]
