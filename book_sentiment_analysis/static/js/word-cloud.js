function create_word_cloud_option() {
    return {
        //设置标题，居中显示
        title: {
            text: '词云图',
            left: 'center',
        },
        tooltip: {
            show: true
        },

        series: [{
            type: 'wordCloud',
            sizeRange: [20, 60],
            rotationRange: [-90, 90],
            shape: 'circle',
            gridSize: 2,
            width: '80%',
            // 画布高
            height: '80%',
            textStyle: {
                fontFamily: 'sans-serif',
                fontWeight: 'bold',
                //生成随机的字体颜色
                color: function () {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                focus: 'self',
                textStyle: {
                    textShadowBlur: 2,
                    textShadowColor: '#333'
            }
                },
            data: [],
        },
        ],
    }
}
