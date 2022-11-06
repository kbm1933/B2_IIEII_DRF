
console.log('top100 list 불러옴')

const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']
console.log(userId)


window.onload = async function loadTop100(){
    const response = await fetch (`http://127.0.0.1:8000/musicplaylist/${userId}/playlist/select/`, {method:"GET"})

    response_json = await response.json()

    console.log(response_json)

    const top100 = document.getElementById('top100_list')

    response_json.forEach(element => {

        const music_check = document.createElement("INPUT")
        music_check.setAttribute("type", "checkbox")
        music_check.setAttribute("value", element.id)
        music_check.setAttribute("name", 'top100_checkbox')

        const top100_music = document.createElement("li")
        top100_music.innerText = element.music_title + '\u00a0'+ '-'  + '\u00a0' + element.music_artist

        const img = document.createElement("IMG")
        img.setAttribute("src", element.music_img)
        
        top100.appendChild(top100_music)
        top100.appendChild(img)
        top100.appendChild(music_check)
    });
} 
