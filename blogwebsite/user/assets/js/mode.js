const light = document.getElementById('light')
const dark = document.getElementById('dark')

light.addEventListener('click', ()=>{
    document.body.style.backgroundColor = "#000"
})
dark.addEventListener('click', ()=>{
    document.body.style.backgroundColor = "#222222"
})
