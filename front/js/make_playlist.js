
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
