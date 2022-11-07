console.log('edit page')

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

var parameter = window.location.href
var plid = getParameterByName('pl_id')

window.onload = async function loadMylist() {
    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${plid}/detail/`, { method: "GET" })

    response_json = await response.json()
    console.log(response_json)

    const title = document.getElementById('page_title')
    if (response_json.playlist_title === null) {
        title.innerText = "playlist" + response_json.id + '수정'
    } else {
        title.innerText = response_json.playlist_title + '수정'
    }
    const my_list = document.getElementById('recommend_playlist')
    list_json = response_json.playlist_select_musics

    list_json.forEach(element => {
        // const add_btn = document.createElement("button")
        // add_btn.innerText = "제거"

        const my_music = document.createElement("li")
        my_music.innerText = element.music_title + '\u00a0' + '-' + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)

        my_list.appendChild(my_music)
        my_list.appendChild(img)
        // my_list.appendChild(add_btn)

    });
}

async function edit_playlist() {
    const token = localStorage.getItem('access')
    const title = document.getElementById("title").value
    const content = document.getElementById("content").value
    console.log(title, content)

    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${plid}/detail/`, {
        headers: {
            'Authorization': 'Bearer ' + token,
            'content-type': 'application/json',
        },
        method: 'PUT',
        body: JSON.stringify({
            // "playlist_select_musics" : [1,2,3],
            "playlist_title": title,
            "playlist_content": content
        })
    })
    console.log(response)
    alert("완료");
    window.location.replace('profile.html')
}

async function delete_playlist() {
    const token = localStorage.getItem('access')
    let delete_msg = confirm("플레이리스트를 삭제할까요?");
    
    if (delete_msg){
    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${plid}/detail/`, {
        headers: {
            'Authorization': 'Bearer ' + token,
            'content-type': 'application/json',
        },
        method: 'DELETE',

    }).then(window.location.replace("profile.html"))
    console.log(response)
    alert("삭제 완료");
}}

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}