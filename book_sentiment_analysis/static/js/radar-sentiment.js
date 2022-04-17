function create_radar_sentiment_option() {
    return {
        title: {
            text: '雷达图'
        },
        legend: {

        },
        tooltip: {
            enterable: true
        },
        radar: {
            // shape: 'circle',
            indicator: [
                {name: 'Max', max: 1},
                {name: 'Medium', max: 1},
                {name: 'Average', max: 1},
                {name: 'Mode', max: 1},
                {name: 'Min', max: 1},
            ]
        },
        series: [
            {
                type: 'radar',
                data: [
                    {
                        value: [],
                    }
                ]
            }
        ]
    }
}
