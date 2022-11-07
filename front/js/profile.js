const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']
const username = personObj['username']

console.log('profile 불러옴')

window.onload = async function loadTop100(){
    const response = await fetch (`http://127.0.0.1:8000/musicplaylist/${userId}/`, {method:"GET"})

    response_json = await response.json()

    console.log(response_json)

    // reponse 유저 리스트 추가

    var length = response_json.user_profile.length;
    for (var i=0; i<length; i++){
        if(userId == response_json.user_profile[i]["id"]){

            
            const user_profile_img = response_json.user_profile[i]["profile_img"]
            console.log(user_profile_img)

            const img = document.createElement('img')
            img.setAttribute('src', `http://127.0.0.1:8000${user_profile_img}`)

            console.log(img)
            
            const user_profile_tag = document.getElementById('user_profile_img')
            user_profile_tag.appendChild(img);
        
        }
    }

    const profile_info = document.getElementById('title')
    const playlist_info = document.getElementById('playlist_info')

    profile_json = response_json.playlist
    profile_info.innerText = username + '님의 Playlist'

    
    profile_json.forEach(element => {

        const playlist_title = document.createElement("li")
        const detail_txt = document.createElement("a")
        const pl_id = element.id
        detail_txt.setAttribute("href",`detail.html?pl_id=${pl_id}`)
        detail_txt.innerText = "보기"

        if(element.playlist_title === null){
            playlist_title.innerText = "Playlist" + element.id
        } else {
            playlist_title.innerText = element.playlist_title
        }
        
        playlist_info.appendChild(playlist_title)
        playlist_info.appendChild(detail_txt)
    });
} 

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}