console.log('detail page')

window.onload = async function loadMylist() {
    const response = await fetch('http://127.0.0.1:8000/musicplaylist/5/detail/', { method: "GET" })

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