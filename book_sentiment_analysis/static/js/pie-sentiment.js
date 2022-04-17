function create_pie_sentiment_option() {
    return {
        title: {
            text: '情感倾向值',
            x: 'center',
            y: '37%',
            textStyle: {
                fontWeight: 'bold',
                color: '#0580f2',
                fontSize: '45',
            },
            subtext: '情感倾向值',
            subtextStyle: {
                fontSize: 20
            }
        },
        color: ['rgba(176, 212, 251, 1)'],
        series: [
            {
                name: 'sentiment',
                type: 'pie',
                clockWise: true,
                radius: ['50%', '66%'],
                itemStyle: {
                    normal: {
                        label: {
                            show: false,
                        },
                        labelLine: {
                            show: false,
                        },
                    },
                },
                hoverAnimation: false,
                data: [
                    {
                        name: 'positive',
                        value: 67,
                        itemStyle: {
                            normal: {
                                color: '#367bec',
                                label: {
                                    show: false,
                                },
                                labelLine: {
                                    show: false,
                                },
                            },
                        },
                    },
                    {
                        name: 'negative',
                        value: 33,
                    },
                ],
            },
        ],
    }
}