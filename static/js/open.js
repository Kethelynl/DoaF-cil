const btn_search = document.querySelector('#search2')
const open_search = document.querySelector('#search-menu')

btn_search.addEventListener('click', open)

function open(){
    open_search.classList.toggle('visible')
}