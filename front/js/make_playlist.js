
const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']

console.log('make playlist불러옴')

window.onload = async function loadTop100(){
    const response = await fetch (`http://127.0.0.1:8000/musicplaylist/${userId}/`, {method:"GET"})

    response_json = await response.json()

    console.log(response_json)

    const musics_list = document.getElementById('recommend_list')

    playlist_response = response_json.music_list

    console.log(playlist_response)

    playlist_response.forEach(element => {

        const music_check = document.createElement("INPUT")
        music_check.setAttribute("type", "checkbox")
        music_check.setAttribute("value", element.id)
        music_check.setAttribute("name", 'playlist_checkbox')

        const musics = document.createElement("li")
        musics.innerText = element.music_title + '\u00a0'+ '-'  + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)
        
        musics_list.appendChild(musics)
        musics_list.appendChild(img)
        musics_list.appendChild(music_check)
    });
} 

async function make_playlist(){
    var length = document.getElementsByName("playlist_checkbox").length;
    const music_id = []
    for (var i=0; i<length; i++){
        if(document.getElementsByName("playlist_checkbox")[i].checked == true){
            music_id.push(document.getElementsByName('playlist_checkbox')[i].value);
        }
    }
    const token = localStorage.getItem('access')
    const title = document.getElementById("title").value
    const content = document.getElementById("content").value
    console.log(title, content,  music_id)

    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${userId}/`,{
        headers: {
            'Authorization' : 'Bearer ' + token,
            'content-type' : 'application/json',
        },
        method : 'POST',
        body : JSON.stringify({
            "playlist_select_musics" : music_id,
            "playlist_title" : title,
            "playlist_content" : content
        })
    }).then(window.location.replace('profile.html'))
    console.log(response)
    alert("완료");
}


function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}

