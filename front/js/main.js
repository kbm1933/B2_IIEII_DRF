
console.log('recommend list 불러옴')

const token = localStorage.getItem('access')

window.onload = async function loadTop100(){
    const response = await fetch ('http://127.0.0.1:8000/musicplaylist/2/playlist/recommended/', {
    headers : { 
        'Authorization' : 'Bearer ' + token,
    },    
    method:"GET"
    })

    response_json = await response.json()

    response_json2 = response_json.playlist_select_musics
    console.log(response_json2)

    
    const recommend = document.getElementById('recommend_music_list')

    response_json2.forEach(element => {

        const recommend_music = document.createElement("li")
        recommend_music.innerText = element.music_title + '\u00a0'+ '-'  + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)
        
        recommend.appendChild(recommend_music)
        recommend.appendChild(img)
    
    });
} 
