const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']

console.log('profile 불러옴')

window.onload = async function loadTop100(){
    const response = await fetch (`http://127.0.0.1:8000/musicplaylist/${userId}/`, {method:"GET"})

    response_json = await response.json()

    console.log(response_json)

    const profile_info = document.getElementById('title')
    const playlist_info = document.getElementById('playlist_info')
    
    profile_json = response_json.playlist
    profile_info.innerText = profile_json[0].playlist_user + '님의 Playlist'

    
    profile_json.forEach(element => {

        const playlist_title = document.createElement("li")
        const detail_txt = document.createElement("a")
        detail_txt.setAttribute("href",'playlist_detail.html')
        detail_txt.innerText = "보기"

        if(element.playlist_title === null){
            playlist_title.innerText = "이름없는 플레이리스트" 
        } else {
            playlist_title.innerText = element.playlist_title
        }
        
        playlist_info.appendChild(playlist_title)
        playlist_info.appendChild(detail_txt)
    });
} 


