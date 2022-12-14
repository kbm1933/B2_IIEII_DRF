function password_valid(password, password2) {
    if (password != password2) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }
    else {
        return true;
    }
}

async function handleSignup(){
    const email = document.getElementById("email").value
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    const password2 = document.getElementById("password2").value
    console.log(email, password)

    if (password_valid(password, password2)) {
        const response = await fetch('http://127.0.0.1:8000/user/signup/', {
            headers:{
                'content-type' : 'application/json',
            },
            method:'POST',
            body: JSON.stringify({
                "email":email,
                "username":username,
                "password":password,
            })
        }).then(window.location.replace("login.html"))
        alert("가입되었습니다!")
        console.log(response)
    }
    else {
        console.log("제출하지 않음")
        window.location.reload()
    }
}

async function handleLogin(){
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    console.log(email, password)

    const response = await fetch("http://127.0.0.1:8000/user/api/token/",{
        headers: {
            'content-type' : 'application/json',
        },
        method : 'POST',
        body : JSON.stringify({
            "email" : email,
            "password": password
        })
    })
    alert("로그인 성공");

    // id, email 등등 jwt.io 정보를 로컬스토리지에 저장하는 코드
    const response_json = await response.json()
    console.log(response_json)

    localStorage.setItem('access',response_json.access);
    localStorage.setItem('refresh', response_json.refresh);

    const base64Url = response_json.access.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g,'/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c){
        return '%' + ('00'+ c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    
    localStorage.setItem('payload', jsonPayload);
    window.location.replace("top100.html")
}

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}

async function music_check() {
    var length = document.getElementsByName("top100_checkbox").length;
    const music_id = []
    for (var i=0; i<length; i++){
        if(document.getElementsByName("top100_checkbox")[i].checked == true){
            music_id.push(document.getElementsByName('top100_checkbox')[i].value);
        }
    }
    const token = localStorage.getItem('access')
    const payload = localStorage.getItem('payload')
    const personObj = JSON.parse(payload)
    const userId = personObj['user_id']

    console.log(music_id)

    const response = await fetch(`http://127.0.0.1:8000/musicplaylist/${userId}/playlist/select/`,{
        headers: {
            'Authorization' : 'Bearer ' + token,
            'content-type' : 'application/json',
        },
        method : 'POST',
        body : JSON.stringify({
            "playlist_select_musics" : music_id,
            "playlist_title" : "playlist"
        }) 
    })
    console.log(response)
    alert("완료");
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