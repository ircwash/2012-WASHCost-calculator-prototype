{% load calculations %}

new Highcharts.Chart({

    chart: {

        renderTo: 'chart-life2',

        plotBackgroundColor: null,

        plotBorderWidth: null,

        plotShadow: false

    },

    credits: {
        enabled: false
    },

    title: {

        text: 'Total cumulative expenditure per cost component after 20 years'

    },

    tooltip: {

        formatter: function() {

            return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.y, 1);

        }

    },

    plotOptions: {

        pie: {

            allowPointSelect: true,

            cursor: 'pointer',

            dataLabels: {

                enabled: true,

                color: '#000000',

                connectorColor: '#000000',

                formatter: function() {

                    return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.y, 2);

                }

            }

        }{% if pdf %},
        series: {
			enableMouseTracking: false,
			shadow: false,
			animation: false
		}
		{% endif %}
    },

    series: [{

        type: 'pie',

        name: 'pie',

        data: [

            ['CapExHrd',   {{ cum_capexhrd.19 }}],
            ['CapManEx', {{ cum_capmanex.19 }}],
            ['ExpIDS', {{ cum_capexpids.19 }}],
            ['CapExSft', {{ cum_capexsft.19 }}],
            ['OpEx', {{ cum_capopex.19 }}],
            ['ExpDS', {{ cum_capexpds.19 }}],

        ]

    }]

});

new Highcharts.Chart({
    chart: {
        renderTo: 'chart-life',
        type: 'column'
    },
    credits: {
        enabled: false
    },

    title: {
        text : 'Cumulative expenditure per stakeholder over 20 years. Who pays for what?'
    },
    xAxis: {
        categories: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        title: {
            text: 'Year'
        },
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Total expenditure'
        },
        stackLabels: {
            enabled: false,
            style: {
                fontweight: 'bold',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'

            }
        }
    },
    tooltip: {
        formatter: function() {
            return Highcharts.numberFormat(this.y, 2);
        }


    },
    legend: {
        align: 'right',
        x: -100,
        verticalAlign: 'top',
        y: 50,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: false,
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
        }{% if pdf %},
        series: {
			enableMouseTracking: false,
			shadow: false,
			animation: false
		}
		{% endif %}
    },
    series: [{
    		name: 'Household',
	        data: {{ HOU_serie }},
            color: '#4572A7'
        }, {
            name: 'Government',
            data: {{ GOV_serie }},
            color: '#AA4643'
        }, {

            name: 'NGO',
            data: {{ NGO_serie }},
            color: '#89A54E'
            }, {
            name: 'Expenditure shortfall',
            data: {{ mod_opex_capman }},
            color: '#80699B'
        }, {
            name: 'Extensions due to population growth',
            data: {{ unalloc_serie }},
            color: '#3D96AE'


        }]
    })

new Highcharts.Chart({
    chart: {
        renderTo: 'chart-life3',
        type: 'column'
    },
    credits: {
        enabled: false
    },

    title: {
        text : 'Cumulative expenditure per cost component over 20 years'
    },
    xAxis: {
        categories: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        title: {
            text: 'Year'
        },
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Total expenditure'
        },
        stackLabels: {
            enabled: false,
            style: {
                fontweight: 'bold',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'

            }
        }
    },
    tooltip: {
        formatter: function() {
            return Highcharts.numberFormat(this.y, 2);
        }


    },

    legend: {
        align: 'right',
        x: -100,
        verticalAlign: 'top',
        y: 50,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: false,
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
        }{% if pdf %}, 
        series: {
			enableMouseTracking: false,
			shadow: false,
			animation: false
		}
		{% endif %}
    },
    series: [{
        name: 'CapExHrd',
        data: {{ cum_capexhrd }}
    }, {
        name: 'CapManEx',
            data: {{ cum_capmanex }}
    }, {
        name: 'ExpIDS',
            data: {{ cum_capexpids }}
    }, {
        name: 'CapExSft',
            data: {{ cum_capexsft }}
    }, {
    name: 'CoC',
        data: {{ COC }}
    }, {
        name: 'OpEx',
            data: {{ cum_capopex }}
    }, {
        name: 'ExpDs',
            data: {{ cum_capexpds }}
}]
})

new Highcharts.Chart({
    chart: {
        renderTo: 'chart-life4',
        type: 'column'
    },
    credits: {
        enabled: false
    },

    title: {
        text : 'Cumulative proportional expenditure per stakeholder'
    },
    xAxis: {
        categories: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        title: {
            text: 'Year'
        },
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Total expenditure'
        },
        stackLabels: {
            enabled: false,
            style: {
                fontweight: 'bold',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'

            }
        }
    },
    tooltip: {
        formatter: function() {
            return Highcharts.numberFormat(this.y, 2);
        }


    },

    legend: {
        align: 'right',
        x: -100,
        verticalAlign: 'top',
        y: 50,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    plotOptions: {
        column: {
            stacking: 'percent',
            dataLabels: {
                enabled: false,
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
        }{% if pdf %},
    series: {
        enableMouseTracking: false,
            shadow: false,
            animation: false
    }
    {% endif %}
},
series: [{
    name: 'Household',
    data: {{ HOU_serie }},
    color: '#4572A7'
}, {
    name: 'Government',
    data: {{ GOV_serie }},
    color: '#AA4643'
}, {
    name: 'NGO',
    data: {{ NGO_serie }},
    color: '#89A54E'
}, {
    name: 'Extension costs',
    data: {{ unalloc_serie }},
    color: '#3D96AE'
}, {
    name: 'Shortfall',
    data: {{ mod_opex_capman }},
    color: '#80699B'
}]
})
