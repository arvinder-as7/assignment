function get_all_url(){
    var table = document.getElementById('url-table')
    var request = new XMLHttpRequest()
    request.open('GET', 'http://127.0.0.1:5000/getall', true)

    request.onload = function() {
        var data = JSON.parse(this.response)
        console.log(this.response)
        if (data['status'] == 200) {
            all_url = data['result']
            console.log(all_url)
            for(var i = 0; i < all_url.length; i++){
                var row = table.insertRow(i+1)
                row.id = all_url[i]['hash'] + '-row'
                var cell1 = row.insertCell(0)
                var cell2 = row.insertCell(1)
                var btn = document.createElement("BUTTON")
                btn.innerHTML = "Delete"
                btn.id = all_url[i]['hash']
                btn.setAttribute('onclick', "myfunc(this.id)")
                var cell3 = row.insertCell(2)
                cell1.innerHTML = all_url[i]['hash']
                cell2.innerHTML = all_url[i]['url']
                cell3.appendChild(btn)
            }
        }
        else{
            alert("Unable to fetch! Try after a minute")
        }
    }
    request.send()

}


function myfunc(hash){

    var row_to_delete = document.getElementById(hash + '-row')
    var table = document.getElementById('url-table')
    console.log(row_to_delete.parent)
    var request = new XMLHttpRequest()
    request.open('DELETE', 'http://127.0.0.1:5000/' + hash, true)

    request.onload = function() {
        var data = JSON.parse(this.response)
        console.log(this.response)
        if (data['status'] == 200) {
            table.removeChild(row_to_delete)
        }
        else{
            alert("Unable to delete! Try after a minute")
        }
    }
    request.send()
}