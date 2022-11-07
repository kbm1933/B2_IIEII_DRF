console.log('detail page')

function getParameterByName(name){
    name = name.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex. exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

var parameter = window.location.href
var plid = getParameterByName('pl_id')

window.onload = async function loadMylist() {
    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${plid}/detail/`, { method: "GET" })

    response_json = await response.json()
    list_json = response_json.playlist_select_musics
    console.log(response_json)

    const title = document.getElementById('title')
    if (response_json.playlist_title === null) {
        title.innerText = "playlist" + response_json.id
    } else {
        title.innerText = response_json.playlist_title
    }


    const content = document.getElementById('content')
    const my_content = document.createElement('p')
    my_content.innerText = response_json.playlist_content
    content.appendChild(my_content)

    const create_at = document.getElementById('create_at')
    const my_create_at = document.createElement('p')
    my_create_at.innerText = response_json.playlist_update_at
    create_at.appendChild(my_create_at)
    const pl_id =  response_json.id

    const btn = document.getElementById('choice_btn')
    const edit_txt = document.createElement('a')
    edit_txt.setAttribute("href", `edit.html?pl_id=${pl_id}`)
    edit_txt.innerText = "수정하기"
    btn.appendChild(edit_txt)

    const my_list = document.getElementById('my_playlist')
    list_json.forEach(element => {

        const my_music = document.createElement("li")
        my_music.innerText = element.music_title + '\u00a0' + '-' + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)

        my_list.appendChild(my_music)
        my_list.appendChild(img)

    });
} 

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}