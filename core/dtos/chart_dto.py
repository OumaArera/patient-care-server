from core.utils.format_null_values import format_value


class ChartResponseDTO:
    """
    Data Transfer Object for Chart Model
    """

    @staticmethod
    def transform_chart(chart):
        """Transforms a Chart model instance into a dictionary."""
        if isinstance(chart, dict):
            return {
                "chartId": chart.get('chartId'),
                "patientId": chart.get('patient__patientId'),
                "patientName": format_value(
                    chart.get('patient__firstName'),
                    chart.get('patient__lastName')
                ),
                "careGiver": format_value(
                    chart.get('careGiver__firstName'),
                    chart.get('careGiver__lastName')
                ),
                "behaviors": chart.get('behaviors'),
                "behaviorsDescription": chart.get('behaviorsDescription'),
                "status": chart.get("status"),
                "reasonNotFiled": chart.get("reasonNotFiled"),
                "dateTaken": chart.get('dateTaken'),
                "createdAt": chart.get('createdAt'),
                "modifiedAt": chart.get("modifiedAt"),
            }
        else:
            return {
                "chartId": chart.chartId,
                "patientId": chart.patient.patientId,
                "patientName": format_value(
                    chart.patient.firstName, 
                    chart.patient.lastName
                ),
                "careGiver": format_value(
                    chart.careGiver.firstName, 
                    chart.careGiver.lastName
                ) if chart.careGiver else None,
                "behaviors": chart.behaviors,
                "behaviorsDescription": chart.behaviorsDescription,
                "status": chart.status,
                "reasonNotFiled": chart.reasonNotFiled,
                "dateTaken": chart.dateTaken,
                "createdAt": chart.createdAt,
                "modifiedAt": chart.modifiedAt,
            }

    @staticmethod
    def transform_chart_list(chart_list):
        """Transforms a list of Chart model instances into a list of dictionaries."""
        return [ChartResponseDTO.transform_chart(chart) for chart in chart_list]