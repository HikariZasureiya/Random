//document elements

const label=document.getElementById('lab1');
const navitems=document.querySelector('list');
const navbox=document.querySelector('.navbox');
const online=document.getElementById('online');
const onlineuserbutton=document.getElementById('onlineuser');
const closebutton=document.getElementById("close");
const emptyspace=document.getElementById("emptyspace");
const mainarea=document.getElementById("mainarea");
const onlineusertext=document.getElementById('onlineusertext');
const send=document.getElementById("send");
const chatspace= document.getElementById("chatspace");

const on_user_box= document.getElementById('users');
const on_users=document.createElement('div');
on_users.setAttribute('id', 'on_users');
const csrfToken = $('[name=csrfmiddlewaretoken]').val();



onlineuserbutton.addEventListener("click",function(){
    online.style.display="block";
    online.style.transform="translateX(0)";
    online.style.left='0px';
    // mainarea.style.width="60%";
    
})

closebutton.addEventListener("click",function(){
    // online.style.transform="translateX(-100%)";
    online.style.left="";
    emptyspace.style.width="";
    mainarea.style.width="";
})

chatspace.addEventListener("click",function(){
    // online.style.transform="translateX(-100%)";
    online.style.left="";
    emptyspace.style.width="";
    mainarea.style.width="";
})



// websocket connection

let url = `wss://${window.location.host}/ws/socket-server/`;
const chatSocket=new WebSocket(url);

let temp_check=[];
        
        chatSocket.onmessage = function(e){
            
            let data= JSON.parse(e.data);
            const onlineusers=data.users_online;


            if(data.type==='user_joined'){
                var currentdate= new Date();
                var current_hour = currentdate.getHours();
                var current_minute = currentdate.getMinutes();

              
                
                on_user_box.innerHTML='';

                

                data.online_list.forEach(usernam=>{
                    on_user_box.insertAdjacentHTML('beforeend',`
                    <div id='on_users'>
                      <h>${usernam}</h>
                    </div>`);
                })

                

                    if(data.online_list.length>temp_check.length){

                        console.log("inside block");
                        
                        temp_check=data.online_list;

                        chatspace.insertAdjacentHTML('beforeend',
                        `<div id='messagebox'>
                            <div id='userinfo'>
                                                    
                                
                                <div id='username'>
                                    <h>Broadcast</h>
                                </div>

                                <div id='timebox'>
                                    <h>${current_hour}:${current_minute}</h>
                                </div>
                            
                            </div>

                            <div id='message'>
                                <p>${data.username} joined the room</p> 
                            </div>       
                        </div>`);

                        console.log('problem')
                        console.log()

                        chatspace.scrollTop=chatspace.scrollHeight;

                

            }
        }


            var currentdate= new Date();
            var current_year = currentdate.getFullYear();
            var current_month= currentdate.getMonth();
            var current_day = currentdate.getDate();
            var current_hour = currentdate.getHours();
            var current_minute = currentdate.getMinutes();
                        
            
            if (data.type==='chat'){

                console.log(data)

                chatspace.insertAdjacentHTML('beforeend',
                `<div id='messagebox'>
                    <div id='userinfo'>

                        <div id='pfp'>
                            
                        </div>
                        
                        <div id='usertime'>
                            <div id='username'>
                                <h>${data.username}</a>
                            </div>

                            <div id='timebox'>
                                <h>${current_hour}:${current_minute}</h>
                            </div>
                        </div>

                        <div id='datetime'>
                            <h>${current_day}/${current_month+1}/${current_year}</h>
                        </div>
                    </div>

                    <div id='message'>
                        <p>${data.message}</p> 
                    </div>       
                </div>`);


                
                chatspace.scrollTop=chatspace.scrollHeight;
            }

            if(data.type==='offline'){
                var currentdate= new Date();
                var current_hour = currentdate.getHours();
                var current_minute = currentdate.getMinutes();

                console.log(data.online_list);
                
                on_user_box.innerHTML='';
                temp_check=data.online_list;

                data.online_list.forEach(usernam=>{
                    on_user_box.insertAdjacentHTML('beforeend',`
                    <div id='on_users'>
                      <h>${usernam}</h>
                    </div>`);
                })

                

                    chatspace.insertAdjacentHTML('beforeend',
                    `<div id='messagebox'>
                        <div id='userinfo'>
                                                
                            
                            <div id='username'>
                                <h>Broadcast</h>
                            </div>

                            <div id='timebox'>
                                <h>${current_hour}:${current_minute}</h>
                            </div>
                        
                        </div>

                        <div id='message'>
                            <p>${data.username} left the the room</p> 
                        </div>       
                    </div>`);

                    chatspace.scrollTop=chatspace.scrollHeight;
                

            }


    
        }


        
        message_send_form= document.getElementById('messagesend')

        message_send_form.addEventListener('submit', (e)=>{

            e.preventDefault()
            let socket_message = e.target.mainarea.value;

            $.ajax({
                url: posturl, 
                type: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                data: {
                    'mainarea': socket_message,
                    'csrfmiddlewaretoken': csrfToken,
                },
                success: function(response) {
                    $('#mainarea').val(''); 
                },
                error: function(xhr, status, error) {
                    console.error('Error sending message:', error);
                }
            });

           
            chatSocket.send(JSON.stringify({
                'message':socket_message
            }))

           

            message_send_form.reset()
        })
        



//get AJAX to display chat

$(document).ready(function(){
    const thelist = $('#chatspace');

        $.ajax({
            type: "GET",
            url: j,
            cache: false,
            success: function(response){
                //console.log('Response:', response); // Check the response in the console
                thelist.empty();

                for(var key in response.online){

                    const messagebox = document.createElement("div"); //message container
                            const userinfo=document.createElement("div"); // user information (pfp, username)
                            const username=document.createElement("div");
                            const message = document.createElement('p');
                            const datetime= document.createElement('div');
                            const usertime= document.createElement('div');
                            const timebox=document.createElement('div');
                            
                            messagebox.setAttribute('id', 'messagebox'); 
                            userinfo.setAttribute("id","userinfo");

                            datetime.setAttribute('id','datetime');
                            username.setAttribute("id","username");
                            message.setAttribute('id', 'message');
                            usertime.setAttribute('id', 'usertime');
                            timebox.setAttribute('id', 'timebox');
                            
                            var user_name=JSON.stringify(response.online[key]['user']);
                
                            username.innerHTML = `<h>${response.online[key]['user']}</h>`;
                            message.innerHTML = response.online[key]['message'];
                            // datetime.innerHTML=response.online[key]['time'];
                            currenttime=response.online[key]['time'];
                            currentUTC= new Date(currenttime);

                            var year = currentUTC.getFullYear();
                            var month= currentUTC.getMonth();
                            var day = currentUTC.getDate();
                            var hour = currentUTC.getHours();
                            var minute = currentUTC.getMinutes();
                            //currentUTCstring=currentUTC.toLocalString();
                            timebox.innerHTML=`${hour}:${minute}`
                            datetime.innerHTML=`${day}/${month+1}/${year}`;
                            
                            usertime.appendChild(username);
                            usertime.appendChild(timebox);
                            userinfo.appendChild(usertime)
                            userinfo.appendChild(datetime);
                            messagebox.appendChild(userinfo);
                            
                            messagebox.appendChild(message);
                            chatspace.appendChild(messagebox)
                };

                chatspace.scrollTop=chatspace.scrollHeight;
                
            },

            error: function(xhr, status, error){
                console.error(xhr.responseText);
                alert("Error occurred. Please check the console for details.");
            }
        });
});


