function myfunc(){
    const url_div = document.getElementById('short-url')
    const url_to_hash = document.getElementsByName('url')[0].value

    var request = new XMLHttpRequest()
    request.open('POST', 'http://127.0.0.1:5000/put/', true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.onload = function() {
        var data = JSON.parse(this.response)
        console.log(this.response)
        if (data['status'] == 200) {
            url_div.style.display = "flex"
            url_div.innerHTML = 'http://127.0.0.1:5000/' + data['short_url']
        }
        if (data['status'] == 429) {
            url_div.style.display = "flex"
            url_div.innerHTML = 'Too many request. Try after in a minute'
        }
    }

    request.send("url=" + url_to_hash)
}