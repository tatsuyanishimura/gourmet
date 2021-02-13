var form = document.forms.search
const info = document.querySelector('#info')
if('geolocation' in navigator){
    info.innerHTML = "確認中"
}else{
    info.innerHTML = "位置が取得出来ません"
}

var wid = navigator.geolocation.watchPosition(watchFunc)
function watchFunc(pos){
    var lng = pos.coords.longitude //経度
    var lat = pos.coords.latitude //緯度
    form.lat.value = lat //緯度
    form.lng.value = lng //経度
    info.innerHTML = ""
}