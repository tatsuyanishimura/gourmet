//曜日名を得る関数
function renderDay(i) {
    return ['日', '月', '火', '水', '木', '金', '土'][i];
}
//  毎分呼び出される関数
function clock() {

    var timer = document.getElementsByClassName('timer');
    var now = new Date();

    //曜日と時刻を表示
    timer.textContent = renderDay(now.getDay()) + '|' + now.getMinutes() +　':' + now.getHours();
}
//起動時に実行するプログラム
setInterval(clock, 60000);
