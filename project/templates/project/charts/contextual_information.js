{% load calculations %}

new Highcharts.Chart({

    chart: {

        renderTo: 'chart-contextual',

        type: 'line',

        margin: [ 50, 50, 100, 80]

    },

    credits: {
        enabled: false
    },
	
	{% if pdf %}
	plotOptions: {
		series: {
			enableMouseTracking: false,
			shadow: false,
			animation: false
		}
	},
	{% endif %}
	
    title: {

        text: 'Predicted Population Size'

    },

    xAxis: {

        categories: [


        ],

        labels: {

            align: 'center',

            style: {

                fontSize: '13px',

                fontFamily: 'Verdana, sans-serif'

            }

        }

    },

    yAxis: {

        min: 0,

        title: {

            text: 'Population'

        }

    },

    legend: {

        enabled: false

    },

    tooltip: {

        formatter: function() {

            return '<b>'+ this.x +'</b><br/>'+

                'Cost: '+ Highcharts.numberFormat(this.y, 1)

        }

    },

        series: [{

        name: 'Cost',
		
		{% with value=answers.1|default:0 exponent=answers.2|default:0 %}
        data: {{ value|yearly_growth:exponent }},
		{% endwith %}

        dataLabels: {

            enabled: true,

            rotation: -90,

            color: '#FFFFFF',

            align: 'right',

            x: -3,

            y: 10,

            formatter: function() {

                return this.y;

            },

            style: {

                fontSize: '13px',

                fontFamily: 'Verdana, sans-serif'

            }

        }

    }]

});