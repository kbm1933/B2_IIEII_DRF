function move(url){ 
    window.location.href = url
};

async function handleSignin(){
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    console.log(email, password)

    const response = await fetch("http://127.0.0.1:8000/user/signup/",{
        headers: {
            'content-type' : 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            "email": email,
            "password": password
        })
    })
    console.log(response);
    move_url = 'login.html'
    move(move_url)
    
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
    move_url = 'top100.html'
    move(move_url)
}


function handleLogout(){
    localStorage.clear()
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

    console.log(music_id)

    const response = await fetch("http://127.0.0.1:8000/musicplaylist/2/playlist/select/",{
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
    move_url = 'main.html'
    move(move_url)
}