function create_scatter_sentiment_option() {
    return {
        title: {
            text: '情感倾向',
            left: 'center',
        },
        xAxis: {
            name: '情感倾向'
        },
        yAxis: {
            name: '数量'
        },
        tooltip: {
            enterable: true,
        },
        series: [
            {
                symbolSize: 8,
                data: [],
                type: 'scatter'
            }
        ]
    }
}