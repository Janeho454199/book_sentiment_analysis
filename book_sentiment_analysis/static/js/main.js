
// 检测到请求时候进行loading
const mask = '<div id="hicap_mask" style="width:100%;height:100rem;top:0px;left:0px;position:fixed;background:#FFF;opacity:0.9;z-index:998;"></div>';
const loading = '<div id="loading"><img src="../static/images/avatar.png" style="width:10rem;position:absolute;left:50%;top:50%;z-index:999;margin-left:-5rem;margin-top:-5rem;" />' +
    '<h2 style="width:10rem;position:absolute;left:52%;top:73%;z-index:999;margin-left:-5rem;margin-top:-5rem;">Loding...</h2></div>';

$(document).on('ajaxStart', function(e){
    $(mask).appendTo('body');
    $(loading).appendTo('body');
})

$(document).on('ajaxStop', function(e){
    $("#hicap_mask").remove();
    $("#loading").remove();
})


function draw(result) {
    // 初始化图表并绑定配置
    // 积极词云图
    const word_cloud_positive = echarts.init(document.getElementById('word-cloud'));
    const word_cloud_positive_option = create_word_cloud_option();
    // 绑定数据
    word_cloud_positive_option.series[0].data = result['data']['word_count'];
    word_cloud_positive_option.title.text = '情感词云图';
    word_cloud_positive.setOption(word_cloud_positive_option);

    // 好评率饼图
    const pie_sentiment = echarts.init(document.getElementById('pie-sentiment'));
    const pie_sentiment_option = create_pie_sentiment_option();
    // 绑定数据
    pie_sentiment_option.title.text = result['data']['positive_rate']['pos'].toString();
    pie_sentiment_option.series[0].data[0].value = result['data']['positive_rate']['pos'];
    pie_sentiment_option.series[0].data[1].value = result['data']['positive_rate']['neg'];
    pie_sentiment.setOption(pie_sentiment_option);

    // 雷达图
    const radar_sentiment = echarts.init(document.getElementById('radar-sentiment'));
    const scatter_radar_sentiment_option = create_radar_sentiment_option();
    scatter_radar_sentiment_option.series[0].data[0].value = result['data']['radar_sentiment'];
    radar_sentiment.setOption(scatter_radar_sentiment_option);

    // 情感值散点
    const scatter_sentiment = echarts.init(document.getElementById('scatter-sentiment'));
    const scatter_sentiment_option = create_scatter_sentiment_option();
    // 数据绑定
    scatter_sentiment_option.series[0].data = result['data']['sentiment_distribution'];
    scatter_sentiment.setOption(scatter_sentiment_option);

    // 好评
    document.getElementById('praise-comment').textContent = result['data']['praise_comment'];
    // 中评
    document.getElementById('medium-comment').textContent = result['data']['medium_comment'];
    // 差评
    document.getElementById('negative-comment').textContent = result['data']['negative_comment'];
    // 关键字
    document.getElementById('keyword').textContent = result['data']['keyword'];
    // 摘要
    document.getElementById('summary').textContent = result['data']['summary'];
    // 显示分析结果
    document.getElementsByClassName("right-box")[0].style.display = "inline-block";
}


function start_analysis(param) {
    $.ajax({
        url: '/detail/analysis/' + param,
        type: 'post',
        timeout: 2400000,
        beforeSend: function () {

            },
        complete: function () {

        },
        success:function(result){
            if (result['code'] === 200) {
                draw(result)
                document.getElementsByClassName('alert')[0].style.display = "none";
            } else if (result['code'] === 201) {
                document.getElementsByClassName('alert')[0].textContent = result['data'];
                document.getElementsByClassName('alert')[0].style.display = "block";
            } else {
                document.getElementsByClassName('alert')[0].textContent = "An error occurred. Please try again!";
                document.getElementsByClassName('alert')[0].style.display = "block";
            }
        },
        error:function(){

        }
    });
}
