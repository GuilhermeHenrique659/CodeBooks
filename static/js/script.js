document.querySelector('#btn-close').addEventListener('click', ()=>{
    document.querySelector('.form-publication').setAttribute('hidden','')
})

document.querySelector('#new-publication').addEventListener('click',()=>{
    document.querySelector('.form-publication').removeAttribute("hidden")
    document.querySelector('#container').scrollTo(0, 0);
} )