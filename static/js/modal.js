const editModal = document.getElementById('editmodal')
editModal.addEventListener('hide.bs.modal', function (event) {
    document.getElementById('title').value = null;
    document.getElementById('description').value = null;
    document.getElementById('idpost').value = null;
})

editModal.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget
    let id = button.getAttribute('data-id')
    let title = button.getAttribute('data-title')
    let desc = button.getAttribute('data-desc')
    console.log(title)
    let id_input = editModal.querySelector('#idpost')
    id_input.value = id
    let title_input = editModal.querySelector('#title')
    title_input.value = title
    let desc_input = editModal.querySelector('#description')
    desc_input.value = desc
})