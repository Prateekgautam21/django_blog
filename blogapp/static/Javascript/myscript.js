var button = document.getElementById('btnnos');
button.addEventListener('click',hideshow,false);

function hideshow(){
    document.getElementById('myid').style.display = 'block';
    this.style.display = 'none';
}
var btn2 = document.getElementById('second_button');
btn2.onclick = function(){
    document.getElementById('myid').style.display = 'none';
    document.getElementById('btnnos').style.display = 'block';
}