
clock();//時計の初期化
setInterval(clock, 1000);//時計の更新

//曜日を表示する関数
function renderDay(i) {
    return ['日', '月', '火', '水', '木', '金', '土'][i];
}

//十の位を表示
function set2fig(num) {
   var ret;
   if( num < 10 ) { ret = "0" + num; }
   else { ret = num; }
   return ret;
}

//時計の表示と更新をする関数
function clock() {
    var timer = document.getElementById('timer');
    var now = new Date();
    var hour = set2fig(now.getHours())
    var minute = set2fig(now.getMinutes())
    timer.innerHTML = '現在<br>'+renderDay(now.getDay()) + '曜日<br>' + hour +　':' + minute;
}

