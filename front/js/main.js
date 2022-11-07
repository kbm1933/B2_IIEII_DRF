console.log('recommend list 불러옴')

const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']
const token = localStorage.getItem('access')

window.onload = async function loadTop100(){
    const response = await fetch (`http://127.0.0.1:8000/musicplaylist/${userId}/playlist/recommended/`, {
    headers : { 
        'Authorization' : 'Bearer ' + token,
    },    
    method:"GET"
    })
    response_json = await response.json()

    // 숫자로 변수 있는게 헷갈려서 response_json2를 세분화해서 변경했습니다.
    playlist_response = response_json.recommend_playlist.playlist_select_musics
    console.log(playlist_response)
    
    const recommend = document.getElementById('recommend_music_list')

    playlist_response.forEach(element => {
        const recommend_music = document.createElement("li")
        recommend_music.innerText = element.music_title + '\u00a0'+ '-'  + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)
        
        recommend.appendChild(recommend_music)
        recommend.appendChild(img)
    
    });
 
    music_top100_response_json = response_json.music_top100
    console.log(playlist_response)
    
    const top100 = document.getElementById('top100_list')

    // 뮤직 top 100 리스트 추가

    music_top100_response_json.forEach(element => {
        const top100_music = document.createElement("li")
        top100_music.innerText = element.music_title + '\u00a0'+ '-'  + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)
        
        top100.appendChild(top100_music)
        top100.appendChild(img)
    });
} 

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}